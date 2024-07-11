import paho.mqtt.client as mqtt
from models.db import db
from datetime import datetime
import json

class Lixeira(db.Model):
    __tablename__ = 'lixeira'
    id_lixeira = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.Integer, nullable=False)
    localizacao = db.Column(db.String(145), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    atuadores = db.relationship('Atuador', backref='lixeira', lazy=True)
    sensores = db.relationship('Sensor', backref='lixeira', lazy=True)
    data_hora_registro = db.Column(db.DateTime, default=datetime.now, nullable=False)

    @staticmethod
    def save_lixeira(estado, localizacao, capacidade):
        lixeira = Lixeira(estado=estado, localizacao=localizacao, capacidade=capacidade)
        db.session.add(lixeira)
        db.session.commit()

    @staticmethod
    def get_lixeiras():
        return Lixeira.query.all()

    @staticmethod
    def get_single_lixeira(id):
        return Lixeira.query.filter_by(id_lixeira=id).first()

    @staticmethod
    def update_lixeira(id, estado=None, localizacao=None, capacidade=None):
        lixeira = Lixeira.query.filter_by(id_lixeira=id).first()
        if lixeira:
            if estado is not None:
                lixeira.estado = estado
            if localizacao is not None:
                lixeira.localizacao = localizacao
            if capacidade is not None:
                lixeira.capacidade = capacidade
            db.session.commit()
            return lixeira

    @staticmethod
    def delete_lixeira(id):
        lixeira = Lixeira.query.filter_by(id_lixeira=id).first()
        if lixeira:
            db.session.delete(lixeira)
            db.session.commit()

# Funções de callback do MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de resultado {rc}")
    client.subscribe("test/publishe")

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload}")
    try:
        data = json.loads(msg.payload)
        estado = data.get(msg.payload)
        localizacao = data.get('localizacao', 'Localização Exemplo')
        capacidade = data.get('capacidade', 100)
        if estado is not None:
            # Salvar o estado no banco de dados
            Lixeira.save_lixeira(estado, localizacao, capacidade)
            print(f"Estado {estado}, localização {localizacao}, capacidade {capacidade} salvo no banco de dados")
        else:
            print("Chave 'estado' não encontrada no payload")
    except json.JSONDecodeError:
        print("Falha ao decodificar a mensagem JSON")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

# Iniciar o loop de escuta do MQTT em uma thread separada
client.loop_start()