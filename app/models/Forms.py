from sys import maxsize
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.fields import html5, SelectField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import html5 as h5widgets


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[
                        InputRequired('Login é Obrigatório')])
    password = PasswordField("inputPassword", validators=[
                             InputRequired('Senha é Obrigatório')])
    lembreme = BooleanField("inputRemember")


class CadastroCliente(FlaskForm):
    nome = StringField('Seu Nome', [InputRequired('Nome é Obrigatório')])
    cidade = StringField('Sua Cidade', validators=[
                         InputRequired('Cidade é Obrigatório')])
    cep = StringField('Seu Cep', validators=[InputRequired('Cep é Obritório')])
    numero = html5.IntegerField('Número', widget=h5widgets.NumberInput(
        min=0), validators=[InputRequired('Número é Obrigatório')])
    bairro = StringField('Seu Bairro', validators=[
                         InputRequired('Bairro é Obrigatório')])
    rua = StringField('Sua rua', validators=[
                      InputRequired('Rua é Obrigatório')])
    email = html5.EmailField(
        'Seu e-mail', validators=[InputRequired('E-mail é Obrigatório')])
    telefone = StringField('Seu telefone', validators=[
                           InputRequired('Telefone é Obrigatório')])
    login = StringField('Seu Login', validators=[
                        InputRequired('Login é Obrigatório')])
    password = PasswordField('Sua Senha', validators=[
                             InputRequired('Senha é Obrigatória')])
    confirmPassword = PasswordField('Confirme a senha', validators=[
                                    InputRequired('Confirmação é Obrigatório')])
    receberEmail = BooleanField('Receber Email')


class CadastroFuncionario(FlaskForm):
    nome = StringField('Nome', validators=[
                       InputRequired('Nome é Obrigatório')])
    cidade = StringField('Cidade', validators=[
                         InputRequired('Cidade é Obrigatório')])
    cep = StringField('Cep', validators=[InputRequired('Cep é Obritório')])
    numero = html5.IntegerField('Número', widget=h5widgets.NumberInput(
        min=0), validators=[InputRequired('Número é Obrigatório')])
    bairro = StringField('Bairro', validators=[
                         InputRequired('Bairro é Obrigatório')])
    rua = StringField('Rua', validators=[InputRequired('Rua é Obrigatório')])
    email = html5.EmailField(
        'E-mail', validators=[InputRequired('E-mail é Obrigatório')])
    telefone = StringField('Telefone', validators=[
                           InputRequired('Telefone é Obrigatório')])
    inicio_contrato = html5.DateField('Data Inicio', validators=[
                                      InputRequired('data requerida')])
    login = StringField('Login', validators=[
                        InputRequired('Login é Obrigatório')])
    is_admin = BooleanField('Adminstrador')
    is_ativo = BooleanField('Ativo')
    password = PasswordField('Senha', validators=[
                             InputRequired('Senha é Obrigatória')])
    confirmPassword = PasswordField('Confirme a senha', validators=[
                                    InputRequired('Confirmação é Obrigatório')])


class Form_listar_frios(FlaskForm):
    consulta = StringField('Consultar')
    campo = SelectField('Campos', choices=[('nome', 'Nome'), ('quantidade', 'Quantidade'), ('preco', 'Preço')])


class CadastrarFrios(FlaskForm):
    nome = StringField('Nome', [InputRequired('Este campo é Obrigatório')])
    quantidade = html5.IntegerField('Quantidade', widget=h5widgets.NumberInput(
        min=1), validators=[InputRequired()])
    preco = html5.DecimalField('Preço', validators=[InputRequired()])


class EditarFrios(FlaskForm):
    id = html5.IntegerField('Id', widget=h5widgets.NumberInput(
        min=0), validators=[InputRequired()])
    nome = StringField('Nome', [InputRequired('Este campo é Obrigatório')])
    quantidade = html5.IntegerField('Quantidade', widget=h5widgets.NumberInput(
        min=1), validators=[InputRequired()])
    preco = html5.DecimalField('Preço', validators=[InputRequired()])
