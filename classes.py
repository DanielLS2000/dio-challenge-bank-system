from abc import ABC, abstractmethod
import datetime

class Conta:
    def __init__(self, numero: int, cliente):
        self._saldo = float(0)
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero: int):
        conta = cls(cliente=cliente, numero=numero)
        return conta
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float):        
        if (valor > 0) and (valor <= self.saldo):
            self.saldo -= valor
            return True
        else:
            return False

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            return True
        else:
            return False

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor: float):

        n_saques = len([transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)])
        
        if (valor > self._limite):
            print("O valor requisitado excede o limite.")
            return False
        elif (n_saques >= self._limite_saques):
            print("O Limite de saques diario foi atingido.")
            return False
        else:
            return super().sacar(valor)
        
    def __str__(self):
        return f"Agencia:\t{self.agencia}\n" + \
                f"C/C:\t{self.numero}\n" + \
                f"Titular:\t{self.cliente.nome}\n"

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, conta: Conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def registrar(conta: Conta):
        pass

    def __str__(self):
        return str(type(self))

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")

    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data
    
    def registrar(self, conta: Conta):
        transacao_sucedida = conta.depositar(self.valor)
        if transacao_sucedida:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")

    @property
    def valor(self):
        return self._valor
    
    @property
    def data(self):
        return self._data
    
    def registrar(self, conta: Conta):
        transacao_sucedida = conta.sacar(self.valor)
        if transacao_sucedida:
            conta.historico.adicionar_transacao(self)