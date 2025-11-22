"""Caching layer for data fetchers."""

import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import aiofiles

from ..config.settings import Settings


class CacheManager:
    """Manage file-based caching for fetched data."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.cache_dir = Path(settings.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def get(self, key: str) -> dict[str, Any] | None:
        """
        Get cached data if available and not expired.

        Args:
            key: Cache key

        Returns:
            Cached data or None if expired/not found
        """
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        try:
            async with aiofiles.open(cache_file, encoding="utf-8") as f:
                content = await f.read()
                cached_data = json.loads(content)

            # Check expiration
            cached_at = datetime.fromisoformat(cached_data.get("cached_at", ""))
            ttl = timedelta(seconds=cached_data.get("ttl", self.settings.cache_ttl_seconds))

            if datetime.now() - cached_at < ttl:
                return cached_data.get("data")

            # Expired - remove file
            await self._remove_cache_file(cache_file)
            return None

        except Exception:
            return None

    async def set(self, key: str, data: dict[str, Any], ttl: int | None = None) -> None:
        """
        Cache data with optional TTL.

        Args:
            key: Cache key
            data: Data to cache
            ttl: Time to live in seconds
        """
        cache_file = self.cache_dir / f"{key}.json"

        cached_data = {
            "cached_at": datetime.now().isoformat(),
            "ttl": ttl or self.settings.cache_ttl_seconds,
            "data": data,
        }

        try:
            async with aiofiles.open(cache_file, "w", encoding="utf-8") as f:
                await f.write(json.dumps(cached_data, indent=2, ensure_ascii=False))
        except Exception as e:
            # Log but don't fail if caching fails
            print(f"Warning: Failed to cache {key}: {e}")

    async def clear(self, key: str | None = None) -> None:
        """
        Clear cache for a specific key or all cached data.

        Args:
            key: Specific key to clear, or None to clear all
        """
        if key:
            cache_file = self.cache_dir / f"{key}.json"
            await self._remove_cache_file(cache_file)
        else:
            # Clear all cache files
            for cache_file in self.cache_dir.glob("*.json"):
                await self._remove_cache_file(cache_file)

    async def _remove_cache_file(self, cache_file: Path) -> None:
        """Remove a cache file safely."""
        try:
            if cache_file.exists():
                await asyncio.to_thread(os.remove, cache_file)
        except Exception:
            pass  # Ignore errors when removing cache files
