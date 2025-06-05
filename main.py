from controller.auth_controller import AuthController

def menu():
    controller = AuthController()

    while True:
        print("\n--- Menu ---")
        print("1. Cadastrar")
        print("2. Login")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            controller.cadastrar_usuario()
        elif opcao == "2":
            controller.login()
        elif opcao == "3":
            controller.dao.fechar()  # encerra a conexão
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
