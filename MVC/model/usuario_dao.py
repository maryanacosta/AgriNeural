# Importa o conector do MySQL para Python
import mysql.connector
# Importa a fábrica que instancia o tipo certo de usuário (Produtor, Operador ou Mosaiqueiro)
from MVC.model.usuario_factory import UsuarioFactory


# Classe responsável por acessar e manipular dados da tabela 'usuarios' no banco
class UsuarioDAO:
    def __init__(self, host='localhost', user='agrineural', password='senha123', database='agrineural'):
        """
        Construtor: Estabelece conexão com o banco MySQL ao instanciar a classe.
        """
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()  # Cria um cursor para executar comandos SQL
            print("[INFO] Conexão com o banco de dados estabelecida com sucesso.")
        except mysql.connector.Error as err:
            # Se ocorrer erro ao conectar, exibe o erro e encerra o programa
            print(f"[ERRO] Falha na conexão com o banco de dados: {err}")
            exit(1)


    def buscar_por_cpf(self, cpf):
        """
        Busca um usuário pelo CPF na tabela 'usuarios'.
        Retorna uma instância de Produtor, Operador ou Mosaiqueiro, usando a factory.
        """
        try:
            sql = "SELECT cpf, senha, tipo, nome FROM usuarios WHERE cpf = %s"
            self.cursor.execute(sql, (cpf,))
            row = self.cursor.fetchone()

            if row:
                cpf, senha, tipo, nome = row
                # Usa a fábrica para retornar o tipo correto de usuário
                return UsuarioFactory.criar_usuario(tipo, cpf, senha, nome=nome)
        except mysql.connector.Error as err:
            print(f"[ERRO] Erro ao buscar usuário: {err}")
        return None  # Se não encontrou ou ocorreu erro


    def cadastro(self, cpf, senha, tipo, nome):
        """
        Cadastra um novo usuário no sistema.
        CPF é a chave primária, então não pode ser duplicado.
        """
        try:
            sql = "INSERT INTO usuarios (cpf, senha, tipo, nome) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (cpf, senha, tipo, nome))
            self.conn.commit()  # Confirma a inserção no banco
            print("[INFO] Usuário cadastrado com sucesso.")
        except mysql.connector.IntegrityError:
            print("[ERRO] Já existe um usuário com esse CPF.")
        except mysql.connector.Error as err:
            print(f"[ERRO] Falha ao cadastrar usuário: {err}")


    def autenticar(self, cpf, senha):
        """
        Verifica se o CPF e a senha correspondem a um usuário existente.
        Se sim, retorna uma instância do usuário correspondente (via factory).
        """
        try:
            sql = "SELECT cpf, senha, tipo, nome FROM usuarios WHERE cpf = %s AND senha = %s"
            self.cursor.execute(sql, (cpf, senha))
            row = self.cursor.fetchone()

            if row:
                cpf, senha, tipo, nome = row
                return UsuarioFactory.criar_usuario(tipo, cpf, senha, nome=nome)
        except mysql.connector.Error as err:
            print(f"[ERRO] Erro ao autenticar usuário: {err}")
        return None  # Usuário não encontrado ou erro


    def fechar(self):
        """
        Encerra a conexão com o banco de dados.
        Deve ser chamada quando o DAO não for mais necessário.
        """
        self.cursor.close()
        self.conn.close()
        print("[INFO] Conexão com o banco de dados encerrada.")
