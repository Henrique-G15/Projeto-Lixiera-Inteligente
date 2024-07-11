from models.db import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id_admin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(145), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(145), nullable=False)
    admincol = db.Column(db.String(145), nullable=False)

class Estatistico(db.Model):
    __tablename__ = 'estatistico'
    id_estatistico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(145), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(145), nullable=False)

class Operador(db.Model):
    __tablename__ = 'operador'
    id_operador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(145), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(145), nullable=False)