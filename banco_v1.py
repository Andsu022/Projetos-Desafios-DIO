extrato_depositos = []
extrato_saques = []
quantidade_saques = 0

def saque_conta(saldo, valor):
    global quantidade_saques
    LIMITE_SAQUES  = 500

    if quantidade_saques < 3:
        if saldo >= valor:
            if valor <= LIMITE_SAQUES:
                saldo -= valor
                print('Operação realizada com sucesso !!')
                quantidade_saques += 1
                extrato_saques.append(valor)
            else:
                print('Operação não realizada, limite de valor por saque ultrapassado !')
        else:
            print('Operação não realizada, saldo insuficiente !')
    else:
        print('Operação não realizada, limite de saques diários ultrapassado !')

    return saldo


def deposito_conta(saldo, valor):
    if valor > 0:
        saldo += valor
        extrato_depositos.append(valor)
        print('Operação realizada com sucesso !!')
    else:
        print('Operação não realizada, não é permitido depositar valores negativos !')
    
    return saldo


def extrato_conta(saldo):
    print('|======EXTRATO SAQUES======|')
    for i in extrato_saques:
        print(f'|Valor: R$ {i:.2f}')
            

    print('|======EXTRATO DEPÓSITOS======|')
    for j in extrato_depositos:
        print(f'|Valor: R$ {j:.2f}')

    print('|==================================')
    print(f'|Saldo atual da conta: R$ {saldo:.2f}') 



def main():
    saldo = 0

    menu = '''
        |======MENU======|
        |                |
        | [1] - Saque    |
        | [2] - Depósito |
        | [3] - Extrato  |
        | [4] - Sair     |
        |================|
        |=> '''
    
    finalizar = '''
        |======FINALIZANDO======|
         '''
    

    while True:

        opc = int(input(menu))

        if opc == 4:
            print(finalizar)
            break

        elif opc == 1:
            if saldo == 0:
                print('Operação não permitida, saldo zerado, por favor faça um depósito !')
            else:
                valor = float(input('Digite uma valor para sacar: '))
                saldo = saque_conta(saldo, valor)
            continue

        elif opc == 2:
                valor = float(input('Digite uma valor para depositar: '))
                saldo = deposito_conta(saldo, valor)
                continue

        elif opc == 3:
            extrato_conta(saldo)
            continue

        else:
            print('Opção inválida, escolha novamente uma operação !')
            continue




main()