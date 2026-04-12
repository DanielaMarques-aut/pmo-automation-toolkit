import os
from google import genai
from dotenv import load_dotenv
# CLEAN CODE: Carregamento centralizado de configurações
# 1. Setup: Carregar a chave do cofre (.env)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


# 2. Configurar o Motor (Kernel)
# Clean Code Principle: Encapsulate the connection in a client object
client = genai.Client(api_key=api_key)

# 3. Execução: O teu primeiro prompt via Código
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Olá Gemini! Confirma que o meu script está ligado?"
)

print(f"Resposta da AI: {response.text}")

# Instead of asking if it's on, send it the status
status_info = "Status: Service running, CPU: 12%, Memory: 450MB"
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=(f"Analise este status do meu script de Ops: {status_info}")
)

print(f"Resposta da AI: {response.text}")

# Optional: List available models to verify connection
print("\nModelos disponíveis:")
for m in client.models.list():
    print(f"- {m.name}")