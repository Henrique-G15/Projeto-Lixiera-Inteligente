from models.db import db
from models.iot.sensor import Sensor

class SensorHistorico(db.Model):
    __tablename__ = 'sensor_historico'
    idsensor_historico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sensor = db.Column(db.Integer, db.ForeignKey('sensor.id_sensor'), nullable=False)
    data_hora_registro = db.Column(db.DateTime, nullable=False)
    dado = db.Column(db.String(145), nullable=False)


    def save_sensor_historico(id_sensor, data_hora_registro, dado):
        sensor_historico = SensorHistorico(id_sensor=id_sensor, data_hora_registro=data_hora_registro, dado=dado)
        db.session.add(sensor_historico)
        db.session.commit()


    def get_sensor_historicos():
        return SensorHistorico.query.all()


    def get_single_sensor_historico(id):
        return SensorHistorico.query.filter_by(idsensor_historico=id).first()


    def delete_sensor_historico(id):
        sensor_historico = SensorHistorico.query.filter_by(idsensor_historico=id).first()
        if sensor_historico:
            db.session.delete(sensor_historico)
            db.session.commit()

    def get_latest_sensor_data(id_sensor):
        return SensorHistorico.query.filter_by(id_sensor=id_sensor).order_by(SensorHistorico.data_hora_registro.desc()).first()
