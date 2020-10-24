from flask import flash, redirect, render_template, Blueprint, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager
from app.models.tables import Login
from app.models.Forms import LoginForm
import bcrypt
from functools import wraps

login_blueprint = Blueprint(
    'login', __name__, static_folder='static', template_folder='models')


# @login_manager.user_loader
# def login_user(id):
#     lg =Login.query.filter_by(id=id).first()
#     return lg
#     # return Login.query.filter_by(id=id).first()


@login_blueprint.route('/',methods=['GET'])
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
                return redirect(url_for('.login'))
        else:
            flash('Não Autorizado, faça o login.', 'danger')
            return redirect(url_for('.login'))
    return wrap


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        lg = Login.query.filter_by(login=form.login.data).first()
        print(f"seu login: {lg.login} - password: {lg.password}")        
        

        if lg and validarSenha(form.password.data, lg.password):
            login_user(lg)
            return redirect(url_for('.index'))
        else:
            error = 'Login ou Senha incorreta'

    return render_template('login.html', form=form, error=error)

# Altenticação-> https://pythonhelp.wordpress.com/2012/11/27/armazenando-senhas-de-forma-segura/


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


def validarSenha(senha_digitada, db_hash_senha):
    if bcrypt.hashpw(senha_digitada, db_hash_senha) == db_hash_senha:
        return True
    else:
        return False
