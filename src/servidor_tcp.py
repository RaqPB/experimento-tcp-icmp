"""
Módulo Servidor Echo TCP (Stateless).

Atua como o endpoint de destino para o experimento de medição de latência.
A arquitetura foi projetada para forçar o encerramento da conexão a cada pacote,
permitindo a captura precisa do custo (overhead) do 3-way handshake do TCP.
"""

import socket

HOST = '127.0.0.1'
PORT = 65432

def iniciar_servidor():
    """
    Inicializa o socket TCP em modo de escuta contínua no loopback local.
    Ouve requisições ativamente e, ao conectar, processa apenas um payload 
    antes de destruir a sessão.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # Habilita SO_REUSEADDR para permitir a reinicialização rápida do script 
        # pelo sistema operacional sem aguardar o timeout do estado TIME_WAIT.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        print(f"Servidor Echo TCP rodando em {HOST}:{PORT}...")
        print("Pressione Ctrl+C para encerrar.\n")
        
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        conn.sendall(data)
                    # Ao sair do bloco 'with conn', o socket do cliente é fechado.
                    # Isso é intencional para forçar um novo handshake no próximo disparo.
            
            except KeyboardInterrupt:
                print("\nServidor encerrado pelo usuário.")
                break
            except Exception:
                # O tratamento silencioso (pass) garante que conexões abandonadas 
                # pelo cliente devido a timeouts não derrubem o loop principal.
                pass

if __name__ == "__main__":
    iniciar_servidor()