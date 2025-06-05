class Usuario:
    def __init__(self, cpf, senha):
        self.cpf = cpf
        self.senha = senha

    def acessar_painel(self):
        raise NotImplementedError
        

class Produtor(Usuario):
    def acessar_painel(self):
        print("Painel do PRODUTOR carregado.")


class Operador(Usuario):
    def acessar_painel(self):
        print("Painel do OPERADOR carregado.")


class Mosaiqueiro(Usuario):
    def acessar_painel(self):
        print("Painel do MOSAIQUEIRO carregado.")
