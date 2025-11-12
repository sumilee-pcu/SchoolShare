"""SQLAlchemy models for SchoolShare's backend."""
from __future__ import annotations

import datetime as dt

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True)
    school_name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)

    facilities = relationship(
        "Facility",
        back_populates="school",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"School(id={self.id}, school_name={self.school_name!r})"


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True)
    facility_type = Column(String, nullable=False)  # e.g., "체육관"
    is_available = Column(String, nullable=False, default="정보없음")
    last_updated = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)

    school = relationship("School", back_populates="facilities")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"Facility(id={self.id}, school_id={self.school_id}, "
            f"facility_type={self.facility_type!r}, availability={self.is_available!r})"
        )
