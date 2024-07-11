from models.db import db
from datetime import datetime

class ComandoRemotoHistorico(db.Model):
    __tablename__ = 'comando_remoto_historico'
    id = db.Column(db.Integer, primary_key=True)
    data_hora_registro = db.Column(db.DateTime, default=datetime.now)
    mensagem = db.Column(db.String(50))
    topico = db.Column(db.String(100))

    def __repr__(self):
        return f"<ComandoRemotoHistorico(id={self.id}, data_hora_registro={self.data_hora_registro}, mensagem={self.mensagem}, topico={self.topico})>"

    @staticmethod
    def save_comando_remoto_historico(mensagem, topico):

        try:
            mensagem = int(mensagem)
        except ValueError:
            # Trate o caso em que a mensagem não pode ser convertida em inteiro
            raise ValueError("A mensagem deve ser um número inteiro.")

        # Define a mensagem baseada no valor fornecido
        mensagem = "fechado" if mensagem == 0 else "aberto"
        comando = ComandoRemotoHistorico(mensagem=mensagem, topico=topico)
        db.session.add(comando)
        db.session.commit()
