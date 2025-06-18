# tests/test_upload_simples.py
import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from MVC.app import app
from MVC.model.usuario import Operador, Produtor # Certifique-se que Produtor está importado se for usado

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_simple_upload_key' # Use uma chave secreta
    with app.test_client() as client:
        yield client

def test_upload_sem_login_simples(client): # teste sem sessão ativa
    response = client.post('/upload')
    assert response.status_code == 403
    assert b'Voc\xc3\xaa precisa estar logado como operador.' in response.data 

@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf') 
def test_upload_nao_operador_simples(mock_buscar_por_cpf, client): # teste para verificar que o upload não é acessado por Produtor ou Mosaiqueiro
    with client.session_transaction() as sess:
        sess['cpf'] = '12345678900' 

    mock_produtor = Produtor(cpf='12345678900', nome='Teste', senha='teste123') # cria um produtor 
    mock_buscar_por_cpf.return_value = mock_produtor 

    response = client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 403
    assert b'Apenas operadores podem enviar imagens.' in response.data 
    

@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
def test_upload_sem_arquivos_simples(mock_buscar_por_cpf, client): # teste de envio sem imagens
    with client.session_transaction() as sess:
        sess['cpf'] = '12345678900' #
    mock_operador = Operador(cpf='12345678900', nome='Operador Teste', senha='senha123', cpf_produtor='98765432100') # cria um Operador
    mock_buscar_por_cpf.return_value = mock_operador 
    response = client.post('/upload', data={}, content_type='multipart/form-data')
    
    assert response.status_code == 400 # verifica se retorna o erro especificado
    assert b'Nenhuma imagem enviada.' in response.data # verifica se retornou a mensagem de erro

@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
def test_upload_latitude_invalida_simples(mock_buscar_por_cpf, client):
    with client.session_transaction() as sess:
        sess['cpf'] = '12345678900' 
        
    mock_operador = Operador(cpf='12345678900', nome='Operador Teste', senha='senha123', cpf_produtor='98765432100') # cria um Operador
    mock_buscar_por_cpf.return_value = mock_operador 

    test_image_file = (BytesIO(b"fake image data"), 'imagem_teste.jpg') 

    data = {
        'imagens': [test_image_file],
        'latitude_0': 'INVALID_LAT', # passa latitude errada
        'longitude_0': '56.78' 
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 400 # verifica se retorna o erro especificado
    assert b'Latitude ou longitude inv\xc3\xa1lida para imagem_teste.jpg' in response.data # verifica se retornou a mensagem de erro