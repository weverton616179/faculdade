# 🔐 Chat Criptografado com RSA Puro em Python

**Sistema de comunicação segura ponto-a-ponto com criptografia assimétrica RSA implementada do zero**

---

> **Disciplina:** Criptografia e Segurança de Sistemas Computacionais  
> **Autor:** Weverton  
> **Linguagem:** Python 3 (somente biblioteca padrão)  
> **Arquitetura:** Cliente-Servidor com handshake RSA e chat bidirecional criptografado

---

## 📖 Resumo

Este projeto implementa um sistema de chat seguro que utiliza **criptografia assimétrica RSA de 1024 bits** para garantir confidencialidade nas mensagens trocadas entre duas partes. Diferentemente da maioria das implementações acadêmicas, o RSA foi implementado **inteiramente do zero**, utilizando apenas bibliotecas nativas do Python (`secrets`, `socket`, `threading`), sem dependências externas. O sistema contempla todas as etapas fundamentais da criptografia assimétrica: geração de primos (Miller-Rabin), cálculo de inverso modular (Euclides estendido), padding PKCS#1 v1.5, chunking para mensagens longas e um protocolo completo de handshake para troca segura de chaves públicas.

**Palavras-chave:** RSA, criptografia assimétrica, PKCS#1 v1.5, Miller-Rabin, handshake criptográfico, chat seguro, Python.

---

## 🎯 Objetivos

1. Demonstrar na prática o funcionamento do algoritmo RSA — o mais difundido sistema de criptografia assimétrica do mundo.
2. Implementar todos os primitivos criptográficos do zero, sem bibliotecas externas, para compreensão profunda dos mecanismos.
3. Construir um protocolo de comunicação completo: handshake de chaves → criptografia de mensagens → chunking → transmissão → descriptografia.
4. Ilustrar conceitos fundamentais: confidencialidade, par de chaves assimétricas, padding criptográfico e teste de primalidade probabilístico.

---

## 🧠 Fundamentação Teórica

### 1. Criptografia Assimétrica e o Algoritmo RSA

A criptografia assimétrica, também chamada de criptografia de chave pública, baseia-se na existência de um par de chaves matematicamente relacionadas:

| Chave | Função | Visibilidade |
|---|---|---|
| **Chave Pública** $(e, n)$ | Criptografar mensagens | Pública — pode ser compartilhada abertamente |
| **Chave Privada** $(d, n)$ | Descriptografar mensagens | Secreta — jamais sai do dispositivo do dono |

O RSA (Rivest–Shamir–Adleman, 1977) fundamenta-se na dificuldade computacional de **fatorar o produto de dois números primos grandes**. Dado $n = p \cdot q$, conhecer $n$ não permite recuperar $p$ e $q$ em tempo viável quando $n$ tem centenas de dígitos.

#### 1.1 Geração de Chaves

O processo de geração do par de chaves segue os seguintes passos matemáticos:

1. **Geração de primos:** Escolhem-se dois números primos aleatórios $p$ e $q$ de $\approx 512$ bits cada, totalizando $1024$ bits para o módulo.
2. **Módulo:** $n = p \cdot q$
3. **Função totiente de Euler:** $\phi(n) = (p-1)(q-1)$
4. **Expoente público:** $e = 65537$ (valor padronizado na indústria — primo de Fermat $F_4$)
5. **Expoente privado:** $d \equiv e^{-1} \pmod{\phi(n)}$, calculado via Algoritmo de Euclides Estendido

O par de chaves resultante é:
- **Pública:** $K_{pub} = (n, e)$
- **Privada:** $K_{priv} = (n, d)$

#### 1.2 Criptografia e Descriptografia

Dada uma mensagem $m$ (como inteiro, $0 \le m < n$):

$$\text{Criptografia: } c = m^e \bmod n$$
$$\text{Descriptografia: } m = c^d \bmod n$$

A correção do RSA baseia-se no **Teorema de Euler**: como $e \cdot d \equiv 1 \pmod{\phi(n)}$, temos $m^{ed} \equiv m \pmod{n}$.

#### 1.3 Segurança do RSA

