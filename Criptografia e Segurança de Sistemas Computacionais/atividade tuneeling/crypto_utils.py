"""
Módulo de criptografia assimétrica para o chat seguro.
Utiliza RSA (biblioteca rsa) com chaves de 1024 bits e chunking
para suportar mensagens maiores que o limite do RSA.
"""

import rsa

# Tamanho da chave RSA em bits
TAMANHO_CHAVE = 1024

# Limite seguro de bytes por chunk para RSA-1024 (máximo teórico: 117 bytes)
TAMANHO_CHUNK = 100


def gerar_chaves(tamanho_bits: int = TAMANHO_CHAVE) -> tuple:
    """
    Gera um par de chaves RSA (pública e privada).

    Args:
        tamanho_bits: Tamanho da chave em bits (padrão: 1024).

    Returns:
        Tupla (chave_publica, chave_privada).
    """
    chave_publica, chave_privada = rsa.newkeys(tamanho_bits)
    return chave_publica, chave_privada


def serializar_chave_publica(chave_publica: rsa.PublicKey) -> bytes:
    """
    Serializa uma chave pública RSA para bytes (formato PKCS1).

    Args:
        chave_publica: Objeto rsa.PublicKey.

    Returns:
        Bytes representando a chave pública no formato PKCS1.
    """
    return chave_publica.save_pkcs1()


def desserializar_chave_publica(dados: bytes) -> rsa.PublicKey:
    """
    Reconstrói uma chave pública RSA a partir de bytes PKCS1.

    Args:
        dados: Bytes no formato PKCS1.

    Returns:
        Objeto rsa.PublicKey reconstruído.
    """
    return rsa.PublicKey.load_pkcs1(dados)


def criptografar_mensagem(mensagem: str, chave_publica: rsa.PublicKey) -> bytes:
    """
    Criptografa uma mensagem de texto usando a chave pública do destinatário.
    Utiliza chunking para suportar mensagens longas.

    Formato do payload: [2 bytes: tamanho_chunk] [chunk_criptografado] ...

    Args:
        mensagem: Texto a ser criptografado.
        chave_publica: Chave pública RSA do destinatário.

    Returns:
        Bytes do payload criptografado (com cabeçalhos de chunk).
    """
    dados = mensagem.encode('utf-8')
    resultado = bytearray()

    for i in range(0, len(dados), TAMANHO_CHUNK):
        chunk = dados[i:i + TAMANHO_CHUNK]
        chunk_criptografado = rsa.encrypt(chunk, chave_publica)
        # Prefixa com 2 bytes indicando o tamanho do chunk criptografado
        tamanho = len(chunk_criptografado)
        resultado.extend(tamanho.to_bytes(2, byteorder='big'))
        resultado.extend(chunk_criptografado)

    return bytes(resultado)


def descriptografar_mensagem(dados_criptografados: bytes, chave_privada: rsa.PrivateKey) -> str:
    """
    Descriptografa um payload criptografado usando a chave privada.

    Formato do payload: [2 bytes: tamanho_chunk] [chunk_criptografado] ...

    Args:
        dados_criptografados: Bytes no formato de chunking.
        chave_privada: Chave privada RSA do destinatário.

    Returns:
        Texto original descriptografado.
    """
    resultado = bytearray()
    pos = 0

    while pos < len(dados_criptografados):
        # Lê o tamanho do chunk (2 bytes big-endian)
        tamanho_chunk = int.from_bytes(dados_criptografados[pos:pos + 2], byteorder='big')
        pos += 2

        # Lê o chunk criptografado
        chunk_criptografado = dados_criptografados[pos:pos + tamanho_chunk]
        pos += tamanho_chunk

        # Descriptografa o chunk
        chunk = rsa.decrypt(chunk_criptografado, chave_privada)
        resultado.extend(chunk)

    return bytes(resultado).decode('utf-8')
