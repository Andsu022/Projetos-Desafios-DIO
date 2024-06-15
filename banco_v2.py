import os
extrato_depositos = []
extrato_saques = []
quantidade_saques = 0
LIMITE_SAQUES = 300
LIMITE_DEPOSITO = 3000
NUMERO_AGENCIA = '0001'
clientes = {}
conta_corrente = {}

def autenticar_acesso(numero_conta, senha_conta):
    for valor in conta_corrente.values():
        if (numero_conta == valor['Número da conta']) and (senha_conta == valor['Senha']):
            return True


    return None


def criar_usuario(nome, cpf, data_nascimento, rua, numero_casa, bairro, cidade, estado):
    if len(clientes) == 0:
        clientes.update({cpf:{'Nome': nome, 'Data de nascimento': data_nascimento, 'Rua': rua, 'Número': numero_casa, 'Bairro': bairro, 'Cidade': cidade, 'Estado': estado}})
    else:
        for chave in clientes.keys():
            if cpf == chave:
                print('\nCPF já cadastrado !!!')
                break
            else:
                clientes.update({cpf:{'Nome': nome, 'Data de nascimento': data_nascimento, 'Rua': rua, 'Número': numero_casa, 'Bairro': bairro, 'Cidade': cidade, 'Estado': estado}})



def criar_conta_corrente(numero_cpf, numero_conta, saldo, senha):
    global NUMERO_AGENCIA
    for chave, valor in clientes.items():
        if numero_cpf == chave:
            titular = valor['Nome']


    conta_corrente.update({numero_cpf: {'Número da conta': numero_conta,'Agência': NUMERO_AGENCIA, 'Titular': titular, 'Saldo da conta': saldo, 'Senha': senha}})


def saque_conta(valor, numero_conta):
    global quantidade_saques
    global LIMITE_SAQUES

    for value in conta_corrente.values():
        if numero_conta == value['Número da conta']:
            saldo = value['Saldo da conta']
    

    if quantidade_saques < 3:
        if saldo >= valor:
            if valor <= LIMITE_SAQUES:
                for value in conta_corrente.values():
                    if numero_conta == value['Número da conta']:
                        value['Saldo da conta'] -= valor
                print('Operação realizada com sucesso !!')
                quantidade_saques += 1
                extrato_saques.append(valor)

            else:
                print('Operação não realizada, limite de valor por saque ultrapassado !')
        else:
            print('Operação não realizada, saldo insuficiente !')
    else:
        print('Operação não realizada, limite de saques diários ultrapassado !')



def deposito_conta(vl, num_conta):
    global LIMITE_DEPOSITO

    if vl > 0 :
        if vl <= LIMITE_DEPOSITO:
            for value in conta_corrente.values():
                    if num_conta == value['Número da conta']:
                        value['Saldo da conta'] += vl
            
            extrato_depositos.append(vl)
            print('Operação realizada com sucesso !!')
        else:
            print(f'Operação não realizada, limite de depósito é de R$ {LIMITE_DEPOSITO}')
    else:
        print('Operação não realizada, não é permitido depositar valores negativos !')


def extrato_conta(num_conta):
    print('|======EXTRATO SAQUES======|')
    if len(extrato_saques) == 0:
        print('| Nenhum saque foi efetuado !')
    else:
        for i in extrato_saques:
            print(f'|Valor: R$ -{i:.2f}')
            

    print('|======EXTRATO DEPÓSITOS======|')
    if len(extrato_depositos) == 0:
        print('| Nenhum depósito foi efetuado !')
    else:
        for j in extrato_depositos:
            print(f'|Valor: R$ +{j:.2f}')

    print('|==================================')

    for value in conta_corrente.values():
            if num_conta == value['Número da conta']:
               saldo = value['Saldo da conta'] 

    print(f'| Saldo atual da conta: R$ {saldo:.2f}') 



def main(): 

    menu_principal = '''
        |============================|
        | [1] - Criar usuário        |
        | [2] - Criar conta corrente |
        | [3] - Acessar conta        |
        | [4] - Finalizar sessão     |
        |============================|
        |=> '''
    
    menu_conta = '''
        |======CONTA======|
        |                 |
        | [1] - Saque     |
        | [2] - Depósito  |
        | [3] - Extrato   |
        | [4] - Finalizar |
        |=================|
        |=> '''
    
    finalizar = '''
        |======FINALIZANDO======|
         '''
    
    erro = '''
        |======ERRO======|
         '''

    while True:
        try:
            opc1 = int(input(menu_principal))
            match opc1:

                case 1:
                    try:
                        nome = input('\nDigite o nome completo: ')
                        cpf = input('\nDigite o CPF: ')
                        data_nascimento = input('\nDigite sua data de nascimento no formato DD/MM/AAAA: ')
                        rua = input('\nDigite seu endereco(rua): ')
                        numero_casa = int(input('\nDigite seu endereco(numero da casa): '))
                        bairro = input('\nDigite seu endereco(bairro): ')
                        cidade = input('\nDigite seu endereco(cidade): ')
                        estado = input('\nDigite seu endereco(sigla estado): ')
                        criar_usuario(nome, cpf, data_nascimento, rua, numero_casa, bairro, cidade, estado)
                        os.system('pause')
                        os.system('cls')
                        continue
                    except:
                        print(erro)
                        continue

                case 2:
                    try:
                        numero_cpf = input('\nDigite o CPF: ')
                        numero_conta = int(input('\nDigite o número da conta(começando com 1): '))
                        saldo = float(input('\nDigite um valor inicial para o saldo da conta: '))
                        senha = int(input('\nDigite uma senha para a conta(somente números): '))
                        criar_conta_corrente(numero_cpf, numero_conta, saldo, senha)
                        os.system('pause')
                        os.system('cls')
                        continue
                    except:
                        print(erro)
                        continue
                
                case 3:
                    try:
                        num_conta = int(input('\nDigite o número da conta: '))
                        senha_conta = int(input('\nDigite a senha: '))
                        acesso = autenticar_acesso(num_conta, senha_conta)
                        os.system('pause')
                        os.system('cls')
                    except:
                        print(erro)
                    
                    if acesso == True:
                        while True:
                            try:
                                opc2 = int(input(menu_conta))
                                match opc2:

                                    case 1:
                                        vl = float(input('Digite um valor para sacar: '))
                                        saque_conta(valor = vl, numero_conta = num_conta)
                                        os.system('pause')
                                        os.system('cls')
                                        continue

                                    case 2:
                                        vl = float(input('Digite um valor para depositar: '))
                                        deposito_conta(vl, num_conta)
                                        os.system('pause')
                                        os.system('cls')
                                        continue

                                    case 3:
                                        extrato_conta(num_conta)
                                        os.system('pause')
                                        os.system('cls')
                                        continue
                                    
                                    case 4:
                                        print(finalizar)
                                        break

                                    case _:
                                        print('Opção inválida, escolha novamente uma operação !')
                                        os.system('pause')
                                        os.system('cls')
                                        continue
                            except:
                                os.system('cls')
                                print(erro)
                                os.system('pause')
                                os.system('cls')
                                
                    else:
                        print('''
                            |==CONTA NÃO ENCONTRADA !==|
                            ''')
                    
                    continue
                
                case 4:
                    print(finalizar)
                    os.system('exit')
                    break

                case _:
                    print('Opção inválida, escolha novamente uma operação !')
                    os.system('pause')
                    os.system('cls')
                    continue
        except:
            os.system('cls')
            print(erro)
            os.system('pause')
            os.system('cls')


main()