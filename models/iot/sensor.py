from models.db import db
from models.iot.lixeira import Lixeira

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id_sensor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_sensor = db.Column(db.String(145), nullable=False)
    id_lixeira = db.Column(db.Integer, db.ForeignKey('lixeira.id_lixeira'), nullable=False)
    topic = db.Column(db.String(145), nullable=False)
    caminho_imagem = db.Column(db.String(255), default="../static/img/sensor.png")  # Modificação aqui

    @staticmethod
    def save_sensor(tipo_sensor, id_lixeira, topic):
        sensor = Sensor(tipo_sensor=tipo_sensor, id_lixeira=id_lixeira, topic=topic)
        db.session.add(sensor)
        db.session.commit()

    @staticmethod
    def get_sensors():
        return Sensor.query.join(Lixeira).add_columns(
            Lixeira.id_lixeira, Lixeira.estado, Lixeira.localizacao, Lixeira.capacidade,
            Sensor.id_sensor, Sensor.tipo_sensor, Sensor.topic
        ).all()

    @staticmethod
    def get_single_sensor(id):
        return Sensor.query.filter_by(id_sensor=id).first()

    @staticmethod
    def update_sensor(id, tipo_sensor, id_lixeira, topic):
        sensor = Sensor.query.filter_by(id_sensor=id).first()
        if sensor:
            sensor.tipo_sensor = tipo_sensor
            sensor.id_lixeira = id_lixeira
            sensor.topic = topic
            db.session.commit()
            return sensor

    @staticmethod
    def delete_sensor(id):
        sensor = Sensor.query.filter_by(id_sensor=id).first()
        if sensor:
            db.session.delete(sensor)
            db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
