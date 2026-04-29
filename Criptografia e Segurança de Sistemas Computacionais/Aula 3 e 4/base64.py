"""
    Este arquivo tem como objetivo a codificação e decodificação de strings para base64
    Feita manualmente sem o uso de bibliotecas prontas
"""
# tabela base64
base64Table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def StringToBase64(string):
    binaryArray = []
    
    # transforma a string em uma array de binarios de 8 bits
    for i, letra in enumerate(string):
        letraBinario = format(ord(letra), '08b')
        binaryArray.append(letraBinario)
    
    # une a array de binarios em uma string
    # divide a string de binarios em grupos de 6 bits
    # se o ultimo grupo de 6 bits nao tiver 6 bits, adiciona zeros no final
    binaryString = "".join(binaryArray)
    sixBitString = [binaryString[i:i+6] for i in range(0, len(binaryString), 6)]
    if len(sixBitString[-1]) < 6: sixBitString[-1] = sixBitString[-1].ljust(6, '0')
    
    base64String = ""
    
    # transforma os grupos de 6 bits em caracteres base64
    for i in sixBitString: base64String += base64Table[int(i, 2)]
    
    return base64String

def Base64ToString(string):
    sixBitArray = []
    for letra in string:
        posicao = base64Table.find(letra)
        sixBitArray.append(format(posicao, '06b'))
        
    sixBitString = "".join(sixBitArray)
    eightBitArray = [sixBitString[i:i+8] for i in range(0, len(sixBitString), 8)]
    if len(eightBitArray[-1]) < 8: del eightBitArray[-1]
    
    texto = ""
    for i in eightBitArray: texto += chr(int(i, 2))
    return texto

if __name__ == "__main__":
    texto = 'meu cavalo albanês'
    base64 = StringToBase64(StringToBase64(StringToBase64(StringToBase64(texto))))
    print(base64)

    resposta = Base64ToString(Base64ToString(Base64ToString(Base64ToString(base64))))
    print(resposta)
    # print(Base64ToString(base64))
    # print(Base64ToString(base64_2))
    # print(Base64ToString(base64_3))
    # print(Base64ToString(base64_4))