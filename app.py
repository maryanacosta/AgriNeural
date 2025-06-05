from flask import Flask, request, render_template, redirect, url_for, session
from model.usuario_dao import UsuarioDAO
from model.usuario import Produtor, Operador, Mosaiqueiro
import os
import time

app = Flask(__name__)
dao = UsuarioDAO(password='senha123')  # ajuste se necessário
app.secret_key = 'chave_secreta_qualquer'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
            session['cpf'] = usuario.cpf  # <- aqui está o ponto certo

            if isinstance(usuario, Produtor):
                return redirect(url_for('area_produtor'))
            elif isinstance(usuario, Operador):
                return redirect(url_for('area_operador'))
            elif isinstance(usuario, Mosaiqueiro):
                return redirect(url_for('area_mosaiqueiro'))
        else:
            return "<h2>Erro: CPF ou senha inválidos.</h2><a href='/login'>Tentar novamente</a>"
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        senha = request.form['senha']
        tipo = request.form['tipo']
        print(f"Cadastro recebido: cpf={cpf}, senha={senha}, tipo={tipo}, nome={nome}")
        dao.cadastro(cpf, senha, tipo, nome)
        return redirect(url_for('login'))
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

@app.route('/area_mosaiqueiro')
def area_mosaiqueiro():
    if 'cpf' not in session:
        return redirect(url_for('login'))
    return render_template('area_mosaiqueiro.html')

UPLOAD_FOLDER = 'uploads'
STATUS_FOLDER = 'status'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATUS_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'cpf' not in session:
        return "Você precisa estar logado como operador.", 403

    cpf = session['cpf']
    arquivos = request.files.getlist('imagens')
    nomes_imagens = []

    upload_path = os.path.join(UPLOAD_FOLDER, cpf)
    status_path_base = os.path.join(STATUS_FOLDER, cpf)

    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(status_path_base, exist_ok=True)

    for file in arquivos:
        if file and file.filename:
            nome = file.filename
            nomes_imagens.append(nome)

            caminho_arquivo = os.path.join(upload_path, nome)
            file.save(caminho_arquivo)

            caminho_status = os.path.join(status_path_base, nome + ".txt")
            with open(caminho_status, 'w') as f:
                f.write("Aguardando processamento")

            # Simula processamento
            time.sleep(0.5)
            with open(caminho_status, 'w') as f:
                f.write("Processando")

            time.sleep(1)
            with open(caminho_status, 'w') as f:
                f.write("Concluído com sucesso ✅")

    return redirect(url_for('status'))

@app.route('/status')
def status():
    if 'cpf' not in session:
        return "Você precisa estar logado como operador.", 403

    cpf = session['cpf']
    status_list = []

    pasta_status = os.path.join(STATUS_FOLDER, cpf)
    if not os.path.exists(pasta_status):
        return render_template('status.html', status_list=[])

    for filename in os.listdir(pasta_status):
        if filename.endswith(".txt"):
            imagem = filename[:-4]
            with open(os.path.join(pasta_status, filename), 'r') as f:
                status = f.read()
            status_list.append((imagem, status))

    return render_template('status.html', status_list=status_list)

@app.route('/logout')
def logout():
    session.pop('cpf', None)  # remove o CPF da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
