import time
import threading
from collections import deque
from app.log.logger import llm_logger


class RateLimiter:
    """
    Strict RPM limiter.
    - Counts ALL attempts
    - Blocks until safe
    - Thread-safe
    - No burst leakage
    """

    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = deque()
        self.lock = threading.Condition()

    def acquire(self):
        with self.lock:
            while True:
                now = time.monotonic()

                # Remove expired calls
                while self.calls and now - self.calls[0] >= self.window:
                    self.calls.popleft()

                if len(self.calls) < self.max_calls:
                    # Reserve slot BEFORE request
                    self.calls.append(now)
                    llm_logger.debug({
                        "event": "RATE_LIMIT_GRANTED",
                        "used": len(self.calls),
                        "limit": self.max_calls
                    })
                    return

                print("wait", {
                    "event": "RATE_LIMIT_BLOCK",
                    "wait_seconds": round(wait_time, 2),
                    "used": len(self.calls),
                    "limit": self.max_calls
                })

                # Need to wait
                wait_time = self.window - (now - self.calls[0])
                wait_time = max(wait_time, 0.01)

                llm_logger.warning({
                    "event": "RATE_LIMIT_BLOCK",
                    "wait_seconds": round(wait_time, 2),
                    "used": len(self.calls),
                    "limit": self.max_calls
                })

                self.lock.wait(timeout=wait_time)
                
