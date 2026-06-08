"""
Módulo de criptografia assimétrica para o chat seguro.
Implementação RSA pura em Python (sem bibliotecas externas),
utilizando apenas a biblioteca padrão (secrets, random).
Inclui padding PKCS#1 v1.5 e chunking para mensagens longas.
"""

import secrets

# Tamanho da chave RSA em bits
TAMANHO_CHAVE = 1024

# Limite seguro de bytes por chunk para RSA-1024
# Com PKCS#1 v1.5, o máximo teórico é k - 11 = 117 bytes para chave de 1024 bits.
# Usamos 100 bytes por segurança e compatibilidade.
TAMANHO_CHUNK = 100

# Expoente público padrão (valor consagrado na indústria)
E_PADRAO = 65537

# Número de rounds do teste de Miller-Rabin (40 = probabilidade de erro < 2^-80)
ROUNDS_MILLER_RABIN = 40


# =============================================================================
# Classes de chave
# =============================================================================

class PublicKey:
    """Chave pública RSA: (n, e)."""

    def __init__(self, n: int, e: int):
        self.n = n
        self.e = e

    def __repr__(self):
        return f"PublicKey(n={self.n}, e={self.e})"


class PrivateKey:
    """Chave privada RSA: (n, d)."""

    def __init__(self, n: int, d: int):
        self.n = n
        self.d = d

    def __repr__(self):
        return f"PrivateKey(n={self.n}, d=...)"


# =============================================================================
# Funções auxiliares privadas — Aritmética modular
# =============================================================================

def _miller_rabin(n: int, k: int = ROUNDS_MILLER_RABIN) -> bool:
    """
    Teste de primalidade probabilístico de Miller-Rabin.

    Args:
        n: Número ímpar >= 3 a ser testado.
        k: Número de rounds (quanto maior, mais preciso).

    Returns:
        True se n é provavelmente primo, False se composto.
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Escreve n-1 como 2^r * d, com d ímpar
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Executa k rounds
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # a ∈ [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composto = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composto = False
                break
        if composto:
            return False
    return True


def _gerar_primo(bits: int) -> int:
    """
    Gera um número primo aleatório com exatamente 'bits' bits.

    Args:
        bits: Número de bits do primo desejado.

    Returns:
        Inteiro primo de 'bits' bits.
    """
    while True:
        # Gera número aleatório e força MSB=1 (bits exatos) e LSB=1 (ímpar)
        candidato = secrets.randbits(bits)
        candidato |= (1 << (bits - 1)) | 1
        if _miller_rabin(candidato):
            return candidato


def _gcd_extendido(a: int, b: int) -> tuple:
    """
    Algoritmo de Euclides estendido.

    Returns:
        Tupla (gcd, x, y) tal que a*x + b*y = gcd.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = _gcd_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def _inverso_modular(e: int, phi: int) -> int:
    """
    Calcula o inverso modular d = e⁻¹ mod φ.

    Args:
        e: Expoente público.
        phi: φ(n) = (p-1)*(q-1).

    Returns:
        d tal que (e * d) ≡ 1 (mod φ).
    """
    gcd, x, _ = _gcd_extendido(e, phi)
    if gcd != 1:
        raise ValueError(f"e={e} e φ={phi} não são coprimos — impossível calcular inverso.")
    return x % phi


# =============================================================================
# Funções auxiliares privadas — Padding PKCS#1 v1.5
# =============================================================================

def _gerar_bytes_nao_nulos(quantidade: int) -> bytes:
    """
    Gera 'quantidade' bytes aleatórios criptograficamente seguros,
    todos diferentes de zero (exigido pelo PKCS#1 v1.5).

    Args:
        quantidade: Número de bytes não-nulos a gerar.

    Returns:
        Bytes aleatórios não-nulos.
    """
    resultado = bytearray()
    while len(resultado) < quantidade:
        # Gera um lote extra para compensar os zeros descartados
        faltam = quantidade - len(resultado)
        lote = secrets.token_bytes(faltam * 2)
        resultado.extend(b for b in lote if b != 0)
    return bytes(resultado[:quantidade])


