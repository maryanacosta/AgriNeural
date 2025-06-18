from flask import Blueprint, request, session, redirect, url_for, current_app
from MVC.model.usuario_dao import UsuarioDAO
from MVC.model.usuario import Operador
from MVC.services.IAService import ModeloAgrineural
import os
import mysql.connector
import cv2
import numpy as np

upload_bp = Blueprint('upload', __name__)
dao = UsuarioDAO(password='senha123')

UPLOAD_FOLDER = 'uploads'
STATUS_FOLDER = 'status'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATUS_FOLDER, exist_ok=True)

# página de upload

@upload_bp.route('/upload', methods=['POST'])
def upload():
    if 'cpf' not in session:
        return "Você precisa estar logado como operador.", 403

    cpf = session['cpf']
    operador = dao.buscar_por_cpf(cpf)
    if not operador or not isinstance(operador, Operador):
       return "Apenas operadores podem enviar imagens.", 403

    cpf_produtor = operador.cpf_produtor
    arquivos  = request.files.getlist('imagens')
    # não mais por filename, mas por índice
    latitudes  = request.form
    longitudes = request.form

    if not arquivos:
        return "Nenhuma imagem enviada.", 400

    conn = mysql.connector.connect(
        host="localhost",
        user="agrineural",
        password="senha123",
        database="agrineural"
    )
    cursor = conn.cursor()

    upload_path      = os.path.join(UPLOAD_FOLDER, cpf_produtor)
    status_path_base = os.path.join(STATUS_FOLDER, cpf_produtor)
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(status_path_base, exist_ok=True)

    for idx, file in enumerate(arquivos):
        if not file or not file.filename:
            continue

        nome = file.filename

        # pega latitude_0, longitude_0, latitude_1, etc.
        try:
            latitude  = float(request.form.get(f'latitude_{idx}', '0'))
            longitude = float(request.form.get(f'longitude_{idx}', '0'))
        except ValueError:
            return f"Latitude ou longitude inválida para {nome}", 400

        # salva a imagem
        caminho_arquivo = os.path.join(upload_path, nome)
        file.save(caminho_arquivo)

        # status inicial
        caminho_status = os.path.join(status_path_base, nome + ".txt")
        with open(caminho_status, 'w', encoding='utf-8') as f:
            f.write("Processando")

        try:
           
           modelo = ModeloAgrineural()
           resultado = modelo.analisarImagem(caminhoArquivo=caminho_arquivo)

           # grava no banco
           cursor.execute(
               "INSERT INTO imagens (nome, latitude, longitude, cpf_produtor) VALUES (%s, %s, %s, %s)",
               (nome, latitude, longitude, cpf_produtor)
           )
           imagem_id = cursor.lastrowid
           cursor.execute(
               "INSERT INTO resultados (id, anomala) VALUES (%s, %s)",
               (imagem_id, resultado == "Anômala")
           )

           # marca sucesso
           with open(caminho_status, 'w') as f:
               f.write(f"Concluído com sucesso! — Resultado: {resultado}")
        except Exception as e:
           with open(caminho_status, 'w') as f:
               f.write(f"Erro no processamento! — {e}")
           print(f"[ERRO] Falha ao processar {nome}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('status.status'))
