from model.usuario import Produtor, Operador, Mosaiqueiro

class UsuarioFactory:
    @staticmethod
    def criar_usuario(tipo, cpf, senha):
        match tipo.lower():
            case 'produtor':
                return Produtor(cpf, senha)
            case 'operador':
                return Operador(cpf, senha)
            case 'mosaiqueiro':
                return Mosaiqueiro(cpf, senha)
            case _:
                raise ValueError("Tipo de usuário inválido.")
