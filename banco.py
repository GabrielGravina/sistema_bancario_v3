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
    
class Conta:
    def __init__(self, nro_agencia, cliente, saldo = 0):
        self._saldo = saldo
        self.nro_agencia = nro_agencia
        self.cliente = cliente

    def depositar(self, valor):
        self._saldo += valor

    def sacar(self, valor):
        if valor<=self._saldo:
            self._saldo -= valor

    @property
    def get_saldo(self):
        return self._saldo
    
    def get_cliente(self):
        return self.cliente
        

cliente01 = Cliente('Gabriel', '123.456.789-01')
cliente02 = Cliente('Juca', '987.654.321-98')
print(Cliente.show_clients())


conta01 = Conta("0001", cliente01)
# conta.depositar(1320)
# print(conta.nro_agencia)
print(conta01.get_saldo)

# print(cliente01)
# print(conta.get_cliente())
