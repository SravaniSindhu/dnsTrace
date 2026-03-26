from flask import Blueprint, request, jsonify, render_template
from app.services.dns_resolver import resolve_domain
import time

resolver_bp = Blueprint("resolver", __name__)

@resolver_bp.route("/")
def home():
    return render_template("index.html")


@resolver_bp.route("/api/resolve")
def resolve():

    domain = request.args.get("domain")
    record_type = request.args.get("type", "ALL")
    provider = request.args.get("resolver", "google")

    if not domain:
        return jsonify({"error": "Domain required"}), 400

    start = time.time()

    records = resolve_domain(domain, record_type, provider)

    end = time.time()

    query_time = round((end - start) * 1000, 2)

    total_records = sum(len(v) for v in records.values())

    return jsonify({
        "domain": domain,
        "resolver": provider,
        "query_time_ms": query_time,
        "record_type": record_type,
        "total_records": total_records,
        "records": records
    })