def _aplicar_padding_pkcs1(mensagem: bytes, tamanho_chave: int) -> bytes:
    """
    Aplica padding PKCS#1 v1.5 para criptografia.

    Formato: 0x00 || 0x02 || PS || 0x00 || M
    onde PS são bytes aleatórios não-nulos (mínimo 8).

    Args:
        mensagem: Bytes da mensagem a ser paddada.
        tamanho_chave: Tamanho da chave em bytes (k).

    Returns:
        Mensagem com padding, exatamente 'tamanho_chave' bytes.
    """
    if len(mensagem) > tamanho_chave - 11:
        raise ValueError(
            f"Mensagem muito longa para padding: {len(mensagem)} bytes "
            f"(máximo {tamanho_chave - 11} para chave de {tamanho_chave} bytes)"
        )

    ps_len = tamanho_chave - len(mensagem) - 3  # 3 bytes fixos: 0x00, 0x02, 0x00
    ps = _gerar_bytes_nao_nulos(ps_len)
    return b'\x00\x02' + ps + b'\x00' + mensagem


def _remover_padding_pkcs1(dados: bytes) -> bytes:
    """
    Remove padding PKCS#1 v1.5 e retorna a mensagem original.

    Args:
        dados: Bytes com padding (exatamente k bytes).

    Returns:
        Mensagem original sem padding.

    Raises:
        ValueError: Se o padding for malformado.
    """
    if len(dados) < 11:
        raise ValueError("Dados muito curtos para conter padding PKCS#1 v1.5")
    if dados[0] != 0x00 or dados[1] != 0x02:
        raise ValueError(
            f"Padding PKCS#1 v1.5 inválido: esperado 0x00 0x02, "
            f"recebido 0x{dados[0]:02x} 0x{dados[1]:02x}"
        )

    # Encontra o separador 0x00 após os bytes de padding
    sep_idx = dados.find(b'\x00', 2)
    if sep_idx == -1:
        raise ValueError("Padding PKCS#1 v1.5 inválido: separador 0x00 não encontrado")

    # Verifica se há pelo menos 8 bytes de padding (exigido pelo PKCS#1)
    ps_len = sep_idx - 2  # desconta 0x00 e 0x02 iniciais
    if ps_len < 8:
        raise ValueError(
            f"Padding PKCS#1 v1.5 inválido: apenas {ps_len} bytes de padding "
            f"(mínimo 8)"
        )

    return dados[sep_idx + 1:]


# =============================================================================
# Funções auxiliares privadas — Criptografia de chunk único
# =============================================================================

def _criptografar_chunk(chunk: bytes, chave_publica: PublicKey) -> bytes:
    """
    Criptografa um único chunk com a chave pública (inclui padding).

    Args:
        chunk: Bytes da mensagem (<= k-11 bytes).
        chave_publica: Chave pública RSA.

    Returns:
        Chunk criptografado (exatamente k bytes).
    """
    k = (chave_publica.n.bit_length() + 7) // 8  # tamanho da chave em bytes
    padded = _aplicar_padding_pkcs1(chunk, k)
    m = int.from_bytes(padded, 'big')
    c = pow(m, chave_publica.e, chave_publica.n)
    return c.to_bytes(k, 'big')


def _descriptografar_chunk(chunk_criptografado: bytes, chave_privada: PrivateKey) -> bytes:
    """
    Descriptografa um único chunk com a chave privada (remove padding).

    Args:
        chunk_criptografado: Bytes criptografados (exatamente k bytes).
        chave_privada: Chave privada RSA.

    Returns:
        Bytes da mensagem original (sem padding).
    """
    k = (chave_privada.n.bit_length() + 7) // 8
    c = int.from_bytes(chunk_criptografado, 'big')
    m = pow(c, chave_privada.d, chave_privada.n)
    padded = m.to_bytes(k, 'big')
    return _remover_padding_pkcs1(padded)


# =============================================================================
# API Pública (mesma interface do módulo original)
# =============================================================================

