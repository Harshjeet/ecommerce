from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Category, Product, Role, User

product_bp = Blueprint("product", __name__)
api = Api(product_bp)

# Helper function to check if user is Admin or Store Manager
def is_admin_or_manager(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user and user.role in [Role.ADMIN, Role.STORE_MANAGER]:
        return True
    return False

### CATEGORY CRUD ###
class CategoryAPI(Resource):
    @jwt_required()
    def post(self):
        """Create a new category (Admin & Store Manager Only)"""
        user_email = get_jwt_identity()["email"]
        if not is_admin_or_manager(user_email):
            return {"error": "Unauthorized access"}, 403

        data = request.get_json()
        if not data or "name" not in data:
            return {"error": "Missing category name"}, 400

        category_exists = Category.query.filter_by(name=data["name"]).first()
        if category_exists:
            return {"error": "Category already exists"}, 400

        new_category = Category(name=data["name"], description=data.get("description"))
        db.session.add(new_category)
        db.session.commit()

        return {"message": "Category created successfully", "category_id": new_category.id}, 201

    def get(self, category_id=None):
        """Retrieve all categories or a specific category"""
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return {"error": "Category not found"}, 404
            return {"id": category.id, "name": category.name, "description": category.description}, 200

        categories = Category.query.all()
        return [{"id": cat.id, "name": cat.name, "description": cat.description} for cat in categories], 200

    @jwt_required()
    def put(self, category_id):
        """Update a category (Admin & Store Manager Only)"""
        user_email = get_jwt_identity()["email"]
        if not is_admin_or_manager(user_email):
            return {"error": "Unauthorized access"}, 403

        category = Category.query.get(category_id)
        if not category:
            return {"error": "Category not found"}, 404

        data = request.get_json()
        if "name" in data:
            category.name = data["name"]
        if "description" in data:
            category.description = data["description"]

        db.session.commit()
        return {"message": "Category updated successfully"}, 200

    @jwt_required()
    def delete(self, category_id):
        """Delete a category (Admin & Store Manager Only)"""
        user_email = get_jwt_identity()["email"]
        if not is_admin_or_manager(user_email):
            return {"error": "Unauthorized access"}, 403

        category = Category.query.get(category_id)
        if not category:
            return {"error": "Category not found"}, 404

        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted successfully"}, 200


### PRODUCT CRUD ###
class ProductAPI(Resource):
    @jwt_required()
    def post(self):
        """Create a new product (Admin & Store Manager Only)"""
        user_email = get_jwt_identity()["email"]
        if not is_admin_or_manager(user_email):
            return {"error": "Unauthorized access"}, 403

        data = request.get_json()
        required_fields = ["name", "price", "category_id"]
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400

        category = Category.query.get(data["category_id"])
        if not category:
            return {"error": "Invalid category"}, 400

        new_product = Product(
            name=data["name"],
            description=data.get("description"),
            price=data["price"],
            category_id=data["category_id"],
            image_url=data.get("image_url"),
            is_available=data.get("is_available", True),
        )
        db.session.add(new_product)
        db.session.commit()

        return {"message": "Product created successfully", "product_id": new_product.id}, 201

    def get(self, product_id=None):
        """Retrieve all products or a specific product"""
        if product_id:
            product = Product.query.get(product_id)
            if not product:
                return {"error": "Product not found"}, 404
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category_id": product.category_id,
                "image_url": product.image_url,
                "is_available": product.is_available,
            }, 200

        products = Product.query.all()
        return [{
            "id": prod.id,
            "name": prod.name,
            "description": prod.description,
            "price": prod.price,
            "category_id": prod.category_id,
            "image_url": prod.image_url,
            "is_available": prod.is_available,
        } for prod in products], 200

    @jwt_required()
    def put(self, product_id):
        """Update a product (Admin & Store Manager Only)"""
        user_email = get_jwt_identity()["email"]
        if not is_admin_or_manager(user_email):
            return {"error": "Unauthorized access"}, 403

        product = Product.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.get_json()
        if "name" in data:
            product.name = data["name"]
        if "description" in data:
            product.description = data["description"]
        if "price" in data:
            product.price = data["price"]
        if "is_available" in data:
            product.is_available = data["is_available"]
        if "image_url" in data:
            product.image_url = data["image_url"]

        db.session.commit()
        return {"message": "Product updated successfully"}, 200

    @jwt_required()
    def delete(self, product_id):
        """Delete a product (Admin & Store Manager Only)"""
        user_email = get_jwt_identity()["email"]
        if not is_admin_or_manager(user_email):
            return {"error": "Unauthorized access"}, 403

        product = Product.query.get(product_id)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200


# Register API routes
api.add_resource(CategoryAPI, "/categories", "/categories/<int:category_id>")
api.add_resource(ProductAPI, "/products", "/products/<int:product_id>")
