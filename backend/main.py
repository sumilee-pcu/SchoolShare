"""Flask API for serving facility data."""
from __future__ import annotations

import logging
from typing import Dict

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from backend.database import SessionLocal
from backend.models import Facility, School

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.logger.setLevel(logging.INFO)

FACILITY_TYPE_PARAM_MAP: Dict[str, str] = {
    "stadium": "운동장",
    "gym": "체육관",
    "auditorium": "강당",
    "general": "일반교실",
    "special": "특별교실",
    "avr": "시청각실",
}

def _resolve_facility_label(param_value: str | None) -> str | None:
    if not param_value:
        return None
    key = param_value.strip().lower()
    if key in FACILITY_TYPE_PARAM_MAP:
        return FACILITY_TYPE_PARAM_MAP[key]
    raise ValueError(f"Unsupported facility type: {param_value}")


@app.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok"})


@app.route("/api/facilities", methods=["GET"])
def get_facilities():
    region = request.args.get("region", "노원구")
    facility_type = request.args.get("type")
    availability = request.args.get("availability")  # No default - show all if not specified
    limit_raw = request.args.get("limit", "50")

    try:
        limit = min(max(int(limit_raw), 1), 200)
    except ValueError:
        return jsonify({"error": "'limit' must be an integer"}), 400

    try:
        resolved_facility = _resolve_facility_label(facility_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    session = SessionLocal()
    try:
        app.logger.info(f"Query params: region={region}, type={facility_type}, availability={availability}, limit={limit}")

        query = (
            session.query(Facility, School)
            .join(School, Facility.school_id == School.id)
        )

        if region:
            query = query.filter(School.address.contains(region))
        if resolved_facility:
            query = query.filter(Facility.facility_type == resolved_facility)
        if availability:
            query = query.filter(Facility.is_available == availability)

        facilities = (
            query.order_by(School.school_name.asc())
            .limit(limit)
            .all()
        )

        app.logger.info(f"Query returned {len(facilities)} results")

        items = []
        for facility, school in facilities:
            items.append(
                {
                    "school_name": school.school_name,
                    "address": school.address,
                    "facility_type": facility.facility_type,
                    "availability": facility.is_available,
                    "last_updated": facility.last_updated.isoformat() if facility.last_updated else None,
                }
            )

        return jsonify({"count": len(items), "items": items})
    except SQLAlchemyError as exc:  # pragma: no cover - simple API surface
        app.logger.exception("Database query failed")
        return jsonify({"error": "Failed to fetch facilities", "detail": str(exc)}), 500
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
