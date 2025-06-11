from flask import Blueprint, session, render_template
import mysql.connector

mosaiqueiro_bp = Blueprint('mosaiqueiro', __name__)


# página do mosaiqueiro

@mosaiqueiro_bp.route('/area_mosaiqueiro')
def area_mosaiqueiro():
    if 'cpf' not in session:
        return "Você precisa estar logado.", 403

    cpf_mosaiqueiro = session['cpf']

    # Conectar banco
    conn = mysql.connector.connect(
        host="localhost",
        user="agrineural",
        password="senha123",
        database="agrineural"
    )
    cursor = conn.cursor(dictionary=True)

    # Buscar CPF do produtor relacionado ao mosaiqueiro
    cursor.execute("""
        SELECT cpf_produtor FROM usuarios WHERE cpf = %s
    """, (cpf_mosaiqueiro,))
    res = cursor.fetchone()
    if not res:
        cursor.close()
        conn.close()
        return "Usuário mosaiqueiro inválido.", 403

    cpf_produtor = res['cpf_produtor']

    # Buscar localização da fazenda do produtor
    cursor.execute("""
        SELECT latitude, longitude, ext_territorial FROM localizacao WHERE cpf_produtor = %s
    """, (cpf_produtor,))
    localizacao = cursor.fetchone()
    if not localizacao:
        cursor.close()
        conn.close()
        return "Localização da fazenda não cadastrada.", 404

    # Buscar imagens e se são anômalas ou não
    cursor.execute("""
        SELECT i.nome, i.latitude, i.longitude, r.anomala
        FROM imagens i
        LEFT JOIN resultados r ON i.id = r.id
        WHERE i.cpf_produtor = %s
    """, (cpf_produtor,))
    imagens = cursor.fetchall()

    cursor.close()
    conn.close()

    # Preparar dados para o template
    centro = {
        'lat': float(localizacao['latitude']),
        'lng': float(localizacao['longitude'])
    }
    raio = float(localizacao['ext_territorial'])  # assumindo em km

    # Formatando imagens para o JS no template
    lista_imagens = []
    for img in imagens:
        lista_imagens.append({
            'nome': img['nome'],
            'lat': float(img['latitude']),
            'lng': float(img['longitude']),
            'anomala': bool(img['anomala'])
        })

    return render_template('area_mosaiqueiro.html',
                           centro=centro,
                           raio=raio,
                           imagens=lista_imagens)