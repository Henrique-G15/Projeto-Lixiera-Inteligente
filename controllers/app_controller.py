import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, jsonify, session
from models.db import db, instance
from controllers.sensors_controller import sensor_bp
from controllers.actuators_controller import actuator_bp
from controllers.lixeiras_controller import lixeira_bp
from controllers.history_controller import history_bp
from controllers.real_time_controller import real_time_bp
from controllers.login_controller import login_controller
from datetime import datetime
from models.iot.sensor import Sensor
from models.iot.atuador import Atuador
from models.history.sensor_historico import SensorHistorico
from models.history.atuador_historico import AtuadorHistorico
from models.iot.comando_remoto_historico import ComandoRemotoHistorico

def create_app():
    app = Flask(__name__, template_folder="../views", static_folder="ProjetoLixeiraInteligente/static", root_path="./")

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    # MQTT configuration
    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5000
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt_client = Mqtt()
    mqtt_client.init_app(app)

    socketio = SocketIO(app)

    app.register_blueprint(sensor_bp, url_prefix='/')
    app.register_blueprint(actuator_bp, url_prefix='/')
    app.register_blueprint(lixeira_bp, url_prefix='/')
    app.register_blueprint(history_bp, url_prefix='/')
    app.register_blueprint(real_time_bp, url_prefix='/real_time')
    app.register_blueprint(login_controller, url_prefix='/')

    topic_subscribe = "/comando"  # Tópico para se inscrever

    # MQTT message handler
    def handle_sensor_message(sensor, message):
        try:
            data_hora_registro = datetime.now()
            dado = message.payload.decode()
            SensorHistorico.save_sensor_historico(sensor.id_sensor, data_hora_registro, dado)
            print(f"Sensor data saved: {dado}")
        except Exception as e:
            print(f"Error saving sensor data: {e}")

    def handle_actuator_message(actuator, message):
        try:
            data_hora_registro = datetime.now()
            dado = message.payload.decode()
            AtuadorHistorico.save_atuador_historico(actuator.id_atuador, data_hora_registro, dado)
            print(f"Actuator data saved: {dado}")
        except Exception as e:
            print(f"Error saving actuator data: {e}")

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            with app.app_context():
                mqtt_client.subscribe(topic_subscribe)  # Inscrição no tópico
                sensors = Sensor.query.all()
                actuators = Atuador.query.all()
                for sensor in sensors:
                    mqtt_client.subscribe(sensor.topic)
                for actuator in actuators:
                    mqtt_client.subscribe(actuator.topic)
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        with app.app_context():
            sensor = Sensor.query.filter_by(topic=message.topic).first()
            if sensor:
                handle_sensor_message(sensor, message)
            else:
                actuator = Atuador.query.filter_by(topic=message.topic).first()
                if actuator:
                    handle_actuator_message(actuator, message)
                else:
                    print(f"Unknown topic: {message.topic}")

    @socketio.on('publish')
    def handle_publish(json_data):
        topic = json_data['topic']
        message = json_data['message']
        mqtt_client.publish(topic, message)

    @app.route('/')
    def start():
        return render_template('start.html')

    @app.route('/home')
    def home():
        return render_template("home.html")

    @app.route('/publish_message', methods=['POST'])
    def publish_message():
        print('publish_message')
        request_data = request.get_json()
        topic = "/comando"  # Tópico único para enviar as mensagens
        message = request_data['message']

        # Publica a mensagem via MQTT
        publish_status, publish_result = mqtt_client.publish(topic, message)

        # Verifica se a publicação foi bem-sucedida
        if publish_status == 0:
            # Salva no banco de dados
            try:
                with app.app_context():
                    ComandoRemotoHistorico.save_comando_remoto_historico(message, topic)
            except Exception as e:
                print(f"Error saving command history: {e}")

            return jsonify({"status": True, "message": message, "topic": topic})
        else:
            # Falha na publicação
            return jsonify({"status": False, "error_message": "Failed to publish message", "message": message, "topic": topic})


    @app.route('/comandoRemoto')
    def comandoRemoto():
        if 'username' not in session or session.get('role') not in ['admin', 'operador']:
            return render_template("accessdenied.html")
        return render_template("comandoRemoto.html")

    return app, socketio, mqtt_client