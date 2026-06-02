"""
Implementação do Algoritmo AES-256 do Zero (para fins didáticos)
Este arquivo contém as funções principais do AES e o modo de operação CBC (Cipher Block Chaining)
com preenchimento (padding) PKCS#7.

Nomes de variáveis foram simplificados e comentários detalhados foram adicionados para facilitar o entendimento.
"""

# S-box (Tabela de substituição)
# É uma tabela de pesquisa usada para trocar os bytes, adicionando "confusão" aos dados.
# Isso impede que padrões nos dados de entrada apareçam nos dados de saída.
Sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# InvSbox (S-box Inversa)
# Tabela usada para reverter a substituição de bytes durante a descriptografia.
InvSbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

# Rcon (Constantes de Rodada)
# Usadas para gerar as chaves de cada rodada. Elas evitam que todas as rodadas tenham cálculos muito parecidos.
Rcon = [
    0x00000000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000,
    0x80000000, 0x1B000000, 0x36000000, 0x6C000000, 0xD8000000, 0xAB000000, 0x4D000000, 0x9A000000
]

def multiplicar_por_2_galois(valor):
    """
    Multiplicação especial por 2 dentro da matemática usada no AES (Corpo de Galois GF(2^8)).
    Isso é usado na hora de embaralhar as colunas.
    """
    if valor & 0x80: # Se o bit mais à esquerda for 1 (valor >= 128)
        return ((valor << 1) ^ 0x11B) & 0xFF
    else:
        return (valor << 1)

def multiplicar_galois(a, b):
    """
    Multiplicação de dois números no Corpo de Galois.
    Usada especificamente na etapa de "MixColumns" (Misturar Colunas).
    """
    resultado = 0
    while b:
        if b & 1: # Se o bit atual de 'b' for 1
            resultado ^= a # XOR funciona como a "soma" nesta matemática especial
        a = multiplicar_por_2_galois(a)
        b >>= 1 # Desloca 'b' para avaliar o próximo bit
    return resultado


