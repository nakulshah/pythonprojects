# snippets/shopsapi.py
from flask import Blueprint, request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy


shop = Blueprint('shop', __name__)
db = SQLAlchemy()


class Shelf(db.Model):
    __tablename__ = 'shelves'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    products = db.relationship('Product', backref='shelf', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelves.id'), nullable=False)

def create_app():
    print('Creating Flask app for shop')
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(shop)
    with app.app_context():
        db.create_all()
    return app

@shop.route('/shop/shelves', methods=['POST'])
def create_shelf():
    data = request.get_json()
    shelf_name = data.get('shelf_name')
    if Shelf.query.filter_by(name=shelf_name).first():
        return jsonify({'error': 'Shelf already exists.'}), 400
    shelf = Shelf(name=shelf_name)
    db.session.add(shelf)
    db.session.commit()
    return jsonify({'message': f'Shelf {shelf_name} created.'}), 201

@shop.route('/shop/shelves/<shelf_name>/products', methods=['POST'])
def add_product(shelf_name):
    data = request.get_json()
    product_name = data.get('product')
    shelf = Shelf.query.filter_by(name=shelf_name).first()
    if not shelf:
        return jsonify({'error': 'Shelf does not exist.'}), 404
    product = Product(name=product_name, shelf=shelf)
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': f'Product added to {shelf_name}.'}), 201

@shop.route('/shop/shelves', methods=['GET'])
def list_shelves():
    shelves = Shelf.query.all()
    return jsonify([shelf.name for shelf in shelves])

@shop.route('/shop/shelves/<shelf_name>/products', methods=['GET'])
def list_products(shelf_name):
    shelf = Shelf.query.filter_by(name=shelf_name).first()
    if not shelf:
        return jsonify({'error': 'Shelf does not exist.'}), 404
    return jsonify([product.name for product in shelf.products])

# create a GET endpoint to return 'hello shop'
@shop.route('/shop/hello', methods=['GET'])
def hello_shop():
    return jsonify({'message': 'Hello, Shop!'})