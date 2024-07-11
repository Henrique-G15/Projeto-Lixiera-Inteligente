from flask import Blueprint, request, render_template, redirect, url_for
from models.iot.atuador import Atuador

actuator_bp = Blueprint("actuator", __name__, template_folder="../views")

@actuator_bp.route('/actuators')
def actuators():
    actuators = Atuador.get_actuators()
    return render_template("actuators.html", atuadores=actuators)

@actuator_bp.route('/register_actuator')
def register_actuator():
    return render_template("register_actuator.html")

@actuator_bp.route('/add_actuator', methods=['POST'])
def add_actuator():
    tipo_atuador = request.form.get("tipo_atuador")
    id_lixeira = request.form.get("id_lixeira")
    topic = request.form.get("topic")
    Atuador.save_actuator(tipo_atuador, id_lixeira, topic)
    return redirect(url_for('actuator.actuators'))

@actuator_bp.route('/edit_actuator/<int:id>')
def edit_actuator(id):
    actuator = Atuador.get_single_actuator(id)
    return render_template("update_actuator.html", actuator=actuator)

@actuator_bp.route('/update_actuator/<int:id>', methods=['POST'])
def update_actuator(id):
    tipo_atuador = request.form.get("tipo_atuador")
    id_lixeira = request.form.get("id_lixeira")
    topic = request.form.get("topic")
    Atuador.update_actuator(id, tipo_atuador, id_lixeira, topic)
    return redirect(url_for('actuator.actuators'))

@actuator_bp.route('/remove_actuator')
def remove_actuator():
    actuators = Atuador.get_actuators()
    return render_template("remove_actuator.html", actuators=actuators)

@actuator_bp.route('/del_actuator/<int:id>', methods=['GET'])
def del_actuator(id):
    Atuador.delete_actuator(id)
    return redirect(url_for('actuator.actuators'))



