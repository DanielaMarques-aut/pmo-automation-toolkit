import os
import pandas as pd

def check_readiness():
    print("--- 🛠️ SUNDAY PRE-FLIGHT CHECK ---")
    
    # Verificar se as pastas de Segunda existem
    path = r"C:\Users\daniq\carrer\Data"
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Pasta {path} criada!")
    
    # Testar se o Pandas está funcional
    test_df = pd.DataFrame({"Status": ["Ready"]})
    print(f"✅ Pandas Status: {test_df['Status'][0]}")
    
    print("\n🚀 Ambiente pronto para as 05:30 de amanhã!")
