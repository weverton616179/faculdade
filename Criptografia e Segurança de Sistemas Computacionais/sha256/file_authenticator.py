#!/usr/bin/env python3
"""
Autenticador de Arquivos via SHA-256
====================================
Aplicação que utiliza a implementação própria do algoritmo SHA-256
(sha256.py) para gerar e verificar hashes de arquivos de qualquer formato.

Uso:
    python file_authenticator.py hash <arquivo>
    python file_authenticator.py verify <arquivo> <hash>

Exemplos:
    python file_authenticator.py hash documento.pdf
    python file_authenticator.py verify documento.pdf a1b2c3...64chars...
"""

import argparse
import sys
from pathlib import Path

from sha256 import SHA256

# Tamanho do chunk de leitura: 64 KiB — equilibra desempenho e uso de memória
TAMANHO_CHUNK = 64 * 1024


def hash_file(caminho: str | Path) -> str:
    """
    Calcula o hash SHA-256 de um arquivo.

    Lê o arquivo em modo binário, em chunks, e alimenta o objeto SHA256
    incrementalmente, funcionando com arquivos de qualquer tamanho e formato.

    Args:
        caminho: Caminho para o arquivo a ser hasheado.

    Returns:
        String hexadecimal de 64 caracteres representando o hash SHA-256.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    arquivo = Path(caminho)
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    sha = SHA256()
    with open(arquivo, "rb") as f:
        while True:
            chunk = f.read(TAMANHO_CHUNK)
            if not chunk:
                break
            sha.update(chunk)

    return sha.hexdigest()


def verify_file(caminho: str | Path, hash_esperado: str) -> tuple[bool, str]:
    """
    Verifica se o hash SHA-256 do arquivo confere com o hash informado.

    Args:
        caminho: Caminho para o arquivo a ser verificado.
        hash_esperado: Hash SHA-256 (64 caracteres hexadecimais) a comparar.

    Returns:
        Tupla (autentico: bool, mensagem: str).

        - autentico=True  → o hash do arquivo confere com o esperado.
        - autentico=False → o hash não confere.
    """
    # Validação do formato do hash
    hash_esperado = hash_esperado.strip().lower()

    if len(hash_esperado) != 64:
        return False, (
            f"Hash inválido: esperados 64 caracteres hexadecimais, "
            f"mas foram fornecidos {len(hash_esperado)}."
        )

    if not all(c in "0123456789abcdef" for c in hash_esperado):
        return False, "Hash inválido: contém caracteres não hexadecimais."

    # Verifica existência do arquivo
    arquivo = Path(caminho)
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    # Calcula o hash real do arquivo
    hash_real = hash_file(caminho)

    if hash_real == hash_esperado:
        return True, "✅ AUTÊNTICO: o hash do arquivo confere com o hash informado."
    else:
        return False, (
            "❌ NÃO AUTÊNTICO: o hash do arquivo NÃO confere com o hash informado.\n"
            f"   Hash do arquivo: {hash_real}\n"
            f"   Hash informado:  {hash_esperado}"
        )


def main() -> None:
    """
    Ponto de entrada da aplicação.
    Processa os argumentos de linha de comando e executa o modo solicitado.
    """
    parser = argparse.ArgumentParser(
        description="Autenticador de Arquivos via SHA-256 — "
                    "Gera e verifica hashes de arquivos de qualquer formato.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python file_authenticator.py hash documento.pdf\n"
            "  python file_authenticator.py verify documento.pdf "
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="comando",
        required=True,
        help="Comando a executar",
    )

    # Subcomando: hash
    parser_hash = subparsers.add_parser(
        "hash",
        help="Gera o hash SHA-256 de um arquivo",
        description="Calcula e exibe o hash SHA-256 do arquivo especificado.",
    )
    parser_hash.add_argument(
        "arquivo",
        help="Caminho para o arquivo a ser hasheado",
    )

    # Subcomando: verify
    parser_verify = subparsers.add_parser(
        "verify",
        help="Verifica a autenticidade de um arquivo a partir do hash",
        description=(
            "Calcula o hash SHA-256 do arquivo e compara com o hash informado, "
            "validando ou invalidando a autenticidade."
        ),
    )
    parser_verify.add_argument(
        "arquivo",
        help="Caminho para o arquivo a ser verificado",
    )
    parser_verify.add_argument(
        "hash",
        help="Hash SHA-256 (64 caracteres hexadecimais) esperado para o arquivo",
    )

    args = parser.parse_args()

    try:
        if args.comando == "hash":
            h = hash_file(args.arquivo)
            print(f"SHA-256: {h}")

        elif args.comando == "verify":
            autentico, mensagem = verify_file(args.arquivo, args.hash)
            print(mensagem)
            sys.exit(0 if autentico else 1)

    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
