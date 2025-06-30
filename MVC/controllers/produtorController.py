# Importa componentes do Flask: Blueprint para modularização, session para controle de login,
# e jsonify para retornar respostas JSON
from flask import Blueprint, session, jsonify

# Cria um Blueprint chamado 'produtor' para agrupar as rotas da área do produtor
produtor_bp = Blueprint('produtor', __name__)

# Define uma rota de API para a área do produtor, que aceita apenas requisições GET
@produtor_bp.route('/area-produtor', methods=['GET'])
def area_produtor():
    # Verifica se há um usuário logado verificando a presença do 'cpf' na sessão
    if 'cpf' not in session:
        # Se não estiver logado, retorna erro 401 (não autorizado) em formato JSON
        return jsonify({'status': 'error', 'message': 'Usuário não autenticado.'}), 401
    
    # Se estiver logado, retorna uma resposta JSON de sucesso
    # Aqui você pode incluir outros dados do produtor futuramente (ex: nome, fazendas, etc.)
    return jsonify({'status': 'success', 'message': 'Acesso autorizado à área do produtor.'})
