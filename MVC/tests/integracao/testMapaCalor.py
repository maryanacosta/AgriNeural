import pytest
from unittest.mock import patch, MagicMock
from MVC.app import app
import mysql.connector

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

class TestMosaiqueiroController:

    def test_area_mosaiqueiro_nao_logado(self, client):
        with client.session_transaction() as sess:
            sess.pop('cpf', None)
        
        response = client.get('/area_mosaiqueiro')
        assert response.status_code == 403
        assert b'Voc\xc3\xaa precisa estar logado.' in response.data 

    @patch('mysql.connector.connect')
    def test_area_mosaiqueiro_cpf_invalido(self, mock_connect, client):
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        
        mock_cursor.fetchone.side_effect = [None] 

        with client.session_transaction() as sess:
            sess['cpf'] = '12345678900' 

        response = client.get('/area_mosaiqueiro')
        assert response.status_code == 403
        assert b'Usu\xc3\xa1rio mosaiqueiro inv\xc3\xa1lido.' in response.data 
        mock_cursor.execute.assert_called_once_with(
            """SELECT cpf_produtor FROM usuarios WHERE cpf = %s""", ('12345678900',) 
        )
        mock_cursor.close.assert_called_once() 
        mock_conn.close.assert_called_once() 

    @patch('mysql.connector.connect')
    def test_area_mosaiqueiro_localizacao_nao_cadastrada(self, mock_connect, client):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.side_effect = [
            {'cpf_produtor': '98765432100'}, 
            None 
        ]

        with client.session_transaction() as sess:
            sess['cpf'] = '12345678900'

        response = client.get('/area_mosaiqueiro')
        assert response.status_code == 404
        assert b'Localiza\xc3\xa7\xc3\xa3o da fazenda n\xc3\xa3o cadastrada.' in response.data 
        
        calls = mock_cursor.execute.call_args_list
        assert len(calls) == 2
        assert calls[0].args[0] == """
        SELECT cpf_produtor FROM usuarios WHERE cpf = %s
    """
        assert calls[0].args[1] == ('12345678900',)
        assert calls[1].args[0] == """
        SELECT latitude, longitude, ext_territorial FROM localizacao WHERE cpf_produtor = %s
    """
        assert calls[1].args[1] == ('98765432100',)
        
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


    @patch('mysql.connector.connect', side_effect=mysql.connector.Error("Erro de conexão simulado"))
    def test_area_mosaiqueiro_erro_conexao_db(self, mock_connect, client):
        with client.session_transaction() as sess:
            sess['cpf'] = '12345678900' 
