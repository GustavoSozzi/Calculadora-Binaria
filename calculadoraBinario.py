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


def binarySubstraction(number_one, number_two):
    def binarySubstraction(number_one, number_two):
        if len(number_one) == 0: return
        if len(number_two) == 0: return

        number_one, number_two = normalizarStrings(number_one, number_two)
        IdxStart = 0
        EndIndex = len(number_one) - 1
        carry = [0] * len(number_one)
        result = ''

        while EndIndex >= IdxStart:
            x = int(number_one[EndIndex])
            y = int(number_two[EndIndex])
            sub = (carry[EndIndex] + x) - y

            if sub == -1:
                result += '1'
                carry[EndIndex] = -1
            elif sub == 1:
                result += '1'
            elif sub == 0:
                result += '0'
            else:
                raise Exception('Error')

            EndIndex -= 1
        return result[::-1]

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

def main():
    op = 1
    total = 0
    print('Entre com o tamanho da representacao do inteiro')
    tamRepresentacao = int(input())

    while(op!=0):
        print('Entre com o primeiro numero: ')
        number_one = int(input())
        print('Entre com o segundo numero: ')
        number_two = int(input())

        number_one_binary = (converte_to_binary(number_one, tamRepresentacao))
        number_two_binary = (converte_to_binary(number_two, tamRepresentacao))

        print('Entre com a operação desejada: \n(+) SOMA | \n(-) SUBTRAÇÃO | \n(*) - MULTIPLICAÇÃO | \n (/) DIVISAO ')
        operador = input()

        if(operador == '+'):
            total = binary_sum(number_one_binary, number_two_binary)
            result = convert_to_decimal(total)
            print(f'Resultado da soma de: {number_one_binary} : ({number_one})  + , {number_two_binary} : ({number_two})  = ', result)

        elif(operador == '-'):
            total = binarySubstraction(number_one_binary, number_two_binary)
            result = convert_to_decimal(total)
            print(f'Resultado da subtração de: {number_one_binary} : ({number_one})  + , {number_two_binary} : ({number_two})  = ',total ,result)

        print('Continuar com a operação: 0 - Não | 1 - Sim')
        op = int(input())

main()