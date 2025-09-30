from google import genai
import os
import logging
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Configuração do logging
logger = logging.getLogger(__name__)

key = os.getenv("GEMINI_API_KEY")
def gera_insights():
    try:
        # Verifica se o arquivo de entrada existe
        if not os.path.exists('gold'):
            logger.error(f"Arquivo de entrada não encontrado em: gold")
            return False

        # Lê o arquivo Parquet para um DataFrame do Pandas
        logger.info(f"Lendo o arquivo Parquet: gold")
        dados_csv = pd.read_parquet('gold').to_csv(index=False)
        logger.info("Leitura concluída.")
        # 3. Crie o prompt, fornecendo os dados e a sua pergunta
        prompt = f"""
        Analise os seguintes dados de vendas no formato CSV:

        --- DADOS ---
        {dados_csv}
        --- FIM DOS DADOS ---

                Instruções importantes:
        1.  **Sua resposta deve começar diretamente com o título "Resumo Executivo", sem nenhuma frase introdutória.**
        2.  Deixe a saída em formato markdown.
        3.  Reduza o texto em 25%.
        Mostre Insights relevantes, como principais motivos para mudanças nas taxas de câmbio no dia presente da coluna time_last_update_utc.
        """
        
        # Substitua "SUA_API_KEY" pela chave que você gerou
        client = genai.Client(api_key= key)

        response = client.models.generate_content(model = "gemini-2.5-flash", contents= prompt)
        return response.text
    except Exception as e:
        logger.error(f"Ocorreu um erro ao gerar Insights: {e}")
        return False