from MVC.model.usuario import Produtor, Operador, Mosaiqueiro

# padrão de projeto para criar um usuário

class UsuarioFactory:
    
    @staticmethod
    def criar_usuario(tipo, cpf, senha, nome=None):
        if tipo == 'produtor':
            return Produtor(cpf, senha, nome)
        elif tipo == 'operador':
            return Operador(cpf, senha, nome)
        elif tipo == 'mosaiqueiro':
            return Mosaiqueiro(cpf, senha, nome)
        else:
            return None
