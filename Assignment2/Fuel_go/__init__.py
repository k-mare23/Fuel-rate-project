from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'afiowt'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://///Users/alpha/Downloads/4353 Group project /front end/Project_Group18/Assignment2/Fuel_go/database.db'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Profile, Quote

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# this is replace the old data with the new data
def create_database(app):
    if not path.exists('Fuel_Go/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

if __name__ == '__main__':
    app = create_app()
    app.run(port=3000)