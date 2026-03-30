#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
GRAPHQL_URL = f"{API_ROOT}/graphql"


class GitHubAPIError(RuntimeError):
    pass


def require_token(env_var: str = "GITHUB_TOKEN") -> str:
    token = os.environ.get(env_var)
    if not token:
        raise GitHubAPIError(f"{env_var} is required")
    return token


def _encode_json(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


class GitHubClientBase:
    def __init__(self, token: str, *, pause_seconds: float = 0.0, user_agent: str = "github-stars-organizer") -> None:
        self.token = token
        self.pause_seconds = pause_seconds
        self.user_agent = user_agent

    def _request(
        self,
        url: str,
        *,
        method: str = "GET",
        accept: str = "application/vnd.github+json",
        json_body: Optional[dict] = None,
    ) -> Tuple[int, Dict[str, str], bytes]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": self.user_agent,
        }
        if accept:
            headers["Accept"] = accept

        payload = None
        if json_body is not None:
            headers["Content-Type"] = "application/json"
            payload = _encode_json(json_body)

        req = Request(url, data=payload, headers=headers, method=method)
        try:
            with urlopen(req) as resp:
                status = resp.getcode()
                response_headers = dict(resp.info().items())
                raw = resp.read()
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise GitHubAPIError(f"GitHub HTTP {exc.code} for {method} {url}: {body}") from exc
        except URLError as exc:
            raise GitHubAPIError(f"GitHub request failed for {method} {url}: {exc}") from exc

        if self.pause_seconds > 0:
            time.sleep(self.pause_seconds)

        return status, response_headers, raw


class GitHubRESTClient(GitHubClientBase):
    def request_json(
        self,
        method: str,
        path: str,
        *,
        query: Optional[dict] = None,
        accept: str = "application/vnd.github+json",
        json_body: Optional[dict] = None,
    ) -> Tuple[int, Dict[str, str], Any]:
        url = f"{API_ROOT}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        status, headers, raw = self._request(url, method=method, accept=accept, json_body=json_body)
        data = None
        if raw:
            data = json.loads(raw.decode("utf-8"))
        return status, headers, data

    def request_status(
        self,
        method: str,
        path: str,
        *,
        query: Optional[dict] = None,
        accept: str = "application/vnd.github+json",
        json_body: Optional[dict] = None,
    ) -> Tuple[int, Dict[str, str]]:
        url = f"{API_ROOT}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        status, headers, _ = self._request(url, method=method, accept=accept, json_body=json_body)
        return status, headers


class GitHubGraphQLClient(GitHubClientBase):
    def call(self, query: str, variables: Optional[dict] = None) -> dict:
        _, _, raw = self._request(
            GRAPHQL_URL,
            method="POST",
            json_body={
                "query": query,
                "variables": variables or {},
            },
        )
        data = json.loads(raw.decode("utf-8"))
        if "errors" in data:
            raise GitHubAPIError(json.dumps(data["errors"], ensure_ascii=False))
        return data["data"]
