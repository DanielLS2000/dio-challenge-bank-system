import os
from classes import *



def menu():
    print(f"""
    {"Bem vindo ao Sistema Bancario A".center(50, "=")}    

    [d] \tDeposito
    [s] \tSaque
    [e] \tExtrato
    [u] \tCriar Usuario
    [c] \tCriar Conta
    [lc] \tListar Contas
    [q] \tSair

    {"".center(50, "=")}
    Digite uma opção para prosseguir.
    """)
    opcao = input()
    return opcao

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sacar(usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = get_usuario(cpf, usuarios)

    if not usuario:
        print("Usuario não encontrado.")
        return
    
    numero_conta = input("Informe o numero da conta: ")
    conta = get_conta(usuario, numero_conta)

    if not conta:
        print("Esta conta não existe.")
        return

    valor = input("Digite um valor a ser sacado: ")

    while not valor.isnumeric():
        valor = input("O Valor inserido precisa ser um numero positivo, digite novamente: ")
    
    valor = float(valor)

    transacao = Saque(valor)
    
    usuario.realizar_transacao(conta, transacao)

def depositar(usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = get_usuario(cpf, usuarios)

    if not usuario:
        print("Usuario não encontrado.")
        return
    
    numero_conta = input("Informe o numero da conta: ")
    conta = get_conta(usuario, numero_conta)

    if not conta:
        print("Esta conta não existe.")
        return

    valor = input("Digite um valor a ser depositado: ")

    while not valor.isnumeric():
        valor = input("O Valor inserido precisa ser um numero positivo, digite novamente: ")
    
    valor = float(valor)

    transacao = Deposito(valor)
    
    usuario.realizar_transacao(conta, transacao)

def exibir_extrato(usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = get_usuario(cpf, usuarios)

    if not usuario:
        print("Usuario não encontrado.")
        return
    
    numero_conta = input("Informe o numero da conta: ")
    conta = get_conta(usuario, numero_conta)

    if not conta:
        print("Esta conta não existe.")
        return

    aux = ""
    aux += (f"EXTRATO".center(50, "="))
    extrato = conta.historico.transacoes
    if extrato:
        for transacao in extrato:
            aux += f"\n{type(transacao).__name__}:\tR${transacao.valor:.2f}"
            aux += f"\t{transacao.data}"
    else:
        aux += ("\nNão foram realizadas movimentações.")
    aux += (f"\nSaldo: R$ {conta.saldo:.2f}\n")
    aux += ("".center(50, "="))
    print(aux)

def criar_usuario(usuarios):
    cpf = input("Insira seu CPF: ")
    usuario = get_usuario(cpf=cpf, usuarios=usuarios)
    if usuario:
        print("Esse CPF já possui uma conta.")
        input("Pressione enter para retornar ao menu.")
        return
    
    nome = input("Insira seu nome: ")
    data_nascimento = input("Insira sua data de nascimento(D/M/Y): ")
    endereco = input("Insira o seu endereco: ")

    novo_usuario = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nascimento)

    usuarios.append(novo_usuario)
    print("Usuario criado com sucesso.")

def criar_conta(usuario, contas):
    if len(contas) > 0:
        ultima_conta = contas[-1]
        numero_conta = ultima_conta.numero + 1
    else:
        numero_conta = 1

    nova_conta = ContaCorrente.nova_conta(usuario, numero_conta)
    usuario.adicionar_conta(nova_conta)

    contas.append(nova_conta)
    print(f"Conta criada: Usuario {usuario.nome}")
    return contas

def get_usuario(cpf, usuarios):
    usuario = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuario[0] if usuario else None

def get_conta(usuario, numero_conta):
    contas_cliente = usuario.contas

    conta = [conta for conta in contas_cliente if conta.numero == int(numero_conta)]
    return conta[0] if conta else None

def listar_contas(contas):
    mensagem = "Lista de Contas".center(50, "#")
    aux = ""
    for conta in contas:
        aux += str(conta)
    
    return mensagem + "\n" + aux

def main():
    usuarios = []
    contas = []

    while True:
        clear_screen()

        opcao = menu()

        if opcao == "d":
            clear_screen()
            depositar(usuarios)
            input("Pressione enter para continuar.")
        elif opcao == "s":
            clear_screen()        
            sacar(usuarios)
            input("Pressione enter para continuar.")
        elif opcao == "e":
            clear_screen()
            exibir_extrato(usuarios=usuarios)
            input("Pressione enter para continuar.")
        elif opcao == "u":
            clear_screen()
            criar_usuario(usuarios=usuarios)
            input("Pressione enter para continuar.")

        elif opcao == "c":
            clear_screen()
            usuario_cpf = input("Informe o cpf do usuario: ")

            usuario = get_usuario(usuario_cpf, usuarios)
            if not usuario:
                usuario_cpf = input("Usuario não encontrado. Pressione enter para continuar.")
                continue

            criar_conta(usuario=usuario,
                        contas=contas)
            input("Pressione enter para continuar.")
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