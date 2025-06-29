from flask import Blueprint, render_template, session, redirect, url_for

operador_bp = Blueprint('operador', __name__)

# página do operador

@operador_bp.route('/area-operador')
def area_operador():
    if 'cpf' not in session:
        return redirect(url_for('auth.login'))
    return render_template('area_operador.html')