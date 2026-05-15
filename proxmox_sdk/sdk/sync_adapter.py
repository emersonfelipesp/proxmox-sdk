"""Small adapters for exposing async helpers through blocking methods."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from inspect import isawaitable
from typing import Any, cast


class BlockingDomainProxy:
    """Reflect async methods of a domain helper as blocking calls."""

    def __init__(self, loop: asyncio.AbstractEventLoop, target: Any) -> None:
        self._loop = loop
        self._target = target

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._target, name)
        if not callable(attr):
            return attr

        def _wrapped(*args: Any, **kwargs: Any) -> Any:
            result = attr(*args, **kwargs)
            if not isawaitable(result):
                return result
            return self._loop.run_until_complete(cast(Awaitable[Any], result))

        return _wrapped


__all__ = ["BlockingDomainProxy"]
