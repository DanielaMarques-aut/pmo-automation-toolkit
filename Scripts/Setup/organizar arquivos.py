from pathlib import Path

def organizar_projeto():
    """
    CLEAN CODE: Professional Project Structure.
    Cria as pastas necessárias para um projeto de IA-Ops escalável.
    """
    pastas = ["data", "logs", "scripts", "archive"]
    
    for pasta in pastas:
        p = Path(pasta)
        if not p.exists():
            p.mkdir()
            print(f"✅ Pasta '{pasta}' criada.")
        else:
            print(f"ℹ️ Pasta '{pasta}' já existe.")

def gerar_requirements():
    """
    PROGRAMMING BASE: Dependency Management.
    Lista as bibliotecas que usaste até agora (pandas, requests, python-dotenv).
    """
    libs = ["pandas", "requests", "python-dotenv", "openpyxl"]
    with open("requirements.txt", "w") as f:
        for lib in libs:
            f.write(f"{lib}\n")
    print("✅ Ficheiro requirements.txt gerado.")

def movearquivos():
    source_dir= Path(".")
     
    for file in source_dir.iterdir():
       
        if file.is_file and file.suffix in[".xlsx", ".csv"]:
            targetdir= Path("data")
            targetpath= targetdir/ file.name
            
            if targetpath.exists:
                nam2=f"{file.stem}2{file.suffix}"
                targetpath= targetdir/ nam2
            
            file.rename(targetpath)

        if file.is_file and file.suffix in [".log",".json"]:
            targetdir= Path("logs")
            targetpath= targetdir/ file.name
            print(file.name)
           
            if targetpath.exists:
                nam2=f"{file.stem}2{file.suffix}"
                targetpath= targetdir/ nam2
            
            file.rename(targetpath)
if __name__ == "__main__":
    organizar_projeto()
    gerar_requirements()
    movearquivos()