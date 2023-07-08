from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    super_name = db.Column(db.String(100))
    powers = db.relationship('HeroPower', back_populates='hero', overlaps="heroes,powers")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': [power.to_dict() for power in self.powers]
        }

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    heroes = db.relationship('HeroPower', back_populates='power', overlaps="heroes,powers")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(100))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    hero = db.relationship('Hero', back_populates='powers', overlaps="heroes,powers")
    power = db.relationship('Power', back_populates='heroes', overlaps="heroes,powers")
    def to_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id
        }

