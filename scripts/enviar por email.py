# Script para enviar email com anexo usando Python
# 1. Configuração do Email (Usando App Passwords para segurança)
# 2. Construção da Mensagem (Assunto, Corpo e Anexo)
# 3. Envio do Email (Tratamento de erros para garantir que o processo é robusto)    
# O objetivo é automatizar o envio de relatórios diários para a equipa PMO, garantindo que todos os stakeholders recebem as informações atualizadas sem falhas.


import smtplib
from email.message import EmailMessage
import os
# 1. Definir apenas o caminho da pasta
pasta_output = r"C:\Users\daniq\carrer\Output"

# 2. Listar todos os ficheiros na pasta para ver o que existe lá
print(f"🔍 Verificando ficheiros em: {pasta_output}")
try:
    ficheiros_na_pasta = os.listdir(pasta_output)
    print(f"📁 Ficheiros encontrados: {ficheiros_na_pasta}")
except Exception as e:
    print(f"❌ Erro ao acessar a pasta: {e}")
def enviar_alerta_pmo(assunto, corpo, nome_ficheiro):   # Configuração (Para Gmail, usa App Passwords)
    EMAIL_ADDRESS = "teu_email_aqui@gmail.com"
    EMAIL_PASSWORD = "tua-app-password"

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS # Envia para ti mesma como log
    msg.set_content(corpo)
    print("📧 Preparando para enviar alerta por email...")
    pathname = rf"C:\Users\daniq\carrer\Output\{nome_ficheiro}"
    try:
        with open(pathname, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(
                file_data, 
                maintype='application', 
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                filename=nome_ficheiro
            )
    except FileNotFoundError:
        print(f"❌ Erro: O ficheiro {pathname} não foi encontrado!")
        return
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)   
                smtp.send_message(msg)
                print("🚀 Alerta enviado com sucesso!")
    except Exception as e:
        print(f"❌ Falha ao enviar alerta: {e}")
        print(f"❌ Falha no envio: {e}")
enviar_alerta_pmo("Relatório Diário de Operações - PMO", "Olá,\n\nSegue em anexo o relatório Excel gerado automaticamente.\n\nCumprimentos,", 'resumo_executivo_terca (2).xlsx')
