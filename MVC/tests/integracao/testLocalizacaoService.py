import pytest
from unittest.mock import patch, MagicMock
from MVC.services.LocationService import salvarLocalizacaoProdutor 
import mysql.connector 

class TestSalvarLocalizacaoProdutor:

    @patch('mysql.connector.connect') 
    def test_salvar_localizacao_produtor_sucesso(self, mock_connect):
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        ok, erro = salvarLocalizacaoProdutor(
            cpf="12345678900",
            latitude=-23.5,
            longitude=-46.6,
            extTerritorial=100
        )
        
        assert ok is True
        assert erro is None
        
        mock_connect.assert_called_once()
        
        mock_conn.cursor.assert_called_once()
        
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO localizacao (cpf_produtor, latitude, longitude, ext_territorial) VALUES (%s, %s, %s, %s)",
            ("12345678900", -23.5, -46.6, 100)
        )
        
        mock_conn.commit.assert_called_once()
        
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_salvar_localizacao_produtor_valores_invalidos(self):
        ok, erro = salvarLocalizacaoProdutor(
            cpf="12345678900",
            latitude="invalido", 
            longitude=-46.6,
            extTerritorial=100
        )
        
        assert ok is False
        assert "latitude, longitude e extensão territorial devem ser números válidos." in erro

        ok, erro = salvarLocalizacaoProdutor(
            cpf="12345678900",
            latitude=-23.5,
            longitude=None, 
            extTerritorial=100
        )
        assert ok is False
        assert "latitude, longitude e extensão territorial devem ser números válidos." in erro


    @patch('mysql.connector.connect')
    def test_salvar_localizacao_produtor_cpf_duplicado(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.execute.side_effect = mysql.connector.IntegrityError("CPF duplicado")
        
        ok, erro = salvarLocalizacaoProdutor(
            cpf="12345678900",
            latitude=-23.5,
            longitude=-46.6,
            extTerritorial=100
        )
        
        assert ok is False
        assert "Já existe uma localização para este CPF." in erro 
        mock_conn.commit.assert_not_called() 
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_salvar_localizacao_produtor_erro_generico_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.execute.side_effect = mysql.connector.Error("Erro inesperado no DB")
        
        ok, erro = salvarLocalizacaoProdutor(
            cpf="12345678900",
            latitude=-23.5,
            longitude=-46.6,
            extTerritorial=100
        )
        
        assert ok is False
        assert "Erro ao salvar localização: Erro inesperado no DB" in erro 
        mock_conn.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_salvar_localizacao_produtor_sem_cpf(self):
        ok, erro = salvarLocalizacaoProdutor(
            cpf="", 
            latitude=-23.5,
            longitude=-46.6,
            extTerritorial=100
        )
        assert ok is False
        assert "CPF, latitude, longitude e extensão territorial são obrigatórios." in erro

        ok, erro = salvarLocalizacaoProdutor(
            cpf=None, 
            latitude=-23.5,
            longitude=-46.6,
            extTerritorial=100
        )
        assert ok is False
        assert "CPF, latitude, longitude e extensão territorial são obrigatórios." in erro