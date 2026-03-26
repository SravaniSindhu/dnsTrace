from flask import Blueprint, request, jsonify
from app.services.dns_trace import trace_domain

trace_bp = Blueprint("trace", __name__)

@trace_bp.route("/api/trace")
def trace():

    domain = request.args.get("domain")
    record_type = request.args.get("type", "A")

    # FIX: handle ALL
    if record_type == "ALL":
        record_type = "A"

    try:
        steps = trace_domain(domain, record_type)

        return jsonify({
            "domain": domain,
            "type": record_type,
            "steps": steps
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500