from flask import Blueprint, request, jsonify
from flask_mqtt import Mqtt
import json

remote_bp = Blueprint('remote', __name__)
mqtt = Mqtt()

ContorleRemotoTopico = 'teste/abrir'

@remote_bp.route('/comandoRemoto', methods=['POST'])
def controle_remoto():
    data = request.json
    topic = data.get('topic', ContorleRemotoTopico)
    message = data.get('message')

    if not topic or not message:
        return jsonify({"error": "Topic and message are required"}), 400

    mqtt.publish(topic, json.dumps(message))
    return jsonify({"status": f"Message sent to topic {topic}"}), 200

@mqtt.on_message()
def handle_remote_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)
    print(f"Received message: {data}")
    # Add logic to handle received messages if needed

def init_mqtt(app):
    mqtt.init_app(app)
    mqtt.subscribe('#')  # Subscribe to all topics for demonstration
    mqtt.on_message = handle_remote_message


