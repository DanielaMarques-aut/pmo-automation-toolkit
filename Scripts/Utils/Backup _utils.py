from pathlib import Path
import shutil
from datetime import datetime

def backup_outputs():
    """
    PROGRAMMING BASES:
    - shutil: Biblioteca para operações de ficheiros de alto nível (copy/move).
    - Abstração: Criamos uma função simples para uma tarefa complexa.
    """
    # 1. Definir caminhos usando Pathlib (Portabilidade)
    base_path = Path.home() / "Desktop" / "PMO_Projects"
    source = Path.home()/ "carrer"
    backup_root = base_path / "04_Archive" / "Backups"
  
    
    # 2. Criar pasta de backup com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    target_dir = backup_root / f"backup_{timestamp}"
    
    try:
        if source.exists():
            # mkdir(parents=True) cria toda a árvore de pastas se não existir
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar ficheiros (Clean Code: usamos loops para granularidade)
            for file in source.iterdir():
                if file.is_file():
                    shutil.copy(file, target_dir)
                    print(f"✔ Backup realizado: {file.name}")
            for folder in source.iterdir():
                if folder.is_dir():
                    if folder.name.startswith('.'):
                        continue
                    # target_dir / folder.name ensures 'archive' goes into 'backup_timestamp/archive'
                    shutil.copytree(folder, target_dir / folder.name, dirs_exist_ok=True)
                    print(f"✔️ Backup realizado: {folder.name}")
                    
        else:
            print("⚠ Pasta de origem não encontrada. Verifica o caminho!")
            
    except Exception as e:
        print(f"❌ Erro durante o backup: {e}")

if __name__ == "__main__":
    backup_outputs()