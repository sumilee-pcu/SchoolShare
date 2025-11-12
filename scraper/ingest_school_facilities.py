"""Persist school facility availability snapshots into the local database."""
from __future__ import annotations

import datetime as dt
from typing import Dict, Iterable, Tuple

from backend.database import SessionLocal, create_db_and_tables
from backend.models import Facility, School

from .config import ScraperSettings
from .seoul_api_client import SchoolRow, SeoulSchoolAPIClient

FACILITY_FIELD_MAP: Dict[str, str] = {
    "운동장": "STDM_OPN_YN",
    "체육관": "GYM_OPN_YN",
    "강당": "HALL_OPN_YN",
    "일반교실": "GNRL_SBJCT_CLAS_OPN_YN",
    "특별교실": "SPC_CLAS_OPN_YN",
    "시청각실": "AVR_OPN_YN",
}

AVAILABILITY_MAP: Dict[str, Tuple[str, str]] = {
    "Y": ("개방", "OPEN"),
    "N": ("미개방", "CLOSED"),
}


def _translate_availability(raw_value: str) -> str:
    normalized = (raw_value or "").strip().upper()
    label, _ = AVAILABILITY_MAP.get(normalized, ("정보없음", "UNKNOWN"))
    return label


def _should_include(row: SchoolRow, settings: ScraperSettings) -> bool:
    return settings.target_region in row.region


def _upsert_school(session, row: SchoolRow) -> School:
    school = session.query(School).filter_by(school_name=row.name).one_or_none()
    if school is None:
        school = School(school_name=row.name, address=row.region)
        session.add(school)
    else:
        school.address = row.region or school.address
    return school


def _upsert_facility(session, school: School, facility_label: str, availability: str) -> None:
    facility = (
        session.query(Facility)
        .filter_by(school_id=school.id, facility_type=facility_label)
        .one_or_none()
    )
    now = dt.datetime.utcnow()
    if facility is None:
        facility = Facility(
            school_id=school.id,
            facility_type=facility_label,
            is_available=availability,
            last_updated=now,
        )
        session.add(facility)
    else:
        facility.is_available = availability
        facility.last_updated = now


def ingest_facilities() -> None:
    settings = ScraperSettings.from_env()
    create_db_and_tables()

    client = SeoulSchoolAPIClient(settings=settings)

    with SessionLocal() as session:
        processed = 0
        for row in client.iter_school_rows():
            if not _should_include(row, settings):
                continue

            school = _upsert_school(session, row)
            session.flush()  # ensures school.id

            for facility_label, field_name in FACILITY_FIELD_MAP.items():
                raw_value = row.raw_fields.get(field_name, "")
                availability = _translate_availability(raw_value)
                _upsert_facility(session, school, facility_label, availability)

            processed += 1
            if processed % 50 == 0:
                session.commit()

        session.commit()


if __name__ == "__main__":
    ingest_facilities()
