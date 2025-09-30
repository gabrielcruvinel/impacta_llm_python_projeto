import logging
import os
import Ingestor
import Transform
import Load
import Llm
import SendEmail
from dotenv import load_dotenv



load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Configuração do logging
logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logger.info("Iniciando o processo de ETL...")
    
    iso_list = os.getenv("EXCHANGE_ISO").split(",")
    #Etapa 1: Ingestão
    try:
        Ingestor.ingest_exchange(iso_list)
        logger.info("Etapa de Ingestão concluída com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro na etapa de Ingestão: {e}")
        exit(1)

    #Etapa 2: Transformação
    try:
        Transform.extract_json_data(iso_list)
        logger.info("Etapa de Transformação concluída com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro na etapa de Transformacao: {e}")
        exit(1)

    # Etapa 3: Persistencia em Parque ( Load)

    try:
        Load.load_parquet()
        logger.info("Etapa de Load concluída com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro na etapa de Load: {e}")
        exit(1)

    # # Etapa 4: Geração de Insights com LLM
    try:
        texto = Llm.gera_insights()
        logger.info("Etapa de Geração de Insights concluída com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro na etapa de Geração de Insights: {e}")
        exit(1)
    #Enviar o email com os insights
    try:
        SendEmail.envia_email(texto)
        logger.info("Etapa de Envio de E-mail concluída com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro na etapa de Envio de E-mail: {e}")
        exit(1)

    logger.info("Processo de ETL concluído com sucesso.")