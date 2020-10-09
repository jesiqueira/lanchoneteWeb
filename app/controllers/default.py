
from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from app.models.tables import Funcionario, Mesa, Cliente, Login, TelefoneCliente, Endereco, TelefoneFuncionario
from app.models.Forms import CadastroFuncionario, LoginForm, CadastroCliente
import bcrypt
from functools import wraps


# @app.route('/teste')
# def teste():
#     return render_template('texte.html')

@login_manager.user_loader
def load_user(id):
    return Login.query.filter_by(id=id).first()


@app.route('/')
def index():
    return render_template('index.html')


def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        logim = Login.query.filter_by(id=current_user.get_id()).first()
        if logim.is_admin:
            return f(*args, **kwargs)
        else:
            flash('Não Autorizado, seu login não tem permissão.', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        login_ = Login.query.filter_by(login=form.login.data).first()

        if login_ and validarSenha(form.password.data, login_.password):
            login_user(login_)
            return redirect(url_for('index'))
        else:
            error = 'Login ou Senha incorreta'
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/lista_mesa')
def lista_mesa():
    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, ordem='id')


# cadastro de clientes
@app.route('/cadastro')
def cadastro():
    form = CadastroCliente()
    return render_template('cadastro.html', form=form)


@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():

    form = CadastroCliente()

    if form.validate_on_submit():
        error = []
        Nome = form.nome.data
        Cidade = form.cidade.data
        Cep = form.cep.data
        Cep = int(Cep.replace('-', ''))
        Numero = int(form.numero.data)
        Bairro = form.bairro.data
        Rua = form.rua.data
        Email = form.email.data
        Telefone = form.telefone.data
        LoginCliente = form.login.data
        ReceberEmail = form.receberEmail.data
        # criptografar a senha para salvar no BD
        if form.password.data == form.confirmPassword.data:
            Password = bcrypt.hashpw(form.password.data, bcrypt.gensalt())

            Is_admin = False
            Is_Ativo = True

            login = Login(LoginCliente, Password, Is_admin, Is_Ativo)
            db.session.add(login)
            db.session.commit()

            Login_id = login.id
            # print('login id', login.id)

            cliente = Cliente(Nome, Email, ReceberEmail, Login_id)
            db.session.add(cliente)
            db.session.commit()

            Cliente_id = cliente.id
            # print('Cliente id ', cliente.id)

            endereco = Endereco(Cidade, Cep, Rua, Bairro, Numero, Cliente_id)
            db.session.add(endereco)
            db.session.commit()

            telefone = TelefoneCliente(Telefone, Cliente_id)
            db.session.add(telefone)
            db.session.commit()

            clientes = Cliente.query.all()
            return render_template('listaCliente.html', clientes=clientes, ordem='id')
        else:
            flash('Senha não confere')
            error = 'senha'
            return render_template('cadastro.html', form=form, error=error)


@app.route('/cadFuncionario', methods=['POST', 'GET'])
@login_required_admin
def cadFuncionario():
    form = CadastroFuncionario()

    if form.validate_on_submit():
        error = []
        Nome = form.nome.data
        Cidade = form.cidade.data
        Cep = form.cep.data
        Cep = int(Cep.replace('-', ''))
        Numero = int(form.numero.data)
        Bairro = form.bairro.data
        Rua = form.rua.data
        Email = form.email.data
        Telefone = form.telefone.data
        Inicio_contrato = form.inicio_contrato.data
        LoginFuncionario = form.login.data
        Admin = form.is_admin.data
        Ativo = form.is_ativo.data

        if form.password.data == form.confirmPassword.data:
            Password = bcrypt.hashpw(form.password.data, bcrypt.gensalt())

            login = Login(LoginFuncionario, Password, Admin, Ativo)
            db.session.add(login)
            db.session.commit()

            Login_id = login.id

            funcionario = Funcionario(
                Nome, Email, Cidade, Bairro, Rua, Cep, Numero, Inicio_contrato, None, Login_id)
            db.session.add(funcionario)
            db.session.commit()

            Funcionario_id = funcionario.id

            telefone_funcionario = TelefoneFuncionario(
                Telefone, Funcionario_id)
            db.session.add(telefone_funcionario)
            db.session.commit()

        else:
            error = 'senha'
            return render_template('cadFuncionario.html', form=form, error=error)

    return render_template('cadFuncionario.html', form=form)


@app.route('/listaCliente')
@login_required_admin
def listaCliente():
    clientes = Cliente.query.all()
    return render_template('listaCliente.html', clientes=clientes, ordem='id')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/selet_mesa', defaults={'id': 0})
@app.route('/selet_mesa/<int:id>')
def selet_mesa(id):
    mesas = Mesa.query.filter_by(id=id).all()
    return render_template('lista_mesa.html', mesas=mesas, ordem='id')


@app.route('/ordenar_mesa/<campo>/<ordem_anterior>')
def ordenar_mesa(campo='id', ordem_anterior=''):
    if campo == 'id':
        if ordem_anterior == campo:
            mesas = Mesa.query.order_by(Mesa.id.desc()).all()
        else:
            mesas = Mesa.query.order_by(Mesa.id).all()
    elif campo == 'numero':
        if ordem_anterior == campo:
            mesas = Mesa.query.order_by(Mesa.numero.desc()).all()
        else:
            mesas = Mesa.query.order_by(Mesa.numero).all()
    else:
        mesas = Mesa.query.order_by(Mesa.id).all()
    return render_template('lista_mesa', mesas=mesas, ordem=campo)


@app.route('/consulta_mesa', methods=['POST'])
def consulta_mesa():
    consulta = '%' + request.form.get('consulta') + '%'
    campo = request.form.get('campo')

    if campo == 'numero':
        mesas = Mesa.query.filter(Mesa.numero.like(consulta)).all()
    else:
        mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, ordem='id')


@app.route('/insert_mesa')
def insert_mesa():
    return render_template('insert_Mesa.html')


@app.route('/salvar_insert_mesa', methods=['POST'])
def salvar_insert_mesa():
    Numero = int(request.form.get('numero'))

    mesa = Mesa(Numero)

    db.session.add(mesa)
    db.session.commit()

    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, erdem='id')


@app.route('/edicao_mesa/<int:id>')
def edicao_mesa(id=0):
    mesa = Mesa.query.filter_by(id=id).first()
    return render_template('edicao_mesa', mesa=mesa)


@app.route('/salvar_edicao_mesa', methods=['POST'])
def salvar_edicao_mesa():
    Id = int(request.form.get('id'))
    Numero = int(request.form.get('numero'))

    mesa = Mesa.query.filter_by(id=Id).first()

    mesa.numero = Numero

    db.session.commit()

    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, erdem='id')


@app.route('/delecao_mesa/<int:id>')
def delecao_mesa(id=0):
    mesa = Mesa.query.filter_by(id=id).first()
    return render_template('delecao_mesa.html', mesa=mesa)


@app.route('/salvar_delecao_mesa', methods=['POST'])
def salvar_delecao_mesa():
    Id = int(request.form.get('id'))

    mesa = Mesa.query.filter_by(id=Id).first()

    db.session.delete(mesa)
    db.session.commit()

    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, erdem='id')


# Altenticação-> https://pythonhelp.wordpress.com/2012/11/27/armazenando-senhas-de-forma-segura/
def validarSenha(senha_digitada, db_hash_senha):
    if bcrypt.hashpw(senha_digitada, db_hash_senha) == db_hash_senha:
        return True
    else:
        return False
