
# classe mãe que possui funcionalidades genéricas

class Usuario:
    def __init__(self, cpf, senha, nome=None):
        self.cpf = cpf
        self.senha = senha
        self.nome = nome  # opcional

    def acessar_painel(self):
        raise NotImplementedError


# classes filhas que herdam de Usuário e possuem funcionalidades específicas

class Produtor(Usuario):
    def acessar_painel(self):
        print("Painel do PRODUTOR carregado.")


class Operador(Usuario):
    def __init__(self, cpf, senha, nome=None, cpf_produtor=None):
        super().__init__(cpf, senha, nome)
        self.cpf_produtor = cpf_produtor

    def acessar_painel(self):
        print("Painel do OPERADOR carregado.")


class Mosaiqueiro(Usuario):
    def __init__(self, cpf, senha, nome=None, cpf_produtor=None):
        super().__init__(cpf, senha, nome)
        self.cpf_produtor = cpf_produtor

    def acessar_painel(self):
        print("Painel do MOSAIQUEIRO carregado.")
