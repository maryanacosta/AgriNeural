from flask import Blueprint, render_template, session, current_app
from utils.usuario_dao import UsuarioDAO
from utils.usuario import Operador
import os

status_bp = Blueprint('status', __name__)
dao = UsuarioDAO(password='senha123')

STATUS_FOLDER = 'status'
os.makedirs(STATUS_FOLDER, exist_ok=True)

# paǵina de status

@status_bp.route('/status')
def status():
    if 'cpf' not in session:
        return "Você precisa estar logado como operador.", 403

    cpf = session['cpf']
    operador = dao.buscar_por_cpf(cpf)
    if not operador or not isinstance(operador, Operador):
        return "Apenas operadores podem ver o status.", 403

    cpf_produtor = operador.cpf_produtor
    status_list = []

    pasta_status = os.path.join(STATUS_FOLDER, cpf_produtor)
    if os.path.exists(pasta_status):
        for filename in os.listdir(pasta_status):
            if filename.endswith(".txt"):
                imagem = filename[:-4]
                with open(os.path.join(pasta_status, filename), 'r') as f:
                    status = f.read()
                status_list.append((imagem, status))

    return render_template('status.html', status_list=status_list)
