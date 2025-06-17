from MVC.services.IAService import analisarImagem # importação da funcionalidade

def test_analisarImagem(): # teste
    resultado = analisarImagem('MVC/tests/imagens/teste.jpg') # chama a função com uma imagem de teste
    assert resultado in ['Normal', 'Anômala'] # verifica se possui o resultado esperado
