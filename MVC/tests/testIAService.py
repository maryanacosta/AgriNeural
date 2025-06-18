from MVC.services.IAService import ModeloAgrineural # importação da funcionalidade


class TestModeloAgrineural:
    
    def test_inicializacao_modelo(self):
        modelo = ModeloAgrineural()  
        assert isinstance(modelo, ModeloAgrineural)

    def test_set_threshold(self):
        modelo = ModeloAgrineural()  
        novo_threshold = 0.005  
        modelo.setTrashold(novo_threshold)  
        assert modelo.threshold == novo_threshold  

    def test_analisarImagem(self): 
        modelo = ModeloAgrineural() 
        resultado = modelo.analisarImagem('MVC/tests/imagens/teste.jpg') 
        assert resultado in ['Normal', 'Anômala'] 

