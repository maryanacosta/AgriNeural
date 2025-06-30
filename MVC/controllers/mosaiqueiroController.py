# Importações do Flask e do mysql.connector
from flask import Blueprint, session, render_template
import mysql.connector

# Cria o Blueprint da área do mosaiqueiro
mosaiqueiro_bp = Blueprint('mosaiqueiro', __name__)


# Rota para a página principal da área do mosaiqueiro
@mosaiqueiro_bp.route('/area-mosaiqueiro')
def area_mosaiqueiro():
    # Verifica se o usuário está logado
    if 'cpf' not in session:
        return "Você precisa estar logado.", 403

    # Obtém o CPF do usuário da sessão
    cpf_mosaiqueiro = session['cpf']

    # Conecta ao banco de dados MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="agrineural",
        password="senha123",
        database="agrineural"
    )
    cursor = conn.cursor(dictionary=True)

    # ❌ INCONSISTENTE: Tenta buscar `cpf_produtor` na tabela `usuarios`, 
    # mas essa coluna não existe lá (no modelo novo, está em `fazendas` ou `usuarios_fazendas`)
    cursor.execute("""
        SELECT cpf_produtor FROM usuarios WHERE cpf = %s
    """, (cpf_mosaiqueiro,))
    res = cursor.fetchone()
    if not res:
        cursor.close()
        conn.close()
        return "Usuário mosaiqueiro inválido.", 403

    cpf_produtor = res['cpf_produtor']

    # ❌ INCONSISTENTE: tenta buscar localização da fazenda em uma tabela `localizacao`
    # que foi removida no novo modelo de banco.
    cursor.execute("""
        SELECT latitude, longitude, ext_territorial FROM localizacao WHERE cpf_produtor = %s
    """, (cpf_produtor,))
    localizacao = cursor.fetchone()
    if not localizacao:
        cursor.close()
        conn.close()
        return "Localização da fazenda não cadastrada.", 404

    # ❌ INCONSISTENTE: busca imagens usando `cpf_produtor` na tabela `imagens`, 
    # mas essa coluna também não existe no modelo novo.
    cursor.execute("""
        SELECT i.nome, i.latitude, i.longitude, r.anomala
        FROM imagens i
        LEFT JOIN resultados r ON i.id = r.id
        WHERE i.cpf_produtor = %s
    """, (cpf_produtor,))
    imagens = cursor.fetchall()

    # Encerra conexão com o banco
    cursor.close()
    conn.close()

    # Prepara os dados da fazenda para o mapa
    centro = {
        'lat': float(localizacao['latitude']),
        'lng': float(localizacao['longitude'])
    }
    raio = float(localizacao['ext_territorial'])  # Raio do círculo no mapa

    # Monta a lista de imagens para o JS (mapa de calor)
    lista_imagens = []
    for img in imagens:
        lista_imagens.append({
            'nome': img['nome'],
            'lat': float(img['latitude']),
            'lng': float(img['longitude']),
            'anomala': bool(img['anomala'])
        })

    # Renderiza o template HTML com os dados passados
    return render_template('area_mosaiqueiro.html',
                           centro=centro,
                           raio=raio,
                           imagens=lista_imagens)
