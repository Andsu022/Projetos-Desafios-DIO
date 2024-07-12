import abc
import datetime

class Autentica(abc.ABC):
    def __init__(self):
        pass

    def autenticar_acesso(self, conta, senha):
        pass

class Extrato(abc.ABC):
    def __init__(self):
        self.lista_operacoes = {}
        self.lista_transferencias = {}

    @abc.abstractmethod
    def extrato_conta(self):
        pass


class Cliente():

    def __init__(self, endereco, cpf, nome, data_nascimento):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._endereco = endereco
        self.lista_clientes = {}


    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    @property
    def endereco(self):
        return self._endereco
    
    def adicionar_cliente(self, nome, cpf, endereco):
        self.lista_clientes.update({cpf:{'Nome': nome, 'Endereço': endereco}})


class Pessoa_Fisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco, cpf, nome, data_nascimento)
        self.lista_clientes.update({self.cpf:{'Nome': self.nome, 'Endereço': self.endereco, 'Data de nascimento': self.data_nascimento}})


    def alterar_cliente(self, cpf):
        menu = '''
            |====SELECIONE A ALTERAÇÃO DESEJADA====|
            | 1 - Alterar Nome                     |
            | 2 - Alterar Endereço                 |    
            |======================================|
            '''
        opc = int(input(menu))
        if opc == 1:
            for chave, valor in self.lista_clientes.items():
                if chave == cpf:
                    novo_nome = input('Digite o nome correto: ')
                    valor['Nome'] = novo_nome
        
        elif opc == 2:
            for chave, valor in self.lista_clientes.items():
                if chave == cpf:
                    novo_endereco = input('Digite o endereço correto: ')
                    valor['Endereço'] = novo_endereco

    def remover_cliente(self, cpf):
        self.lista_clientes.pop(cpf)
    

class Conta(Extrato):
    def __init__(self, numero, nome_cliente, cpf_cliente, senha):
        self._saldo = 0
        self._numero_conta = numero
        self._agencia = '0001'
        self._cliente = nome_cliente
        self._cpf_cliente = cpf_cliente
        self._senha = senha
        self.lista_contas = {}

    @property
    def titular(self):
        return self._cliente
    
    @property
    def numero_conta(self):
        return self._numero_conta
    
    @property
    def cpf(self):
        return self._cpf_cliente
    
    @property
    def saldo_conta(self):
        return self._saldo
    
    @property
    def senha(self):
        return self._senha
    
    @property
    def numero_agencia(self):
        return self._agencia
    
    def adicionar_conta(self, nome, cpf, numero_conta):
        self.lista_contas.update({cpf:{'Titular': nome, 'Número da conta': numero_conta, 'Agência': self._agencia, 'Saldo': self._saldo}})

    def alterar_titular(self, conta, novo_titular):
        for value in self.lista_contas.values():
            if conta == value['Número da conta']:
                self.lista_contas.update({'Número da conta': novo_titular})

    def remover_conta(self, cpf):
        self.lista_contas.pop(cpf)

