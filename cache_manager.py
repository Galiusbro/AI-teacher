#!/usr/bin/env python3
"""
Cache manager for AI-generated lessons.
Provides caching functionality to avoid redundant API calls.
"""

import os
import json
import hashlib
import time
from typing import Dict, Any, Optional
from pathlib import Path


class LessonCache:
    """Cache manager for AI-generated lessons."""

    def __init__(self, cache_dir: str = ".lesson_cache"):
        """Initialize cache manager."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_cache_age = 24 * 60 * 60  # 24 hours in seconds

    def _get_cache_key(self, module_code: str, lesson_type: str, locale: str) -> str:
        """Generate cache key from parameters."""
        cache_string = f"{module_code}:{lesson_type}:{locale}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{cache_key}.json"

    def get_cached_lesson(self, module_code: str, lesson_type: str, locale: str = 'ru') -> Optional[Dict[str, Any]]:
        """Get cached lesson if available and not expired."""
        cache_key = self._get_cache_key(module_code, lesson_type, locale)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Check if cache is expired
            if time.time() - cache_data['timestamp'] > self.max_cache_age:
                cache_path.unlink()  # Remove expired cache
                return None

            return cache_data['lesson']

        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return None

    def save_lesson_to_cache(self, module_code: str, lesson_type: str, lesson: Dict[str, Any], locale: str = 'ru') -> None:
        """Save lesson to cache."""
        cache_key = self._get_cache_key(module_code, lesson_type, locale)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            'timestamp': time.time(),
            'module_code': module_code,
            'lesson_type': lesson_type,
            'locale': locale,
            'lesson': lesson
        }

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save lesson to cache: {e}")

    def clear_cache(self) -> None:
        """Clear all cached lessons."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_files = len(list(self.cache_dir.glob("*.json")))
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))

        return {
            'total_cached_lessons': total_files,
            'cache_size_bytes': total_size,
            'cache_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir)
        }


# Global cache instance
lesson_cache = LessonCache()


def get_cached_lesson(module_code: str, lesson_type: str, locale: str = 'ru') -> Optional[Dict[str, Any]]:
    """Get cached lesson."""
    return lesson_cache.get_cached_lesson(module_code, lesson_type, locale)


def save_lesson_to_cache(module_code: str, lesson_type: str, lesson: Dict[str, Any], locale: str = 'ru') -> None:
    """Save lesson to cache."""
    lesson_cache.save_lesson_to_cache(module_code, lesson_type, lesson, locale)


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    return lesson_cache.get_cache_stats()


def clear_lesson_cache() -> None:
    """Clear all cached lessons."""
    lesson_cache.clear_cache()
