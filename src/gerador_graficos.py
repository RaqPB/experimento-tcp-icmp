"""
Módulo de Visualização de Dados.

Responsável por gerar os artefatos visuais obrigatórios para o artigo acadêmico.
Consome o dataset do experimento e plota um gráfico comparativo de barras,
salvando a figura em alta resolução para importação direta no LaTeX.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Ingestão do dataset consolidado gerado pelo script de coleta
df = pd.read_csv('dados_experimento.csv')

# O isolamento estrito de pacotes com sucesso impede que falhas de conexão
# (timeouts) sejam contabilizadas, o que distorceria a média real de latência.
df_sucesso = df[df['sucesso'] == True]

# Agregação estatística para obter a métrica principal do gráfico
medias = df_sucesso.groupby('protocolo')['rtt_ms'].mean()

# Configuração da figura com proporções adequadas para caber em uma coluna do formato IEEE
plt.figure(figsize=(8, 5))
cores = ['#2ca02c', '#1f77b4'] # Contraste de cores para facilitar a leitura técnica
medias.plot(kind='bar', color=cores, edgecolor='black')

plt.title('Comparação de Latência Média: ICMP vs TCP')
plt.ylabel('Tempo de Resposta (ms)')
plt.xlabel('Protocolo')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Anotação explícita dos valores exatos sobre as barras para garantir que 
# o leitor do artigo não precise inferir os números apenas olhando para o eixo Y.
for i, valor in enumerate(medias):
    plt.text(i, valor + 0.01, f'{valor:.3f} ms', ha='center', fontweight='bold')

# Ajusta as margens preventivamente para evitar cortes na imagem no PDF final
plt.tight_layout()

# O parâmetro dpi=300 é o padrão ouro de exigência para figuras em publicações científicas
plt.savefig('grafico_latencia.png', dpi=300)
print("Gráfico 'grafico_latencia.png' gerado com sucesso em alta resolução!")