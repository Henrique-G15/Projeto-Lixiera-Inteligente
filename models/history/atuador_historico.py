from models.db import db
from models.iot.atuador import Atuador

class AtuadorHistorico(db.Model):
    __tablename__ = 'atuador_historico'
    idatuador_historico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_atuador = db.Column(db.Integer, db.ForeignKey('atuador.id_atuador'), nullable=False)
    data_hora_registro = db.Column(db.DateTime, nullable=False)
    dado = db.Column(db.String(145), nullable=False)


    def save_atuador_historico(id_atuador, data_hora_registro, dado):
        atuador_historico = AtuadorHistorico(id_atuador=id_atuador, data_hora_registro=data_hora_registro, dado=dado)
        db.session.add(atuador_historico)
        db.session.commit()


    def get_atuador_historicos():
        return AtuadorHistorico.query.all()


    def get_single_atuador_historico(id):
        return AtuadorHistorico.query.filter_by(idatuador_historico=id).first()


    def delete_atuador_historico(id):
        atuador_historico = AtuadorHistorico.query.filter_by(idatuador_historico=id).first()
        if atuador_historico:
            db.session.delete(atuador_historico)
            db.session.commit()

    def get_latest_actuator_data(id_atuador):
        return AtuadorHistorico.query.filter_by(id_atuador=id_atuador).order_by(AtuadorHistorico.data_hora_registro.desc()).first()