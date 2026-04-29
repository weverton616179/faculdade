"""
    Este arquivo tem como objetivo a derivação de chave usando o PBKDF2.
    Ele fornece funções prontas para serem importadas em outros scripts (como AES256.py).
"""
import base64
import os
import hashlib
import hmac
import struct

# gera o salt aleatório
def gerar_salt(tamanho: int = 16):
    return os.urandom(tamanho)

# gera a chave utilizando o pbkdf2 do python
# def derivar_chave(senha: str, salt: bytes, iteracoes: int = 100000, tamanho_chave: int = 32):
#     return hashlib.pbkdf2_hmac(
#         hash_name='sha256',
#         password=senha.encode('utf-8'),
#         salt=salt,
#         iterations=iteracoes,
#         dklen=tamanho_chave
#     )

# gera a chave utilizando o pbkdf2 do zero
def derivar_chave(senha: str, salt: bytes, iteracoes: int = 100000, tamanho_chave: int = 32):
    senha_bytes = senha.encode('utf-8')
    hash_module = hashlib.sha256
    h_len = hash_module().digest_size
    
    l = (tamanho_chave + h_len - 1) // h_len
    
    chave_derivada = bytearray()
    
    for i in range(1, l + 1):
        u_c = hmac.new(senha_bytes, salt + struct.pack(">I", i), hash_module).digest()
        f_block = bytearray(u_c)
        
        for _ in range(1, iteracoes):
            u_c = hmac.new(senha_bytes, u_c, hash_module).digest()
            for j in range(h_len):
                f_block[j] ^= u_c[j]
                
        chave_derivada.extend(f_block)
        
    return bytes(chave_derivada[:tamanho_chave])


def verificar_senha(senha_digitada: str, salt_salvo: bytes, chave_esperada: bytes, iteracoes: int = 100000):
    tamanho_chave = len(chave_esperada)
    chave_tentativa = derivar_chave(senha_digitada, salt_salvo, iteracoes, tamanho_chave)
    return hmac.compare_digest(chave_tentativa, chave_esperada)


def gerar_hash_com_salt(senha: str, iteracoes: int = 100000) -> str:
    salt = gerar_salt(16)
    chave_aes = derivar_chave(senha, salt, iteracoes, 32)
    
    string_para_salvar = f"{salt.hex()}:{iteracoes}:{chave_aes.hex()}"
    string_para_salvar = base64.StringToBase64(string_para_salvar)
    return chave_aes, string_para_salvar


def verificar_hash_com_salt(senha_digitada: str, string_salva: str) -> bool:
    try:
        # Separa a string nos 3 pedaços usando o ":"
        string_salva = base64.Base64ToString(string_salva)
        salt_hex, iteracoes_str, chave_esperada_hex = string_salva.split(':')
        
        salt = bytes.fromhex(salt_hex)
        iteracoes = int(iteracoes_str)
        chave_esperada = bytes.fromhex(chave_esperada_hex)
        
        return verificar_senha(senha_digitada, salt, chave_esperada, iteracoes)
    except Exception:
        return False

if __name__ == "__main__":
    # Exemplo prático de como utilizar o arquivo (como seria em seu AES256.py)
    
    print("--- Teste de Derivação de Chave PBKDF2 ---")
    minha_senha = "minha_senha_super_secreta"
    
    chave_aes, string_salva = gerar_hash_com_salt(minha_senha)
    print(f"String gerada: {string_salva}")
    print(f"Chave AES gerada: {chave_aes.hex()}")
    print(f"Chave AES gerada: {chave_aes}")
    print(f"Verificando senha: {verificar_hash_com_salt('senha_errada', string_salva)}")
    print(f"Verificando senha: {verificar_hash_com_salt(minha_senha, string_salva)}")