"""Configuration helpers for the scraper package."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ScraperSettings:
    """Runtime configuration for ingesting Seoul school facility data."""

    api_key: str
    base_url: str = "http://openapi.seoul.go.kr:8088"
    resource: str = "schoolInfoOpen"
    target_region: str = "노원구"
    batch_size: int = 500

    @classmethod
    def from_env(cls) -> "ScraperSettings":
        api_key = os.getenv("SEOUL_OPENAPI_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "SEOUL_OPENAPI_KEY environment variable is not set. "
                "Request a key from the Seoul Open API portal and export it before running the scraper."
            )

        target_region = os.getenv("SCHOOLSHARE_TARGET_REGION", "노원구").strip() or "노원구"
        batch_size_raw = os.getenv("SCHOOLSHARE_BATCH_SIZE", "")
        batch_size = int(batch_size_raw) if batch_size_raw.isdigit() else 500

        return cls(
            api_key=api_key,
            target_region=target_region,
            batch_size=batch_size,
        )

    @property
    def resource_url(self) -> str:
        return f"{self.base_url}/{self.api_key}/xml/{self.resource}"
