from models.db import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_lixeira = db.Column(db.Integer, db.ForeignKey('lixeira.id_lixeira'), nullable=False)
    nome = db.Column(db.String(145), nullable=False)
    email = db.Column(db.String(145), nullable=False)
    senha = db.Column(db.String(145), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)

    @classmethod
    def get_all_users(cls):
        return cls.query.all()