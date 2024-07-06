from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    all_clientes = []

    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        Cliente.all_clientes.append(self)

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave} = {valor}' for chave, valor in self.__dict__.items()])}"

    @classmethod
    def show_clients(cls):
        return "\n".join([str(cliente) for cliente in cls.all_clientes])

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now()
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.sacar(self.valor)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf):
        super().__init__(nome, cpf)

class Conta:
    all_contas = []

    def __init__(self, nro_agencia, cliente, saldo=0):
        self._saldo = saldo
        self.nro_agencia = nro_agencia
        self._cliente = cliente
        self.historico = Historico()
        Conta.all_contas.append(self)

    @classmethod
    def nova_conta(cls, cliente, nro_agencia, saldo_inicial=0):
        return cls(nro_agencia, cliente, saldo_inicial)

    def depositar(self, valor):
        self._saldo += valor
        self.historico.adicionar_transacao(Deposito(valor))

    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            return True
        else:
            return False

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    @property
    def cliente(self):
        return str(self._cliente)

    def get_cliente(self):
        return self.cliente

    def __str__(self):
        return f"Conta: Agência {self.nro_agencia}, Cliente: {self.cliente}, Saldo: {self.saldo}"

class ContaCorrente(Conta):
    def __init__(self, nro_agencia, cliente, saldo=0, limite=1000, limite_saques=9999):
        super().__init__(nro_agencia, cliente, saldo)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            raise ValueError("Limite de saques excedido")
        if valor <= self.saldo + self.limite:
            self.saldo -= valor
            self.saques_realizados += 1
            self.limite -= valor
            self.historico.adicionar_transacao(Saque(valor))
            return True
        else:
            return False

def encontrar_cliente_por_cpf(cpf):
    for cliente in Cliente.all_clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def encontrar_conta_por_cliente(cliente):
    for conta in Conta.all_contas:
        if conta._cliente == cliente:
            return conta
    return None

def menu():
    while True:
        print("=== Menu ===")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Exibir Extrato")
        print("4. Criar Cliente")
        print("5. Criar Conta")
        print("6. Listar Contas")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cpf = input("Digite o CPF do cliente: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if cliente:
                conta = encontrar_conta_por_cliente(cliente)
                if conta:
                    valor = float(input("Digite o valor para depósito: "))
                    conta.depositar(valor)
                    print("Depósito realizado com sucesso.")
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '2':
            cpf = input("Digite o CPF do cliente: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if cliente:
                conta = encontrar_conta_por_cliente(cliente)
                if conta:
                    valor = float(input("Digite o valor para saque: "))
                    if conta.sacar(valor):
                        print("Saque realizado com sucesso.")
                    else:
                        print("Não foi possível realizar o saque.")
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '3':
            cpf = input("Digite o CPF do cliente: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if cliente:
                conta = encontrar_conta_por_cliente(cliente)
                if conta:
                    conta.historico.transacoes
                    for transacao in conta.historico.transacoes:
                        print(f"Tipo: {transacao['tipo']}, Valor: {transacao['valor']}, Data: {transacao['data']}")
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '4':
            nome = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF do cliente: ")
            cliente = Cliente(nome, cpf)
            print(f"Cliente {nome} criado com sucesso.")
        elif opcao == '5':
            cpf = input("Digite o CPF do cliente: ")
            cliente = encontrar_cliente_por_cpf(cpf)
            if cliente:
                nro_agencia = input("Digite o número da agência: ")
                saldo_inicial = float(input("Digite o saldo inicial: "))
                conta = ContaCorrente.nova_conta(cliente, nro_agencia, saldo_inicial)
                print("Conta criada com sucesso.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '6':
            for conta in Conta.all_contas:
                print(conta)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
