# tests/test_ia_service.py
from MVC.services.IAService import analisarImagem

def test_analisarImagem():
    resultado = analisarImagem('tests/imagens/teste.jpg')
    assert resultado in ['Normal', 'Anômala']
