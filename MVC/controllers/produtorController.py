from flask import Blueprint, render_template, session, redirect, url_for

produtor_bp = Blueprint('produtor', __name__)

# página do produtor

@produtor_bp.route('/area_produtor')
def area_produtor():
    if 'cpf' not in session:
        return redirect(url_for('auth.login'))
    return render_template('area_produtor.html')