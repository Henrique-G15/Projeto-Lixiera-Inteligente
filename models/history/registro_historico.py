from models.db import db
from datetime import datetime

class RegistroHistorico(db.Model):
    tablename = 'registro_historico'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_admin = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    data_cadastro = db.Column(db.DateTime,  default=datetime.utcnow)

    @classmethod
    def save_registro(cls, id_admin, id_usuario,data_cadastro):
        registro = cls(id_admin=id_admin, id_usuario=id_usuario, data_cadastro=data_cadastro)
        db.session.add(registro)
        db.session.commit()

    @classmethod
    def get_registros(cls):
        return cls.query.all()

    @classmethod
    def get_single_registro(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def update_registro(cls, id, descricao):
        registro = cls.query.filter_by(id=id).first()
        if registro:
            registro.descricao = descricao
            db.session.commit()
        return cls.get_registros()

    @classmethod
    def delete_registro(cls, id):
        registro = cls.query.filter_by(id=id).first()
        if registro:
            db.session.delete(registro)
            db.session.commit()
        return cls.get_registros()