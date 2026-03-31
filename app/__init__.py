from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "tu_clave_secreta"

    # Rutas
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    return app