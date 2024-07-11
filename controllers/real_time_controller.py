from flask import Blueprint, render_template, request, session
from models.iot.lixeira import Lixeira
from models.iot.sensor import Sensor
from models.iot.atuador import Atuador
from models.user.user import Usuario
from models.db import db
from models.history.sensor_historico import SensorHistorico
from models.history.atuador_historico import AtuadorHistorico
from datetime import datetime
from flask_socketio import emit, join_room, leave_room

real_time_bp = Blueprint('real_time', __name__)

@real_time_bp.route('/tempo_real', methods=['GET', 'POST'])
def tempo_real():
    user_id = session.get('user_id')
    
    # Primeiro, consulte o usuário logado pelo id_usuario
    user = Usuario.query.filter_by(id_usuario=user_id).first()
    
    if user is None:
        # Se o usuário não for encontrado, defina como usuário com id 1
        user = Usuario.query.filter_by(id_usuario=1).first()
        if user is None:
            # Se o usuário com id 1 também não for encontrado, retorne um erro ou tome outra ação apropriada
            return "Erro: Usuário não encontrado", 404

    # Depois, utilize o id_lixeira do usuário para buscar as lixeiras relacionadas
    lixeiras = Lixeira.query.filter_by(id_lixeira=user.id_lixeira).all()
    
    selected_lixeira = None
    atuadores = []
    sensores = []

    if request.method == 'POST':
        lixeira_id = request.form.get('lixeira')
    else:
        lixeira_id = lixeiras[0].id_lixeira if lixeiras else None

    if lixeira_id:
        selected_lixeira = Lixeira.query.filter_by(id_lixeira=lixeira_id).first()
        
        if selected_lixeira:
            # Consulta os atuadores e seus últimos registros históricos
            atuadores_query = db.session.query(
                Atuador.id_atuador,
                Atuador.tipo_atuador,
                Atuador.id_lixeira,
                db.func.max(AtuadorHistorico.data_hora_registro).label('data_hora_registro'),
                AtuadorHistorico.dado,
                Atuador.caminho_imagem  # Adiciona o caminho da imagem do atuador
            ).join(AtuadorHistorico, Atuador.id_atuador == AtuadorHistorico.id_atuador).filter(
                Atuador.id_lixeira == lixeira_id
            ).group_by(
                Atuador.id_atuador,
                Atuador.tipo_atuador,
                Atuador.id_lixeira,
                AtuadorHistorico.dado
            ).all()

            # Converter os resultados da consulta em dicionários
            atuadores = [atuador._asdict() for atuador in atuadores_query]

            # Consulta os sensores e seus últimos registros históricos
            sensores_subquery = db.session.query(
                SensorHistorico.id_sensor,
                db.func.max(SensorHistorico.data_hora_registro).label('latest_data_hora_registro')
            ).group_by(
                SensorHistorico.id_sensor
            ).subquery()

            sensores_query = db.session.query(
                Sensor.id_sensor,
                Sensor.tipo_sensor,
                Sensor.id_lixeira,
                SensorHistorico.data_hora_registro,
                SensorHistorico.dado,
                Sensor.caminho_imagem  # Adiciona o caminho da imagem do sensor
            ).join(
                sensores_subquery, 
                (SensorHistorico.id_sensor == sensores_subquery.c.id_sensor) & 
                (SensorHistorico.data_hora_registro == sensores_subquery.c.latest_data_hora_registro)
            ).join(
                Sensor, Sensor.id_sensor == SensorHistorico.id_sensor
            ).filter(
                Sensor.id_lixeira == lixeira_id
            ).all()

            # Converter os resultados da consulta em dicionários
            sensores = [sensor._asdict() for sensor in sensores_query]

            # Atualize a sessão do usuário com os novos dados
            session['atuadores'] = atuadores
            session['sensores'] = sensores

    return render_template('tempoReal.html', lixeiras=lixeiras, selected_lixeira=selected_lixeira, atuadores=atuadores, sensores=sensores)

# Funções de socketio
def create_socketio_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('subscribe')
    def handle_subscribe(data):
        room = data.get('room')
        join_room(room)
        emit('status', {'msg': f'Joined room: {room}'}, room=room)

    @socketio.on('unsubscribe')
    def handle_unsubscribe(data):
        room = data.get('room')
        leave_room(room)
        emit('status', {'msg': f'Left room: {room}'}, room=room)

    @socketio.on('sensor_data')
    def handle_sensor_data(data):
        id_sensor = data.get('id_sensor')
        dado = data.get('dado')
        data_hora_registro = datetime.now()
        SensorHistorico.save_sensor_historico(id_sensor, data_hora_registro, dado)
        emit('new_sensor_data', data, broadcast=True)

    @socketio.on('actuator_data')
    def handle_actuator_data(data):
        id_atuador = data.get('id_atuador')
        dado = data.get('dado')
        data_hora_registro = datetime.now()
        AtuadorHistorico.save_atuador_historico(id_atuador, data_hora_registro, dado)
        emit('new_actuator_data', data, broadcast=True)
