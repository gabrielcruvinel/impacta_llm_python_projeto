import requests
import os
import json
from datetime import datetime
import logging


API_EXCHANGE_KEY = os.getenv("API_EXCHANGE_KEY")


# Configura o logging para exibir mensagens no console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do logging
logger = logging.getLogger(__name__)
def ingest_exchange(iso_list):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("raw", exist_ok=True)
    logger.info("Iniciando ingestão de dados...")
    for sigla in iso_list:
        url = f"https://v6.exchangerate-api.com/v6/{API_EXCHANGE_KEY}/latest/"
        path = f"{url}/{sigla}"
        try:
            response = requests.get(path)
            data = response.json()
            filename = f"raw/{sigla}_{today}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2) 
            logger.info(f"INGESTOR - Dados salvos em .raw\{filename}\n") 
        except requests.RequestException as e:
            logger.error(f"Erro ao conectar à API: {e}")       