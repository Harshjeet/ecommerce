from flask import Flask
from .config import Config
from .models import User, db, Role

def create_admin():
    email = "admin@email.com"
   
    admin_exists = User.query.filter_by(email=email).first()
    if not admin_exists:  
        admin = User(
            username="admin",
            email=email,
            password="admin",
            role=Role.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully")
    else:
            print("Admin already exists")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # intialize db
    db.init_app(app)   
    create_database(app)     
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        create_admin()
        print("Database created successfully")
    