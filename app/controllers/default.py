from flask import render_template, request
from app import app, db
from app.models.tables import Mesa


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/lista_mesa')
def lista_mesa():
    mesas = Mesa.query.all()
    return render_template('lista_mesa.html', mesas=mesas, ordem='id')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


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
