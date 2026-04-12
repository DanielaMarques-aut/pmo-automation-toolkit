"""
Módulo para agregação e análise de dados de PMO (Project Management Office).

Este módulo fornece funções para carregar dados de CSV, validar e sanitizar os dados,
calcular métricas de saúde do portfólio de projetos e gerar relatórios formatados.
Também inclui funcionalidades para envio de notificações via Slack.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, List, Union
import notificaçao
from notificaçao import gerar_report_pmo
from testaiproject import analisar_risco_com_ia
from testaiproject import consultar_mitigação_ia

# Configuração de Logs persistentes (conforme o teu sucesso de ontem!)
logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s - %(message)s')


def carregar_dados(caminho_csv: str) -> Optional[pd.DataFrame]:
    """
    Carrega dados de um arquivo CSV e valida a existência do arquivo.

    Args:
        caminho_csv (str): Caminho absoluto ou relativo para o arquivo CSV.

    Returns:
        pd.DataFrame or None: DataFrame com os dados carregados se bem-sucedido,
                              None se o arquivo não existir ou houver erro na leitura.

    Raises:
        Nenhum: Erros são logados e None é retornado.
    """
    if not Path(caminho_csv).exists():
        logging.error(f"❌ Ficheiro crítico em falta: {caminho_csv}")
        return None

    try:
        df = pd.read_csv(caminho_csv)
        logging.info(f"✅ CSV carregado: {caminho_csv} ({len(df)} linhas)")
        return df
    except Exception as e:
        logging.error(f"💥 Erro ao carregar CSV '{caminho_csv}': {e}")
        return None


def validar_colunas(df: pd.DataFrame, colunas_esperadas: List[str]) -> bool:
    """
    Verifica se o DataFrame contém todas as colunas necessárias.

    Args:
        df (pd.DataFrame): DataFrame a ser validado.
        colunas_esperadas (list): Lista de nomes das colunas que devem estar presentes.

    Returns:
        bool: True se todas as colunas estiverem presentes, False caso contrário.
    """
    faltam = [c for c in colunas_esperadas if c not in df.columns]
    if faltam:
        logging.error(f"💥 Colunas em falta: {faltam}")
        return False
    return True


def sanitizar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove valores nulos e converte tipos de dados nas colunas-chave.

    Args:
        df (pd.DataFrame): DataFrame a ser sanitizado.

    Returns:
        pd.DataFrame: DataFrame sanitizado com tipos convertidos e nulos removidos.
    """
    if df['Status'].isnull().any():
        logging.warning("⚠️ Encontrados valores nulos no Status. A limpar...")
        df = df.dropna(subset=['Status'])

    
    df['Tempo_Gasto']=pd.to_numeric(df.get('Tempo_Gasto', pd.Series(dtype='float64')), errors='coerce').fillna(0)
    if 'Tempo_Gasto' in df.columns:
       df['Tempo Gasto'] = df['Tempo_Gasto'].astype(str).str.replace('h', '', case=False)
       df['Tempo_Gasto'] = pd.to_numeric(df['Tempo_Gasto'], errors='coerce')
        
    print(df)

    return df


def preparar_dados(caminho_csv: str) -> Optional[pd.DataFrame]:
    """
    Pipeline completa para carregamento, validação e sanitização dos dados.

    Args:
        caminho_csv (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame or None: DataFrame preparado se bem-sucedido, None em caso de falha.
    """
    df = carregar_dados(caminho_csv)
    if df is None:
        return None

    colunas_esperadas = ['Status', 'Projeto', "Tempo_Gasto"]
    if not validar_colunas(df, colunas_esperadas):
        return None
   
    

    return sanitizar_dados(df)


def calcular_metrica_saude(df: pd.DataFrame):
    """
    Calcula métricas de saúde do portfólio de projetos.

    Args:
        df (pd.DataFrame): DataFrame com os dados dos projetos.

    Returns:
        dict or None: Dicionário com as métricas calculadas ou None se não houver tarefas.
    """
    total_tarefas = len(df)
    if total_tarefas == 0:
        logging.warning("⚠️ O ficheiro CSV está vazio. Não há tarefas para calcular.")
        return None

    atrasados = len(df[df['Status'] == 'Atrasado'])
    concluidos = len(df[df['Status'] == 'Concluído'])
    nao_reportados = int(df['Tempo_Gasto'].isna().sum())

    df.loc[df['Tempo_Gasto'].isna(), 'Status'] = 'Erro de Reporte'

    base = total_tarefas - nao_reportados
    percentual_risco = (atrasados / base) * 100 if base > 0 else 0
    taxa_conclusao = (concluidos / base) * 100 if base > 0 else 0
    taxa_nao_reportados = (nao_reportados / total_tarefas) * 100
    print(total_tarefas)
 

    if percentual_risco > 50:
        logging.warning(f"⚠️ Alta taxa de risco detectada: {percentual_risco:.1f}% dos projetos estão atrasados.")
    if taxa_conclusao < 50:
        logging.warning(f"⚠️ Baixa taxa de conclusão detectada: Apenas {taxa_conclusao:.1f}% dos projetos estão concluídos.")
    if taxa_nao_reportados > 20:
        logging.warning(f"⚠️ Alta taxa de não reportados: {taxa_nao_reportados:.1f}% das tarefas não têm tempo gasto reportado.")
    if [df['Status'] == 'Atrasado']:
        test=analisar_risco_com_ia([df['Projeto']],5)
        
    return {
        'total_tarefas': total_tarefas,
        'percentual_risco': percentual_risco,
        'taxa_conclusao': taxa_conclusao,
        'taxa_nao_reportados': taxa_nao_reportados,
        'respostaai': test,
        
        
    }


