from flask import Blueprint, request, render_template

teste_blueprint = Blueprint('teste', __name__, static_folder='static')


@teste_blueprint.route("/teste")
def teste():
    return render_template('teste.html')
