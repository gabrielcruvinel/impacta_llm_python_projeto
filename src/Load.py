import pandas as pd
import os
import logging

# Configuração básica do logger para mensagens informativas
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_parquet():

    try:
        # Verifica se o arquivo de entrada existe
        if not os.path.exists('staging/result.csv'):
            logger.error(f"Arquivo de entrada não encontrado em: staging/result.csv")
            return False

        # 1. Lê o arquivo CSV para um DataFrame do Pandas
        logger.info(f"Lendo o arquivo CSV: staging/result.csv")
        df = pd.read_csv('staging/result.csv', sep=';')

        # Garante que o diretório de saída exista
        output_dir = os.path.dirname('gold')
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 2. Salva o DataFrame em formato Parquet
        logger.info(f"Salvando o arquivo Parquet em /gold")
        df.to_parquet('gold', engine='pyarrow', index=False, partition_cols=['base_code', 'data_last_update'])
        
        logger.info("Conversão de CSV para Parquet concluída com sucesso!")
        return True

    except Exception as e:
        logger.error(f"Ocorreu um erro durante a conversão: {e}")
        return False