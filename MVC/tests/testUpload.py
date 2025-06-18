import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO 
from MVC.app import app
from MVC.model.usuario import Operador, Produtor 


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key_for_upload' 
    with app.test_client() as client:
        yield client


def test_upload_sem_login(client): # teste
    response = client.post('/upload') # ação: tentar entrar na página de upload
    assert response.status_code == 403  # verificação: verificar se o usuário consegue realizar o upload sem o login


@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
@patch('MVC.services.IAService.analisarImagem')
@patch('os.makedirs') # Moca a criação de diretórios
@patch('builtins.open', new_callable=MagicMock) # Moca a função 'open' para simular escrita de arquivos
@patch('mysql.connector.connect') # Moca a conexão com o banco de dados
def test_upload_valido_operador(mock_mysql_connect, mock_open, mock_makedirs, mock_analisar_imagem, mock_buscar_por_cpf, client):
    
    with client.session_transaction() as sess:
        sess['cpf'] = '12345678900' #simula o cpf de um operador válido

    # 2. Configurar o mock para UsuarioDAO.buscar_por_cpf
    mock_operador = Operador(cpf='12345678900', nome='Teste', senha='senha123', cpf_produtor='98765432100')
    mock_buscar_por_cpf.return_value = mock_operador

    # 3. Configurar o mock para IAService.analisarImagem
    mock_analisar_imagem.return_value = "Normal" # Simula um resultado de análise

    # Cria mocks para cursor e connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_mysql_connect.return_value = mock_conn

    # Simula o lastrowid para o INSERT da imagem
    mock_cursor.lastrowid = 1 # Define um ID de imagem simulado para o resultado

    # 5. Criar um arquivo de imagem de teste em memória
    # Nota: Para um teste real, você pode querer um conteúdo de imagem válido,
    # mas para este teste de unidade, um byte vazio é suficiente.
    test_image_data = b"fake image data"
    test_image_file = (BytesIO(test_image_data), 'imagem_teste.jpg')

    # 6. Preparar os dados do formulário
    # Flask espera os arquivos na lista `files` e os outros campos em `data`
    data = {
        'imagens': [test_image_file],
        'latitude_0': '12.34',
        'longitude_0': '56.78'
    }

    # 7. Realizar a requisição POST
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # 8. Verificações
    assert response.status_code == 302 # Espera um redirecionamento (para /status)
    assert '/status' in response.headers['Location'] # Verifica o redirecionamento correto

    # Verificações de chamadas aos mocks:

    # Verifica se o operador foi buscado pela sessão
    mock_buscar_por_cpf.assert_called_once_with('11122233344')

    # Verifica se os diretórios foram criados
    mock_makedirs.assert_any_call('uploads/99988877766', exist_ok=True)
    mock_makedirs.assert_any_call('status/99988877766', exist_ok=True)

    # Verifica se o arquivo foi "salvo" (ou seja, file.save foi chamado)
    # mock_open.call_args_list[0][0][0] acessa o primeiro argumento da primeira chamada a open, que é o caminho do arquivo
    # mock_open.return_value.write.call_args_list[0][0][0] acessa o primeiro argumento da primeira chamada a write
    assert 'uploads/99988877766/imagem_teste.jpg' in [call.args[0] for call in mock_open.call_args_list]

    # Verifica se o status inicial foi escrito
    mock_open.return_value.write.assert_any_call("Processando")

    # Verifica se a função analisarImagem foi chamada com o caminho correto
    # O caminho completo é construído pelo controller, então verificamos a substring
    args, _ = mock_analisar_imagem.call_args
    assert 'uploads/99988877766/imagem_teste.jpg' in args[0] #

    # Verifica as interações com o banco de dados
    mock_mysql_connect.assert_called_once() # Conexão estabelecida
    mock_cursor.execute.assert_any_call(
        "INSERT INTO imagens (nome, latitude, longitude, cpf_produtor) VALUES (%s, %s, %s, %s)",
        ('imagem_teste.jpg', 12.34, 56.78, '99988877766')
    ) # Insert de imagem
    mock_cursor.execute.assert_any_call(
        "INSERT INTO resultados (id, anomala) VALUES (%s, %s)",
        (1, False) # 'Normal' -> False (não anômala)
    ) # Insert de resultado
    mock_conn.commit.assert_called_once() # Commit foi chamado
    mock_cursor.close.assert_called_once() # Cursor fechado
    mock_conn.close.assert_called_once() # Conexão fechada

    # Verifica se o status final foi escrito
    mock_open.return_value.write.assert_any_call(f"Concluído com sucesso! — Resultado: Normal")


# --- Testes de Falha Adicionais para Upload ---

@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
def test_upload_nao_operador(mock_buscar_por_cpf, client):
    # Simula um produtor logado
    with client.session_transaction() as sess:
        sess['cpf'] = '99988877766'
    
    # Moca buscar_por_cpf para retornar um Produtor
    mock_produtor = Produtor(cpf='99988877766', nome='Produtor Teste', senha='senha123')
    mock_buscar_por_cpf.return_value = mock_produtor

    response = client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 403
    assert b'Apenas operadores podem enviar imagens.' in response.data

@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
def test_upload_sem_arquivos(mock_buscar_por_cpf, client):
    with client.session_transaction() as sess:
        sess['cpf'] = '11122233344'
    mock_operador = Operador(cpf='11122233344', nome='Operador Teste', senha='senha123', cpf_produtor='99988877766')
    mock_buscar_por_cpf.return_value = mock_operador

    response = client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'Nenhuma imagem enviada.' in response.data

@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
@patch('os.makedirs')
@patch('builtins.open', new_callable=MagicMock)
@patch('mysql.connector.connect')
def test_upload_latitude_invalida(mock_mysql_connect, mock_open, mock_makedirs, mock_buscar_por_cpf, client):
    with client.session_transaction() as sess:
        sess['cpf'] = '11122233344'
    mock_operador = Operador(cpf='11122233344', nome='Operador Teste', senha='senha123', cpf_produtor='99988877766')
    mock_buscar_por_cpf.return_value = mock_operador

    test_image_data = b"fake image data"
    test_image_file = (BytesIO(test_image_data), 'imagem_teste.jpg')

    data = {
        'imagens': [test_image_file],
        'latitude_0': 'INVALID_LAT', # Latitude inválida
        'longitude_0': '56.78'
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'Latitude ou longitude inv\xc3\xa1lida para imagem_teste.jpg' in response.data

# Você pode adicionar mais testes para:
# - Erro no IAService (simular exceção de analisarImagem)
# - Erro no MySQL (simular exceção no cursor.execute ou conn.commit)
# - Upload de múltiplas imagens