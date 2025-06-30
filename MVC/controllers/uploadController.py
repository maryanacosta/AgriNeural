# Importações necessárias
from flask import Blueprint, request, session, redirect, url_for, current_app
from MVC.model.usuario_dao import UsuarioDAO                # DAO para buscar dados do usuário
from MVC.model.usuario import Operador                      # Classe Operador para verificação
from MVC.services.IAService import ModeloAgrineural         # Modelo de IA que analisará a imagem
import os                                                   # Para manipulação de arquivos
import mysql.connector                                      # Para conexão com o MySQL
import cv2                                                  # OpenCV (não usado diretamente aqui, mas possivelmente dentro de ModeloAgrineural)
import numpy as np                                          # Também não usado aqui diretamente

# Define o Blueprint de upload
upload_bp = Blueprint('upload', __name__)

# DAO para acesso ao banco
dao = UsuarioDAO(password='senha123')

# Define pastas padrão para upload e status
UPLOAD_FOLDER = 'uploads'
STATUS_FOLDER = 'status'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATUS_FOLDER, exist_ok=True)

# Rota que trata o upload de imagens
@upload_bp.route('/upload', methods=['POST'])
def upload():
    # Garante que o usuário está logado
    if 'cpf' not in session:
        return "Você precisa estar logado como operador.", 403

    # Busca o operador no banco de dados
    cpf = session['cpf']
    operador = dao.buscar_por_cpf(cpf)
    if not operador or not isinstance(operador, Operador):
        return "Apenas operadores podem enviar imagens.", 403

    # Obtém o CPF do produtor associado ao operador
    cpf_produtor = operador.cpf_produtor

    # Recupera arquivos e coordenadas do formulário
    arquivos = request.files.getlist('imagens')       # Lista de arquivos enviados
    latitudes = request.form                          # As latitudes vêm nos campos tipo latitude_0, latitude_1, etc.
    longitudes = request.form                         # Mesma ideia para longitudes

    # Verifica se há imagens
    if not arquivos:
        return "Nenhuma imagem enviada.", 400

    # Conecta ao banco de dados
    conn = mysql.connector.connect(
        host="localhost",
        user="agrineural",
        password="senha123",
        database="agrineural"
    )
    cursor = conn.cursor()

    # Cria pastas específicas para o produtor
    upload_path = os.path.join(UPLOAD_FOLDER, cpf_produtor)
    status_path_base = os.path.join(STATUS_FOLDER, cpf_produtor)
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(status_path_base, exist_ok=True)

    # Itera sobre os arquivos enviados
    for idx, file in enumerate(arquivos):
        if not file or not file.filename:
            continue  # Pula arquivos inválidos

        nome = file.filename  # Nome do arquivo

        # Extrai latitude e longitude do formulário
        try:
            latitude = float(request.form.get(f'latitude_{idx}', '0'))
            longitude = float(request.form.get(f'longitude_{idx}', '0'))
        except ValueError:
            return f"Latitude ou longitude inválida para {nome}", 400

        # Salva a imagem no servidor
        caminho_arquivo = os.path.join(upload_path, nome)
        file.save(caminho_arquivo)

        # Cria arquivo de status inicial
        caminho_status = os.path.join(status_path_base, nome + ".txt")
        with open(caminho_status, 'w', encoding='utf-8') as f:
            f.write("Processando")

        try:
            # Instancia e usa o modelo de IA
            modelo = ModeloAgrineural()
            resultado = modelo.analisarImagem(caminhoArquivo=caminho_arquivo)

            # Insere a imagem no banco
            cursor.execute(
                "INSERT INTO imagens (nome, latitude, longitude, cpf_produtor) VALUES (%s, %s, %s, %s)",
                (nome, latitude, longitude, cpf_produtor)
            )
            imagem_id = cursor.lastrowid  # Recupera o ID da imagem inserida

            # Insere o resultado (anômala ou não)
            cursor.execute(
                "INSERT INTO resultados (id, anomala) VALUES (%s, %s)",
                (imagem_id, resultado == "Anômala")
            )

            # Atualiza o status para sucesso
            with open(caminho_status, 'w') as f:
                f.write(f"Concluído com sucesso! — Resultado: {resultado}")

        except Exception as e:
            # Em caso de erro, grava no arquivo de status e loga no console
            with open(caminho_status, 'w') as f:
                f.write(f"Erro no processamento! — {e}")
            print(f"[ERRO] Falha ao processar {nome}: {e}")

    # Finaliza transação no banco
    conn.commit()
    cursor.close()
    conn.close()

    # Redireciona para a página de status
    return redirect(url_for('status.status'))
