from flask import Blueprint, request, render_template, redirect, url_for, session
from model.usuario_dao import UsuarioDAO
from model.usuario import Produtor, Operador, Mosaiqueiro
from services.LocationService import salvarLocalizacaoProdutor

auth_bp = Blueprint('auth', __name__)
dao = UsuarioDAO(password='senha123')


# página de login do usuário

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # se o usuário faz uma requisição 
        cpf = request.form['cpf'] # recebe o cpf do usuário
        senha = request.form['senha'] # recebe a senha do usuário
        usuario = dao.autenticar(cpf, senha) # verifica se o usuário existe no banco de dados
        if usuario: # se é um usuário válido
            session['cpf'] = usuario.cpf 
            if isinstance(usuario, Produtor): # caso seja produtor, é redirecionado para a página do produtor
                return redirect(url_for('produtor.area_produtor'))
            elif isinstance(usuario, Operador): # caso seja operador, é redirecionado para a página do operador
                return redirect(url_for('operador.area_operador'))
            elif isinstance(usuario, Mosaiqueiro): # caso seja mosaiqueiro, é redirecionado para a página do mosaiqueiro
                return redirect(url_for('mosaiqueiro.area_mosaiqueiro'))
        return "<h2>Erro: CPF ou senha inválidos.</h2><a href='/login'>Tentar novamente</a>"
    return render_template('login.html')


# página de cadastro de usuário

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST': # usuário faz a requisição de cadastro
        pass
        cpf = request.form.get('cpf') # recebe o cpf
        nome = request.form.get('nome') # recebe o nome
        senha = request.form.get('senha') # recebe a senha
        tipo = request.form.get('tipo') # recebe o tipo (produtor, operador ou mosaiqueiro)
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
                accept, error = salvarLocalizacaoProdutor(cpf=cpf, latitude=latitude, longitude=longitude, extTerritorial=ext_territorial)
                if not accept:
                    return render_template("cadastro.html", erro=error)

            return redirect(url_for('auth.login'))
        except Exception as e:
            erro = f"Erro ao cadastrar usuário: {str(e)}"
            return render_template("cadastro.html", erro=erro)

    # GET: apenas renderiza formulário
    return render_template('cadastro.html')



@auth_bp.route('/logout')
def logout():
    session.pop('cpf', None)
    return redirect(url_for('auth.login'))