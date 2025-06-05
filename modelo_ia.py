import os

UPLOAD_FOLDER = 'uploads'

def listar_imagens_por_operador():
    imagens_por_operador = {}

    # Para cada pasta dentro de 'uploads' (cada CPF)
    for cpf in os.listdir(UPLOAD_FOLDER):
        caminho_operador = os.path.join(UPLOAD_FOLDER, cpf)
        if os.path.isdir(caminho_operador):
            imagens = []
            for arquivo in os.listdir(caminho_operador):
                if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    imagens.append(os.path.join(caminho_operador, arquivo))
            imagens_por_operador[cpf] = imagens

    return imagens_por_operador

# Exemplo de uso (para testar direto)
if __name__ == '__main__':
    dados = listar_imagens_por_operador()
    for cpf, imagens in dados.items():
        print(f"Operador {cpf} enviou:")
        for imagem in imagens:
            print(f"  - {imagem}")
