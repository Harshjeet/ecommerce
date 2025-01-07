from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()

class Role(enum.Enum):
    ADMIN = 'admin'
    STORE_MANAGER = 'store_manager'
    CUSTOMER = 'customer'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.CUSTOMER)
    
    def __init__(self, username, email, password,role: Role.CUSTOMER):
        
        self.role = role
        self.email = email
        self.set_password(password)
        self.username = username
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.email} - {self.role.value}>'