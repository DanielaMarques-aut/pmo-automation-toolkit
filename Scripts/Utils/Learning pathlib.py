from pathlib import Path
from datetime import datetime, timedelta
import shutil

def configurar_ambiente_projeto(nome_projeto: str):
    """
    Cria uma estrutura de pastas profissional para um novo projeto de Ops.
    Princípio Clean Code: Single Responsibility (Esta função só cria pastas).
    
 
    BASES DE PROGRAMAÇÃO: 
    1. Boilerplate: Código inicial necessário para o ambiente.
    2. f-strings: Forma moderna de injetar variáveis em texto.
    """
    # Path.home() garante que funciona no teu PC e no do teu chefe (Portabilidade)
    # Criar caminho para a pasta de logs de forma segura e portável
    base_path = Path.home() / "Desktop" / "PMO_Projects" / nome_projeto
    base_path.mkdir(parents=True, exist_ok=True)
    # Lista de subpastas necessárias
    subpastas = ["01_Inputs", "02_Processamento", "03_Outputs", "04_Archive"]
    
    print(f"--- Iniciando configuração em: {base_path} ---")
    
    for pasta in subpastas:
        caminho_completo = base_path / pasta
        # parents=True cria as pastas pai se não existirem
        # exist_ok=True evita que o script pare se a pasta já lá estiver, evita ifs desnecessários
        caminho_completo.mkdir(parents=True, exist_ok=True)
        print(f"✔ Pasta garantida: {pasta}")

    # Criar um ficheiro de log de boas-vindas
    # Gerar nome de ficheiro com timestamp (evita overwrites)
    log_file = base_path / f"setup_log_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Projeto {nome_projeto} iniciado em {datetime.now()}\n")
        f.write("Recuperação de Quarta-feira concluída.\n")
        f.write(f"Caminho do objeto: {base_path}\n")
        f.write(f"Apenas o nome: {log_file.name}\n")
        f.write(f"Localização do Objeto: {log_file.absolute()}")
    
    print(f"--- Setup concluído. Log em: {log_file.name} ---")
    return base_path

def backup_old_files(source_dir: str, target_dir: str,  base_path: Path, days_trashold: int =25):
        # Definir os caminhos base
        source = Path(base_path/source_dir)
        target = Path(base_path/target_dir)

        # Garantir que a pasta de destino existe
        target.mkdir(parents=True, exist_ok=True)

        # Definir o limite temporal
        now = datetime.now()
        limit_date = now - timedelta(days=days_trashold)

        print(f"--- Iniciando backup: Ficheiros anteriores a {limit_date.strftime('%Y-%m-%d')} ---")

        # Iterar sobre todos os ficheiros na pasta de origem
        for file_path in source.iterdir():
            if file_path.is_file():
                # 1. Obter mtime e converter para datetime
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

                # 2. Comparação
                if mtime < limit_date:
                    try:
                        # Mover o ficheiro (shutil é preferível para mover entre sistemas de ficheiros)
                        shutil.move(str(file_path), str(target / file_path.name))
                        print(f"Movido: {file_path.name} (Modificado em: {mtime.date()})")
                    except Exception as e:
                        print(f"Erro ao mover {file_path.name}: {e}")
        print(f"---Backup concluido com sucesso---")

if __name__ == "__main__":
    Projeto_path = configurar_ambiente_projeto("Automacao_Relatorios_Abril")
    backup_old_files('03_Outputs', '04_Archive', base_path=Projeto_path)