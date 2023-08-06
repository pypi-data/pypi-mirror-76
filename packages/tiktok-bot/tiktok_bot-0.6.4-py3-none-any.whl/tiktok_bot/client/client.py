from collections import deque
from time import time
from typing import Deque, Optional
from uuid import uuid4

from httpx import Client, Response
from loguru import logger

from .utils import generate_as, generate_cp, generate_mas


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        default_headers: Optional[dict] = None,
        default_params: Optional[dict] = None,
        history_len: int = 30,
    ):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.default_params = default_params or {}

        self.history: Deque[Response] = deque(maxlen=history_len)

        self.http_client = Client(
            base_url=self.base_url, headers=default_headers, params=self.default_params
        )

    def get(self, url: str, params: dict, headers: Optional[dict] = None):
        custom_headers = headers or {}
        all_params = {**self._generate_params(), **params}

        logger.debug(f"Sending request to {url}", params=all_params, custom_headers=custom_headers)
        response = self.http_client.get(url=url, params=all_params, headers=custom_headers)

        self.history.append(response)

        body = response.text or "is empty!"

        logger.debug(f"Response return status_code: {response.status_code}, body: {body}")

        for cookie_name, cookie_data in response.cookies.items():
            self.http_client.cookies.set(cookie_name, cookie_data)
            logger.debug(f"New cookies: {dict(response.cookies)}")

        return response

    def post(
        self, url: str, data: dict, headers: Optional[dict] = None, params: Optional[dict] = None
    ):
        custom_headers = headers or {}
        custom_params = params or {}
        # merge parameters
        all_params = {**self._generate_params(), **custom_params}

        logger.debug(
            f"Sending request to {url}", params=all_params, custom_headers=custom_headers, data=data
        )

        response = self.http_client.post(
            url=url, params=all_params, data=data, headers=custom_headers,
        )

        self.history.append(response)

        body = response.text or "is empty!"
        logger.debug(f"Response return status_code: {response.status_code}, body: {body}")

        for cookie_name, cookie_data in response.cookies.items():
            self.http_client.cookies.set(cookie_name, cookie_data)
            logger.debug(f"New cookies: {dict(response.cookies)}")

        return response

    def _generate_params(self):
        now = str(int(round(time() * 1000)))

        params = {
            "_rticket": now,
            "ts": now,
            "mas": generate_mas(now),
            "as": generate_as(now),
            "cp": generate_cp(now),
            "idfa": str(uuid4()).upper(),
        }

        return params