A segurança repousa no **Problema RSA**: dados $n$, $e$ e $c = m^e \bmod n$, encontrar $m$ é computacionalmente inviável sem conhecer $d$. A melhor abordagem conhecida para derivar $d$ a partir de $(n, e)$ é fatorar $n$, problema para o qual **não se conhece algoritmo clássico de tempo polinomial**. Para $n$ de 1024 bits, estima-se que a fatoração demandaria milhares de anos mesmo com recursos computacionais massivos.

### 2. Padding PKCS#1 v1.5

O RSA "cru" (textbook RSA) apresenta vulnerabilidades graves:
- É **determinístico** — mesma mensagem produz sempre a mesma cifra.
- É **maleável** — um atacante pode modificar cifras de forma previsível.

O padding PKCS#1 v1.5 resolve essas questões introduzindo aleatoriedade:

```
Formato do bloco paddado (k bytes):
┌──────┬──────┬─────────────────────┬──────┬──────────┐
│ 0x00 │ 0x02 │  PS (≥ 8 bytes)     │ 0x00 │  M       │
│      │      │  bytes não-nulos    │      │ mensagem │
│      │      │  aleatórios          │      │ original │
└──────┴──────┴─────────────────────┴──────┴──────────┘
```

- `0x00 0x02`: identificador de padding para criptografia
- `PS` (Padding String): no mínimo 8 bytes aleatórios **não-nulos**
- `0x00`: byte separador
- `M`: mensagem original

Para chave de 1024 bits ($k = 128$ bytes), a capacidade máxima de payload é $k - 11 = 117$ bytes.

### 3. Teste de Primalidade de Miller-Rabin

O teste de Miller-Rabin é um algoritmo probabilístico que determina se um número é composto ou **provavelmente primo**. Dado um candidato $n$ ímpar:

1. Escreve-se $n-1 = 2^r \cdot d$, com $d$ ímpar.
2. Escolhe-se uma base aleatória $a \in [2, n-2]$.
3. Computa-se $x = a^d \bmod n$.
4. Se $x = 1$ ou $x = n-1$, o teste passa (n é provavelmente primo para esta base).
5. Eleva-se $x$ ao quadrado repetidamente; se $x = n-1$ em algum momento, passa.
6. Caso contrário, $n$ é **composto** com certeza.

Repetindo o teste com $k = 40$ bases independentes, a probabilidade de um composto ser confundido com primo é inferior a $2^{-80}$, valor desprezível para fins práticos.

---

## 🏗️ Arquitetura do Sistema

### Visão Geral

O sistema é composto por três módulos:

```
atividade tuneeling/
├── crypto_utils.py      ← Núcleo criptográfico (RSA, padding, serialização)
├── server_app.py        ← Aplicação servidora (aguarda conexão)
└── client_app.py        ← Aplicação cliente (inicia conexão)
```

```
┌─────────────────────────┐          ┌─────────────────────────┐
│     SERVER_APP.PY       │          │     CLIENT_APP.PY        │
│                         │          │                         │
│  1. Gera par RSA        │  TCP/IP  │  1. Gera par RSA        │
│  2. Aguarda conexão     │◄────────▶│  2. Conecta ao servidor │
│  3. Handshake: troca    │  :5000   │  3. Handshake: troca    │
│     de chaves públicas  │          │     de chaves públicas  │
│  4. Chat bidirecional   │          │  4. Chat bidirecional   │
│                         │          │                         │
│  🧵 Thread Tx: envio    │          │  🧵 Thread Tx: envio    │
│  🧵 Thread Rx: receb.   │          │  🧵 Thread Rx: receb.   │
└─────────────────────────┘          └─────────────────────────┘
```

### Pilha de Protocolos

```
┌──────────────────────────────────────────┐
│          Camada de Aplicação             │
│   Chat: input do usuário, comandos       │
├──────────────────────────────────────────┤
│        Camada de Criptografia            │
│   RSA-1024 + PKCS#1 v1.5 + Chunking      │
│   (crypto_utils.py)                      │
├──────────────────────────────────────────┤
│       Camada de Enquadramento            │
│   Prefixo de 4 bytes (uint32 big-endian) │
│   com o tamanho total do payload         │
├──────────────────────────────────────────┤
│         Camada de Transporte             │
│   TCP/IP — Socket (127.0.0.1:5000)      │
└──────────────────────────────────────────┘
```

