from datetime import datetime
from flask import Blueprint, request, render_template, session, redirect, url_for
from models.history.registro_historico import RegistroHistorico
from models.db import db
from models.user.user import Usuario
from models.admin import Admin, Estatistico, Operador
login_controller = Blueprint("login_controller", __name__, template_folder="../templates")

@login_controller.route('/validated_user', methods=['POST', 'GET'])
def validated_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        # Buscar no banco de dados por um usuário
        usuario = Usuario.query.filter_by(email=user).first()
        if usuario and usuario.senha == password:
            session['username'] = user
            session['user_id'] = usuario.id_usuario 
            session['role'] = 'user'
            return redirect(url_for('home'))

        # Buscar no banco de dados por um administrador
        admin = Admin.query.filter_by(email=user).first()
        if admin and admin.senha == password:
            session['username'] = user
            session['user_id'] = admin.id_admin 
            session['role'] = 'admin'
            return redirect(url_for('home'))
        
        # Buscar no banco de dados por um estatistico
        estatistico = Estatistico.query.filter_by(email=user).first()
        if estatistico and estatistico.senha == password:
            session['username'] = user
            session['user_id'] = estatistico.id_estatistico
            session['role'] = 'estatistico'
            return redirect(url_for('home'))
        

        # Buscar no banco de dados por um operador
        operador = Operador.query.filter_by(email=user).first()
        if operador and operador.senha == password:
            session['username'] = user
            session['user_id'] = operador.id_operador
            session['role'] = 'operador'
            return redirect(url_for('home'))

        

        return '<h1>Credenciais Inválidas!</h1>'
    else:
        return render_template('login.html')


@login_controller.route('/edit_user/<int:id>', methods=['GET'])
def edit_user(id):
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    usuario = Usuario.query.get(id)
    return render_template("edit_user.html", usuario=usuario)

@login_controller.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    usuario = Usuario.query.get(id)
    if usuario:
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        usuario.cpf = request.form['cpf']
        usuario.id_lixeira = request.form['id_lixeira']
        db.session.commit()
    return redirect(url_for('.list_users'))

@login_controller.route('/list_admins')
def list_admins():
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    else:
        admins = Admin.query.all()
        return render_template("admins.html", devices=admins)

@login_controller.route('/register_user')
def register_user():
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    else:
        return render_template("register_user.html")

@login_controller.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session or session.get('role') != 'admin':
         return render_template("accessdenied.html")
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']
        id_lixeira = request.form['id_lixeira']
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, cpf=cpf, id_lixeira=id_lixeira)
        db.session.add(novo_usuario)
        db.session.commit()

        # Adicionando registro histórico
        id_admin = session.get('user_id')  # Obtendo o ID do admin da sessão
        RegistroHistorico.save_registro(id_admin, novo_usuario.id_usuario, datetime.utcnow())

        
        return redirect(url_for('.list_users'))
    else:
        return redirect(url_for('.register_user'))

@login_controller.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if 'username' not in session or session.get('role') != 'admin':
         return render_template("accessdenied.html")
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        admincol = request.form['admincol']
        novo_admin = Admin(nome=nome, email=email, senha=senha, admincol=admincol)
        db.session.add(novo_admin)
        db.session.commit()
        return redirect(url_for('.list_admins'))
    else:
        return redirect(url_for('.register_user'))

@login_controller.route('/del_user/<int:id>', methods=['GET', 'POST'])
def del_user(id):
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    
    usuario = Usuario.query.get(id)
    if usuario:
        # Exclua o registro histórico do usuário
        historico_usuario = RegistroHistorico.query.filter_by(id_usuario=usuario.id_usuario).first()
        if historico_usuario:
            db.session.delete(historico_usuario)
        
        # Exclua o usuário
        db.session.delete(usuario)
        db.session.commit()
    
    return redirect(url_for('login_controller.list_users'))


@login_controller.route('/remove_admin')
def remove_admin():
    if 'username' not in session or session.get('role') != 'admin':
         return render_template("accessdenied.html")
    admins = Admin.query.all()
    return render_template("remove_admin.html", devices=admins)

@login_controller.route('/list_users')
def list_users():
    if 'username' not in session or session.get('role') not in ['admin', 'estatistico']:
        return render_template("accessdenied.html")
    else:
        usuarios = Usuario.query.all()
        return render_template("users.html", usuarios=usuarios)
    
@login_controller.route('/del_admin', methods=['GET', 'POST'])
def del_admin():
    if 'username' not in session or session.get('role') != 'admin':
        return render_template("accessdenied.html")
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
        return redirect(url_for('.list_admins'))
    else:
        return redirect(url_for('.remove_admin'))