import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from app import db


class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)


class Comix(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String(120), unique=False, nullable=True)
    autor_id = db.Column(db.Integer, ForeignKey("autor.id"), nullable=False)

    def __repr__(self):
        return "<Comix %r>" % self.id


class ComixPages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    elements = db.Column(db.JSON, default=None, nullable=True)
    comix_id = db.Column(db.Integer, ForeignKey("comix.id"), nullable=False)

    def __repr__(self):
        return "<ComixPage %r>" % self.id