---

## 📁 Descrição Detalhada dos Módulos

### `crypto_utils.py` — Núcleo Criptográfico

Este módulo contém toda a lógica criptográfica implementada do zero. Suas principais estruturas e funções são:

#### Classes de Chave

| Classe | Atributos | Descrição |
|---|---|---|
| `PublicKey` | `n: int, e: int` | Chave pública RSA |
| `PrivateKey` | `n: int, d: int` | Chave privada RSA |

#### Constantes

| Constante | Valor | Significado |
|---|---|---|
| `TAMANHO_CHAVE` | 1024 | Tamanho da chave RSA em bits |
| `TAMANHO_CHUNK` | 100 | Máximo de bytes por chunk (limite conservador) |
| `E_PADRAO` | 65537 | Expoente público padrão (primo de Fermat $F_4$) |
| `ROUNDS_MILLER_RABIN` | 40 | Rounds do teste de primalidade ($P(\text{erro}) < 2^{-80}$) |

#### Funções Internas (Aritmética Modular)

| Função | Descrição | Complexidade |
|---|---|---|
| `_miller_rabin(n, k)` | Teste probabilístico de primalidade | $O(k \log^3 n)$ |
| `_gerar_primo(bits)` | Gera primo aleatório com o tamanho exato de bits | $O(\log^3 n)$ esperado |
| `_gcd_extendido(a, b)` | Algoritmo de Euclides estendido | $O(\log \min(a,b))$ |
| `_inverso_modular(e, phi)` | Calcula $d = e^{-1} \bmod \phi$ | $O(\log \phi)$ |

#### Funções Internas (Padding)

| Função | Descrição |
|---|---|
| `_gerar_bytes_nao_nulos(qtd)` | Gera bytes aleatórios não-nulos (criptograficamente seguros) |
| `_aplicar_padding_pkcs1(msg, k)` | Aplica padding PKCS#1 v1.5 para criptografia |
| `_remover_padding_pkcs1(dados)` | Remove padding e valida o formato |

#### API Pública

| Função | Descrição |
|---|---|
| `gerar_chaves(bits)` | Gera par `(PublicKey, PrivateKey)` |
| `serializar_chave_publica(pub)` | Converte `PublicKey` → `bytes` |
| `desserializar_chave_publica(bytes)` | Reconstrói `PublicKey` a partir de `bytes` |
| `criptografar_mensagem(str, pub)` | Criptografa texto com chunking → `bytes` |
| `descriptografar_mensagem(bytes, priv)` | Descriptografa payload com chunking → `str` |

### `server_app.py` — Aplicação Servidora

O servidor segue a seguinte máquina de estados:

1. **Inicialização:** Gera par de chaves RSA.
2. **Escuta:** `bind()` na porta 5000, `listen()` por conexões.
3. **Conexão:** `accept()` — aguarda o cliente conectar.
4. **Handshake:** Envia sua chave pública → Recebe a chave pública do cliente.
5. **Chat:** Inicia thread de recebimento + loop principal de envio.

### `client_app.py` — Aplicação Cliente

O cliente é simétrico ao servidor pós-handshake, com a diferença na ordem de inicialização:

1. **Inicialização:** Gera par de chaves RSA.
2. **Conexão:** `connect()` ao servidor.
3. **Handshake:** Recebe a chave pública do servidor → Envia sua chave pública.
4. **Chat:** Inicia thread de recebimento + loop principal de envio.

### Funções de Rede (compartilhadas por ambas as aplicações)

| Função | Descrição |
|---|---|
| `enviar_dados(sock, dados)` | Envia `[4 bytes: tamanho][payload]` via `sendall()` |
| `receber_dados(sock)` | Lê `[4 bytes: tamanho]` e faz loop até receber o payload completo |
| `thread_receber(sock, chave_privada)` | Thread que descriptografa e exibe mensagens recebidas |

---

## 🔄 Protocolo de Comunicação

