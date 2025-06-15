# tests/test_auth.py
import pytest
from MVC.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data  # Verifica se contém 'Login' no HTML

def test_login_post_invalido(client):
    response = client.post('/auth/login', data={
        'cpf': '00000000000',
        'senha': 'senhaerrada'
    })
    assert response.status_code == 200
    assert b'inv' in response.data  # Verifica que aparece algum erro no HTML

