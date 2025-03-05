import os

home = f"""
    {"Bem vindo ao Sistema Bancario A".center(50, "=")}    
    
    [d] - Deposito
    [s] - Saque
    [e] - Extrato
    [q] - Sair

    {"".center(50, "=")}

    Digite uma opção para prosseguir.
    """

saldo = 0
limite = 500
extrato = []
saques = 0
LIMITE_DE_SAQUES = 3

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    clear_screen()

    opcao = input(home)

    if opcao == "d":
        clear_screen()

        valor = input("Digite um valor a ser depositado: ")

        while not valor.isnumeric():
            valor = input("O Valor inserido precisa ser um numero positivo, digite novamente: ")
        
        valor = float(valor)

        if valor > 0:
            saldo += valor
            extrato.append(f"Deposito: R$ {valor:.2f}")
            input("Deposito realizado com sucesso, pressione enter para continuar")
        else:
            print("O Valor inserido precisa ser maior que 0.")
            input("Precione enter para retornar ao menu.")

    elif opcao == "s":
        clear_screen()

        if saques >= LIMITE_DE_SAQUES:
            input("O Limite de saques diario foi atingido, pressione enter para continuar")
            continue

        valor = input("Digite um valor a ser sacado: ")

        while not valor.isnumeric():
            valor = input("O Valor inserido precisa ser um numero positivo, digite novamente: ")

        valor = float(valor)

        if valor > saldo:
            input("O valor requisitado é superior ao saldo em conta, pressione enter para continuar")
            continue
        if valor > limite:
            input("O valor requisitado excede o limite, pressione enter para continuar")
            continue
        if valor > 0:
            saldo -= valor
            extrato.append(f"Saque: R$ {valor:.2f}")
            saques += 1
            
            input("Saque realizado com sucesso, pressione enter para continuar")
            continue
    elif opcao == "e":
        clear_screen()
        print(f"EXTRATO".center(50, "="))
        print("Não foram realizadas movimentações." if not extrato else "\n".join(extrato))
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("".center(50, "="))
        input("Pressione enter para continuar.")
    elif opcao == "q":
        clear_screen()
        break
    else:
        clear_screen()
        input("Comando invalido, pressione enter para continuar...")
     