### Handshake (Troca de Chaves)

```
Servidor                              Cliente
   │                                     │
   │  Gera (pub_S, priv_S)               │  Gera (pub_C, priv_C)
   │  listen()                           │
   │◄──────────── TCP connect ───────────│
   │                                     │
   │─── [4B|pub_S_bytes] ───────────────▶│  ← Servidor envia chave pública primeiro
   │                                     │  (evita deadlock)
   │◄─── [4B|pub_C_bytes] ──────────────│  ← Cliente envia sua chave pública
   │                                     │
   │  ✅ Handshake concluído             │  ✅ Handshake concluído
```

### Formato das Mensagens na Rede

**Mensagem de handshake (chave pública):**
```
┌────────────────┬──────────────────────────────┐
│ 4 bytes        │ Chave pública serializada     │
│ (uint32 BE)    │ [2B|len_n][n_bytes][2B|len_e][e_bytes] │
└────────────────┴──────────────────────────────┘
```

**Mensagem de chat (texto criptografado com chunking):**
```
┌────────────────┬───────────────────────────────────────────────┐
│ 4 bytes        │ Payload criptografado                         │
│ (uint32 BE)    │ ┌──────────┬─────────────┬──────────┬───────┐ │
│                │ │ 2B|len₁  │ ciphertext₁ │ 2B|len₂  │ ctx₂  │ │
│                │ └──────────┴─────────────┴──────────┴───────┘ │
└────────────────┴───────────────────────────────────────────────┘
```

Cada `ciphertextᵢ` tem exatamente 128 bytes (1024 bits ÷ 8), correspondendo ao tamanho fixo da saída do RSA com chave de 1024 bits.

### Chunking — Superando o Limite do RSA

O RSA impõe um limite ao tamanho da mensagem: com chave de 1024 bits e padding PKCS#1 v1.5, o máximo é $128 - 11 = 117$ bytes por operação. Para mensagens maiores, o sistema divide o texto em chunks e criptografa cada um individualmente:

```
"Olá, como vai você?" (22 bytes UTF-8)
        │
        ▼ (apenas 1 chunk, pois 22 < 100)
┌──────────────────┐
│ [2B: 128] [128B] │  = 130 bytes de payload criptografado
└──────────────────┘

"Mensagem muito longa..." (250 bytes UTF-8)
        │
        ▼ (3 chunks de 100, 100 e 50 bytes)
┌──────────┬─────────────┬──────────┬─────────────┬──────────┬─────────────┐
│ 2B: 128  │ ciphertext₁ │ 2B: 128  │ ciphertext₂ │ 2B: 128  │ ciphertext₃ │
└──────────┴─────────────┴──────────┴─────────────┴──────────┴─────────────┘
                           = 390 bytes de payload criptografado
```

---

## 🔬 Funcionamento Interno do RSA — Exemplo Numérico

Para ilustrar o algoritmo com números pequenos (não seguros, mas didáticos):

### Geração de Chaves

```
1. Primos:         p = 61, q = 53
2. Módulo:         n = 61 × 53 = 3233
3. Totiente:       φ(n) = 60 × 52 = 3120
4. Expoente públ:  e = 17  (coprimo com 3120)
5. Expoente priv:  d = 17⁻¹ mod 3120 = 2753
```

### Criptografia de $m = 65$

$$c = 65^{17} \bmod 3233 = 2790$$

### Descriptografia

$$m = 2790^{2753} \bmod 3233 = 65 \quad \checkmark$$

> ⚠️ Nosso sistema utiliza números de 1024 bits (~309 dígitos decimais), não estes valores triviais.

---

## ⚙️ Como Executar

### Pré-requisitos

- **Python 3.7+** — Nenhuma biblioteca externa necessária!

### Execução

Abra **dois terminais** na pasta do projeto:

**Terminal 1 — Servidor:**
```bash
python server_app.py
```

**Terminal 2 — Cliente:**
```bash
python client_app.py
```

### Comandos do Chat

| Comando | Ação |
|---|---|
| Qualquer texto | Envia mensagem criptografada ao parceiro |
| `/sair` | Encerra o chat e fecha a conexão |
| `Ctrl+C` | Interrompe a aplicação imediatamente |

