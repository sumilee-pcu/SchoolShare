"""Backward-compatible CLI entry point for the scraper."""
from scraper.ingest_school_facilities import ingest_facilities


if __name__ == "__main__":
    ingest_facilities()
