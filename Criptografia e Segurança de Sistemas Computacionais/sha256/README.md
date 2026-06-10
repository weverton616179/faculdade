# 🔐 Autenticador de Arquivos via SHA-256

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

**Implementação didática do algoritmo SHA-256 (FIPS 180-4) para geração e verificação de hashes de arquivos**

</div>

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina de **Criptografia e Segurança de Sistemas Computacionais**. O objetivo foi implementar o algoritmo **SHA-256** do zero (conforme a especificação **NIST FIPS 180-4**) e utilizá-lo em uma aplicação capaz de:

1. **Gerar** o hash SHA-256 de qualquer arquivo
2. **Verificar** a autenticidade de um arquivo comparando seu hash com um hash fornecido

> ⚠️ **Importante:** O algoritmo foi implementado **sem utilizar** a biblioteca `hashlib` do Python — apenas recursos da biblioteca padrão (`struct`) foram empregados, garantindo o caráter didático do projeto.

---

## 🧠 O que é SHA-256?

**SHA-256** (Secure Hash Algorithm 256 bits) é uma função hash criptográfica pertencente à família SHA-2, publicada pelo **NIST** em 2001 (FIPS 180-4). Ela produz um resumo (hash) de **256 bits (32 bytes)** — geralmente representado como **64 caracteres hexadecimais** — a partir de uma entrada de qualquer tamanho.

### Características fundamentais:

| Propriedade | Descrição |
|-------------|-----------|
| **Determinístico** | Mesma entrada → sempre o mesmo hash |
| **Unidirecional** | Não é possível reverter o hash para obter a entrada original |
| **Resistência a colisões** | Extremamente difícil encontrar duas entradas diferentes com o mesmo hash |
| **Efeito avalanche** | Uma pequena alteração na entrada produz um hash completamente diferente |
| **Tamanho fixo** | Sempre 256 bits (64 caracteres hex), independentemente do tamanho da entrada |

---

## 🏗️ Estrutura do Projeto

```
sha256/
├── sha256.py                 # Implementação pura do SHA-256 (classe SHA256)
├── file_authenticator.py     # Aplicação CLI de autenticação de arquivos
├── teste.txt                 # Arquivo de exemplo para testes
├── comandos.txt              # Exemplos de comandos
├── instrucoes.txt            # Instruções da atividade
├── intrucoes_autenticacao_documentos.txt
└── README.md                 # Este arquivo
```

---

## ⚙️ Como Funciona

### 1️⃣ Algoritmo SHA-256 (`sha256.py`)

A classe `SHA256` implementa todas as etapas do algoritmo:

1. **Pré-processamento (Padding Merkle-Damgård):**
   - Adiciona o bit `1` (byte `0x80`) ao final dos dados
   - Preenche com zeros até que o comprimento seja congruente a 448 mod 512 bits
   - Anexa o comprimento original da mensagem em bits como um inteiro de 64 bits

2. **Processamento em blocos de 512 bits (64 bytes):**
   - Expande 16 palavras para 64 palavras
   - Executa 64 rodadas de compressão usando as funções lógicas:
     - `Σ₀`, `Σ₁` (maiúsculas) — usadas na compressão
     - `σ₀`, `σ₁` (minúsculas) — usadas na expansão da mensagem
     - `Ch` (Choose) — função de seleção de bits
     - `Maj` (Majority) — função de maioria de bits
   - Utiliza as 64 constantes `K[0..63]` (raízes cúbicas dos primeiros 64 primos)

3. **Finalização:**
   - Os 8 registradores `H₀` a `H₇` (inicializados com as raízes quadradas dos primeiros 8 primos) são convertidos em 32 bytes (big-endian)

### 2️⃣ Aplicação CLI (`file_authenticator.py`)

A interface de linha de comando oferece dois modos de operação:

```
python file_authenticator.py hash    <arquivo>
python file_authenticator.py verify  <arquivo> <hash_esperado>
```

- **Modo `hash`:** Calcula e exibe o hash SHA-256 do arquivo
- **Modo `verify`:** Calcula o hash do arquivo e compara com o hash fornecido, informando se o arquivo é **autêntico** ou **não autêntico**

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa (apenas biblioteca padrão)

### Gerar o hash de um arquivo

```bash
python file_authenticator.py hash documento.pdf
# Saída: SHA-256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### Verificar a autenticidade de um arquivo

```bash
python file_authenticator.py verify documento.pdf e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
# Saída: ✅ AUTÊNTICO: o hash do arquivo confere com o hash informado.
```

### Exemplo com alteração no arquivo

```bash
# 1. Gere o hash do arquivo original
python file_authenticator.py hash mensagem.txt
# SHA-256: a1b2c3d4... (64 chars)

# 2. Altere o arquivo (adicione um caractere)

# 3. Verifique novamente com o hash original
python file_authenticator.py verify mensagem.txt a1b2c3d4...
# ❌ NÃO AUTÊNTICO: o hash do arquivo NÃO confere com o hash informado.
```

---

## 🧪 Testes

O próprio `sha256.py` inclui uma suíte de testes que compara os resultados com a implementação oficial da `hashlib`:

```bash
python sha256.py
```

Casos testados:
- ✅ String vazia
- ✅ `"abc"` (caso clássico do FIPS 180-4)
- ✅ Mensagem longa (vetor de teste do NIST)
- ✅ 1000 caracteres `"a"`
- ✅ Múltiplos updates equivalentes a um único update
- ✅ Tamanho correto da saída (32 bytes / 64 caracteres hex)
- ✅ Chamadas repetidas a `digest()`/`hexdigest()` retornam o mesmo valor

---

## 📚 Conceitos Abordados

| Conceito | Aplicação no Projeto |
|----------|---------------------|
| **Funções hash criptográficas** | Implementação completa do SHA-256 |
| **Padding Merkle-Damgård** | Estrutura de construção para hash seguro |
| **Operações bit-a-bit** | Rotações, deslocamentos, XOR, AND, NOT |
| **Expansão de mensagem** | Geração de 64 palavras a partir de 16 |
| **Compressão** | 64 rodadas com funções Σ, σ, Ch e Maj |
| **Autenticação de arquivos** | Verificação de integridade via hash |
| **CLI em Python** | Interface com argparse para terminal |

---

## 🎯 Propósito Educacional

Este projeto foi desenvolvido para demonstrar na prática:

1. O funcionamento interno de uma **função hash criptográfica**
2. A importância da **integridade de arquivos** em segurança da informação
3. Como **pequenas alterações** em um arquivo são detectadas instantaneamente
4. A aplicação prática de conceitos teóricos de criptografia

---

## 📖 Referências

- [NIST FIPS 180-4](https://csrc.nist.gov/publications/detail/fips/180/4/final) — Secure Hash Standard (SHS)
- [SHA-2 na Wikipedia](https://en.wikipedia.org/wiki/SHA-2)

---

<div align="center">
<p><strong>Disciplina:</strong> Criptografia e Segurança de Sistemas Computacionais</p>
<p>Implementação puramente didática — não recomendada para uso em produção</p>
</div>
