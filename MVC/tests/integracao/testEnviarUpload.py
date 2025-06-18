import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from MVC.app import app
from MVC.model.usuario import Operador
 
@patch('MVC.model.usuario_dao.UsuarioDAO.buscar_por_cpf')
@patch('MVC.services.IAService.analisarImagem')
@patch('os.makedirs')
@patch('builtins.open', new_callable=MagicMock)
@patch('mysql.connector.connect')
def test_upload_valido_operador_simples(mock_mysql_connect, mock_open, mock_makedirs, mock_analisar_imagem, mock_buscar_por_cpf, client):
    
    with client.session_transaction() as sess:
        sess['cpf'] = '12345678900' 

    mock_operador = Operador(cpf='12345678900', nome='Operador Teste', senha='senha123', cpf_produtor='98765432100') #cria um Operador
    mock_buscar_por_cpf.return_value = mock_operador 

    mock_analisar_imagem.return_value = "Normal" 

    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_mysql_connect.return_value = mock_conn
    mock_cursor.lastrowid = 1 

    test_image_file = (BytesIO(b"fake image data"), 'imagem_teste.jpg') 

    data = {
        'imagens': [test_image_file],
        'latitude_0': '12.34',
        'longitude_0': '56.78'
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 302 # verifica se houve redirecionamento
    assert '/status' in response.headers['Location'] # verifica se foi redirecionado para os status
    mock_buscar_por_cpf.assert_called_once() 
    mock_analisar_imagem.assert_called_once() 
    mock_mysql_connect.assert_called_once() 
    mock_conn.commit.assert_called_once() 