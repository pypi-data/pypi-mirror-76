import structlog
from aredis import StrictRedis

from runnel.logging import init_logging
from runnel.processor import Processor
from runnel.settings import Settings
from runnel.stream import Stream

logger = structlog.get_logger(__name__)


class App:
    """
    This is the main abstraction provided by Runnel. Use the :meth:`~.stream` and
    :meth:`~.processor` methods to define partitioned event streams and processors
    respectively. Apps will be run by workers via the CLI.

    Parameters
    ----------
    name : str
        An app identifier. Will be used as a component of the Redis keys for the
        under-the-hood data structures.
    kwargs : Dict
        Any of the settings found in :mod:`runnel.settings` to override any options
        provided by environment variables.

    Examples
    --------
    >>> from runnel import App, Record
    ...
    >>> app = App(
    ...     name="example",
    ...     log_level="info",
    ...     redis_url="127.0.0.1:6379",
    ... )

    Specify your event types using the Record class:

    >>> class Order(Record):
    ...     order_id: int
    ...     created_at: datetime
    ...     amount: int
    ...     item_ids: List[int]

    Streams are configured to be partitioned by a chosen key.

    >>> orders = app.stream("orders", record=Order, partition_by="order_id")

    Processor functions iterate over the event stream and can rely on receiving events
    in the order they were created per key.

    >>> @app.processor(orders)
    ... async def printer(events):
    ...     async for order in events.records():
    ...         print(order.amount)

    Under the hood, Runnel will take care of partitioning the stream to enable scalable
    distributed processing. We also take care of concurrently running the async processor
    functions -- one for every partition in your stream. This processing may be
    distributed across many workers on different machines and Runnel will coordinate
    ownership of partitions dynamically as workers join or leave.
    """
    def __init__(self, name: str, **kwargs):
        self.name: str = name
        self.settings: Settings = Settings(**kwargs)
        self.redis = StrictRedis.from_url(self.settings.redis_url)
        self.workers = set()
        self.processors = {}
        self.scripts = {}  # Lua scripts, loaded by workers at startup.

        init_logging(
            level=self.settings.log_level,
            format=self.settings.log_format,
        )

    def stream(
        self,
        name,
        record,
        partition_by,
        serializer=None,
        partition_count=None,
        partition_size=None,
        hasher=None,
    ):
        """
        A set of partitioned Redis streams, containing events as structured Record types.

        Kwargs, if provided, will override the default settings configured on the App
        instance or via environment variables (see :mod:`runnel.settings`) for this
        stream.

        Parameters
        ----------
        name : str
            An stream identifier. Will be used as a component of the Redis keys for the
            under-the-hood data structures.
        record: Type[Record]
            A class that inherits from Record, which specifies the structure of the event
            data this stream expects. See :class:`runnel.Record`.
        partition_by : Union[str, Callable[Record, Any]]
            A str representing an attribute of the Record type (or a callable to compute
            a value) which should be used to partition events. For example, if your events
            concern user activity and you want to process events in-order per user, you
            might choose the "user_id" attribute to partition by.
        serializer : Serializer
            An object implementing the :class:`runnel.interfaces.Serializer` interface
            which controls how records are stored in the Redis streams.
        partition_count : int
            How many partitions to create.
        partition_size : int
            The max length of each partition. (Implemented approximately via Redis' MAXLEN
            option to XACK.) Represents the size of the buffer in case processors are
            offline or cannot keep up with the event rate.
        hasher: Callable[Any, int]
            A function used to hash the partition key to decide to which partition to
            send a record.

        Examples
        --------
        >>> from runnel import App, Record, JSONSerializer
        ...
        >>> app = App(name="example")
        ...
        >>> class Order(Record):
        ...     order_id: int
        ...     amount: int

        Streams are configured to be partitioned by a chosen key.

        >>> orders = app.stream(
        ...     name="orders",
        ...     record=Order,
        ...     partition_by="order_id",
        ...     partition_count=16,
        ...     serializer=JSONSerializer(),
        ... )
        """
        if serializer is None and not record._primitive:
            serializer = self.settings.default_serializer

        return Stream(
            app=self,
            name=name,
            record=record,
            partition_by=partition_by,
            serializer=serializer,
            partition_count=partition_count or self.settings.default_partition_count,
            partition_size=partition_size or self.settings.default_partition_size,
            hasher=hasher or self.settings.default_hasher,
        )

    def processor(
        self,
        stream,
        name=None,
        exception_policy=None,
        middleware=None,
        lock_expiry=None,
        read_timeout=None,
        prefetch_count=None,
        assignment_attempts=None,
        assignment_sleep=None,
        grace_period=None,
        pool_size=None,
        join_delay=None
    ):
        """
        A wrapper around an async Python function which iterates over a continuous event
        stream.

        Kwargs, if provided, will override the default settings configured on the App
        instance or via environment variables (see :mod:`runnel.settings`) for this
        processor.

        Notes
        -----
        Events are acknowledged at the end of every processing loop. This means that if
        your processor crashed before completion, that section of work will be repeated
        when the processor is restarted. Therefore Runnel provides 'at least once'
        semantics.

        Parameters
        ----------
        exception_policy : ExceptionPolicy
            How to handle exceptions raised in the user-provided processor coroutine.

            * ``HALT``: Raise the exception, halting execution of the affected partition.
            * ``QUARANTINE``: Mark the affected partition as poisoned, and continue with others.
            * ``IGNORE``: Suppress the exception and continue processing regardless.

            Default: ``HALT``.
        middleware : List[Middleware]
            A list of Middleware objects for managaing the data pipeline. Can be used to
            implement custom exception handling (e.g. dead letter queues).
        lock_expiry : int (seconds)
            The duration of the lock on stream partitions owned by executors of this
            processor. This controls the worst case lag a partition's events may
            experience since other executors will have to wait acquire the lock in case
            the owner has died.
        read_timeout : int (milliseconds)
            How long to stay blocked reading from Redis via XREADGROUP. Nothing depends
            on this.
        prefetch_count : int
            The maximum number of events to read from Redis per partition owned by an
            executor. (If a single executor owns all 16 partitions in a stream and
            prefetch_count is 10, then 160 events may be read at once.) Purely an
            optimisation.
        assignment_attempts : int
            How many times to try to complete a rebalance operation (i.e. acquire our
            declared partitions) before giving up.
        assignment_sleep : float (seconds)
            How long to wait between attempts to complete a rebalance operation.
        grace_period : float (seconds)
            How long to wait for execution to complete gracefully before cancelling it.
        pool_size : int
            How many concurrent connections to make to Redis to read events.
        join_delay : int (seconds)
            How long to wait after joining before attempting to acquire partitions.
            Intended to mitigate a thundering herd problem of multiple workers joining
            simultaneously and needing to rebalance multiple times.

        Examples
        --------
        >>> from runnel import App, Record
        ...
        >>> app = App(name="example")
        ...
        >>> class Order(Record):
        ...     order_id: int
        ...     amount: int
        ...
        >>> orders = app.stream(name="orders", record=Order, partition_by="order_id")
        ...
        >>> @app.processor(orders)
        ... async def printer(events):
        ...     async for order in events.records():
        ...         print(order.amount)
        """
        kwargs = {
            "exception_policy": exception_policy or self.settings.default_exception_policy,
            "middleware": middleware or [],
            "lock_expiry": lock_expiry or self.settings.default_lock_expiry,
            "read_timeout": read_timeout or self.settings.default_read_timeout,
            "prefetch_count": prefetch_count or self.settings.default_prefetch_count,
            "assignment_attempts": assignment_attempts or self.settings.default_assignment_attempts,
            "assignment_sleep": assignment_sleep or self.settings.default_assignment_sleep,
            "grace_period": grace_period or self.settings.default_grace_period,
            "pool_size": pool_size or self.settings.default_pool_size,
            "join_delay": join_delay or self.settings.default_join_delay,
        }

        def decorator(f):
            x = name or f.__name__
            assert x not in self.processors

            self.processors[x] = Processor(
                stream=stream,
                f=f,
                name=x,
                **kwargs,
            )
            return self.processors[x]

        return decorator
