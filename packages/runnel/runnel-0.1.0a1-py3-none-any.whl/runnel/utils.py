import base64
import importlib
import time
import uuid
from contextlib import contextmanager
from typing import Any, Generator


def base64uuid() -> str:
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b"=").decode("ascii")


def now() -> float:
    return time.time()


@contextmanager
def duration(logger, event: str, **extra: Any) -> Generator:
    logger.info(f"started-{event}", **extra)
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    logger.info(f"ended-{event}", duration=duration, **extra)


def get_object(name: str) -> Any:
    module_name, instance_name = name.split(":", 1)
    module = importlib.import_module(module_name)
    return getattr(module, instance_name)


def chunks(seq, n):
    d, r = divmod(len(seq), n)
    for i in range(n):
        si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
        yield seq[si:si + (d + 1 if i < r else d)]
