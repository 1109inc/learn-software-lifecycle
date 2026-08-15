import logging
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_context import set_request_id

logger = logging.getLogger(__name__)

# Kubernetes hits these every few seconds, per pod. Logging them would bury
# every real request under probe noise.
SILENT_PATHS = frozenset(
    {
        "/api/v1/health/live",
        "/api/v1/health/ready",
    }
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        set_request_id(request_id)

        started = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started) * 1000, 2)

        if request.url.path not in SILENT_PATHS:
            logger.info(
                "request completed",
                extra={
                    "context": {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                    }
                },
            )

        response.headers["X-Request-ID"] = request_id
        return response
