from flask import Flask, request, render_template, redirect, url_for, session
from model.usuario_dao import UsuarioDAO
from model.usuario import Produtor, Operador, Mosaiqueiro
import os
import time
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import mysql.connector
from geopy.geocoders import Nominatim

# Carrega o modelo uma vez
modelo_ae = load_model("modelo_ia/model_checkpoint.h5transistor_AE_epoch_48.h5", compile=False)
threshold = 0.003638065652921796

app = Flask(__name__)
dao = UsuarioDAO(password='senha123')
app.secret_key = 'chave_secreta_qualquer'
UPLOAD_FOLDER = 'uploads'
STATUS_FOLDER = 'status'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATUS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']
        usuario = dao.autenticar(cpf, senha)
        if usuario:
            session['cpf'] = usuario.cpf
            if isinstance(usuario, Produtor):
                return redirect(url_for('area_produtor'))
            elif isinstance(usuario, Operador):
                return redirect(url_for('area_operador'))
            elif isinstance(usuario, Mosaiqueiro):
                return redirect(url_for('area_mosaiqueiro'))
        return "<h2>Erro: CPF ou senha inválidos.</h2><a href='/login'>Tentar novamente</a>"
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')
        cpf_produtor = request.form.get('cpf_produtor', '').strip() or None

        # Campos de localização (apenas para produtor)
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        ext_territorial = request.form.get('ext_territorial')

        # Validações básicas
        if not cpf or not nome or not senha or not tipo:
            erro = "Por favor, preencha todos os campos obrigatórios."
            return render_template("cadastro.html", erro=erro)

        if tipo in ('operador', 'mosaiqueiro') and not cpf_produtor:
            erro = "CPF do produtor é obrigatório para operadores e mosaiqueiros."
            return render_template("cadastro.html", erro=erro)

        if tipo == "produtor":
            # Validar dados de localização para produtor
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                ext_territorial = float(ext_territorial)
            except (TypeError, ValueError):
                erro = "Para produtores, latitude, longitude e extensão territorial devem ser números válidos."
                return render_template("cadastro.html", erro=erro)

        # Tenta cadastrar usuário
        try:
            # 1. Cadastra na tabela usuarios via DAO
            dao.cadastro(cpf=cpf, senha=senha, tipo=tipo, nome=nome, cpf_produtor=cpf_produtor)

            # 2. Se for produtor, insere localização na tabela localizacao
            if tipo == "produtor":
                from mysql.connector import connect, Error

                try:
                    with connect(
                        host="localhost",
                        user="agrineural",
                        password="senha123",
                        database="agrineural"
                    ) as conn:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                """
                                INSERT INTO localizacao (cpf_produtor, latitude, longitude, ext_territorial)
                                VALUES (%s, %s, %s, %s)
                                """,
                                (cpf, latitude, longitude, ext_territorial)
                            )
                            conn.commit()
                except Error as e:
                    erro = f"Erro ao salvar localização: {str(e)}"
                    return render_template("cadastro.html", erro=erro)

            return redirect(url_for('login'))
        except Exception as e:
            erro = f"Erro ao cadastrar usuário: {str(e)}"
            return render_template("cadastro.html", erro=erro)

    # GET: apenas renderiza formulário
    return render_template('cadastro.html')

@app.route('/area_produtor')
def area_produtor():
    if 'cpf' not in session:
        return redirect(url_for('login'))
    return render_template('area_produtor.html')

@app.route('/area_operador')
def area_operador():
    if 'cpf' not in session:
        return redirect(url_for('login'))
    return render_template('area_operador.html')

import mysql.connector
from flask import session, render_template

import mysql.connector
from flask import session, render_template

@app.route('/area_mosaiqueiro')
def area_mosaiqueiro():
    if 'cpf' not in session:
        return "Você precisa estar logado.", 403

    cpf_mosaiqueiro = session['cpf']

    # Conectar banco
    conn = mysql.connector.connect(
        host="localhost",
        user="agrineural",
        password="senha123",
        database="agrineural"
    )
    cursor = conn.cursor(dictionary=True)

    # Buscar CPF do produtor relacionado ao mosaiqueiro
    cursor.execute("""
        SELECT cpf_produtor FROM usuarios WHERE cpf = %s
    """, (cpf_mosaiqueiro,))
    res = cursor.fetchone()
    if not res:
        cursor.close()
        conn.close()
        return "Usuário mosaiqueiro inválido.", 403

    cpf_produtor = res['cpf_produtor']

    # Buscar localização da fazenda do produtor
    cursor.execute("""
        SELECT latitude, longitude, ext_territorial FROM localizacao WHERE cpf_produtor = %s
    """, (cpf_produtor,))
    localizacao = cursor.fetchone()
    if not localizacao:
        cursor.close()
        conn.close()
        return "Localização da fazenda não cadastrada.", 404

    # Buscar imagens e se são anômalas ou não
    cursor.execute("""
        SELECT i.nome, i.latitude, i.longitude, r.anomala
        FROM imagens i
        LEFT JOIN resultados r ON i.id = r.id
        WHERE i.cpf_produtor = %s
    """, (cpf_produtor,))
    imagens = cursor.fetchall()

    cursor.close()
    conn.close()

    # Preparar dados para o template
    centro = {
        'lat': float(localizacao['latitude']),
        'lng': float(localizacao['longitude'])
    }
    raio = float(localizacao['ext_territorial'])  # assumindo em km

    # Formatando imagens para o JS no template
    lista_imagens = []
    for img in imagens:
        lista_imagens.append({
            'nome': img['nome'],
            'lat': float(img['latitude']),
            'lng': float(img['longitude']),
            'anomala': bool(img['anomala'])
        })

    return render_template('area_mosaiqueiro.html',
                           centro=centro,
                           raio=raio,
                           imagens=lista_imagens)

@app.route('/upload', methods=['POST'])
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
            img = cv2.imread(caminho_arquivo)
            img = cv2.resize(img, (256, 256))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_norm = img.astype("float32") / 255.0
            entrada = np.expand_dims(img_norm, axis=0)

            reconstruida = modelo_ae.predict(entrada)[0]
            erro = np.mean((img_norm - reconstruida) ** 2)
            resultado = "Anômala" if erro > threshold else "Normal"

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
    return redirect(url_for('status'))

@app.route('/status')
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

@app.route('/logout')
def logout():
    session.pop('cpf', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
