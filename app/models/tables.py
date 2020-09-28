from app import db


class Login(db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=0)
    is_ativo = db.Column(db.Boolean, default=0)

    def __init__(self, login, password, is_admin, is_ativo):
        self.login = login
        self.password = password
        self.is_admin = is_admin
        self.is_ativo = is_ativo

    def __repr__(self):
        return '<Login %r>' % self.login


friosLanche = db.Table(
    'friosLanche',
    db.Column('frios_id', db.Integer, db.ForeignKey('frios.id'), primary_key=True),
    db.Column('lanche_id', db.Integer, db.ForeignKey('lanche.id'), primary_key=True)
)


class Frios(db.Model):
    __tablename__ = 'frios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    friosLanche = db.relationship('Lanche', secondary=friosLanche, lazy='dynamic',
                                  backref=db.backref('friosLanche', lazy=True))

    def __init__(self, nome='default', quantidade=1, preco=1.2):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __repr__(self):
        return '<Frios %r>' % self.nome


saladaLanche = db.Table(
    'saladaLanche',
    db.Column('salada_id', db.Integer, db.ForeignKey('salada.id'), primary_key=True),
    db.Column('lanche_id', db.Integer, db.ForeignKey('lanche.id'), primary_key=True)
)


class Salada(db.Model):
    __tablename__ = 'salada'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    saladaLanche = db.relationship('Lanche', secondary=saladaLanche, lazy='dynamic',
                                   backref=db.backref('saladaLanche', lazy=True))

    def __init__(self, nome='default', quantidade=1, preco=1.1):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __repr__(self):
        return '<Salada %r>' % self.nome


class Carne(db.Model):
    __tablename__ = 'carne'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)

    def __init__(self, nome='default', quantidade=1, preco=1.1, peso=1.1):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.peso = peso

    def __repr__(self):
        return '<Carne %r>' % self.nome


class Pao(db.Model):
    __tablename__ = 'pao'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def __init__(self, nome='default', quantidade=1, preco=1.1):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __repr__(self):
        return '<Pao %r>' % self.nome


class Mesa(db.Model):
    __tablename__ = 'mesa'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, numero=1):
        self.numero = numero

    def __repr__(self):
        return '<Numero %r>' % self.numero


class Promocao(db.Model):
    __tablename__ = 'promocao'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)

    def __init__(self, valor=0.0):
        self.valor = valor

    def __repr__(self):
        return '<Valor %r>' % self.valor


pedidoLanche = db.Table(
    'pedidoLanche',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('lanche_id', db.Integer, db.ForeignKey('lanche.id'), primary_key=True)
)


class Lanche(db.Model):
    __tablename__ = 'lanche'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(100))
    pao_id = db.Column(db.Integer, db.ForeignKey('pao.id'))
    carne_id = db.Column(db.Integer, db.ForeignKey('carne.id'))
    promocao_id = db.Column(db.Integer, db.ForeignKey('promocao.id'))

    pao = db.relationship('Pao', foreign_keys=pao_id)
    carne = db.relationship('Carne', foreign_keys=carne_id)
    promocao = db.relationship('Promocao', foreign_keys=promocao_id)

    pedidoLanche = db.relationship('Pedido', secondary=pedidoLanche, lazy='dynamic',
                                   backref=db.backref('pedidoLanche', lazy=True))

    def __init__(self, nome, preco, img, pao_id, carne_id, promocao_id):
        self.nome = nome
        self.preco = preco
        self.img = img
        self.pao_id = pao_id
        self.carne_id = carne_id
        self.promocao_id = promocao_id

    def __repr__(self):
        return '<Lanche %r>' % self.nome


