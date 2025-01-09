from flask import Flask
from .config import Config
from .models import User, db, Role
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize db
    db.init_app(app)
    jwt = JWTManager(app)
    with app.app_context():
        create_database(app)
        
# Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
   
    
    return app

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

def create_database(app):
    with app.app_context():
        db.create_all()
        create_admin()
        print("Database created successfully")