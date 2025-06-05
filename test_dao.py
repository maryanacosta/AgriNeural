from model.usuario_dao import UsuarioDAO

dao = UsuarioDAO(password='SUA_SENHA_AQUI')

# Cadastro de teste
dao.cadastrar("12345678901", "senha123", "produtor")

# Login de teste
usuario = dao.autenticar("12345678901", "senha123")
if usuario:
    usuario.acessar_painel()

dao.fechar()
