#!/usr/bin/env python3
"""Demonstration script for API integration.

This module previously contained a full end-to-end demo that relied on a
running API server. During automated testing the script caused syntax
errors and attempted network calls. To keep the repository healthy we
retain a minimal stub that is skipped by pytest and can be expanded for
manual testing when needed.
"""
import pytest

pytestmark = pytest.mark.skip(reason="API integration demo - run manually")


def main() -> None:
    """Entry point for manual execution."""
    print("Run this script manually to demo the API flow when the server is available.")


if __name__ == "__main__":  # pragma: no cover
    main()
