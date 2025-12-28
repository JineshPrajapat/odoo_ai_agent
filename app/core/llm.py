import json
import uuid
import re
import time
import httpx
from openai import OpenAI
from datetime import datetime
from openai import RateLimitError, APIError, Timeout
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL
from app.exceptions.app_exceptions import AppException
from app.log.logger import llm_logger
from app.rate_limit.rate_limiter import RateLimiter

client = OpenAI(
    api_key=OPENAI_API_KEY,
    max_retries=0,
    timeout=httpx.Timeout(20.0),
)


class LLMClient:
    def __init__(self):
        self.rate_limiter = RateLimiter(
            max_calls=2,          # strict RPM
            window_seconds=60
        )

    def complete(self, system_prompt: str, user_prompt: str,) -> dict:
        print("lenght", len(user_prompt))
        self.rate_limiter.acquire()
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                # prompt_cache_retention="24h"
            )

            content = response.choices[0].message.content.strip()

            usage = response.usage
            self._log_request(user_prompt, content, usage)
            return json.loads(content)

        except json.JSONDecodeError:
            raise AppException(
                message="LLM returned invalid JSON.",
                error_code="LLM_INVALID_JSON",
                source="llm",
                status_code=502
            )

        except RateLimitError as e:
            print("e", e)
            self._handle_rate_limit(e)

        except Timeout:
            raise AppException(
                message="The request took too long to respond. Please try again.",
                error_code="LLM_TIMEOUT",
                source="llm",
                status_code=504
            )

        except APIError as e:
            raise AppException(
                message="LLM service error.",
                error_code="LLM_API_ERROR",
                source="llm",
                status_code=502,
                details={"reason": str(e)}
            )

        except Exception:
            raise AppException(
                message="Unexpected LLM failure.",
                error_code="LLM_UNKNOWN_ERROR",
                source="llm",
                status_code=500
            )

    # def generate(self, prompt: str) -> str:
    #     ''' Generate a text response '''
    #     self._respect_rate_limit()
    #     try:
    #         response = client.chat.completions.create(
    #             model= OPENAI_MODEL,
    #             messages=[{"role": "user", "content": prompt}],
    #             temperature=0.2,
    #             prompt_cache_retention="24h"
    #         )

    #         content = response.choices[0].message.content.strip()
    #         usage = response.usage

    #         self._log_request(prompt, content, usage)
    #         return response.choices[0].message.content.strip()

    #     except RateLimitError as rle:
    #         print("rle", rle)
    #         raise AppException(
    #             message="You’ve reached the message limit. Please try again later.",
    #             error_code="LLM_QUOTA_EXCEEDED",
    #             source="llm",
    #             status_code=429
    #         )

    #     except Exception:
    #         raise AppException(
    #             message="Response generation failed.",
    #             error_code="LLM_GENERATE_FAILED",
    #             source="llm",
    #             status_code=502
    #         )

    def _log_request(self, prompt: str, response: str | None, usage: dict | None, error: str | None = None):
        """
        Save request details in a log file.
        """
        log_data = {
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "prompt_length": len(prompt),
            "usage": usage,
            "error": error
        }
        print("logdata", log_data)
        llm_logger.info(log_data)

    def _handle_rate_limit(self, e: RateLimitError):
        """
        Extract wait time from error message and raise a friendly exception.
        """
        msg = str(e)
        wait_time = None

        # Extract wait time from message using regex (e.g., "Please try again in 1h0m2.88s")
        match = re.search(r"in ([0-9hms.:]+)", msg)
        if match:
            wait_time = match.group(1)

        friendly_message = (
            f"You’ve reached the message limit. "
            f"{f'Please try again after {wait_time}.' if wait_time else 'Please try again later.'}"
        )

        llm_logger.warning(
            {"error": "LLM_QUOTA_EXCEEDED", "wait_time": wait_time})

        raise AppException(
            message=friendly_message,
            error_code="LLM_QUOTA_EXCEEDED",
            source="llm",
            status_code=429,
            details={"retry_after": wait_time},
        )

    def _respect_rate_limit(self):
        """
        Ensures no more than MAX_CALLS_PER_MINUTE are made per minute.
        Delays execution if limit is reached.
        """
        with self._lock:
            now = time.time()

            # Remove timestamps older than 60 seconds
            self._call_timestamps = [
                ts for ts in self._call_timestamps
                if now - ts < self.WINDOW_SECONDS
            ]

            if len(self._call_timestamps) >= self.MAX_CALLS_PER_MINUTE:
                wait_time = self.WINDOW_SECONDS - \
                    (now - self._call_timestamps[0])
                wait_time = max(wait_time, 0)

                llm_logger.warning({
                    "event": "LLM_RATE_LIMIT_DELAY",
                    "wait_seconds": round(wait_time, 2)
                })

                time.sleep(wait_time)

            # Register this call
            self._call_timestamps.append(time.time())


llm_client = LLMClient()
