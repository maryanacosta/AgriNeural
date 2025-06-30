# Importa componentes do Flask necessários para rotas, sessão, redirecionamento e renderização de templates
from flask import Blueprint, render_template, session, redirect, url_for

# Cria um Blueprint chamado 'operador' para agrupar as rotas da área do operador
operador_bp = Blueprint('operador', __name__)

# Define a rota da área do operador (painel principal)
@operador_bp.route('/area-operador')
def area_operador():
    # Verifica se há um usuário autenticado (com 'cpf' na sessão)
    if 'cpf' not in session:
        # Se não estiver logado, redireciona para a rota de login definida no Blueprint 'auth'
        return redirect(url_for('auth.login'))
    
    # Se estiver logado, renderiza o template da página do operador
    return render_template('area_operador.html')
