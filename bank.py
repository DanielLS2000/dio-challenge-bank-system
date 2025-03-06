import os
import datetime



def menu():
    print(f"""
    {"Bem vindo ao Sistema Bancario A".center(50, "=")}    

    [d] - Deposito
    [s] - Saque
    [e] - Extrato
    [u] - Criar Usuario
    [c] - Criar Conta
    [lc] - Listar Contas
    [q] - Sair

    {"".center(50, "=")}
    Digite uma opção para prosseguir.
    """)
    opcao = input()
    return opcao

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, transacoes, limite_transacao, DATE_FORMAT):
    if numero_saques >= limite_saques:
        input("O Limite de saques diario foi atingido, pressione enter para continuar")
    
    elif transacoes >= limite_transacao:
        input("O Limite de transações diario foi atingido, pressione enter para continuar")
    
    elif valor > saldo:
        input("O valor requisitado é superior ao saldo em conta, pressione enter para continuar")
    
    elif valor > limite:
        input("O valor requisitado excede o limite, pressione enter para continuar")
    
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}\tData/Hora: {datetime.datetime.now().strftime(DATE_FORMAT)}")
        numero_saques += 1
        transacoes += 1
        input("Saque realizado com sucesso, pressione enter para continuar")
    else:
        print("O Valor inserido precisa ser maior que 0.")
        input("Precione enter para retornar ao menu.")
    
    return saldo, extrato, numero_saques, transacoes

def depositar(saldo, valor, extrato, transacoes, limite_transacao, DATE_FORMAT, /):
    if transacoes >= limite_transacao:
        input("O Limite de transações diario foi atingido, pressione enter para continuar")
    elif valor > 0:
        saldo += valor
        extrato.append(f"Deposito: R$ {valor:.2f}\tData/Hora: {datetime.datetime.now().strftime(DATE_FORMAT)}")
        transacoes += 1
        input("Deposito realizado com sucesso, pressione enter para continuar")
    else:
        print("O Valor inserido precisa ser maior que 0.")
        input("Precione enter para retornar ao menu.")
    return saldo, extrato, transacoes

def exibir_extrato(saldo, /, *,  extrato):
    print(f"EXTRATO".center(50, "="))
    print("Não foram realizadas movimentações." if not extrato else "\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("".center(50, "="))

def criar_usuario(usuarios):
    cpf = input("Insira seu CPF: ")
    usuario = get_usuario(cpf=cpf, usuarios=usuarios)
    if usuario:
        print("Esse CPF já possui uma conta.")
        input("Pressione enter para retornar ao menu.")
        return
    
    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira sua data de nascimento(D/M/Y): ")
    logradouro = input("Insira o seu logradouro: ")
    numero = input("Insira o numero de sua residencia: ")
    bairro = input("Insira o seu bairro: ")
    cidade = input("Insira a sau cidade e estado: ")
    
    novo_usuario = {
        "nome": nome,
        "nascimento": data_nascimento,
        "cpf": cpf,
        "endereco" : {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade
        }
    }

    usuarios.append(novo_usuario)
    input("Usuario criado com sucesso. Pressione enter para continuar.")

def criar_conta(usuario_cpf, contas, usuarios):
    if len(contas) > 0:
        ultima_conta = contas[-1]
        numero_conta = ultima_conta["numero"] + 1
    else:
        numero_conta = 1

    usuario = get_usuario(usuario_cpf, usuarios=usuarios)
    
    nova_conta = {
        "agencia": "0001",
        "numero": numero_conta,
        "usuario": usuario
    }
    contas.append(nova_conta)
    print(f"Conta criada: Usuario {usuario["nome"]}")
    input("Pressione enter para continuar.")
    return contas

def get_usuario(cpf, usuarios):
    usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario[0] if usuario else None

def listar_contas(contas):
    mensagem = "Lista de Contas".center(50, "#")
    aux = ""
    for conta in contas:
        aux += f"Agencia:\t{conta["agencia"]}\n" + \
        f"Numero:\t{conta["numero"]}\n" + \
        f"Usuario:\t{conta["usuario"]["nome"]}\n\n"
    
    return mensagem + "\n" + aux

def main():
    saldo = 0
    limite = 500
    extrato = []
    saques = 0
    transacoes = 0
    usuarios = []
    contas = []
    LIMITE_DE_SAQUES = 3
    LIMITE_DE_TRANSACAO = 10
    DATE_FORMAT = "%H:%M - %d/%m/%Y"


    while True:
        clear_screen()

        opcao = menu()

        if opcao == "d":
            clear_screen()
            
            valor = input("Digite um valor a ser depositado: ")

            while not valor.isnumeric():
                valor = input("O Valor inserido precisa ser um numero positivo, digite novamente: ")
            
            valor = float(valor)

            saldo, extrato, transacoes = depositar(
                saldo,
                valor,
                extrato,
                transacoes,
                LIMITE_DE_TRANSACAO,
                DATE_FORMAT
            )   

        elif opcao == "s":
            clear_screen()        
            valor = input("Digite um valor a ser sacado: ")

            while not valor.isnumeric():
                valor = input("O Valor inserido precisa ser um numero positivo, digite novamente: ")

            valor = float(valor)

            
            saldo, extrato, saques, transacoes = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=saques,
                limite_saques=LIMITE_DE_SAQUES,
                transacoes=transacoes,
                limite_transacao=LIMITE_DE_TRANSACAO,
                DATE_FORMAT=DATE_FORMAT
            )
        elif opcao == "e":
            clear_screen()
            exibir_extrato(saldo, extrato=extrato)
            input("Pressione enter para continuar.")
        elif opcao == "u":
            clear_screen()

            criar_usuario(usuarios=usuarios)

        elif opcao == "c":
            clear_screen()
            cpfs_cadastrados = [usuario["cpf"] for usuario in usuarios]
            usuario_cpf = input("Informe o cpf do usuario: ")

            if usuario_cpf not in cpfs_cadastrados:
                usuario_cpf = input("Usuario não encontrado. Pressione enter para continuar.")
                continue

            criar_conta(usuario_cpf=usuario_cpf, 
                        contas=contas,
                        usuarios=usuarios)
        elif opcao == "lc":
            clear_screen()
            print(listar_contas(contas=contas))
            input("Pressine enter para continuar.")
        elif opcao == "q":
            clear_screen()
            break
        else:
            clear_screen()
            input("Comando invalido, pressione enter para continuar...")

main()