import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from datetime import datetime
import logging  
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do logging
logger = logging.getLogger(__name__)
load_dotenv()


def envia_email(texto_markdown):
    
    email_remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("SENHA_APP")
    email_destinatario = os.getenv("EMAIL_DESTINATARIO")


# Pega a data atual para o assunto do e-mail
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    assunto_email = f"Resumo Financeiro Diário - {data_hoje}"



    html_do_markdown = markdown.markdown(texto_markdown)
    # -- Criando a Mensagem --
    html_final = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{assunto_email}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; background-color: #f4f7f9;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; margin: 20px auto; background-color: #ffffff; border: 1px solid #e0e0e0;">
                <tr>
                    <td style="padding: 30px 40px;">
                        <h1 style="color: #333333; margin: 0; font-size: 24px;">Resumo financeiro diário</h1>
                        
                        <hr style="border: 0; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                        
                        <div class="markdown-content" style="color: #555555; font-size: 16px; line-height: 1.6;">
                            {html_do_markdown}
                        </div>
                    </td>
                </tr>
                <tr>
                    <td align="center" style="padding: 20px; background-color: #fafafa; color: #999999; font-size: 12px;">
                        <p style="margin: 0;">E-mail gerado automaticamente em {data_hoje}.</p>
                        <p style="margin: 5px 0 0 0;">Por favor, não responda a esta mensagem.</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    # Cria a mensagem principal como "multipart" para suportar texto e HTML
    mensagem = MIMEMultipart("alternative")
    mensagem['From'] = email_remetente
    mensagem['To'] = email_destinatario
    mensagem['Subject'] = assunto_email


    # Cria a parte de HTML
    parte_html = MIMEText(html_final, "html")
    mensagem.attach(parte_html)

    # -- Enviando o E-mail --
    try:
        # Conectando ao servidor SMTP do Gmail
        logger.info(f"Realizando conexao copm servidor SMTP")
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()  # Habilitando a criptografia
        servidor.login(email_remetente, senha_app)
        
        # Enviando a mensagem
        texto_mensagem = mensagem.as_string()
        servidor.sendmail(email_remetente, email_destinatario, texto_mensagem)
        logger.info(f"E-mail enviado com sucesso!")
    except Exception as e:
        logger.error(f'Ocorreu um erro ao enviar o e-mail: {e}')
    finally:
        # Fechando a conexão
        servidor.quit()