def formatar_relatorio_kpis(kpis: Optional[Dict[str, Union[int, float]]]) -> str:
    """
    Formata as métricas calculadas em um relatório de texto.

    Args:
        kpis (dict or None): Dicionário com as métricas ou None.

    Returns:
        str: Relatório formatado em texto.
    """
    if kpis is None:
        return "Nenhuma tarefa encontrada no relatório."

    return (
      # f"📊 *Resumo de Saúde do Portfólio*\n"
       #f"Total de Projetos: {kpis['total_tarefas']}\n"
       #f"🔴 Taxa de Risco: {kpis['percentual_risco']:.1f}%\n"
       #f"🟢 Taxa de Conclusão: {kpis['taxa_conclusao']:.1f}%\n"
       #f"🟡 Taxa de Não Reportados: {kpis['taxa_nao_reportados']:.1f}%\n"
       kpis
    )


def calcular_saude_projeto(caminho_csv: str) -> Optional[str]:
    """
    Função principal para calcular a saúde do projeto a partir de um CSV.

    Args:
        caminho_csv (str): Caminho para o arquivo CSV.

    Returns:
        str or None: Relatório formatado ou None em caso de falha.
    """
    df = preparar_dados(caminho_csv)
    if df is None:
        logging.error("💥 Falha na preparação dos dados.")
        return None

    kpis = calcular_metrica_saude(df)
    if [df['Status'] == 'Atrasado']:
        test=analisar_risco_com_ia([df['Projeto']],5)
        analise= consultar_mitigação_ia([df['Projeto']],5,kpis)
    if kpis is not None:
        return formatar_relatorio_kpis(kpis), analise
    else:
        return "Relatório não gerado: Projeto não está atrasado.", analise


def enviar_notificacoes(resultado, arquivo, analise_ia=None, canal=notificaçao.obter_configuracoes_slack().get("canal_id")):
                                      #envia notificações  com o resultado do cálculo.
    """
Args: 
       Resultado (str or None): Relatório a ser enviado ou None em caso de falha.
        arquivo (str): Caminho do arquivo para anexar.
        canal (str): ID do canal do Slack (padrão: notificaçao.CANAL_ID).
""" 

    if not resultado:
        payload = notificaçao.construir_payload_visual(
            "💥 Falha ao calcular a saúde do projeto. Verifique os logs para detalhes.",
            "https://www.exemplo.com/relatorio-pmo.xlsx",
        )
        notificaçao.enviar_alerta_slack(payload)
        return

    notificaçao.test_api_configuration()
    payload = notificaçao.construir_payload_visual(resultado, "https://www.exemplo.com/relatorio-pmo.xlsx")
    layout_final= notificaçao.gerar_report_pmo("diario", resultado)
    if analise_ia:
        bloco_ia = {
            "type": "section",
            "text": {
                "type": "mrkdwn", 
                "text": f"*🤖 Análise da IA (Mitigação):*\n>{analise_ia}"
            }
        }
        # Adicionamos o bloco ao final da lista de blocos do payload
        payload["blocks"].append(bloco_ia)
    notificaçao.enviar_alerta_slack(payload, layout_final)
    notificaçao.enviar_ficheiro_slack(arquivo, canal)

if __name__ == "__main__":
    caminho = 'dados_pmo_segunda2.csv'
   # 1. Recebe os dois valores separadamente (Unpacking)
    relatorio_kpis, analise_ia = calcular_saude_projeto(caminho)
    enviar_notificacoes(relatorio_kpis, caminho, analise_ia=analise_ia)

    if  relatorio_kpis:
     print( relatorio_kpis, analise_ia)
    else:
        logging.error("💥 Falha ao calcular a saúde do projeto. Verifique os logs para detalhes.")
        enviar_notificacoes(resultado, caminho) 
    