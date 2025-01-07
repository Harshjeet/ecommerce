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
    
    def __init__(self, username, email, password,role=Role.CUSTOMER):
        
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
    
    
#Category table
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Category {self.name}>'

#Product table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_url = db.Column(db.String(255))  # Store product image URL
    is_available = db.Column(db.Boolean, default=True)

    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name} - ${self.price}>'

#stock table
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())

    product = db.relationship('Product', backref=db.backref('stock', lazy=True))

    def __repr__(self):
        return f'<Stock {self.product.name} - {self.quantity} items>'

# cart table
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('cart', lazy=True))

    def __repr__(self):
        return f'<Cart {self.id} - User {self.user_id}>'

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    cart = db.relationship('Cart', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f'<CartItem {self.product.name} - {self.quantity} items>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")  # Status: Pending, Shipped, Delivered, Cancelled
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.id} - User {self.user_id} - Status: {self.status}>'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at purchase time

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __repr__(self):
        return f'<OrderItem {self.product.name} - {self.quantity} items>'


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_method = db.Column(db.String(50))  # Example: Credit Card, PayPal, Cash on Delivery
    status = db.Column(db.String(50), default="Pending")  # Example: Pending, Completed, Failed
    transaction_id = db.Column(db.String(255))  # Store Stripe or PayPal Transaction ID
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    order = db.relationship('Order', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.id} - Order {self.order_id} - Status: {self.status}>'