class AES256:
    """
    Classe principal que executa a encriptação/desencriptação pura (core) do AES.
    O bloco de dados do AES tem sempre 128 bits (16 bytes).
    A chave usada aqui será de 256 bits (32 bytes).
    """
    def __init__(self, chave_principal: bytes):
        if len(chave_principal) != 32:
            raise ValueError("O AES-256 exige uma chave de exatamente 32 bytes (256 bits)")
        
        self.palavras_na_chave = 8  # Número de palavras (de 32 bits) na chave original (Nk = 8)
        self.colunas_no_bloco = 4   # O bloco de 16 bytes é tratado como uma grade de 4 colunas (Nb = 4)
        self.total_de_rodadas = 14  # O AES-256 é feito sempre em 14 etapas/rodadas (Nr = 14)
        
        # O AES cria várias "chaves de rodada" a partir da chave original (Key Expansion).
        # Teremos uma subchave para usar a cada etapa do algoritmo.
        self.chaves_expandidas = self._expandir_chave(chave_principal)

    def _substituir_palavra(self, palavra):
        """Aplica a tabela de substituição (S-box) a cada um dos 4 bytes de uma palavra (32 bits)."""
        # Extrai os 4 bytes da palavra e os substitui usando a Sbox
        return (Sbox[(palavra >> 24) & 0xFF] << 24 |
                Sbox[(palavra >> 16) & 0xFF] << 16 |
                Sbox[(palavra >> 8) & 0xFF] << 8 |
                Sbox[palavra & 0xFF])

    def _rotacionar_palavra(self, palavra):
        """Move o primeiro byte de uma palavra para o final (ex: [A,B,C,D] vira [B,C,D,A])."""
        return ((palavra << 8) & 0xFFFFFFFF) | (palavra >> 24)

    def _expandir_chave(self, chave_original):
        """
        Gera o conjunto completo de "chaves de rodada".
        Ele cria 60 palavras no total (4 palavras por rodada, em 15 rodadas: de 0 a 14).
        """
        chaves_geradas = [0] * (self.colunas_no_bloco * (self.total_de_rodadas + 1))
        
        # As primeiras 8 palavras (32 bytes) são a própria chave original intacta
        for i in range(self.palavras_na_chave):
            chaves_geradas[i] = int.from_bytes(chave_original[4*i:4*i+4], 'big')
            
        # O resto das chaves é calculado misturando as palavras geradas anteriormente
        for i in range(self.palavras_na_chave, len(chaves_geradas)):
            palavra_temporaria = chaves_geradas[i - 1]
            
            # A cada 8 palavras, aplicamos transformações mais complexas na palavra_temporaria
            if i % self.palavras_na_chave == 0:
                palavra_temporaria = self._substituir_palavra(self._rotacionar_palavra(palavra_temporaria)) ^ Rcon[i // self.palavras_na_chave]
            # No AES-256, há uma substituição extra no meio do caminho (posição múltipla de 4, que não seja de 8)
            elif self.palavras_na_chave > 6 and i % self.palavras_na_chave == 4:
                palavra_temporaria = self._substituir_palavra(palavra_temporaria)
                
            # Faz um XOR da palavra calculada com a palavra que está 8 posições atrás
            chaves_geradas[i] = chaves_geradas[i - self.palavras_na_chave] ^ palavra_temporaria
            
        return chaves_geradas

    # --- ETAPAS DO AES ---

    def _adicionar_chave_da_rodada(self, matriz_estado, rodada_atual):
        """
        AddRoundKey: Mistura os dados atuais (a matriz_estado) com a chave específica 
        desta rodada usando a operação XOR.
        """
        for coluna in range(self.colunas_no_bloco):
            palavra_da_chave = self.chaves_expandidas[rodada_atual * self.colunas_no_bloco + coluna]
            matriz_estado[0][coluna] ^= (palavra_da_chave >> 24) & 0xFF
            matriz_estado[1][coluna] ^= (palavra_da_chave >> 16) & 0xFF
            matriz_estado[2][coluna] ^= (palavra_da_chave >> 8) & 0xFF
            matriz_estado[3][coluna] ^= palavra_da_chave & 0xFF

    def _substituir_bytes(self, matriz_estado):
        """SubBytes: Troca cada byte do estado por outro da tabela de substituição (S-box)."""
        for linha in range(4):
            for coluna in range(self.colunas_no_bloco):
                matriz_estado[linha][coluna] = Sbox[matriz_estado[linha][coluna]]

    def _substituir_bytes_inverso(self, matriz_estado):
        """InvSubBytes: Troca cada byte usando a tabela reversa (usado para descriptografar)."""
        for linha in range(4):
            for coluna in range(self.colunas_no_bloco):
                matriz_estado[linha][coluna] = InvSbox[matriz_estado[linha][coluna]]

    def _deslocar_linhas(self, matriz_estado):
        """
        ShiftRows: Desloca os bytes das linhas para a esquerda.
        Isso espalha as informações da coluna por todo o bloco.
        - Linha 0: fica parada
        - Linha 1: move 1 casa para esquerda
        - Linha 2: move 2 casas para esquerda
        - Linha 3: move 3 casas para esquerda
        """
        matriz_estado[1][0], matriz_estado[1][1], matriz_estado[1][2], matriz_estado[1][3] = matriz_estado[1][1], matriz_estado[1][2], matriz_estado[1][3], matriz_estado[1][0]
        matriz_estado[2][0], matriz_estado[2][1], matriz_estado[2][2], matriz_estado[2][3] = matriz_estado[2][2], matriz_estado[2][3], matriz_estado[2][0], matriz_estado[2][1]
        matriz_estado[3][0], matriz_estado[3][1], matriz_estado[3][2], matriz_estado[3][3] = matriz_estado[3][3], matriz_estado[3][0], matriz_estado[3][1], matriz_estado[3][2]

    def _deslocar_linhas_inverso(self, matriz_estado):
        """InvShiftRows: Desfaz o deslocamento das linhas (move para a direita) - para descriptografar."""
        matriz_estado[1][0], matriz_estado[1][1], matriz_estado[1][2], matriz_estado[1][3] = matriz_estado[1][3], matriz_estado[1][0], matriz_estado[1][1], matriz_estado[1][2]
        matriz_estado[2][0], matriz_estado[2][1], matriz_estado[2][2], matriz_estado[2][3] = matriz_estado[2][2], matriz_estado[2][3], matriz_estado[2][0], matriz_estado[2][1]
        matriz_estado[3][0], matriz_estado[3][1], matriz_estado[3][2], matriz_estado[3][3] = matriz_estado[3][1], matriz_estado[3][2], matriz_estado[3][3], matriz_estado[3][0]

    def _misturar_colunas(self, matriz_estado):
        """
        MixColumns: Embaralha os bytes de cada coluna matematicamente.
        Assim, uma mudança de 1 único bit na entrada afetará o bloco inteiro (efeito avalanche).
        """
        for coluna in range(self.colunas_no_bloco):
            b0, b1, b2, b3 = matriz_estado[0][coluna], matriz_estado[1][coluna], matriz_estado[2][coluna], matriz_estado[3][coluna]
            matriz_estado[0][coluna] = multiplicar_galois(0x02, b0) ^ multiplicar_galois(0x03, b1) ^ b2 ^ b3
            matriz_estado[1][coluna] = b0 ^ multiplicar_galois(0x02, b1) ^ multiplicar_galois(0x03, b2) ^ b3
            matriz_estado[2][coluna] = b0 ^ b1 ^ multiplicar_galois(0x02, b2) ^ multiplicar_galois(0x03, b3)
            matriz_estado[3][coluna] = multiplicar_galois(0x03, b0) ^ b1 ^ b2 ^ multiplicar_galois(0x02, b3)

    def _misturar_colunas_inverso(self, matriz_estado):
        """InvMixColumns: Desfaz o embaralhamento das colunas (para descriptografar)."""
        for coluna in range(self.colunas_no_bloco):
            b0, b1, b2, b3 = matriz_estado[0][coluna], matriz_estado[1][coluna], matriz_estado[2][coluna], matriz_estado[3][coluna]
            matriz_estado[0][coluna] = multiplicar_galois(0x0E, b0) ^ multiplicar_galois(0x0B, b1) ^ multiplicar_galois(0x0D, b2) ^ multiplicar_galois(0x09, b3)
            matriz_estado[1][coluna] = multiplicar_galois(0x09, b0) ^ multiplicar_galois(0x0E, b1) ^ multiplicar_galois(0x0B, b2) ^ multiplicar_galois(0x0D, b3)
            matriz_estado[2][coluna] = multiplicar_galois(0x0D, b0) ^ multiplicar_galois(0x09, b1) ^ multiplicar_galois(0x0E, b2) ^ multiplicar_galois(0x0B, b3)
            matriz_estado[3][coluna] = multiplicar_galois(0x0B, b0) ^ multiplicar_galois(0x0D, b1) ^ multiplicar_galois(0x09, b2) ^ multiplicar_galois(0x0E, b3)

    def encriptar_bloco(self, dados_entrada: bytes) -> bytes:
        """
        Recebe exatamente 16 bytes e os transforma em 16 bytes encriptados (texto cifrado).
        """
        # Converte os 16 bytes em uma matriz de estado 4x4
        matriz_estado = [[dados_entrada[linha + 4*coluna] for coluna in range(self.colunas_no_bloco)] for linha in range(4)]
        
        # Passo Inicial: Mistura a primeira chave antes de começar as rodadas
        self._adicionar_chave_da_rodada(matriz_estado, 0)

        # 13 Rodadas Principais (Para o AES-256)
        for rodada_atual in range(1, self.total_de_rodadas):
            self._substituir_bytes(matriz_estado)
            self._deslocar_linhas(matriz_estado)
            self._misturar_colunas(matriz_estado)
            self._adicionar_chave_da_rodada(matriz_estado, rodada_atual)

        # Rodada Final (Rodada 14 - não tem a etapa de "misturar colunas")
        self._substituir_bytes(matriz_estado)
        self._deslocar_linhas(matriz_estado)
        self._adicionar_chave_da_rodada(matriz_estado, self.total_de_rodadas)

        # Converte a matriz 4x4 de volta para uma sequência de 16 bytes
        saida_bytes = bytearray(16)
        for coluna in range(self.colunas_no_bloco):
            for linha in range(4):
                saida_bytes[linha + 4*coluna] = matriz_estado[linha][coluna]
                
        return bytes(saida_bytes)

    def desencriptar_bloco(self, dados_cifrados: bytes) -> bytes:
        """
        Recebe 16 bytes cifrados e faz as etapas ao contrário para recuperar os 16 bytes originais.
        """
        matriz_estado = [[dados_cifrados[linha + 4*coluna] for coluna in range(self.colunas_no_bloco)] for linha in range(4)]
        
        # Passo Inicial Inverso: Começamos pela última chave gerada
        self._adicionar_chave_da_rodada(matriz_estado, self.total_de_rodadas)

        # 13 Rodadas em ordem decrescente (do 13 ao 1)
        for rodada_atual in range(self.total_de_rodadas - 1, 0, -1):
            self._deslocar_linhas_inverso(matriz_estado)
            self._substituir_bytes_inverso(matriz_estado)
            self._adicionar_chave_da_rodada(matriz_estado, rodada_atual)
            self._misturar_colunas_inverso(matriz_estado)

        # Rodada Final Inversa
        self._deslocar_linhas_inverso(matriz_estado)
        self._substituir_bytes_inverso(matriz_estado)
        self._adicionar_chave_da_rodada(matriz_estado, 0)

        saida_bytes = bytearray(16)
        for coluna in range(self.colunas_no_bloco):
            for linha in range(4):
                saida_bytes[linha + 4*coluna] = matriz_estado[linha][coluna]
                
        return bytes(saida_bytes)


# -------------------------------------------------------------------------
# FUNCIONALIDADES EXTRAS: PADDING (PREENCHIMENTO) E MODO DE OPERAÇÃO CBC
# -------------------------------------------------------------------------

def pad(dados_originais: bytes) -> bytes:
    """
    O AES só consegue criptografar pedaços de exatamente 16 bytes.
    Se o seu arquivo ou texto não for múltiplo de 16, preenchemos o final (Padding PKCS#7).
    Exemplo: se faltam 4 bytes, adicionamos 4 vezes o número 0x04.
    """
    bytes_faltando = 16 - (len(dados_originais) % 16)
    return dados_originais + bytes([bytes_faltando] * bytes_faltando)

def unpad(dados_preenchidos: bytes) -> bytes:
    """
    Remove os bytes de preenchimento que foram adicionados antes da encriptação.
    Lê qual é o último byte (que indica o número de bytes adicionados) e corta esse número do final.
    """
    bytes_faltando = dados_preenchidos[-1]
    return dados_preenchidos[:-bytes_faltando]

def aes256_cbc_encrypt(chave: bytes, vetor_inicializacao: bytes, dados_em_texto: bytes) -> bytes:
    """
    Encripta dados de qualquer tamanho usando AES-256 no modo CBC (Cipher Block Chaining).
    O modo CBC resolve a fraqueza de encriptar blocos repetidos sempre do mesmo jeito.
    Aqui, o bloco atual é sempre misturado (XOR) com o bloco cifrado anterior antes de ser encriptado.
    """
    aes = AES256(chave)
    dados_com_preenchimento = pad(dados_em_texto)
    resultado_cifrado = bytearray()
    
    # O primeiro bloco é misturado com o Vetor de Inicialização (IV)
    bloco_anterior = vetor_inicializacao
    
    # Processa tudo de 16 em 16 bytes (1 bloco por vez)
    for indice in range(0, len(dados_com_preenchimento), 16):
        bloco_atual = dados_com_preenchimento[indice:indice+16]
        
        # No CBC, fazemos XOR do bloco atual com o bloco cifrado anterior
        bloco_com_xor = bytes(byte_atual ^ byte_anterior for byte_atual, byte_anterior in zip(bloco_atual, bloco_anterior))
        
        # Encripta o bloco que acabou de ser misturado
        bloco_encriptado = aes.encriptar_bloco(bloco_com_xor)
        
        resultado_cifrado.extend(bloco_encriptado)
        
        # Guarda o bloco cifrado atual para misturar com o próximo
        bloco_anterior = bloco_encriptado
        
    return bytes(resultado_cifrado)

def aes256_cbc_decrypt(chave: bytes, vetor_inicializacao: bytes, dados_cifrados: bytes) -> bytes:
    """
    Reverte o processo do modo CBC, recuperando o texto original.
    """
    aes = AES256(chave)
    resultado_original = bytearray()
    
    bloco_anterior = vetor_inicializacao
    
    # Processa os dados cifrados de 16 em 16 bytes
    for indice in range(0, len(dados_cifrados), 16):
        bloco_atual = dados_cifrados[indice:indice+16]
        
        # Desencripta o bloco usando a função do AES
        bloco_desencriptado = aes.desencriptar_bloco(bloco_atual)
        
        # Desfaz a mistura que foi feita com o bloco cifrado anterior na encriptação
        bloco_texto_real = bytes(byte_desencriptado ^ byte_anterior for byte_desencriptado, byte_anterior in zip(bloco_desencriptado, bloco_anterior))
        
        resultado_original.extend(bloco_texto_real)
        
        # Guarda o bloco cifrado atual para usar na próxima iteração
        bloco_anterior = bloco_atual
        
    # Remove o preenchimento extra (padding) que foi adicionado originalmente
    return unpad(bytes(resultado_original))