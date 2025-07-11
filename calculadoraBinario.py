import os

from unicodedata import decimal


def converte_to_binary(n, tamRepresentacao):
    if tamRepresentacao not in [8,16,32]:
        raise ValueError("O numero de bits deve ser de 8, 16 e 32 bits")

    if not isinstance(n, int):
        raise ValueError("A entrada tem que ser um inteiro")
    if n < 0:
        binary = bin(abs(n))[2:].zfill(tamRepresentacao)
        #inverte todos os bits
        binary = ''.join(['1' if bit == '0' else '0' for bit in binary])
        binary_int = int(binary,2) + 1
        binary = bin(binary_int)[2:].zfill(tamRepresentacao)
        return binary
    else:
        binary = bin(n)[2:]
        if len(binary) > tamRepresentacao:
            return "Overflow"
        return binary.zfill(tamRepresentacao)

def binary_sum(number_one, number_two):
    max_len = max(len(number_one), len(number_two))
    number_one = number_one.zfill(max_len)
    number_two = number_two.zfill(max_len)
    result = ''
    carry = 0

    for i in range(max_len - 1, -1, -1):
        r = carry
        r+= 1 if number_one[i] == '1' else 0
        r+= 1 if number_two[i] == '1' else 0
        result = ('1' if r %2 == 1 else '0') + result

        carry = 0 if r < 2 else 1
    if carry != 0:
        result = '1' + result
    return result[-max_len:]
    #complexidade O(n)

def twoComplement(binary):
    invertido = ''.join('1' if bit == '0' else '0' for bit in binary)
    vai_um = binary_sum(invertido, '1'.zfill(len(binary)))
    return vai_um


def binarySubtraction(number_one, number_two):
    number_one, number_two = normalizarStrings(number_one, number_two)
    n = len(number_one)
    b_invertido = ''.join('1' if bit == '0' else '0' for bit in number_two)

    b_complemento = binary_sum(b_invertido, '0' * (n - 1) + '1')
    resultado = binary_sum(number_one, b_complemento)
    return resultado[-n:]

def normalizarStrings(number_one, number_two):
    diff = abs((len(number_one) - len(number_two)))
    if len(number_one) < len(number_two):
        number_one = '0' * diff + number_one
    else:
        number_two = '0' * diff + number_two
    return [number_one, number_two]

def convert_to_decimal(binary):
    if binary[0] == '0':
        return int(binary,2)
    else:
        inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
        decimal_value = int(inverted,2) + 1
        return -decimal_value

def shift_esquerda(number, LSB):
    MSB = number[0]
    number = number[1:] + LSB
    return number, MSB

def add_division(A, M):
    result = format(int(A, 2) + int(M,2), 'b')
    return result[len(result)-len(A):]

def DivisionAlgorithm(Q, M, tamRepresentacao):
    A = '0' * tamRepresentacao

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"A": ^{tamRepresentacao}} {"Q": ^{tamRepresentacao}} {"M": ^{tamRepresentacao}}\n')
    print(A, Q, M, ' Valores Iniciais\n')

    for i in range(tamRepresentacao):
        Q, MSB = shift_esquerda(Q, '0')
        A, _ = shift_esquerda(A, MSB)

        print(A, Q, M, ' Shift left A, Q            ─┐')

        A = binarySubtraction(A, M)  # A <- A - M
        print(A, Q, M, ' A <- A - M', f'                 ├── Ciclo {i+1}')

        if A[0] == '1':
            Q = Q[:-1] + '0'
            A = binary_sum(A, M)  # Restore A
            print(A, Q, M, '  Restore A, Set Q[0] = 0   ─┘')
        else:
            Q = Q[:-1] + '1'
            print(A, Q, M, ' Set Q[0] = 1               ─┘')

        print('')

    return Q, A


def main():
    op = 1
    total = 0
    print('Entre com o tamanho da representacao do inteiro : 8 bits | 16 bits | 32 bits')
    tamRepresentacao = int(input())

    if tamRepresentacao == 8 or tamRepresentacao == 16 or tamRepresentacao == 32:
        while (op != 0):
            print('Entre com o primeiro numero: ')
            number_one = int(input())
            print('Entre com o segundo numero: ')
            number_two = int(input())

            number_one_binary = (converte_to_binary(number_one, tamRepresentacao))
            number_two_binary = (converte_to_binary(number_two, tamRepresentacao))

            print(
                'Entre com a operação desejada: \n(+) SOMA | \n(-) SUBTRAÇÃO | \n(*) - MULTIPLICAÇÃO | \n(/) DIVISAO ')
            operador = input()

            if (operador == '+'):
                total = binary_sum(number_one_binary, number_two_binary)
                result = convert_to_decimal(total)
                print(
                    f'Resultado da soma de: {number_one_binary} : ({number_one})  + , {number_two_binary} : ({number_two})  = ',
                    total, result)

            elif (operador == '-'):
                total = binarySubtraction(number_one_binary, number_two_binary)
                result = convert_to_decimal(total)
                print(
                    f'Resultado da subtração de: {number_one_binary} : ({number_one})  + , {number_two_binary} : ({number_two})  = {total} : {result}')
            elif (operador == '/'):
                Quociente, Resto_A = DivisionAlgorithm(number_one_binary, number_two_binary, tamRepresentacao)
                result = convert_to_decimal(Quociente)
                print(f'Resultado da divisão de : {number_one_binary} : ({number_one}) + {number_two_binary} : ({number_two}) = {result}')
                Decimal_A = convert_to_decimal(Resto_A)
                print(f'Quociente : {Quociente} e Resto de A: {Resto_A} : {Decimal_A}')

            print('Continuar com a operação: 0 - Não | 1 - Sim')
            op = int(input())
    else:
        print('O tamanho da Representação deve ser de 8, 16 ou 32 bits')



main()