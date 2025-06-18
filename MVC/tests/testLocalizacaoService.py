import pytest
from unittest.mock import patch, MagicMock
from MVC.services.LocationService import salvarLocalizacaoProdutor
from mysql.connector import Error 

@patch('mysql.connector.connect') 
def test_salvarLocalizacaoProdutor_sucesso(mock_connect):
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor 
    mock_connect.return_value.__enter__.return_value = mock_conn 

    # simula os dados
    cpf = "12345678900"
    latitude = -23.5
    longitude = -46.6
    ext_territorial = 100

    ok, erro = salvarLocalizacaoProdutor( # chama a funcionalidade
        cpf=cpf,
        latitude=latitude,
        longitude=longitude,
        extTerritorial=ext_territorial
    )

    assert ok is True # verifica se o retorno de sucesso é True
    assert erro is None # verifica se a mensagem de erro é None para sucesso

    # verifica se a conexão com o banco de dados foi feita
    mock_connect.assert_called_once_with(
        host="localhost",
        user="agrineural",
        password="senha123",
        database="agrineural"
    )

    # verifica se o método execute foi chamado com a query SQL correta e os parâmetros
    mock_cursor.execute.assert_called_once_with(
        """
                    INSERT INTO localizacao (cpf_produtor, latitude, longitude, ext_territorial)
                    VALUES (%s, %s, %s, %s)
                    """,
        (cpf, latitude, longitude, ext_territorial)
    )

    # verifica se o commit foi chamado na conexão
    mock_conn.commit.assert_called_once()


@patch('mysql.connector.connect')
def test_salvarLocalizacaoProdutor_falha_db(mock_connect):
    mock_connect.side_effect = Error("Erro de conexão simulado")

    # simula valores
    cpf = "invalid_cpf"
    latitude = 0.0
    longitude = 0.0
    ext_territorial = 0

    ok, erro = salvarLocalizacaoProdutor( # chama a funcionalidade
        cpf=cpf,
        latitude=latitude,
        longitude=longitude,
        extTerritorial=ext_territorial
    )

    assert ok is False # verifica se o retorno de falha é False
    assert "Erro de conexão simulado" in erro # verifica se a mensagem de erro contém a mensagem esperada

    mock_connect.assert_called_once()