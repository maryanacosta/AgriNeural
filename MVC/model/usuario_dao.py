import mysql.connector
from MVC.model.usuario_factory import UsuarioFactory

# classe para encapsular ações no banco de dados

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

    def buscar_por_cpf(self, cpf):
        try:
            sql = "SELECT cpf, senha, tipo, nome FROM usuarios WHERE cpf = %s"
            self.cursor.execute(sql, (cpf,))
            row = self.cursor.fetchone()

            if row:
                cpf, senha, tipo, nome = row
                return UsuarioFactory.criar_usuario(tipo, cpf, senha, nome=nome)
        except mysql.connector.Error as err:
            print(f"[ERRO] Erro ao buscar usuário: {err}")
        return None

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
            sql = "SELECT cpf, senha, tipo, nome FROM usuarios WHERE cpf = %s AND senha = %s"
            self.cursor.execute(sql, (cpf, senha))
            row = self.cursor.fetchone()

            if row:
                cpf, senha, tipo, nome = row
                return UsuarioFactory.criar_usuario(tipo, cpf, senha, nome=nome)
        except mysql.connector.Error as err:
            print(f"[ERRO] Erro ao autenticar usuário: {err}")
        return None
    

    def fechar(self):
        self.cursor.close()
        self.conn.close()
        print("[INFO] Conexão com o banco de dados encerrada.")