---

## 🖥️ Exemplo de Execução

### Servidor

```
============================================================
  CHAT CRIPTOGRAFADO COM RSA - MODO SERVIDOR
============================================================

[*] Gerando par de chaves RSA (1024 bits)...
[*] Gerando primos de 512 bits cada...
[✓] Chaves geradas com sucesso!
[*] Aguardando conexão em 127.0.0.1:5000...
[✓] Cliente conectado: 127.0.0.1:54321

[*] Iniciando handshake - troca de chaves públicas...
[→] Chave pública enviada ao cliente.
[←] Chave pública do cliente recebida.
[✓] Handshake concluído. Chaves públicas trocadas com sucesso!
------------------------------------------------------------

[*] Chat iniciado! Digite suas mensagens.
[*] Digite '/sair' para encerrar.

[DEBUG] Mensagem cifrada recebida (130 bytes): a3f2b81c9d4e7f3a...
[Parceiro]: Olá! Tudo bem?
[Você]:
```

### Cliente

```
============================================================
  CHAT CRIPTOGRAFADO COM RSA - MODO CLIENTE
============================================================

[*] Gerando par de chaves RSA (1024 bits)...
[*] Gerando primos de 512 bits cada...
[✓] Chaves geradas com sucesso!
[*] Conectando ao servidor 127.0.0.1:5000...
[✓] Conectado ao servidor!

[*] Iniciando handshake - troca de chaves públicas...
[←] Chave pública do servidor recebida.
[→] Chave pública enviada ao servidor.
[✓] Handshake concluído. Chaves públicas trocadas com sucesso!
------------------------------------------------------------

[*] Chat iniciado! Digite suas mensagens.
[*] Digite '/sair' para encerrar.

[Você]: Olá! Tudo bem?
[DEBUG] Mensagem cifrada enviada (130 bytes): b7e2a14f3c8d9e2b...

[DEBUG] Mensagem cifrada recebida (130 bytes): 1c4d8f2a9e3b7c51...
[Parceiro]: Tudo ótimo! E com você?
[Você]:
```

> 📝 As linhas `[DEBUG]` exibem os primeiros bytes do ciphertext em hexadecimal, comprovando que os dados trafegam cifrados pela rede.

---

## 🔍 Demonstração de Segurança

### O que trafega na rede

Se um atacante interceptar o tráfego TCP entre as aplicações, verá apenas:

```
Sem criptografia (hipotético):
  00 00 00 02 4F 69              ← "Oi" em texto plano

Com criptografia (sistema real):
  00 00 00 82 00 80 A3 F2 1B 8C 9D 4E 7F 3A 51 C2 ... (130 bytes)
  └─tamanho─┘ └tam┘ └────── ciphertext (128 bytes) ──────┘
```

### Propriedades de segurança garantidas

| Propriedade | Como é garantida |
|---|---|
| **Confidencialidade** | RSA-1024: somente o detentor da chave privada consegue descriptografar |
| **Aleatoriedade das cifras** | Padding PKCS#1 v1.5 com bytes não-nulos aleatórios — mesma mensagem gera cifras diferentes a cada envio |
| **Integridade do padding** | Validação rigorosa na remoção: verifica-se `0x00 0x02`, ≥ 8 bytes de padding e separador `0x00` |
| **Resistência a fatoração** | Módulo $n$ de 1024 bits inviabiliza a recuperação de $p$ e $q$ |

---

## 📊 Análise de Complexidade

| Operação | Complexidade | Observação |
|---|---|---|
| Geração de primos (Miller-Rabin) | $O(k \cdot \log^3 n)$ | $k=40$ rounds; executa ~1-3s para 512 bits |
| Criptografia RSA | $O(\log e \cdot \log^2 n)$ | $e=65537$: apenas 17 multiplicações modulares |
| Descriptografia RSA | $O(\log d \cdot \log^2 n)$ | $d \approx n$: ~3072 multiplicações modulares |
| Padding PKCS#1 | $O(k)$ | Simples concatenação de bytes |
| Chunking | $O(\lceil L / C \rceil)$ | $L$ = tamanho da mensagem, $C$ = 100 bytes |

