import os
import json
import logging
import pandas as pd
from datetime import datetime 


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do logging
logger = logging.getLogger(__name__)

def extract_json_data(iso_list):
    #Verifica existencia de dados na pasta raw
    if len(os.listdir('raw')) == 0:
        logger.warning("A pasta 'raw' está vazia. Nenhum dado para processar. Refaça a ingestão.")
        return False
    #leitura dos arquivos json na pasta ra w
    else:
        os.makedirs("staging", exist_ok=True)
        #percorro todos os arquivos da pasta raw
        dados_processados = [] # Lista para armazenar todos os dados para o DataFrame final
        for arquivo in os.listdir('raw'):
            caminho_arquivo = os.path.join('raw', arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as fr:
                data = json.load(fr)
                #PEGO TODOS OS CAMBIOS DA INGESTAO
                rates_dict = data.get('conversion_rates', {})
                base_code = data.get('base_code')
                time_last_update_utc_obj = datetime.strptime(data.get('time_last_update_utc'), '%a, %d %b %Y %H:%M:%S +0000')


                time_last_update_utc = time_last_update_utc_obj.strftime('%Y-%m-%d %H:%M:%S')

                data_last_update = time_last_update_utc_obj.strftime('%Y-%m-%d')
                # aqui trago somente os que estao dentro da iso_list
                conversion_rates = {rate: rates_dict[rate] for rate in iso_list if rate in rates_dict}

                # cria um dicionário base com as informações comuns.
                item_base = {
                    "base_code": base_code,
                    "time_last_update_utc": time_last_update_utc,
                    "data_last_update": data_last_update
                }
                
                # As chaves de 'conversion_rates' viram chaves no nível principal.
                item_pivotado = {**item_base, **conversion_rates}
                # Adiciona o resultado a lista de dados processados
            dados_processados.append(item_pivotado)
        #Gera o arquivo CSV após processar todos os JSONs
        if not dados_processados:
            logger.warning("Nenhum dado foi processado para gerar o CSV.")
            return False
        try:
            # Converte a lista de dicionários em um DataFrame do Pandas
            df = pd.DataFrame(dados_processados)
            
            # Garante que o diretório de saída exista
            output_dir = os.path.dirname('staging')
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            # Salva o DataFrame em um arquivo CSV
            df.to_csv('staging/result.csv', index=False, sep=';', encoding='utf-8-sig')
            
            logger.info(f"Arquivo CSV consolidado salvo com sucesso em staging/result.csv")
            return True
        except Exception as e:
            logger.error(f"Ocorreu um erro ao gerar o arquivo CSV: {e}")
            return False
    return logger.info("Transformação concluída.")
