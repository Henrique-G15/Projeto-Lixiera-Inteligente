from models.db import db
from models.iot.lixeira import Lixeira

class ControleRemoto(db.Model):
    __tablename__ = 'controle_remoto'
    id_controle = db.Column(db.Integer, primary_key=True)
    id_lixeira = db.Column(db.Integer, db.ForeignKey('lixeira.id_lixeira'), nullable=False)
    estado = db.Column(db.Boolean, default=False)

    def __init__(self, id_lixeira, estado=False):
        self.id_lixeira = id_lixeira
        self.estado = estado

    @staticmethod
    def ligar_controle(id_controle):
        controle = ControleRemoto.query.filter_by(id_controle=id_controle).first()
        if controle:
            controle.estado = True
            db.session.commit()
            return controle

    @staticmethod
    def desligar_controle(id_controle):
        controle = ControleRemoto.query.filter_by(id_controle=id_controle).first()
        if controle:
            controle.estado = False
            db.session.commit()
            return controle

    @staticmethod
    def verificar_estado(id_controle):
        controle = ControleRemoto.query.filter_by(id_controle=id_controle).first()
        if controle:
            return controle.estado

    @staticmethod
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
