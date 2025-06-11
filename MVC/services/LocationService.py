from mysql.connector import connect, Error


# função para salvar a localização do produtor

def salvarLocalizacaoProdutor(cpf, latitude, longitude, extTerritorial):
    try:
        with connect(
            host="localhost",
            user="agrineural",
            password="senha123",
            database="agrineural"
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO localizacao (cpf_produtor, latitude, longitude, ext_territorial)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (cpf, latitude, longitude, extTerritorial)
                )
                conn.commit()
        return True, None
    except Error as e:
        return False, str(e)