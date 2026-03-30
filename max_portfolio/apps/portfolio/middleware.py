import logging
import time

logger = logging.getLogger("apps.portfolio")


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - started) * 1000
        if request.path.startswith("/api/"):
            logger.info("API request %s completed in %.2fms", request.path, duration_ms)
        return response