def gerar_chaves(tamanho_bits: int = TAMANHO_CHAVE) -> tuple:
    """
    Gera um par de chaves RSA (pública e privada).

    Args:
        tamanho_bits: Tamanho da chave em bits (padrão: 1024).

    Returns:
        Tupla (PublicKey, PrivateKey).
    """
    print(f"[*] Gerando primos de {tamanho_bits // 2} bits cada...")
    meio = tamanho_bits // 2
    p = _gerar_primo(meio)
    q = _gerar_primo(meio)

    # Garante que p ≠ q (extremamente improvável, mas verificamos)
    while p == q:
        q = _gerar_primo(meio)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = E_PADRAO
    d = _inverso_modular(e, phi)

    chave_publica = PublicKey(n, e)
    chave_privada = PrivateKey(n, d)

    return chave_publica, chave_privada


def serializar_chave_publica(chave_publica: PublicKey) -> bytes:
    """
    Serializa uma chave pública RSA para bytes (formato customizado simples).

    Formato: [2 bytes: tamanho_n] [n bytes: n] [2 bytes: tamanho_e] [e bytes: e]

    Args:
        chave_publica: Objeto PublicKey.

    Returns:
        Bytes representando a chave pública.
    """
    n_bytes = chave_publica.n.to_bytes(
        (chave_publica.n.bit_length() + 7) // 8, 'big'
    )
    e_bytes = chave_publica.e.to_bytes(
        (chave_publica.e.bit_length() + 7) // 8, 'big'
    )

    resultado = bytearray()
    resultado.extend(len(n_bytes).to_bytes(2, 'big'))
    resultado.extend(n_bytes)
    resultado.extend(len(e_bytes).to_bytes(2, 'big'))
    resultado.extend(e_bytes)

    return bytes(resultado)


def desserializar_chave_publica(dados: bytes) -> PublicKey:
    """
    Reconstrói uma chave pública RSA a partir de bytes (formato customizado).

    Formato: [2 bytes: tamanho_n] [n bytes: n] [2 bytes: tamanho_e] [e bytes: e]

    Args:
        dados: Bytes no formato customizado.

    Returns:
        Objeto PublicKey reconstruído.
    """
    pos = 0

    # Lê n
    tamanho_n = int.from_bytes(dados[pos:pos + 2], 'big')
    pos += 2
    n = int.from_bytes(dados[pos:pos + tamanho_n], 'big')
    pos += tamanho_n

    # Lê e
    tamanho_e = int.from_bytes(dados[pos:pos + 2], 'big')
    pos += 2
    e = int.from_bytes(dados[pos:pos + tamanho_e], 'big')

    return PublicKey(n, e)


def criptografar_mensagem(mensagem: str, chave_publica: PublicKey) -> bytes:
    """
    Criptografa uma mensagem de texto usando a chave pública do destinatário.
    Utiliza chunking com padding PKCS#1 v1.5 para suportar mensagens longas.

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
        chunk_criptografado = _criptografar_chunk(chunk, chave_publica)
        # Prefixa com 2 bytes indicando o tamanho do chunk criptografado
        tamanho = len(chunk_criptografado)
        resultado.extend(tamanho.to_bytes(2, 'big'))
        resultado.extend(chunk_criptografado)

    return bytes(resultado)


def descriptografar_mensagem(dados_criptografados: bytes, chave_privada: PrivateKey) -> str:
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
        if pos + 2 > len(dados_criptografados):
            raise ValueError("Payload malformado: cabeçalho de chunk incompleto")

        tamanho_chunk = int.from_bytes(
            dados_criptografados[pos:pos + 2], 'big'
        )
        pos += 2

        # Lê o chunk criptografado
        if pos + tamanho_chunk > len(dados_criptografados):
            raise ValueError("Payload malformado: chunk incompleto")

        chunk_criptografado = dados_criptografados[pos:pos + tamanho_chunk]
        pos += tamanho_chunk

        # Descriptografa o chunk
        chunk = _descriptografar_chunk(chunk_criptografado, chave_privada)
        resultado.extend(chunk)

    return bytes(resultado).decode('utf-8')
