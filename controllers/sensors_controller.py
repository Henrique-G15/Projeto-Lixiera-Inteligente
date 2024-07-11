from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.sensor import Sensor
from flask import Blueprint, request, render_template, session, redirect, url_for
from models.db import db
from models.user.user import Usuario
from models.admin import Admin, Estatistico, Operador
sensor_bp = Blueprint("sensor", __name__, template_folder="../views")

@sensor_bp.route('/sensors')
def sensors():
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensores=sensors)

@sensor_bp.route('/register_sensor')
def register_sensor():
    return render_template("register_sensor.html")

@sensor_bp.route('/add_sensor', methods=['POST'])
def add_sensor():
    tipo_sensor = request.form.get("tipo_sensor")
    id_lixeira = request.form.get("id_lixeira")
    topic = request.form.get("topic")
    Sensor.save_sensor(tipo_sensor, id_lixeira, topic)
    return redirect(url_for('sensor.sensors'))

@sensor_bp.route('/edit_sensor/<int:id>')
def edit_sensor(id):
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor=sensor)



@sensor_bp.route('/update_sensor/<int:id>', methods=['POST'])
def update_sensor(id):
    tipo_sensor = request.form.get("tipo_sensor")
    id_lixeira = request.form.get("id_lixeira")
    topic = request.form.get("topic")
    Sensor.update_sensor(id, tipo_sensor, id_lixeira, topic)
    return redirect(url_for('sensor.sensors'))

@sensor_bp.route('/remove_sensor')
def remove_sensor():
    sensors = Sensor.get_sensors()
    return render_template("remove_sensor.html", sensors=sensors)

@sensor_bp.route('/tempoReal')
def tempoReal():
    if 'username' not in session or session.get('role') not in ['admin', 'estatistico']:
         return render_template("accessdenied.html")
    return render_template("tempoReal.html")


@sensor_bp.route('/del_sensor/<int:id>', methods=['GET'])
def del_sensor(id):
    Sensor.delete_sensor(id)
    return redirect(url_for('sensor.sensors'))

