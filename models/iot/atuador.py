from models.db import db
from models.iot.lixeira import Lixeira

class Atuador(db.Model):
    __tablename__ = 'atuador'
    id_atuador = db.Column(db.Integer, primary_key=True)
    tipo_atuador = db.Column(db.String(145), nullable=False)
    id_lixeira = db.Column(db.Integer, db.ForeignKey('lixeira.id_lixeira'), nullable=False)
    topic = db.Column(db.String(145), nullable=False)
    caminho_imagem = db.Column(db.String(255), default="../static/img/servo.png")

    @staticmethod
    def save_actuator(tipo_atuador, id_lixeira, topic):
        atuador = Atuador(tipo_atuador=tipo_atuador, id_lixeira=id_lixeira, topic=topic)
        db.session.add(atuador)
        db.session.commit()

    @staticmethod
    def get_actuators():
        return Atuador.query.join(Lixeira).add_columns(
            Lixeira.id_lixeira, Lixeira.estado, Lixeira.localizacao, Lixeira.capacidade,
            Atuador.id_atuador, Atuador.tipo_atuador, Atuador.topic
        ).all()

    @staticmethod
    def get_single_actuator(id):
        return Atuador.query.filter_by(id_atuador=id).first()

    @staticmethod
    def update_actuator(id, tipo_atuador, id_lixeira, topic):
        atuador = Atuador.query.filter_by(id_atuador=id).first()
        if atuador:
            atuador.tipo_atuador = tipo_atuador
            atuador.id_lixeira = id_lixeira
            atuador.topic = topic
            db.session.commit()
            return atuador

    @staticmethod
    def delete_actuator(id):
        atuador = Atuador.query.filter_by(id_atuador=id).first()
        if atuador:
            db.session.delete(atuador)
            db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}