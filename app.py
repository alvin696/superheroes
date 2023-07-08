#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def home():
        return 'Hello, world!'

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if hero is None:
            return jsonify({'error': 'Hero not found'}), 404
        return jsonify(hero.to_dict())

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if power is None:
            return jsonify({'error': 'Power not found'}), 404
        return jsonify(power.to_dict())

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if power is None:
            return jsonify({'error': 'Power not found'}), 404
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
        db.session.commit()
        return jsonify(power.to_dict())

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
        if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
            return jsonify({'errors': ['Invalid request data']}), 400
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']
        hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5555)
