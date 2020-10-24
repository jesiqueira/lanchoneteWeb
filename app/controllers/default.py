
from logging import error
from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from app.models.tables import Funcionario, Mesa, Cliente, Login, TelefoneCliente, Endereco, TelefoneFuncionario, Frios
from app.models.Forms import CadastroFuncionario, EditarFrios, LoginForm, CadastroCliente, CadastrarFrios,Form_listar_frios
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
        login = Login.query.filter_by(id=current_user.get_id()).first()
        if login != None:
            if login.is_admin:
                return f(*args, **kwargs)
            else:
                flash('Não Autorizado, seu login não tem permissão.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Não Autorizado, faça o login.', 'danger')
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


@app.route('/listarCliente')
@login_required_admin
def listarCliente():
    # r = db.session.query(Cliente.id, Cliente.nome, Cliente.email, Login.login, Login.is_admin).outerjoin(Login, Cliente.id == Login.id).all()
    result = db.session.query(Cliente.id, Cliente.nome, Cliente.email,
                              Login.login, Login.is_admin).join(Login, Cliente.id == Login.id).all()
    # for resul in r:
    #     print(f'Nome: {resul.nome}, Adminstrador: {resul.is_admin}')

    return render_template('listarCliente.html', clientes=result, ordem=id)


@app.route('/selecionarCliente/<int:id>')
@login_required_admin
def selecionarCliente(id=0):
    result = db.session.query(Cliente.id, Cliente.nome, Cliente.email, Login.login, Login.is_admin).join(
        Cliente).join(Login).filter(Login.id == id).all()

    return render_template('listarCliente.html', clientes=result, ordem='id')


# @app.route('/ordenarCliente/<campo>/<ordem_anterior>')
# def ordenarCliente(campo='id', ordem_anterior=''):
#     # if ordem_anterior == campo
#     # cadastro de clientes


@app.route('/cadastro')
def cadastro():
    form = CadastroCliente()
    return render_template('cadastro.html', form=form)


@ app.route('/salvar_cliente', methods=['POST'])
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


@ app.route('/cadFuncionario', methods=['POST', 'GET'])
@ login_required_admin
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


# @app.route('/listaCliente')
# @login_required_admin
# def listaCliente():
#     clientes = Cliente.query.all()
#     return render_template('listaCliente.html', clientes=clientes, ordem='id')


@app.route('/listafrios')
@login_required_admin
def listafrios():
    form = Form_listar_frios()
    frios = Frios.query.all()
    return render_template('listafrios.html',form=form ,frios=frios, ordem='id')


@app.route('/selecionarfrios/<int:id>')
@login_required_admin
def selecionarfrios(id=0):
    frios = Frios.query.filter_by(id=id).all()
    return render_template('listafrios.html', frios=frios, ordem='id')


@app.route('/ordenarfrios/<campo>/<ordem_anterior>')
def ordenarfrios(campo='id', ordem_anterior=''):
    if campo == 'id':
        if ordem_anterior == campo:
            frios = Frios.query.order_by(Frios.id.desc()).all()
        else:
            frios = Frios.query.order_by(Frios.id).all()
    elif campo == 'nome':
        if ordem_anterior == campo:
            frios = Frios.query.order_by(Frios.nome.desc()).all()
        else:
            frios = Frios.query.order_by(Frios.nome).all()
    elif campo == 'quantidade':
        if ordem_anterior == campo:
            frios = Frios.query.order_by(Frios.quantidade.desc()).all()
        else:
            frios = Frios.query.order_by(Frios.quantidade).all()
    elif campo == 'preco':
        if ordem_anterior == campo:
            frios = Frios.query.order_by(Frios.preco.desc()).all()
        else:
            frios = Frios.query.order_by(Frios.preco).all()
    else:
        frios = Frios.query.order_by(Frios.id).all()

    return render_template('listafrios.html', frios=frios, ordem=campo)


