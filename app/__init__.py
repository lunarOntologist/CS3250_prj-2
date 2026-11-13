from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login' # Assuming a login route exists

    # Register Blueprints
    from app.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Placeholder for a simple user loader for testing
    @login_manager.user_loader
    def load_user(user_id):
        # In a real app, this fetches from DB. For testing setup, we'll mock or handle it simply.
        # We need a minimal user structure for tests to work.
        from app.models import User
        return User.query.get(int(user_id))

    return app
