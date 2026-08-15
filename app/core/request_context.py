from contextvars import ContextVar

# Holds the ID of the request currently being handled.
#
# A ContextVar is NOT one shared value. It holds a separate value per async
# task, and FastAPI runs every request as its own task — so each request gets
# its own request_id and they never overwrite each other.
#
# "request_id" is just a label used in debugging output.
# default=None is what you get before anything has been set.
_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(value: str) -> None:
    """Store the request ID for the request currently being handled."""
    _request_id.set(value)


def get_request_id() -> str | None:
    """Return the current request's ID, or None if there isn't one."""
    return _request_id.get()
