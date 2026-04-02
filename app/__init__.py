from flask import Flask, session

def create_app():
    app = Flask(__name__)
    app.secret_key = "tu_clave_secreta"

    # Rutas
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.inventario_routes import inventario_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inventario_bp)
    
    @app.context_processor
    def inject_user():
        return dict(usuario=session.get("usuario"))


    return app