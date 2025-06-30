# Importa módulos do Flask e outros utilitários
from flask import Blueprint, render_template, session, current_app
from MVC.model.usuario_dao import UsuarioDAO               # DAO para acesso ao banco de dados
from MVC.model.usuario import Operador                     # Classe Operador para validação de tipo
import os                                                  # Módulo para manipulação de arquivos e diretórios

# Cria um Blueprint chamado 'status' para agrupar rotas relacionadas ao status das imagens
status_bp = Blueprint('status', __name__)

# Instancia o DAO com a senha correta do banco
dao = UsuarioDAO(password='senha123')

# Define a pasta onde os arquivos de status (textos) ficarão armazenados
STATUS_FOLDER = 'status'
os.makedirs(STATUS_FOLDER, exist_ok=True)  # Garante que a pasta 'status/' exista (senão, cria)


# Define a rota da página de status das imagens analisadas
@status_bp.route('/status')
def status():
    # Verifica se o usuário está logado (tem 'cpf' na sessão)
    if 'cpf' not in session:
        return "Você precisa estar logado como operador.", 403

    # Pega o CPF do usuário da sessão
    cpf = session['cpf']

    # Busca o usuário no banco usando o DAO
    operador = dao.buscar_por_cpf(cpf)

    # Verifica se o usuário logado é mesmo um operador (por segurança)
    if not operador or not isinstance(operador, Operador):
        return "Apenas operadores podem ver o status.", 403

    # Pega o CPF do produtor vinculado a esse operador
    cpf_produtor = operador.cpf_produtor

    status_list = []  # Lista para armazenar tuplas (nome_imagem, status_texto)

    # Monta o caminho da pasta com os arquivos de status do produtor
    pasta_status = os.path.join(STATUS_FOLDER, cpf_produtor)

    # Verifica se a pasta existe (ou seja, se há arquivos de status para esse produtor)
    if os.path.exists(pasta_status):
        for filename in os.listdir(pasta_status):  # Itera sobre todos os arquivos na pasta
            if filename.endswith(".txt"):          # Considera apenas arquivos .txt
                imagem = filename[:-4]             # Remove o '.txt' do nome do arquivo (fica só o nome da imagem)
                with open(os.path.join(pasta_status, filename), 'r') as f:
                    status = f.read()              # Lê o conteúdo do arquivo (status da imagem)
                status_list.append((imagem, status))  # Adiciona à lista final

    # Renderiza o template HTML passando a lista de (imagem, status)
    return render_template('status.html', status_list=status_list)
