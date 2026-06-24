"""
Módulo Coletor de Dados.

Responsável por orquestrar a bateria de testes comparativos de latência e integridade 
entre o protocolo TCP (Camada de Aplicação/Transporte) e ICMP (Camada de Rede).
Gera um dataset estruturado (CSV) para posterior análise estatística.
"""

import socket
import time
import subprocess
import csv

HOST = '127.0.0.1'
PORT = 65432
ITERACOES = 100
PAYLOAD = b'Attack_on_Packet_Echo'

def executar_experimento_tcp():
    """
    Executa iterações TCP individuais contra o endpoint do servidor Echo.
    A arquitetura desta função abre e fecha um socket distinto para cada iteração.
    Isso isola e contabiliza intencionalmente o tempo de estabelecimento da conexão
    (3-way handshake) e de encerramento, permitindo uma comparação justa de 
    overhead com pacotes "connectionless" do ICMP.
    """
    resultados = []
    print(f"Executando {ITERACOES} iterações do experimento TCP (1 conexão por pacote)...")
    
    for i in range(1, ITERACOES + 1):
        inicio = time.perf_counter()
        sucesso = False
        rtt_ms = 0
        
        try:
            # O socket instanciado dentro do laço garante a recriação da conexão.
            # Isso impede o reaproveitamento de rotas e força o protocolo a pagar o custo 
            # de handshake em todas as iterações, essencial para a métrica do artigo.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0) # Previne congelamento do script em caso de perda de pacote.
                s.connect((HOST, PORT))
                s.sendall(PAYLOAD)
                data = s.recv(1024)
                
                # Validação estrita de integridade exigida pela metodologia do trabalho.
                if data == PAYLOAD:
                    fim = time.perf_counter()
                    rtt_ms = (fim - inicio) * 1000
                    sucesso = True
                    
        except socket.timeout:
            print(f"[-] TCP Amostra {i} perdida (Timeout)")
        except ConnectionRefusedError:
            print(f"[-] TCP Amostra {i} falhou (Servidor offline?)")
            
        resultados.append({
            "id_pacote": i,
            "protocolo": "TCP",
            "rtt_ms": round(rtt_ms, 4) if sucesso else None,
            "sucesso": sucesso
        })
        
        # Mitiga sobrecarga de buffer e esgotamento de portas locais rápidas (TIME_WAIT).
        time.sleep(0.01)
            
    return resultados

def coletar_amostra_icmp():
    """
    Executa medições de latência ICMP delegando o processo ao subsistema do SO.
    Utiliza o comando 'ping' nativo do kernel do Linux para obter o tempo de resposta
    base da rede, sem o peso da travessia pela pilha de aplicação em Python.
    """
    print(f"Executando {ITERACOES} iterações de amostragem ICMP (Ping do SO)...")
    resultados = []
    
    # O parâmetro '-c' é mandatório em distribuições Linux (para Windows o parâmetro é '-n')
    # para evitar que o ping entre em um loop infinito no terminal.
    comando = ['ping', '-c', str(ITERACOES), HOST]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    id_pacote = 1
    for linha in resultado.stdout.split('\n'):
        if 'time=' in linha:
            # Parseamento do output padrão do terminal para extração do RTT puro.
            tempo_str = linha.split('time=')[1].split(' ')[0]
            resultados.append({
                "id_pacote": id_pacote,
                "protocolo": "ICMP",
                "rtt_ms": float(tempo_str),
                "sucesso": True
            })
            id_pacote += 1
            
    # Reconciliação de dados: Garante que pacotes perdidos no terminal também 
    # sejam registrados no dataset final como falhas de entrega.
    while len(resultados) < ITERACOES:
        resultados.append({
            "id_pacote": len(resultados) + 1,
            "protocolo": "ICMP",
            "rtt_ms": None,
            "sucesso": False
        })
        
    return resultados

if __name__ == "__main__":
    dados_tcp = executar_experimento_tcp()
    dados_icmp = coletar_amostra_icmp()
    
    dados_totais = dados_tcp + dados_icmp
    
    # A exportação em CSV puro garante que os dados brutos permaneçam imutáveis
    # e prontos para serem ingeridos e transformados pelo script de análise.
    if dados_totais:
        with open('dados_experimento.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["id_pacote", "protocolo", "rtt_ms", "sucesso"])
            writer.writeheader()
            writer.writerows(dados_totais)
        print("\nExperimento concluído! Arquivo 'dados_experimento.csv' gerado.")