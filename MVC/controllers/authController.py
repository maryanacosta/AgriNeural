from flask import Blueprint, request, jsonify, session, redirect

from MVC.model.usuario_dao import UsuarioDAO
from MVC.model.usuario import Produtor, Operador, Mosaiqueiro

auth_bp = Blueprint('auth', __name__)
dao = UsuarioDAO(password='senha123')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Redireciona para a página React de login
        return redirect('http://localhost:5173/login')

    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')

    usuario = dao.autenticar(cpf, senha)
    if usuario:
        session['cpf'] = usuario.cpf
        if isinstance(usuario, Produtor):
            tipo = 'produtor'
        elif isinstance(usuario, Operador):
            tipo = 'operador'
        elif isinstance(usuario, Mosaiqueiro):
            tipo = 'mosaiqueiro'
        else:
            tipo = 'desconhecido'

        return jsonify({'status': 'success', 'tipo': tipo})

    return jsonify({'status': 'error', 'message': 'CPF ou senha inválidos'}), 401


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        # Redireciona para a página React de cadastro
        return redirect('http://localhost:5173/register')

    data = request.get_json()

    cpf = data.get('cpf')
    nome = data.get('nome')
    senha = data.get('senha')
    tipo = data.get('tipo')

    if not cpf or not nome or not senha or not tipo:
        return jsonify({'status': 'error', 'message': 'Preencha todos os campos obrigatórios.'}), 400

    try:
        dao.cadastro(cpf=cpf, senha=senha, tipo=tipo, nome=nome)
        return jsonify({'status': 'success', 'message': 'Usuário cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erro ao cadastrar usuário: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('cpf', None)
    return redirect('http://localhost:5173/login')
