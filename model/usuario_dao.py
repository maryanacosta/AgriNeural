import mysql.connector
from model.usuario_factory import UsuarioFactory

class UsuarioDAO:
    def __init__(self, host='localhost', user='agrineural', password='senha123', database='agrineural'):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("[INFO] Conexão com o banco de dados estabelecida com sucesso.")
        except mysql.connector.Error as err:
            print(f"[ERRO] Falha na conexão com o banco de dados: {err}")
            exit(1)

    def cadastro(self, cpf, senha, tipo, nome):
        try:
            sql = "INSERT INTO usuarios (cpf, senha, tipo, nome) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (cpf, senha, tipo, nome))
            self.conn.commit()
            print("[INFO] Usuário cadastrado com sucesso.")
        except mysql.connector.IntegrityError:
            print("[ERRO] Já existe um usuário com esse CPF.")
        except mysql.connector.Error as err:
            print(f"[ERRO] Falha ao cadastrar usuário: {err}")

    def autenticar(self, cpf, senha):
        try:
            sql = "SELECT senha, tipo FROM usuarios WHERE cpf = %s"
            self.cursor.execute(sql, (cpf,))
            result = self.cursor.fetchone()

            if result:
                senha_db, tipo = result
                if senha_db == senha:
                    print("[INFO] Autenticação bem-sucedida.")
                    return UsuarioFactory.criar_usuario(tipo, cpf, senha)
                else:
                    print("[ERRO] Senha incorreta.")
            else:
                print("[ERRO] Usuário não encontrado.")
        except mysql.connector.Error as err:
            print(f"[ERRO] Falha ao autenticar usuário: {err}")
        return None

    def fechar(self):
        self.cursor.close()
        self.conn.close()
        print("[INFO] Conexão com o banco de dados encerrada.")