---

## 🧪 Validação e Testes

O sistema foi testado com os seguintes cenários:

| Cenário | Resultado |
|---|---|
| Mensagem curta (1 caractere) | ✅ Criptografada e descriptografada corretamente |
| Mensagem média (~50 caracteres) | ✅ Cabem em 1 chunk |
| Mensagem longa (~500 caracteres) | ✅ Chunking divide em múltiplos chunks |
| Mensagem com caracteres especiais (UTF-8) | ✅ Codificação UTF-8 preserva emojis e acentos |
| Conexão interrompida | ✅ Thread detecta e encerra graciosamente |
| Comando `/sair` | ✅ Ambos os lados encerram corretamente |
| Ciphertexts distintos para mesma mensagem | ✅ Padding aleatório garante não-determinismo |

---

## ⚠️ Limitações e Considerações

| Limitação | Explicação | Melhoria possível |
|---|---|---|
| **RSA puro para chat** | Na prática, usa-se RSA apenas para trocar uma chave simétrica AES (criptografia híbrida) | Implementar ECDHE + AES-GCM |
| **Sem autenticação** | Não há certificados — um atacante MITM poderia substituir as chaves públicas | Adicionar PKI ou Trust On First Use (TOFU) |
| **Sem Perfect Forward Secrecy** | Se a chave privada for comprometida, todas as conversas passadas podem ser decifradas | Implementar Diffie-Hellman Efêmero (DHE) |
| **Apenas 2 participantes** | O modelo é estritamente 1-a-1 | Expandir para chat em grupo com troca de chaves em anel |
| **Chaves efêmeras** | Chaves geradas em memória — perdidas ao reiniciar | Persistir chaves em keystore protegido por senha |
| **Sem assinatura digital** | Mensagens não são autenticadas (não-repúdio) | Adicionar ECDSA ou RSA-PSS para assinatura |

---

## 🎓 Conclusão

Este projeto demonstra, de forma prática e pedagogicamente transparente, os fundamentos da criptografia assimétrica RSA aplicados a um cenário real de comunicação segura. A implementação do zero de todos os primitivos criptográficos — desde o teste de primalidade de Miller-Rabin até o padding PKCS#1 v1.5 — proporciona compreensão profunda dos mecanismos que sustentam a segurança de sistemas como HTTPS, SSH e PGP.

O sistema evidencia que, com fundamentos matemáticos sólidos e uma implementação cuidadosa, é possível construir canais de comunicação onde **a confidencialidade das mensagens é garantida matematicamente**, independentemente de a rede ser hostil ou monitorada.

---

## 📚 Referências

1. **Rivest, R. L.; Shamir, A.; Adleman, L.** (1978). "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems". *Communications of the ACM*, 21(2), pp. 120–126.

2. **PKCS #1 v1.5** — RSA Cryptography Standard. RFC 2313 (obsoleta), RFC 3447 (PKCS #1 v2.1). Disponível em: https://tools.ietf.org/html/rfc3447

3. **Miller, G. L.** (1976). "Riemann's Hypothesis and Tests for Primality". *Journal of Computer and System Sciences*, 13(3), pp. 300–317.

4. **Rabin, M. O.** (1980). "Probabilistic Algorithm for Testing Primality". *Journal of Number Theory*, 12(1), pp. 128–138.

5. **Menezes, A. J.; van Oorschot, P. C.; Vanstone, S. A.** (1996). *Handbook of Applied Cryptography*. CRC Press. Capítulos 4, 8 e 11.

6. **Katz, J.; Lindell, Y.** (2014). *Introduction to Modern Cryptography*. 2ª ed. Chapman & Hall/CRC. Capítulos 11–13.

---

> 📝 *Trabalho acadêmico desenvolvido para a disciplina de Criptografia e Segurança de Sistemas Computacionais. O código-fonte completo está disponível nos arquivos `crypto_utils.py`, `server_app.py` e `client_app.py`. A documentação estendida com diagramas e analogias encontra-se em `explicacao_sistema.md`.*
