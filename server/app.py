#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Home route
@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# GET all bakeries
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    response = make_response(jsonify(bakeries_serialized), 200)
    return response

# GET bakery by ID
@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({"message": "Bakery not found"}), 404
    bakery_serialized = bakery.to_dict()
    response = make_response(jsonify(bakery_serialized), 200)
    return response

# GET baked goods sorted by price
@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    response = make_response(jsonify(baked_goods_by_price_serialized), 200)
    return response

# GET the most expensive baked good
@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive is None:
        return jsonify({"message": "No baked goods found"}), 404
    most_expensive_serialized = most_expensive.to_dict()
    response = make_response(jsonify(most_expensive_serialized), 200)
    return response

# POST a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    new_baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
    db.session.add(new_baked_good)
    db.session.commit()

    return jsonify(new_baked_good.to_dict()), 201

# PATCH a bakery's name by ID
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return jsonify({"message": "Bakery not found"}), 404

    new_name = request.form.get('new_name')
    bakery.name = new_name
    db.session.commit()

    return jsonify(bakery.to_dict()), 200

# DELETE a baked good by ID
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good is None:
        return jsonify({"message": "Baked Good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked Good deleted successfully"}), 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)