class Conta_Corrente(Conta, Autentica):
    def __init__(self, numero, cliente, cpf, senha):
        super().__init__(numero, cliente, cpf, senha)
        self.limite_saques_quantidade = 3
        self._limite_saque_valor = 300
        self.limite_deposito = 3000
        self.lista_contas.update({self.cpf:{'Titular': self.titular, 'Número da conta': self.numero_conta, 'Agência': self.numero_agencia, 'Saldo': self.saldo_conta, 'Senha': self.senha}})

    def autenticar_acesso(self, conta, senha):
        for value in self.lista_contas.values():
            if (value['Senha'] == senha) and (value['Número da conta'] == conta):
                return True

        return None

    def sacar(self, conta, valor):
        for valor in self.lista_contas.values():
            if conta == valor['Número da conta']:
                saldo = valor['Saldo']

                if self.limite_saques_quantidade < 3:
                    if saldo >= valor:
                        if valor <= self._limite_saque_valor:
                            for value in self.lista_contas.values():
                                if conta == value['Número da conta']:
                                    value['Saldo da conta'] -= valor
                                    print('Operação realizada com sucesso !!')
                                    self.limite_saques_quantidade += 1
                                    self.lista_operacoes.update({'SAQUE':{'Valor': valor, 'Data': datetime.now().strftime("%d-%m-%Y %H:%M:%s")}})
                
                        else:
                            print('Operação não realizada, limite de valor por saque ultrapassado !')
                
                    else:
                        print('Operação não realizada, saldo insuficiente !')
                
                else:
                    print('Operação não realizada, limite de saques diários ultrapassado !')


    def depositar(self, conta, valor):
        if valor > 0 :
            if valor <= self.limite_deposito:
                for value in self.lista_contas.values():
                    if conta == value['Número da conta']:
                        value['Saldo da conta'] += valor
                        self.lista_operacoes.update({'DEPÓSITO':{'Valor': valor, 'Data': datetime.now().strftime("%d-%m-%Y %H:%M:%s")}})
                        print('Operação realizada com sucesso !!')
            
            else:
                print(f'Operação não realizada, limite de depósito é de R$ {self.limite_deposito}')
        
        else:
            print('Operação não realizada, não é permitido depositar valores negativos !')


    def transferencia(self, valor, conta_origem, conta_destino):
        for value in self.lista_contas.values():
            achado = True if (conta_origem == value['Número da conta']) and (conta_destino == value['Número da conta']) else False
        
        if achado == True:
            for value in self.lista_contas.values():
                saldo_origem = value['Saldo'] if conta_origem == value['Número da conta'] else 0
                saldo_destino = value['Saldo'] if conta_destino == value['Número da conta'] else 0

            saldo_origem -= valor if saldo_origem > valor else 'Erro na transferência'
            saldo_destino += valor if saldo_origem != 'Erro na transferência' else 'Erro'

            if (saldo_origem != 'Erro na transferência') and (saldo_destino != 'Erro'):
                for value in self.lista_contas.values():
                    value['Saldo'] = saldo_origem if conta_origem == value['Número da conta'] else 0
                    value['Saldo'] = saldo_destino if conta_destino == value['Número da conta'] else 0
                
                self.lista_transferencias.update({'TRANSFERÊNCIA':{'Valor': valor, 'Conta Origem': conta_origem, 'Conta destino': conta_destino, 'Data': datetime.now().strftime("%d-%m-%Y %H:%M:%s")}})
                print('Operação realizada com sucesso !!')

            else:
                print('Transferência não realizada !')        
        
        else:
            print('Erro ao procurar contas !')


    def extrato_conta(self):
        for chave, value in self.lista_operacoes.items():
            print(f'OPERAÇÃO:{chave} - VALOR:R${value['Valor']} - DATA:{value['Data']}')
        
        for chave, value in self.lista_transferencias.items():
            print(f'OPERAÇÃO:{chave} - VALOR:R${value['Valor']} - CONTA ORIGEM:{value['Conta origem']} - CONTA DESTINO:{value['Conta destino']} - DATA:{value['Data']}')


