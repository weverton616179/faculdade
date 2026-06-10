"""
Implementação do Algoritmo SHA-256 do Zero (para fins didáticos)
Este arquivo contém a classe SHA256 que implementa o algoritmo de hash SHA-256
seguindo a especificação NIST FIPS 180-4, usando apenas a biblioteca padrão do Python.

Uso:
    from sha256 import SHA256
    hash_obj = SHA256()
    hash_obj.update(b"abc")
    resultado = hash_obj.hexdigest()  # string hexadecimal de 64 caracteres
    # ou
    resultado = hash_obj.digest()     # 32 bytes
"""

import struct


class SHA256:
    """
    Implementação pura do algoritmo SHA-256 (FIPS 180-4).

    A classe encapsula todo o estado do hash e fornece a mesma interface da hashlib:
    update(), digest() e hexdigest().
    """

    # --------------------------------------------------------------------------
    # Constantes de rodada K[0..63]
    # Extraídas da parte fracionária das raízes cúbicas dos primeiros 64 primos.
    # --------------------------------------------------------------------------
    K = (
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    )

    # --------------------------------------------------------------------------
    # Valores iniciais do hash H0..H7
    # Extraídos da parte fracionária das raízes quadradas dos primeiros 8 primos.
    # --------------------------------------------------------------------------
    H_INITIAL = (
        0x6a09e667,  # H0 — √2
        0xbb67ae85,  # H1 — √3
        0x3c6ef372,  # H2 — √5
        0xa54ff53a,  # H3 — √7
        0x510e527f,  # H4 — √11
        0x9b05688c,  # H5 — √13
        0x1f83d9ab,  # H6 — √17
        0x5be0cd19,  # H7 — √19
    )

    # --------------------------------------------------------------------------
    # Métodos auxiliares de operações bit-a-bit (32 bits)
    # Todos retornam inteiros no intervalo [0, 2³²−1].
    # --------------------------------------------------------------------------

    @staticmethod
    def _rotr(x: int, n: int) -> int:
        """Rotação circular à direita de n bits."""
        return ((x >> n) | ((x << (32 - n)) & 0xFFFFFFFF)) & 0xFFFFFFFF

    @staticmethod
    def _right_shift(x: int, n: int) -> int:
        """Deslocamento lógico à direita (preenche com zeros)."""
        return (x >> n) & 0xFFFFFFFF

    @staticmethod
    def _ch(x: int, y: int, z: int) -> int:
        """Função Choose: (x ∧ y) ⊕ (¬x ∧ z)."""
        return (x & y) ^ ((~x & 0xFFFFFFFF) & z)

    @staticmethod
    def _maj(x: int, y: int, z: int) -> int:
        """Função Majority: (x ∧ y) ⊕ (x ∧ z) ⊕ (y ∧ z)."""
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def _sigma0(x: int) -> int:
        """
        σ₀ minúsculo — usada na expansão da mensagem.
        ROTR⁷(x) ⊕ ROTR¹⁸(x) ⊕ SHR³(x)
        """
        return (
            SHA256._rotr(x, 7) ^
            SHA256._rotr(x, 18) ^
            SHA256._right_shift(x, 3)
        )

    @staticmethod
    def _sigma1(x: int) -> int:
        """
        σ₁ minúsculo — usada na expansão da mensagem.
        ROTR¹⁷(x) ⊕ ROTR¹⁹(x) ⊕ SHR¹⁰(x)
        """
        return (
            SHA256._rotr(x, 17) ^
            SHA256._rotr(x, 19) ^
            SHA256._right_shift(x, 10)
        )

    @staticmethod
    def _Sigma0(x: int) -> int:
        """
        Σ₀ maiúsculo — usada na rodada de compressão.
        ROTR²(x) ⊕ ROTR¹³(x) ⊕ ROTR²²(x)
        """
        return (
            SHA256._rotr(x, 2) ^
            SHA256._rotr(x, 13) ^
            SHA256._rotr(x, 22)
        )

    @staticmethod
    def _Sigma1(x: int) -> int:
        """
        Σ₁ maiúsculo — usada na rodada de compressão.
        ROTR⁶(x) ⊕ ROTR¹¹(x) ⊕ ROTR²⁵(x)
        """
        return (
            SHA256._rotr(x, 6) ^
            SHA256._rotr(x, 11) ^
            SHA256._rotr(x, 25)
        )

    # --------------------------------------------------------------------------
    # Inicialização e gerenciamento de estado
    # --------------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Inicializa o estado interno com os valores H0..H7 padronizados,
        zera o buffer de bytes e o contador de bits da mensagem.
        """
        self._h: list[int] = list(self.H_INITIAL)  # estado hash (8 × 32 bits)
        self._buffer: bytearray = bytearray()       # bytes ainda não processados
        self._bit_length: int = 0                   # tamanho total em bits

    # --------------------------------------------------------------------------
    # Processamento de um bloco de 512 bits (64 bytes)
    # --------------------------------------------------------------------------

    def _process_block(self, block: bytes) -> None:
        """
        Processa um bloco de exatamente 64 bytes (512 bits), atualizando
        o estado interno H0..H7 conforme as 64 rodadas do SHA-256.
        """
        # 1. Converte os 64 bytes em 16 palavras de 32 bits (big-endian)
        W: list[int] = list(struct.unpack(">16I", block))

        # 2. Expande W para 64 palavras (W[16] até W[63])
        for t in range(16, 64):
            s0 = self._sigma0(W[t - 15])
            s1 = self._sigma1(W[t - 2])
            W.append((s1 + W[t - 7] + s0 + W[t - 16]) & 0xFFFFFFFF)

        # 3. Inicializa os oito registradores de trabalho com o estado atual
        a, b, c, d, e, f, g, h = self._h

        # 4. Executa 64 rodadas de compressão
        for t in range(64):
            T1 = (h + self._Sigma1(e) + self._ch(e, f, g) + self.K[t] + W[t]) & 0xFFFFFFFF
            T2 = (self._Sigma0(a) + self._maj(a, b, c)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

        # 5. Soma os registradores ao estado atual (mantendo 32 bits)
        self._h[0] = (self._h[0] + a) & 0xFFFFFFFF
        self._h[1] = (self._h[1] + b) & 0xFFFFFFFF
        self._h[2] = (self._h[2] + c) & 0xFFFFFFFF
        self._h[3] = (self._h[3] + d) & 0xFFFFFFFF
        self._h[4] = (self._h[4] + e) & 0xFFFFFFFF
        self._h[5] = (self._h[5] + f) & 0xFFFFFFFF
        self._h[6] = (self._h[6] + g) & 0xFFFFFFFF
        self._h[7] = (self._h[7] + h) & 0xFFFFFFFF

    # --------------------------------------------------------------------------
    # Gerenciamento da entrada (update)
    # --------------------------------------------------------------------------

    def update(self, data: bytes) -> "SHA256":
        """
        Adiciona dados à mensagem a ser hasheada.
        Processa blocos completos de 64 bytes conforme vão sendo acumulados.

        Retorna self para permitir encadeamento de chamadas.
        """
        self._buffer.extend(data)
        self._bit_length += len(data) * 8

        # Processa blocos completos de 64 bytes
        while len(self._buffer) >= 64:
            block = bytes(self._buffer[:64])
            del self._buffer[:64]
            self._process_block(block)

        return self

    # --------------------------------------------------------------------------
    # Padding MERKLE-DAMGÅRD
    # --------------------------------------------------------------------------

    def _pad(self) -> bytes:
        """
        Aplica o padding MERKLE-DAMGÅRD aos dados restantes no buffer:

        1. Adiciona o byte 0x80 (bit '1' seguido de zeros).
        2. Adiciona k bytes 0x00 de modo que:
           (dados + 0x80 + zeros + 8 bytes de comprimento) seja múltiplo de 64.
        3. Anexa o comprimento original da mensagem em bits como
           inteiro de 64 bits big-endian.

        Retorna:
            bytes contendo o(s) último(s) bloco(s) pronto(s) para processamento
            (tamanho múltiplo de 64).
        """
        # Cópia dos dados restantes
        remaining = bytes(self._buffer)

        # Calcula quantos bytes de zero são necessários
        # Queremos: (len(remaining) + 1 + zeros + 8) % 64 == 0
        remaining_len = len(remaining)
        zeros_needed = (56 - (remaining_len + 1) % 64) % 64

        # Monta o padding
        padded = remaining + b"\x80" + b"\x00" * zeros_needed
        # Anexa o comprimento em bits (64-bit big-endian)
        padded += struct.pack(">Q", self._bit_length)

        return padded

    # --------------------------------------------------------------------------
    # Finalização e obtenção do hash
    # --------------------------------------------------------------------------

    def digest(self) -> bytes:
        """
        Finaliza o hash e retorna o resumo de 32 bytes (256 bits).

        O estado interno é preservado para que o objeto possa ser consultado
        novamente (digest/hexdigest retornam o mesmo resultado em chamadas
        consecutivas).

        Retorna:
            bytes — 32 bytes representando o hash SHA-256.
        """
        # Salva o estado original para restaurá-lo depois
        original_h = self._h.copy()
        original_buffer = self._buffer.copy()
        original_bit_length = self._bit_length

        # Obtém os blocos com padding
        padded = self._pad()

        # Processa cada bloco de 64 bytes do padding
        for i in range(0, len(padded), 64):
            block = padded[i:i + 64]
            self._process_block(block)

        # Converte os 8 valores H0..H7 em 32 bytes (big-endian)
        result = struct.pack(">8I", *self._h)

        # Restaura o estado original
        self._h = original_h
        self._buffer = original_buffer
        self._bit_length = original_bit_length

        return result

    def hexdigest(self) -> str:
        """
        Retorna o hash SHA-256 como uma string hexadecimal de 64 caracteres
        (minúsculos), assim como hashlib.sha256(...).hexdigest().

        Retorna:
            str — 64 caracteres hexadecimais.
        """
        return self.digest().hex()


# Testes de comparação com hashlib
if __name__ == "__main__":
    import hashlib
    
    casos_para_teste = [b"", b"abc", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", b"a" * 1000]

    todos_ok = True
    for dados in casos_para_teste:
        nosso = SHA256()
        nosso.update(dados)
        nosso_hex = nosso.hexdigest()
        ref_hex = hashlib.sha256(dados).hexdigest()

        print("\nMeu hex:", nosso_hex)
        print("Hex de comparação:", ref_hex)
        if nosso_hex == ref_hex:
            print(f"OK, dado enviado: {dados}")
        else:
            print(f"Fail, dado enviado: {dados}")
            todos_ok = False

    # Teste multiplos updates devem equivaler a um update unico
    print()
    print("--- Teste de multiplos updates ---")
    dados_parte1 = b"abc"
    dados_parte2 = b"def"
    dados_completo = b"abcdef"

    hash_multiplo = SHA256()
    hash_multiplo.update(dados_parte1)
    hash_multiplo.update(dados_parte2)

    hash_unico = SHA256()
    hash_unico.update(dados_completo)

    if hash_multiplo.hexdigest() == hash_unico.hexdigest():
        print("OK  Multiplos updates equivalentes a update unico")
    else:
        print("FAIL Falha no teste de multiplos updates")
        todos_ok = False

    # Teste se digest() retorna 32 bytes e hexdigest() 64 caracteres
    print()
    print("--- Teste de tamanhos de saida ---")
    hash_obj = SHA256()
    hash_obj.update(b"teste")
    d = hash_obj.digest()
    h = hash_obj.hexdigest()

    if len(d) == 32:
        print("OK  digest() retorna 32 bytes")
    else:
        print(f"FAIL digest() retornou {len(d)} bytes (esperado: 32)")
        todos_ok = False

    if len(h) == 64:
        print("OK  hexdigest() retorna 64 caracteres")
    else:
        print(f"FAIL hexdigest() retornou {len(h)} caracteres (esperado: 64)")
        todos_ok = False

    # Teste se chamar digest/hexdigest repetidas vezes retorna o mesmo valor
    print()
    print("--- Teste de chamadas repetidas a digest/hexdigest ---")
    hash_obj2 = SHA256()
    hash_obj2.update(b"verificacao")
    d1 = hash_obj2.digest()
    d2 = hash_obj2.digest()
    h1 = hash_obj2.hexdigest()
    h2 = hash_obj2.hexdigest()

    if d1 == d2 and h1 == h2:
        print("OK  Chamadas repetidas retornam o mesmo resultado")
    else:
        print("FAIL Falha no teste de chamadas repetidas")
        todos_ok = False

    # Resultado final
    print()
    if todos_ok:
        print("=== TODOS OS TESTES PASSARAM ===")
    else:
        print("=== ALGUNS TESTES FALHARAM ===")
