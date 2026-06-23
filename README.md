# Análise Comparativa de Latência: TCP vs ICMP

Este repositório contém o código-fonte, os dados e a análise estatística de um experimento laboratorial focado em medir o *overhead* (custo computacional e de rede) associado à garantia de integridade do protocolo TCP em comparação com a latência do protocolo ICMP.

Este projeto foi desenvolvido como parte de um Artigo Científico (formato IEEE) para o curso de Sistemas de Informação.

## Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Bibliotecas:** `socket`, `subprocess`, `pandas`, `matplotlib`
* **Ambiente de Teste:** Zorin OS (Linux) - *O experimento depende do kernel Linux para execução de parâmetros nativos do ICMP.*

## Arquitetura do Experimento e Estrutura de Pastas
A coleta e análise dos dados são divididas em 4 módulos autônomos localizados na pasta `/src`. Todos os scripts necessários para a reprodução estão concentrados nela:

1. `servidor_tcp.py`: Endpoint receptor (Stateless Echo Server).
2. `experimento_protocolos.py`: Dispara as requisições TCP isoladas (forçando o 3-way handshake) e executa o ping (ICMP) nativo do SO. Ao final, gera o arquivo `dados_experimento.csv` diretamente na pasta `src/`.
3. `analise_estatistica.py`: Processamento de dados via Pandas para geração da tabela comparativa a partir do arquivo csv recém-criado na pasta `src/`.
4. `gerador_graficos.py`: Renderização visual dos resultados da latência a partir do arquivo csv, gerando e salvando a imagem final dentro da pasta `src/`.

> **⚠️ Nota sobre os arquivos do repositório:** As pastas `/dados` e `/imagens` presentes na raiz deste repositório contêm **apenas** os arquivos estáticos exatos (o CSV e o PNG) que foram gerados em nossa execução principal e utilizados para escrever o artigo final. Novas execuções do experimento gerarão os novos arquivos temporários dentro da pasta `src/`.

## Como Reproduzir o Experimento

**1. Clone o repositório e instale as dependências:**
```bash
git clone [https://github.com/RaqPB/experimento-tcp-icmp.git](https://github.com/RaqPB/experimento-tcp-icmp.git)
cd experimento-tcp-icmp
pip install -r requisitos.txt

2. Navegue até a pasta de código-fonte (src/):
Para que o experimento funcione corretamente, o seu terminal deve obrigatoriamente estar dentro da pasta src/, pois os códigos geram e leem os arquivos a partir do diretório atual.
```bash
cd src


3. Inicie o Servidor TCP:
Ainda dentro da pasta src/, inicie o servidor (ele ficará aguardando conexões e pode ser deixado em segundo plano):
```bash
python3 servidor_tcp.py


4. Execute a Coleta de Dados:
Abra uma nova aba ou janela no terminal, acesse novamente a pasta src/ (cd src) e inicie a bateria de testes:
```bash
python3 experimento_protocolos.py


(Aguarde aproximadamente 2 minutos até o fim do processo. Após a conclusão, o arquivo dados_experimento.csv será gerado e ficará salvo na pasta src/).

5. Gere a Tabela Estatística:
Com o arquivo CSV gerado, execute a análise para processar a tabela estatística que aparecerá no seu terminal:
```bash
python3 analise_estatistica.py


6. Gere o Gráfico de Resultados:
Por fim, rode o gerador de visualização. A imagem com o gráfico de barras (grafico_latencia.png) será criada e salva automaticamente dentro da pasta src/:
```bash
python3 gerador_graficos.py


Autor: Raquel Pereira