funcPedido = db.Table(
    'funcPedido',
    db.Column('funcionario_id', db.Integer, db.ForeignKey('funcionario.id'), primary_key=True),
    db.Column('pedidoNumero', db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
)


class Funcionario(db.Model):
    __tablename__ = 'funcionario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    inicio_contrato = db.Column(db.Date, nullable=False)
    termino_contrato = db.Column(db.Date, nullable=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.id'))

    login = db.relationship('Login', foreign_keys=login_id)

    funcPedido = db.relationship('Pedido', secondary=funcPedido, lazy='dynamic',
                                 backref=db.backref('funcionarioPedido', lazy=True))

    def __init__(self, nome, email, cidade, bairro, cep, numero, inicio_contrato, termino_contrato, login_id):
        self.nome = nome
        self.email = email
        self.cidade = cidade
        self.bairro = bairro
        self.cep = cep
        self.numero = numero
        self.inicio_contrato = inicio_contrato
        self.termino_contrato = termino_contrato
        self.login_id = login_id

    def __repr__(self):
        return '<Funcionario %r>' % self.nome


class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    login_id = db.Column(db.Integer, db.ForeignKey('login.id'))

    login = db.relationship('Login', foreign_keys=login_id)

    def __init__(self, nome, login_id):
        self.nome = nome
        self.login_id = login_id

    def __repr__(self):
        return '<Cliente %r>' % self.nome


class Endereco(db.Model):
    __tablename__ = 'endereco'

    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.Integer, nullable=False)
    rua = db.Column(db.String(50), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))

    cliente = db.relationship('Cliente', foreign_keys=cliente_id)

    def __init__(self, cidade, cep, rua, bairro, numero, cliente_id):
        self.cidade = cidade
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.numero = numero
        self.cliente_id = cliente_id

    def __repr__(self):
        return '<Cidade %r>' % self.cidade


pedidoPorcao = db.Table(
    'pedidoPorcao',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('porcao_id', db.Integer, db.ForeignKey('porcao.id'), primary_key=True)
)

pedidoBebida = db.Table(
    'pedidoBebida',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('bebida_id', db.Integer, db.ForeignKey('bebida.id'), primary_key=True)
)


class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    statusPedido = db.Column(db.Boolean)
    troco = db.Column(db.Float, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'))

    mesa = db.relationship('Mesa', foreign_keys=mesa_id)

    pedidoPorcao = db.relationship('Porcao', secondary=pedidoPorcao, lazy='dynamic',
                                   backref=db.backref('pedidoPorcao', lazy=True))

    pedidoBebidas = db.relationship('Bebida', secondary=pedidoBebida, lazy='dynamic',
                                    backref=db.backref('pedidoBebida', lazy=True))

    def __init__(self, numero='default', statusPedido=1, troco=1.1, preco=1.1, data='2020-09-17'):
        self.numero = numero
        self.statusPedido = statusPedido
        self.troco = troco
        self.preco = preco
        self.data = data

    def __repr__(self):
        return '<Numero %r>' % self.numero


class Entrega(db.Model):
    __tablename__ = 'entrega'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))

    cliente = db.relationship('Cliente', foreign_keys=cliente_id)
    pedido = db.relationship('Pedido', foreign_keys=pedido_id)

    def __init__(self, valor=0.0):
        self.valor = valor

    def __repr__(self):
        return '<Entrega %r>' % self.valor


class Bebida(db.Model):
    __tablename__ = 'bebida'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    fabricante = db.Column(db.String(20), unique=True, nullable=False)
    validade = db.Column(db.DateTime)
    preco = db.Column(db.Float)
    is_alcoolica = db.Column(db.Boolean, default=0)

    def __init__(self, nome, fabricante, validade, preco, is_alcoolica):
        self.nome = nome
        self.fabricante = fabricante
        self.validade = validade
        self.preco = preco
        self.is_alcoolica = is_alcoolica

    def __repr__(self):
        '<Bebida %r>' % self.nome


class Porcao(db.Model):
    __tablename__ = 'porcao'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float)
    carne_id = db.Column(db.Integer, db.ForeignKey('carne.id'))

    carne = db.relationship('Carne', foreign_keys=carne_id)

    def __init__(self, nome, preco, carne_id):
        self.nome = nome
        self.preco = preco
        self.carne_id = carne_id

    def __repr__(self):
        return '<Porcao %r>' % self.nome


class TelefoneFuncionario(db.Model):
    __tablename__ = 'telefoneFuncionario'

    numero = db.Column(db.Integer, nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), primary_key=True)

    funcionario = db.relationship('Funcionario', foreign_keys=funcionario_id)

    def __init__(self, numero, funcionario_id):
        self.numero = numero
        self.funcionario_id = funcionario_id

    def __repr__(self):
        return '<Numero %r>' % self.numero


class TelefoneCliente(db.Model):
    __tablename__ = 'telefoneCliente'

    numero = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), primary_key=True)

    cliente = db.relationship('Cliente', foreign_keys=cliente_id)

    def __init__(self, numero, cliente_id):
        self.numero = numero
        self.cliente_id = cliente_id

    def __repr__(self):
        return '<Numero %r>' % self.numero
