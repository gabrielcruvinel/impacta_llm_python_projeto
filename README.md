# Projeto Final - Pipeline de Cotações Cambiais com Python + LLM
## Integrantes


## 📌 Descrição
Este projeto implementa um pipeline de dados para coleta, processamento e análise de cotações cambiais, utilizando Python.
O fluxo segue o conceito de camadas (raw, staging, gold) e inclui a integração com uma LLM (Large Language Model) para gerar insights automáticos e interativos em linguagem natural.

Ele tambem contempla o envio de um email informativo ao final da execução, afim de que os responsaveis pelo negocio possam receber de forma simples os reports das operações

## 🚀 Estrutura do Projeto
```
├── .env  # Variaveis de ambiente
├── requirements.txt 
├── gold # Pasta com arquivos parquet particionado pelo nome do cambio e data
├── raw # Pasta de dados bruta
├── src #Pasta com codigos fonte
    ├── Ingestor.py # ETL De Injestao de dados
    ├── Llm.py # ETL de geração de Insights
    ├── Load.py # ETL de Carga de Dados
    ├── SendEmail.py # Envio de email
    ├── Transform.py # ETL de Transformação os dados brutos 
    └── main.py
└── staging #Cama intermediaria de dados, que armazena a transformacao em CSV
```

# Clone repositorio
```
git clone https://github.com/gabrielcruvinel/impacta_llm_python_projeto.git
```

# Acesso ao repositorio
```
cd impacta_llm_python_projeto
```

# Criar e ativar ambiente virtual
```
python -m venv python_llm
Linux: source ./python_llm/bin/activate
Windows: ./python_llm/scripts/activate
```

# Instale as dependências
```
pip install -r requirements.txt
```

# 🔑 Variáveis de Ambiente (.env)
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo (exemplo):

```
API_EXCHANGE_KEY = chave_api_exchange
GEMINI_API_KEY = gemini_key
EXCHANGE_ISO = "USD,EUR,JPY,GBP,AUD,CAD,CHF,CNY,HKD,NZD,BRL,INR"
EMAIL_REMETENTE = 'email_remetente@gmail.com' -> Precisa ser gmail
SENHA_APP = 'senha_16_digitos'
EMAIL_DESTINATARIO = 'email_destiono@email.com'
```

# Como Executar o Projeto
 Apos criado o .ENV com as keys definidas anteriormente, basta ativar o venv e executar
  ```
 python src/main.py
 ```

 # Exemplos de insight:
 Por utilizar cargas historicas pontuais e comparar com outros cambios pre processados, o LLM consegue ver uma evolução ou decrescimo entre as moedas e analisar quais os principais motivos impactaram a volatilidade daquele cambio

 "Qual moeda teve uma maior valorização dentro do periodo analisado ? "


 " Qual obteve uma menor desvalorização ?"
  
 Estes são exemplos de insights gerados e enviados via email pela aplicação

 # Tecnologias Empregadas
  - Python ( Pandas, Logging,  dontenv,)
  - Api Gemini

# Entrega
 - Codigo no GITHUB
 - Dados parquet em /gold
 - Readme Documentado
 # Desenvolvido por:
 ```
Caio Macedo Santos - 2502444
 Gabriel Gonçalves Cruvinel - 2502454
 ```