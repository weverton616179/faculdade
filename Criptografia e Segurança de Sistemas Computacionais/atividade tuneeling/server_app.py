"""
Aplicação Servidora do Chat Criptografado.
Aguarda conexão do cliente, realiza handshake de chaves públicas RSA
e inicia o chat bidirecional com criptografia assimétrica.
"""

import socket
import sys
import threading
from crypto_utils import (
    gerar_chaves,
    serializar_chave_publica,
    desserializar_chave_publica,
    criptografar_mensagem,
    descriptografar_mensagem,
)

# Configurações de rede
HOST = '127.0.0.1'
PORTA = 5000


def enviar_dados(sock: socket.socket, dados: bytes) -> None:
    """
    Envia dados pelo socket com prefixo de 4 bytes indicando o tamanho.
    """
    tamanho = len(dados)
    sock.sendall(tamanho.to_bytes(4, byteorder='big'))
    sock.sendall(dados)


def receber_dados(sock: socket.socket) -> bytes:
    """
    Recebe dados do socket, lendo primeiro o prefixo de 4 bytes com o tamanho.
    Retorna bytes vazios se a conexão for fechada.
    """
    # Lê os 4 bytes do tamanho
    header = sock.recv(4)
    if not header:
        return b''
    tamanho = int.from_bytes(header, byteorder='big')

    # Lê o payload completo
    dados = bytearray()
    while len(dados) < tamanho:
        restante = tamanho - len(dados)
        parte = sock.recv(min(restante, 4096))
        if not parte:
            break
        dados.extend(parte)
    return bytes(dados)


def thread_receber(sock: socket.socket, chave_privada) -> None:
    """
    Thread que fica escutando mensagens do parceiro, descriptografa e exibe.
    """
    while True:
        try:
            dados_cripto = receber_dados(sock)
            if not dados_cripto:
                print("\n[!] Conexão encerrada pelo parceiro.")
                break

            # Exibe o ciphertext para demonstração acadêmica
            print(f"\n[DEBUG] Mensagem cifrada recebida ({len(dados_cripto)} bytes): "
                  f"{dados_cripto[:40].hex()}...")

            # Descriptografa com a chave privada
            mensagem = descriptografar_mensagem(dados_cripto, chave_privada)
            print(f"\n[Parceiro]: {mensagem}\n[Você]: ", end='', flush=True)

        except (ConnectionError, OSError) as e:
            print(f"\n[!] Erro de conexão: {e}")
            break
        except Exception as e:
            print(f"\n[!] Erro ao processar mensagem: {e}")
            break

    print("\n[*] Encerrando chat. Pressione Enter para sair...")
    sys.exit(0)


def main():
    print("=" * 60)
    print("  CHAT CRIPTOGRAFADO COM RSA - MODO SERVIDOR")
    print("=" * 60)

    # --- Geração de chaves ---
    print("\n[*] Gerando par de chaves RSA (1024 bits)...")
    chave_publica, chave_privada = gerar_chaves()
    print("[✓] Chaves geradas com sucesso!")

    # --- Configuração do socket servidor ---
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PORTA))
        servidor.listen(1)
        print(f"[*] Aguardando conexão em {HOST}:{PORTA}...")

        sock, endereco = servidor.accept()
        print(f"[✓] Cliente conectado: {endereco[0]}:{endereco[1]}")

        # --- Handshake: Troca de chaves públicas ---
        print("\n[*] Iniciando handshake - troca de chaves públicas...")

        # Envia a chave pública (PKCS1)
        minha_chave_bytes = serializar_chave_publica(chave_publica)
        enviar_dados(sock, minha_chave_bytes)
        print("[→] Chave pública enviada ao cliente.")

        # Recebe a chave pública do cliente
        chave_parceiro_bytes = receber_dados(sock)
        chave_publica_parceiro = desserializar_chave_publica(chave_parceiro_bytes)
        print("[←] Chave pública do cliente recebida.")

        print("[✓] Handshake concluído. Chaves públicas trocadas com sucesso!")
        print("-" * 60)

        # --- Inicia thread de recebimento ---
        thread_recv = threading.Thread(
            target=thread_receber,
            args=(sock, chave_privada),
            daemon=True,
        )
        thread_recv.start()

        # --- Loop principal de envio ---
        print("\n[*] Chat iniciado! Digite suas mensagens.")
        print("[*] Digite '/sair' para encerrar.\n")

        while True:
            mensagem = input('[Você]: ')

            if mensagem.lower() == '/sair':
                print("[*] Encerrando conexão...")
                break

            if not mensagem.strip():
                continue

            # Criptografa com a chave pública do parceiro
            dados_cripto = criptografar_mensagem(mensagem, chave_publica_parceiro)

            # Exibe o ciphertext gerado para demonstração acadêmica
            print(f"[DEBUG] Mensagem cifrada enviada ({len(dados_cripto)} bytes): "
                  f"{dados_cripto[:40].hex()}...")

            try:
                enviar_dados(sock, dados_cripto)
            except (ConnectionError, OSError) as e:
                print(f"\n[!] Erro ao enviar: {e}")
                break

    except KeyboardInterrupt:
        print("\n[*] Servidor interrompido pelo usuário.")
    except Exception as e:
        print(f"\n[!] Erro inesperado: {e}")
    finally:
        try:
            sock.close()
        except Exception:
            pass
        try:
            servidor.close()
        except Exception:
            pass
        print("[*] Conexão fechada. Até logo!")


if __name__ == '__main__':
    main()
