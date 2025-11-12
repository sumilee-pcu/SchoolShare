"""Client helpers for the Seoul Open API."""
from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, Iterator, Optional

import requests

from .config import ScraperSettings


class SeoulOpenAPIError(RuntimeError):
    """Raised when the upstream API call fails."""


@dataclass(frozen=True)
class SchoolRow:
    """A lightweight representation of a school row returned by the API."""

    name: str
    region: str
    raw_fields: Dict[str, Optional[str]]


class SeoulSchoolAPIClient:
    """Wraps Seoul's Open API for school facility information."""

    def __init__(self, settings: ScraperSettings, session: Optional[requests.Session] = None) -> None:
        self._settings = settings
        self._session = session or requests.Session()

    def fetch_total_count(self) -> int:
        root = self._request_page(1, 1)
        element = root.find("list_total_count")
        if element is None or not element.text:
            raise SeoulOpenAPIError("list_total_count is missing in the API response")
        return int(element.text)

    def iter_school_rows(self) -> Iterator[SchoolRow]:
        total = self.fetch_total_count()
        batch_size = self._settings.batch_size
        total_pages = math.ceil(total / batch_size)

        for page_idx in range(total_pages):
            start = page_idx * batch_size + 1
            end = min((page_idx + 1) * batch_size, total)
            root = self._request_page(start, end)
            for row in root.findall("row"):
                school_name = self._get_text(row, "SCHL_NM")
                region = self._get_text(row, "RGN")
                if not school_name:
                    continue
                fields = {child.tag: (child.text or "").strip() for child in row}
                yield SchoolRow(name=school_name.strip(), region=region.strip(), raw_fields=fields)

    def _request_page(self, start: int, end: int) -> ET.Element:
        url = f"{self._settings.resource_url}/{start}/{end}/"
        response = self._session.get(url, timeout=30)
        if response.status_code != requests.codes.ok:
            raise SeoulOpenAPIError(f"Request to {url} failed with status {response.status_code}")
        try:
            return ET.fromstring(response.content)
        except ET.ParseError as exc:  # pragma: no cover - defensive
            raise SeoulOpenAPIError(f"Failed to parse XML response: {exc}") from exc

    @staticmethod
    def _get_text(element: ET.Element, tag_name: str) -> str:
        target = element.find(tag_name)
        return (target.text or "").strip() if target is not None else ""
