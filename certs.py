from flask import Blueprint, request, jsonify
import ssl, socket

certs_bp = Blueprint("certs", __name__)

def parse_cert_field(field):
    result = {}
    for item in field:
        for pair in item:
            key, value = pair
            result[key] = value
    return result


@certs_bp.route("/api/certs")
def get_cert():

    domain = request.args.get("domain")

    ctx = ssl.create_default_context()

    with socket.create_connection((domain, 443)) as sock:
        with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    return jsonify({
        "issuer": parse_cert_field(cert.get("issuer")),
        "subject": parse_cert_field(cert.get("subject")),
        "notBefore": cert.get("notBefore"),
        "notAfter": cert.get("notAfter")
    })