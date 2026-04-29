import sys
import os
import getpass
from PBKDF2 import derivar_chave
from AES256 import aes256_cbc_encrypt, aes256_cbc_decrypt, AES256

def cifrar(arquivo: str):
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return

    senha = getpass.getpass("Digite a senha para cifrar: ")
    confirmacao = getpass.getpass("Confirme a senha: ")
    
    if senha != confirmacao:
        print("Erro: As senhas não coincidem.")
        return

    # Lê o conteúdo do arquivo
    with open(arquivo, 'rb') as f:
        plaintext = f.read()

    # Gera Salt e IV
    salt = os.urandom(16)
    iv = os.urandom(16)

    print("Derivando a chave... (isso pode levar alguns instantes)")
    chave = derivar_chave(senha, salt, 100000, 32)

    print("Cifrando o arquivo...")
    ciphertext = aes256_cbc_encrypt(chave, iv, plaintext)

    # Salva no formato: [salt(16)] + [IV(16)] + [ciphertext]
    arquivo_saida = arquivo + ".cifrado"
    with open(arquivo_saida, 'wb') as f:
        f.write(salt)
        f.write(iv)
        f.write(ciphertext)

    print(f"Sucesso! Arquivo cifrado salvo em: {arquivo_saida}")


def decifrar(arquivo: str):
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return

    senha = getpass.getpass("Digite a senha para decifrar: ")

    # Lê o arquivo cifrado
    with open(arquivo, 'rb') as f:
        conteudo = f.read()

    if len(conteudo) < 32:
        print("Erro: O arquivo cifrado é inválido ou está corrompido (muito pequeno).")
        return

    # Extrai o Salt, IV e o Ciphertext
    salt = conteudo[:16]
    iv = conteudo[16:32]
    ciphertext = conteudo[32:]

    print("Derivando a chave... (isso pode levar alguns instantes)")
    chave = derivar_chave(senha, salt, 100000, 32)

    print("Decifrando o arquivo...")
    try:
        plaintext = aes256_cbc_decrypt(chave, iv, ciphertext)
        print("\n--- CONTEÚDO DECIFRADO ---")
        
        try:
            print(plaintext.decode('utf-8'))
        except UnicodeDecodeError:
            print("[O conteúdo não é texto UTF-8 válido. Exibindo representação hexadecimal]")
            print(plaintext.hex())
            
        print("--------------------------\n")
        
        # Salva o arquivo decifrado
        if arquivo.endswith(".cifrado"):
            arquivo_saida = arquivo[:-8] + ".decifrado"
        else:
            arquivo_saida = arquivo + ".decifrado"
            
        with open(arquivo_saida, 'wb') as f:
            f.write(plaintext)
        print(f"Cópia do arquivo decifrado salva em: {arquivo_saida}")
        
    except Exception as e:
        print(f"Erro durante a decifragem: {e}")
        print("A senha pode estar incorreta ou o arquivo corrompido.")


def testar():
    print("Executando teste com vetor do NIST (SP 800-38A, F.2.5 CBC-AES256.Encrypt)...")
    
    # NIST SP 800-38A F.2.5
    key = bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")
    iv = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    
    plaintext = bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
        "ae2d8a571e03ac9c9eb76fac45af8e51"
        "30c81c46a35ce411e5fbc1191a0a52ef"
        "f69f2445df4f9b17ad2b417be66c3710"
    )
    
    expected_ciphertext = bytes.fromhex(
        "f58c4c04d6e5f1ba779eabfb5f7bfbd6"
        "9cfc4e967edb808d679f777bc6702c7d"
        "39f23369a9d9bacfa530e26304231461"
        "b2eb05e2c39be9fcda6c19078c6a9d1b"
    )
    
    # Testa o encadeamento dos blocos diretamente sem padding, pois o vetor do NIST é múltiplo de 16
    cipher = AES256(key)
    ciphertext_result = bytearray()
    prev_block = iv
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        xored = bytes(a ^ b for a, b in zip(block, prev_block))
        enc_block = cipher.encrypt_block(xored)
        ciphertext_result.extend(enc_block)
        prev_block = enc_block

    if bytes(ciphertext_result) == expected_ciphertext:
        print("Teste de Cifragem CBC-AES256: SUCESSO")
    else:
        print("Teste de Cifragem CBC-AES256: FALHA")
        print("Esperado:", expected_ciphertext.hex())
        print("Obtido:  ", bytes(ciphertext_result).hex())
        
    # Testar decifragem
    plaintext_result = bytearray()
    prev_block = iv
    for i in range(0, len(expected_ciphertext), 16):
        block = expected_ciphertext[i:i+16]
        dec_block = cipher.decrypt_block(block)
        xored = bytes(a ^ b for a, b in zip(dec_block, prev_block))
        plaintext_result.extend(xored)
        prev_block = block
        
    if bytes(plaintext_result) == plaintext:
        print("Teste de Decifragem CBC-AES256: SUCESSO")
    else:
        print("Teste de Decifragem CBC-AES256: FALHA")

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python cofre.py cifrar <arquivo>")
        print("  python cofre.py decifrar <arquivo.cifrado>")
        print("  python cofre.py testar")
        sys.exit(1)

    comando = sys.argv[1].lower()

    if comando == "cifrar":
        if len(sys.argv) < 3:
            print("Erro: Especifique o arquivo para cifrar.")
            sys.exit(1)
        cifrar(sys.argv[2])
    elif comando == "decifrar":
        if len(sys.argv) < 3:
            print("Erro: Especifique o arquivo cifrado para decifrar.")
            sys.exit(1)
        decifrar(sys.argv[2])
    elif comando == "testar":
        testar()
    else:
        print(f"Comando desconhecido: {comando}")

if __name__ == "__main__":
    main()
