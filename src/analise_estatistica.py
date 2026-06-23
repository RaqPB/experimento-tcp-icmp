"""
Módulo de Análise de Dados.

Responsável por ingerir os dados brutos gerados pelo experimento de rede,
aplicar transformações estatísticas utilizando a biblioteca Pandas e 
estruturar a tabela final de resultados. A saída formatada deste script 
está pronta para ser transcrita diretamente para a seção de Resultados 
do artigo acadêmico.
"""

import pandas as pd

# Ingestão do dataset consolidado gerado pelo script de coleta
df = pd.read_csv('dados_experimento.csv')

# O isolamento estrito de pacotes com sucesso é mandatório matematicamente.
# Incluir pacotes perdidos (timeouts) no cálculo de tempo distorceria a 
# métrica de latência real da rede.
df_sucesso = df[df['sucesso'] == True]

# Agregação estatística das métricas de tempo (Round-Trip Time)
metricas = df_sucesso.groupby('protocolo')['rtt_ms'].agg(['min', 'max', 'mean']).reset_index()
metricas.columns = ['Protocolo', 'Latência Mínima (ms)', 'Latência Máxima (ms)', 'Latência Média (ms)']

# Contagem absoluta da volumetria do experimento para apuração de integridade
total_pacotes = df.groupby('protocolo').size().reset_index(name='total')
pacotes_perdidos = df[df['sucesso'] == False].groupby('protocolo').size().reset_index(name='perdidos')

# A utilização de um merge à esquerda (left join) seguido de fillna(0) 
# garante que protocolos com 100% de integridade (zero perdas) não desapareçam da tabela.
perdas_df = pd.merge(total_pacotes, pacotes_perdidos, on='protocolo', how='left').fillna(0)

# Consolidação do dataframe final cruzando métricas de tempo com métricas de perda
metricas = pd.merge(metricas, perdas_df[['protocolo', 'perdidos']], left_on='Protocolo', right_on='protocolo')
metricas = metricas.drop('protocolo', axis=1)
metricas.rename(columns={'perdidos': 'Pacotes Perdidos'}, inplace=True)

print("=== INFORMAÇÕES COLETADAS ===")
print(metricas.round(3).to_string(index=False))