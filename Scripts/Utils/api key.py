import os
from dotenv import load_dotenv
import google.genai as genai
import time
from google.api_core import exceptions

# PROGRAMMING BASE: Environment Isolation
# We never hardcode keys. We load them from the environment.
load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
else:
    client= genai.Client(api_key=api_key)
    print("✅ Gemini API Secured and Ready.")

# CLEAN CODE PRINCIPLE: Fail Early
# We check if the key exists before running the whole script. 
# This prevents wasting cloud compute/tokens on a broken setup.
# Now we can list available models to confirm the client works.
for model in client.models.list():
    print(f"Available model: {model.name}")
def generate_with_retry(model_name, contents, retries=3):
    """
    CLEAN CODE: Resilience Pattern
    Implementa um 'Backoff' simples. Se o servidor 503 falhar, 
    esperamos uns segundos e tentamos de novo.
    """
    for i in range(retries):
        try:
            return client.models.generate_content(model=model_name, contents=contents)
        except exceptions.InternalServerError:
            wait_time = (i + 1) * 2 # Espera 2s, depois 4s...
            print(f"⚠️ Servidor ocupado (503). A tentar novamente em {wait_time}s...")
            time.update(wait_time)
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            break
    return None
# You then use this client to interact with models
response = generate_with_retry( 
    model_name="gemini-flash-latest",
    contents="A# INSTRUCTIONS: Create a dummy 'projects.csv' with columns: ProjectName, Deadline, Status, Manager, Budget"
)
if response:
    print("✅ Resposta recebida do modelo:")
    print(response.text)