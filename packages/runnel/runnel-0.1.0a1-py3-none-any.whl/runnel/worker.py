import signal
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Set

import anyio
import structlog

from runnel.context import worker_id
from runnel.exceptions import Misconfigured
from runnel.executor import Executor
from runnel.utils import base64uuid

if TYPE_CHECKING:
    from runnel.app import App

logger = structlog.get_logger(__name__)


@dataclass
class Worker:
    """
    Runs processors for a given app. By default, will concurrently spawn an Executor
    task for every Processor known to the app. (The Executor in turn will spawn n tasks
    to actually process events -- one for every partition of the stream it owns.)
    """
    app: "App"
    id: str = field(default_factory=base64uuid)
    executors: Set[Executor] = field(default_factory=set)
    started: bool = False

    def __hash__(self):
        return object.__hash__(self)

    def start(self, processors="all"):
        """
        The main entrypoint.

        Parameters
        ----------
        processors : Union[str, List[str]]
            If "all", then run all processors known to the app. Otherwise only run those
            named in the processors list.

        Notes
        -----
        For every processor, the first worker to start will create a consumer group for
        in Redis if it does not already exist. It will set the starting ID to "0", which
        means "process the entire stream history". If you want to select a specific
        consumer group starting ID, see :func:`runnel.Processor.reset`.

        Examples
        --------
        >>> from runnel import Worker
        >>> from mymodule import myapp
        ...
        >>> # Run all processors.
        >>> Worker(myapp).start()
        ...
        >>> # Run specific processors.
        >>> Worker(myapp).start(["myproc1", "myproc2"])

        $ # Run named processor starting at specific ID from the shell
        $ runnel processor reset mymodule:myproc --start=12345-0
        $ runnel worker mymodule:myapp --processors=myproc
        """
        anyio.run(self._start, processors, backend="asyncio")

    async def _start(self, processors="all"):
        worker_id.set(self.id)
        assert processors == "all" or isinstance(processors, list)

        if self.started:
            raise Misconfigured("Worker already running")
        logger.info("starting-worker", processors=processors)

        # Load lua scripts.
        for script in (Path(__file__).parent / "lua").glob("*.lua"):
            self.app.scripts[script.stem] = self.app.redis.register_script(script.read_text())

        # Create executors for all chosen processors.
        for proc in self.app.processors.values():
            if processors == "all" or proc.name in processors:
                await proc.prepare()
                self.executors.add(Executor(id=base64uuid(), processor=proc))

        self.app.workers.add(self)
        try:
            async with anyio.open_signal_receiver(signal.SIGINT) as signals:
                async with anyio.create_task_group() as tg:
                    for e in self.executors:
                        await tg.spawn(e.start)
                    self.started = True

                    # Allow for graceful shutdown on SIGINT.
                    async for signum in signals:
                        if signum == signal.SIGINT:
                            logger.critical("sigint")
                            await tg.cancel_scope.cancel()
                            return
        finally:
            self.app.workers.remove(self)
            if not self.app.workers:
                self.app.redis.connection_pool.disconnect()
            logger.critical("worker-exit", eids=[e.id for e in self.executors])
