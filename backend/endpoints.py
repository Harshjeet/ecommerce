from flask_restful import Api, Resource
from flask import Blueprint
from product import CategoryAPI, ProductAPI

product_bp = Blueprint("product", __name__)
api = Api(product_bp)

# Register API routes
api.add_resource(CategoryAPI, "/categories", "/categories/<int:category_id>")
api.add_resource(ProductAPI, "/products", "/products/<int:product_id>")