# Importações necessárias do Flask e dos arquivos do projeto
from flask import Blueprint, request, jsonify, session, redirect

# Importa o DAO para interações com o banco de dados
from MVC.model.usuario_dao import UsuarioDAO

# Importa as classes de usuário (para checar o tipo de usuário logado)
from MVC.model.usuario import Produtor, Operador, Mosaiqueiro

# Cria um Blueprint chamado 'auth' para agrupar rotas relacionadas à autenticação
auth_bp = Blueprint('auth', __name__)

# Instancia o DAO para acesso ao banco de dados (com senha do banco definida)
dao = UsuarioDAO(password='senha123')


# Rota de login - aceita GET (redireciona) e POST (realiza autenticação)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Quando acessado por GET, redireciona o usuário para a tela de login do front-end
        return redirect('http://localhost:5173/login')

    # Quando acessado por POST, tenta autenticar o usuário
    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')

    # Usa o DAO para autenticar com base no CPF e senha
    usuario = dao.autenticar(cpf, senha)
    if usuario:
        # Se autenticado com sucesso, salva o CPF do usuário na sessão
        session['cpf'] = usuario.cpf

        # Identifica o tipo de usuário com base na classe da instância
        if isinstance(usuario, Produtor):
            tipo = 'produtor'
        elif isinstance(usuario, Operador):
            tipo = 'operador'
        elif isinstance(usuario, Mosaiqueiro):
            tipo = 'mosaiqueiro'
        else:
            tipo = 'desconhecido'

        # Retorna sucesso com o tipo de usuário
        return jsonify({'status': 'success', 'tipo': tipo})

    # Se não autenticado, retorna erro com status 401 (não autorizado)
    return jsonify({'status': 'error', 'message': 'CPF ou senha inválidos'}), 401


# Rota de cadastro - aceita GET (redireciona) e POST (cadastra)
@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        # Quando acessado por GET, redireciona o usuário para a tela de cadastro do front-end
        return redirect('http://localhost:5173/register')

    # Quando acessado por POST, realiza o cadastro
    data = request.get_json()

    # Extrai os dados do corpo da requisição
    cpf = data.get('cpf')
    nome = data.get('nome')
    senha = data.get('senha')
    tipo = data.get('tipo')

    # Verifica se todos os campos obrigatórios foram preenchidos
    if not cpf or not nome or not senha or not tipo:
        return jsonify({'status': 'error', 'message': 'Preencha todos os campos obrigatórios.'}), 400

    try:
        # Chama o método do DAO para cadastrar o novo usuário
        dao.cadastro(cpf=cpf, senha=senha, tipo=tipo, nome=nome)
        return jsonify({'status': 'success', 'message': 'Usuário cadastrado com sucesso!'})
    except Exception as e:
        # Em caso de erro inesperado, retorna mensagem de erro genérica
        return jsonify({'status': 'error', 'message': f'Erro ao cadastrar usuário: {str(e)}'}), 500


# Rota de logout - limpa a sessão do usuário
@auth_bp.route('/logout', methods=['GET'])
def logout():
    # Remove o CPF do usuário da sessão (deslogando)
    session.pop('cpf', None)
    # Redireciona o usuário para a página de login
    return redirect('http://localhost:5173/login')
