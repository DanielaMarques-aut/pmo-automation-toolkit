import google.genai as genai
from google.genai import Client

client= Client(api_key="AIzaSyBdAjBcWri0iY3PKHsUeDhxaZE3_bhUKVs")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Olá! Quem és tu?"
)

print(response.text)

