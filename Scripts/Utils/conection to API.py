import requests
import logging

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def test_api_connection():
    logging.info("🌐 A tentar conectar com a API de teste...")
    
    # Vamos usar uma API pública de teste (JSONPlaceholder)
    url = "https://jsonplaceholder.typicode.com/todos/1"
    
    try:
        response = requests.get(url)
        
        # Verificar se a ligação teve sucesso (Status 200)
        if response.status_code == 200:
            data = response.json()
            logging.info("✅ Conexão estabelecida com sucesso!")
            print(f"Tarefa recebida da Nuvem: {data['title']}")
        else:
            logging.warning(f"⚠️ Erro de conexão: Status {response.status_code}")
            
    except Exception as e:
        logging.error(f"💥 Falha crítica na API: {e}")
test_api_connection()