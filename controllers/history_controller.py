from flask import Blueprint, request, render_template
from sqlalchemy import join
from models.history.sensor_historico import SensorHistorico
from models.history.atuador_historico import AtuadorHistorico
from models.iot.sensor import Sensor
from models.iot.atuador import Atuador
from models.iot.lixeira import Lixeira
from models.iot.comando_remoto_historico import ComandoRemotoHistorico
from models.history.registro_historico import RegistroHistorico
from models.admin import Admin 
from models.user.user import Usuario  
from models.db import db

history_bp = Blueprint("history", __name__, template_folder="../views")

@history_bp.route('/history', methods=['GET', 'POST'])
def get_history():
    sensors = Sensor.query.all()
    actuators = Atuador.query.all()
    lixeiras = Lixeira.query.all()
    usuarios = RegistroHistorico.query.all()
    history = []
    item_type = 'sensor'
    start_time = None
    end_time = None

    if request.method == 'POST':
        item_type = request.form.get('type')
        start_time = request.form.get('start')
        end_time = request.form.get('end')

        if item_type == 'sensor':
            history = db.session.query(
                SensorHistorico,
                Sensor.tipo_sensor
            ).join(Sensor, SensorHistorico.id_sensor == Sensor.id_sensor)\
             .filter(SensorHistorico.data_hora_registro.between(start_time, end_time)).all()
        elif item_type == 'actuator':
            history = db.session.query(
                AtuadorHistorico,
                Atuador.tipo_atuador
            ).join(Atuador, AtuadorHistorico.id_atuador == Atuador.id_atuador)\
             .filter(AtuadorHistorico.data_hora_registro.between(start_time, end_time)).all()
        elif item_type == 'lixeira':
            history = Lixeira.query.filter(Lixeira.data_hora_registro.between(start_time, end_time)).all()
        elif item_type == 'comando_remoto_historico':
            history = ComandoRemotoHistorico.query.filter(ComandoRemotoHistorico.data_hora_registro.between(start_time, end_time)).all()
        elif item_type == 'usuario':
            print("abriu")
            history = db.session.query(RegistroHistorico, Admin.nome.label('nome_admin'), Usuario.nome.label('nome_usuario')).join(Admin, RegistroHistorico.id_admin == Admin.id_admin)\
             .join(Usuario, RegistroHistorico.id_usuario == Usuario.id_usuario)\
             .filter(RegistroHistorico.data_cadastro.between(start_time, end_time)).all()
            print(history)
    return render_template('history.html', sensors=sensors, actuators=actuators, lixeiras=lixeiras, usuarios=usuarios, history=history, type=item_type, start=start_time, end=end_time)