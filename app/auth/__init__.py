from .routes import auth_bp


def init_auth_module(app):
    """Initialize authentication module"""
    app.register_blueprint(auth_bp)

__all__=['auth_bp', 'init_auth_module']