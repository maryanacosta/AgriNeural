import pytest
from unittest.mock import patch, MagicMock
from MVC.app import app
from MVC.model.usuario import Produtor, Operador, Mosaiqueiro

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data  

def test_login_post_invalido(client):
    response = client.post('/auth/login', data={
        'cpf': '00000000000',
        'senha': 'senhaerrada'
    })
    assert response.status_code == 200
    assert b'inv' in response.data  # Verifica que aparece algum erro no HTML

@patch('MVC.model.usuario_dao.UsuarioDAO.autenticar') 
def test_login_produtor_sucesso(mock_autenticar, client): # teste de autenticação do produtor
    mock_produtor = Produtor(cpf='12345678900', nome='Teste', senha='teste123') # cria um produtor válido
    mock_autenticar.return_value = mock_produtor 

    response = client.post('/auth/login', data={ # evia requisição com cpf e senha de teste
        'cpf': '12345678900',
        'senha': 'teste123'
    })
    assert response.status_code == 302 # verifica se houve redirecionamento
    assert '/area_produtor' in response.headers['Location'] # verifica se redirecionou para a área do mosaiqueiro
    mock_autenticar.assert_called_once_with('12345678900', 'teste123') # verifica se o método autenticar foi chamado
    

@patch('MVC.model.usuario_dao.UsuarioDAO.autenticar')
def test_login_operador_sucesso(mock_autenticar, client): # teste de autenticação do operador
    mock_operador = Operador(cpf='12345678900', nome='Teste', senha='teste123', cpf_produtor='98765432100') # cria um operador válido
    mock_autenticar.return_value = mock_operador

    response = client.post('/auth/login', data={
        'cpf': '12345678900',
        'senha': 'teste123'
    })
    assert response.status_code == 302 # verifica se houve redirecionamento
    assert '/area_operador' in response.headers['Location'] # verifica se redirecionou para a área do mosaiqueiro
    mock_autenticar.assert_called_once_with('12345678900', 'teste123') # Verifica se o método autenticar foi chamado com os dados corretos
    
@patch('MVC.model.usuario_dao.UsuarioDAO.autenticar')
def test_login_mosaiqueiro_sucesso(mock_autenticar, client): # teste de autenticação do mosaiqueiro
    mock_mosaiqueiro = Mosaiqueiro(cpf='12345678900', nome='Teste', senha='teste123', cpf_produtor='98765432100') # cria um objeto válido
    mock_autenticar.return_value = mock_mosaiqueiro

    response = client.post('/auth/login', data={ # envia o POST com cpf e senha 
        'cpf': '12345678900',
        'senha': 'teste123'
    })
    assert response.status_code == 302 # verifica se houve redirecionamento
    assert '/area_mosaiqueiro' in response.headers['Location'] # verifica se redirecionou para a área do mosaiqueiro
    mock_autenticar.assert_called_once_with('12345678900', 'teste123') # Verifica se o método autenticar foi chamado com os dados corretos
    