def main(): 

    menu_principal = '''
        |=============================|
        | [1] - Criar usuário         |
        | [2] - Criar conta corrente  |
        | [3] - Acessar conta         |
        | [4] - Alterar cliente       |
        | [5] - Alterar conta         |
        | [6] - Finalizar sessão      |
        |=============================|
        |=> '''
    
    menu_conta = '''
        |========CONTA========|
        | [1] - Saque         |
        | [2] - Depósito      |
        | [3] - Transferência |
        | [4] - Extrato       |
        | [5] - Finalizar     |
        |=====================|
        |=> '''
    
    finalizar = '''
        |======FINALIZANDO======|
         '''
    
    erro = '''
        |======ERRO======|
         '''
    
    while True:
        menu1 = int(input(menu_principal))
        match menu1:
            case 1:
                try:
                    nome = input('Digite o nome: ')
                    cpf = input('Digite o CPF: ')
                    data_nascimento = input('Digite a data de nascimento no formato DD/MM/AAAA: ')
                    endereco = input('Digite seu endereço: ')
                    cliente_pessoa_fisica = Pessoa_Fisica(endereco, cpf, nome, data_nascimento)
                    continue
                except:
                    print(erro)
                    continue

            case 2:
                try:
                    nome_cliente = input('Digite o nome do titular da conta: ')
                    cpf_titular = input('Digite o CPF do titular: ')
                    numero_conta = int(input('Digite um número pra conta(começando por 1): '))
                    senha_conta = int(input('Digite uma senha(somente números): '))
                    conta_corrente = Conta_Corrente(numero_conta, nome_cliente, cpf_titular, senha_conta)
                    continue
                except:
                    print(erro)
                    continue
            
            case 3:
                try:
                    numero_conta_acesso = int(input('Digite o número da conta: '))
                    senha_acesso = int(input(('Digite a senha: ')))
                    acesso = conta_corrente.autenticar_acesso(numero_conta_acesso, senha_acesso)
                except:
                    print(erro)
                    continue

                if acesso == True:
                    try:
                        menu2 = int(input(menu_conta))
                        while True:
                            match menu2:
                                case 1:
                                    try:
                                        valor_saque = int(input(('Digite um valor para sacar: ')))
                                        conta_corrente.sacar(numero_conta_acesso, valor_saque)
                                        continue
                                    except:
                                        print(erro)
                                        continue
                                
                                case 2:
                                    try:
                                        valor_deposito = int(input(('Digite um valor para depositar: ')))
                                        conta_corrente.depositar(numero_conta_acesso, valor_deposito)
                                        continue
                                    except:
                                        print(erro)
                                        continue

                                case 3:
                                    try:
                                        valor_transferencia = int(input('Digite um valor para transferir: '))
                                        conta_origem = numero_conta_acesso
                                        conta_destino = int(input('Digite a conta de destino: '))
                                        conta_corrente.transferencia(valor_transferencia, conta_origem, conta_destino)
                                        continue
                                    except:
                                        print(erro)
                                        continue
                                
                                case 4:
                                    conta_corrente.extrato_conta()
                                    continue

                                case 5:
                                    print(finalizar)
                                    break
                                
                                case _:
                                    print(erro)
                                    continue
                    except:
                        print(erro)
                        continue               
            
            case 4:
                opc = '''
                    |====SELECIONE A ALTERAÇÃO DESEJADA====|
                    | 1 - Alterar Dados                    |
                    | 2 - Remover Cliente                  |    
                    |======================================|
                    '''
                while True:

                    menu_alterar = int(input(opc))
                    if menu_alterar == 1:
                        cpf_alterar = input('Digite o cpf para alterar: ')
                        cliente_pessoa_fisica.alterar_cliente(cpf_alterar)
                        continue
                    elif menu_alterar == 2:
                        cpf_remover = input('Digite o cpf para remover: ')
                        cliente_pessoa_fisica.remover_cliente(cpf_remover)
                        continue

            case 5:
                opc = '''
                    |====SELECIONE A ALTERAÇÃO DESEJADA====|
                    | 1 - Alterar Dados                    |
                    | 2 - Remover Conta                    |    
                    |======================================|
                    '''
                
                while True:
                    menu_alterar = int(input(opc))
                    if menu_alterar == 1:
                        conta_alterar = input('Digite o número da conta para alterar: ')
                        novo_titular = input('Digite o nome do novo titular: ')
                        conta_corrente.alterar_titular(conta_alterar, novo_titular)
                        continue
                    elif menu_alterar == 2:
                        conta_remover = input('Digite o número da conta para remover: ')
                        conta_corrente.remover_conta(conta_remover)
                        continue
            
            case 6:
                print(finalizar)
                break

            case _:
                print(erro)
                continue


main()