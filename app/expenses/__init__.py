from .routes import expense_bp


def init_expense_module(app):
    app.register_blueprint(expense_bp)

__all__=['expense', 'init_expense_module']