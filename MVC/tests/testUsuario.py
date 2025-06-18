import pytest
from unittest.mock import MagicMock, patch
from MVC.model.usuario import Usuario, Produtor, Operador, Mosaiqueiro #
from MVC.model.usuario_dao import UsuarioDAO #
from MVC.model.usuario_factory import UsuarioFactory #

class TestUsuario:
    
    def test_usuario_base(self):
        user = Usuario("12345678900", "senha123", "João") 
        assert user.cpf == "12345678900"
        assert user.senha == "senha123" 
        assert user.nome == "João"

    def test_produtor(self):
        produtor = Produtor("12345678900", "senhaProdutor", "Teste") 
        assert produtor.cpf == "12345678900" 
        assert produtor.nome == "Teste" 

    def test_operador(self):
        operador = Operador("12345678900", "senhaOperador", "Teste", "98765432100") 
        assert operador.cpf == "12345678900" 
        assert operador.nome == "Teste" 
        assert operador.cpf_produtor == "98765432100" 

    def test_mosaiqueiro(self):
        mosaiqueiro = Mosaiqueiro("12345678900", "senhaMosaico", "Teste", "98765432100") 
        assert mosaiqueiro.cpf == "12345678900" 
        assert mosaiqueiro.nome == "Teste" 
        assert mosaiqueiro.cpf_produtor == "98765432100" 

class TestUsuarioFactory:
    
    def test_criar_produtor(self):
        produtor = UsuarioFactory.criar_usuario("produtor", "12345678900", "senha123", "Produtor Teste") 
        assert isinstance(produtor, Produtor) 
        assert produtor.cpf == "12345678900" 
        assert produtor.nome == "Produtor Teste" 

    def test_criar_operador(self):
        operador = UsuarioFactory.criar_usuario("operador", "12345678900", "senha123", "Operador Teste", "98765432100") 
        assert isinstance(operador, Operador) 
        assert operador.cpf == "12345678900" 
        assert operador.nome == "Operador Teste" 
        assert operador.cpf_produtor == "98765432100" 

    def test_criar_mosaiqueiro(self):
        mosaiqueiro = UsuarioFactory.criar_usuario("mosaiqueiro", "12345678900", "senha123", "Mosaiqueiro Teste", "98765432100") 
        assert isinstance(mosaiqueiro, Mosaiqueiro) 
        assert mosaiqueiro.cpf == "12345678900" 
        assert mosaiqueiro.nome == "Mosaiqueiro Teste" 
        assert mosaiqueiro.cpf_produtor == "98765432100" 

    def test_criar_usuario_invalido(self):
        usuario = UsuarioFactory.criar_usuario("tipo_invalido", "12345678900", "senha123") 
        assert usuario is None 
