from flask import Blueprint, redirect, request, render_template, session, url_for
from models.iot.lixeira import Lixeira
from models.iot.atuador import Atuador
from models import db

lixeira_bp = Blueprint("lixeira", __name__, template_folder="../views")

@lixeira_bp.route('/lixeiras')
def lixeiras():
    lixeiras = Lixeira.get_lixeiras()
    return render_template("lixeiras.html", lixeiras=lixeiras)

@lixeira_bp.route('/register_lixeira')
def register_lixeira():
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    else:
        return render_template("cadastrarlixeira.html")

@lixeira_bp.route('/cadastrar_lixeira', methods=['POST'])
def cadastrar_lixeira():
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")

    if request.method == 'POST':
        capacidade = request.form['capacidade']
        estado = request.form['estado']
        localizacao = request.form['localizacao']

        Lixeira.save_lixeira(estado, localizacao, capacidade)

        return redirect(url_for('lixeira.lixeiras'))
    else:
        return redirect(url_for('lixeira.register_lixeira'))

@lixeira_bp.route('/add_lixeira', methods=['POST'])
def add_lixeira():
    estado = request.form.get("estado")
    localizacao = request.form.get("localizacao")
    capacidade = request.form.get("capacidade")
    data = request.form.get("data_hora_registro")
    Lixeira.save_lixeira(estado, localizacao, capacidade, data)
    lixeiras = Lixeira.get_lixeiras()
    return render_template("lixeiras.html", lixeiras=lixeiras)

@lixeira_bp.route('/edit_lixeira')
def edit_lixeira():
    id = request.args.get('id', None)
    lixeira = Lixeira.get_single_lixeira(id)
    return render_template("update_lixeira.html", lixeira=lixeira)

@lixeira_bp.route('/update_lixeira', methods=['POST'])
def update_lixeira():
    id = request.form.get("id")
    estado = request.form.get("estado")
    localizacao = request.form.get("localizacao")
    capacidade = request.form.get("capacidade")
    Lixeira.update_lixeira(id, estado, localizacao, capacidade)
    lixeiras = Lixeira.get_lixeiras()
    return render_template("lixeiras.html", lixeiras=lixeiras)

@lixeira_bp.route('/remove_lixeira')
def remove_lixeira():
    lixeiras = Lixeira.get_lixeiras()
    return render_template("remove_lixeira.html", devices=lixeiras)

@lixeira_bp.route('/del_lixeira', methods=['GET'])
def del_lixeira():
    id = request.args.get('id', None)
    Lixeira.delete_lixeira(id)
    lixeiras = Lixeira.get_lixeiras()
    return render_template("lixeiras.html", lixeiras=lixeiras)

@lixeira_bp.route('/historico')
def historico():
    if 'username' not in session or session.get('role') not in ['admin', 'estatistico']:
         return render_template("accessdenied.html")
    return render_template("history.html")