@app.route('/consultafrios', methods=['POST'])
def consultafrios():
    consulta = '%'+request.form.get('consulta')+'%'
    campo = request.form.get('campo')

    if campo == 'nome':
        frios = Frios.query.filter(Frios.nome.like(consulta)).all()
    elif campo == 'quantidade':
        frios = Frios.query.filter(Frios.quantidade.like(consulta)).all()
    elif campo == 'preco':
        frios = Frios.query.filter(Frios.preco.like(consulta)).all()
    else:
        frios = Frios.query.all()

    return render_template('listafrios.html', frios=frios, ordem='id')


@app.route('/insertfrios')
@login_required_admin
def insertfrios():
    return render_template('insertfrios.html')


@app.route('/salvar_insertfrios', methods=['POST', 'GET'])
@login_required_admin
def salvar_insertfrios():
    form = CadastrarFrios()

    if form.validate():
        Nome = form.nome.data
        Quantidade = int(form.quantidade.data)
        Preco = float(form.preco.data)

        frios = Frios(Nome, Quantidade, Preco)

        db.session.add(frios)
        db.session.commit()

        frious = Frios.query.all()

        return render_template('listafrios.html', frios=frious, ordem='id')


@app.route('/editarfrios/<int:id>')
@login_required_admin
def editarfrios(id=0):
    frios = Frios.query.filter_by(id=id).first()
    return render_template('editarfrios.html', frios=frios)


@app.route('/salvar_editarfrios', methods=['POST'])
@login_required_admin
def salvar_editarfrios():
    form = EditarFrios()

    if form.validate():
        Id = form.id.data
        Nome = form.nome.data
        Quantidade = int(form.quantidade.data)
        Preco = float(form.preco.data)

        frios = Frios.query.filter_by(id=Id).first()
        frios.nome = Nome
        frios.quantidade = Quantidade
        frios.preco = Preco

        db.session.commit()

        frios = Frios.query.all()

        return render_template('listafrios.html', frios=frios, ordem='id')


@app.route('/deletar_frios/<int:id>')
@login_required_admin
def deletar_frios(id=0):
    frios = Frios.query.filter_by(id=id).first()
    return render_template('deletar_frios.html', frios=frios)


@app.route('/salvar_delecao_frios', methods=['POST'])
@login_required_admin
def salvar_delecao_frios():
    Id = int(request.form.get('id'))

    frios = Frios.query.filter_by(id=Id).first()

    db.session.delete(frios)
    db.session.commit()

    frios = Frios.query.all()

    return render_template('listafrios.html', frios=frios, ordem='id')


@ app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@ app.route('/selet_mesa', defaults={'id': 0})
@ app.route('/selet_mesa/<int:id>')
def selet_mesa(id):
    mesas = Mesa.query.filter_by(id=id).all()
    return render_template('lista_mesa.html', mesas=mesas, ordem='id')


@ app.route('/ordenar_mesa/<campo>/<ordem_anterior>')
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


@ app.route('/consulta_mesa', methods=['POST'])
def consulta_mesa():
    consulta = '%' + request.form.get('consulta') + '%'
    campo = request.form.get('campo')

    if campo == 'numero':
        mesas = Mesa.query.filter(Mesa.numero.like(consulta)).all()
    else:
        mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, ordem='id')


@ app.route('/insert_mesa')
def insert_mesa():
    return render_template('insert_Mesa.html')


@ app.route('/salvar_insert_mesa', methods=['POST'])
def salvar_insert_mesa():
    Numero = int(request.form.get('numero'))

    mesa = Mesa(Numero)

    db.session.add(mesa)
    db.session.commit()

    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, erdem='id')


@ app.route('/edicao_mesa/<int:id>')
def edicao_mesa(id=0):
    mesa = Mesa.query.filter_by(id=id).first()
    return render_template('edicao_mesa', mesa=mesa)


@ app.route('/salvar_edicao_mesa', methods=['POST'])
def salvar_edicao_mesa():
    Id = int(request.form.get('id'))
    Numero = int(request.form.get('numero'))

    mesa = Mesa.query.filter_by(id=Id).first()

    mesa.numero = Numero

    db.session.commit()

    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, erdem='id')


@ app.route('/delecao_mesa/<int:id>')
def delecao_mesa(id=0):
    mesa = Mesa.query.filter_by(id=id).first()
    return render_template('delecao_mesa.html', mesa=mesa)


@ app.route('/salvar_delecao_mesa', methods=['POST'])
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
