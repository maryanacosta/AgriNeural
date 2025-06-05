from flask import session
from model.usuario_dao import UsuarioDAO

class AuthController:
    def __init__(self):
        self.dao = UsuarioDAO()

    def cadastrar_usuario(self):
        cpf = input("CPF: ")
        senha = input("Senha: ")
        tipo = input("Tipo de usuário (produtor, operador, mosaiqueiro): ").lower()
        self.dao.cadastrar(cpf, senha, tipo)

    def login(self):
        cpf = input("CPF: ")
        senha = input("Senha: ")
        usuario = self.dao.autenticar(cpf, senha)
        if usuario:
            print("Login bem-sucedido!")
            session['cpf'] = usuario.cpf  # <- isso aqui deve estar DENTRO do login
            usuario.acessar_painel()
        else:
            print("CPF ou senha inválidos.")
