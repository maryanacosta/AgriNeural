# Agrineural Auth (Etapa 4 - INF221)

## Requisitos
- Python 3.10+
- MySQL Server
- Instalar dependências:
  pip install -r requirements.txt

## Setup
1. Execute o script SQL `schema.sql` no seu MySQL.
2. Altere as credenciais de conexão no `usuario_dao.py` se necessário.
3. Rode:
   python main.py

## Funcionalidades
- Cadastro e login de usuários com CPF, senha e tipo (produtor, operador, mosaiqueiro).
- Acesso ao painel diferenciado por perfil.
- Uso dos padrões Factory e MVC.

