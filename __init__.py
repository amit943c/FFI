import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = '7e77a3fe-ec53-40b2-92e6-f6bb53d9e5df'
    app.secret_key = 'f1342697-6r62-44ff-82f5-3f1e32045b47'
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    sess.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app