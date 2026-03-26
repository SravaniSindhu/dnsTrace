from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.resolver import resolver_bp
    from app.routes.certs import certs_bp
    from app.routes.trace import trace_bp

    app.register_blueprint(resolver_bp)
    app.register_blueprint(certs_bp)
    app.register_blueprint(trace_bp)

    return app
