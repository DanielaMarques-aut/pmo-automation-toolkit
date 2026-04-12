import requests
import os
import logging
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Optional, Dict, Union


# Configuração de Logs profissional: essencial para monitorizar o que acontece em produção
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_RELATORIOS = {
    "diario": {"emoji": "📅", "titulo": "Status Diário de Ops", "cor": "primary"},
    "semanal": {"emoji": "📊", "titulo": "Relatório Semanal PMO", "cor": "primary"},
    "urgente": {"emoji": "🚨", "titulo": "ALERTA CRÍTICO: Risco Elevado", "cor": "danger"}
}
def obter_configuracoes_slack() -> Dict[str, Optional[str]]:
    """
    Extrai variáveis de configuração do Slack do arquivo .env e valida sua existência.

    Carrega as variáveis de ambiente necessárias para a integração com o Slack,
    incluindo webhook URL, token de API e ID do canal.

    Returns:
        dict: Dicionário contendo as configurações do Slack com as chaves:
            - 'webhook_url': URL do webhook do Slack
            - 'token': Token de API do Slack
            - 'canal_id': ID do canal do Slack

    Raises:
        Nenhum erro é levantado diretamente, mas logs de erro são gerados se o .env não for encontrado.
    """
    if not load_dotenv():
        logging.error("ERRO: Ficheiro .env não encontrado na pasta atual.")

    config: Dict[str, Optional[str]] = {
        "webhook_url": os.getenv("url_slack"),
        "token": os.getenv("key"),
        "canal_id": os.getenv("id"),
    }
    for chave, valor in config.items():
        if valor is None:
            logging.error(f"❌ Variável de ambiente para '{chave}' não definida!")
    return config

def configurar_cliente_slack(token: str)-> WebClient:
    """
    Configura e retorna uma instância do cliente WebClient para a API do Slack.

    Args:
        token (str): Token de autenticação da API do Slack.

    Returns:
        WebClient: Instância configurada do cliente Slack.

    Raises:
        ValueError: Se o token não for fornecido ou estiver vazio.
    """
    if not token:
        raise ValueError("Token do Slack não configurado")
    try:
        # Retorna a instância tipada
        return WebClient(token)
    except Exception as e:
        logging.error(f"🔥 Erro ao instanciar o WebClient: {str(e)}")
        raise


def test_api_configuration()-> None:
    """
    Testa a configuração da API do Slack verificando se as variáveis necessárias estão definidas.

    Carrega as configurações do Slack e verifica cada variável crítica,
    logando o status de configuração ou alertando sobre valores ausentes.
    Útil para depuração e validação antes de usar a API.

    Returns:
        None: Esta função não retorna valores, apenas loga informações.
    """
    logging.info("🔍 A testar a configuração da API do Slack...")
    cfg:Dict[str, Optional[str]] = obter_configuracoes_slack()

    for chave in ["webhook_url", "token", "canal_id"]:
        valor:Optional[str] = cfg[chave]
        if valor:
            logging.info(f"{chave}: Configurado (Primeiros 5 caracteres: {valor[:5]}...)")
        else:
            logging.error(f"{chave}: NÃO CONFIGURADO. Verifica .env")


# --- BASES: ESTRUTURAS DE DADOS ---
# Usamos dicionários (dict) e listas (list) para representar o JSON do Slack.
def criar_bloco_cabecalho(tipo: str) -> dict:
    conf = CONFIG_RELATORIOS.get(tipo, CONFIG_RELATORIOS["diario"])
    return {
        "type": "header",
        "text": {"type": "plain_text", "text": f"{conf['emoji']} {conf['titulo']}"}
    }
def criar_bloco_campos(dados_campos: dict) -> dict:
    # Transforma um dicionário de dados numa lista de campos mrkdwn
    fields = []
    for k, v in dados_campos.items():
        # Check if the value is a number before applying float formatting
        if isinstance(v, (int, float)):
            val_str = f"{v:.1f}%"
        else:
            val_str = str(v)
            
        fields.append({
            "type": "mrkdwn",
            "text": f"*{k}:*\n{val_str}"
        })
    
    return {"type": "section", "fields": fields}

def gerar_report_pmo(tipo_relatorio: str, metricas: dict) -> list:
    """
    ENGINE: Constrói qualquer relatório baseado no tipo e nos dados fornecidos.
    """
    layout = [
        criar_bloco_cabecalho(tipo_relatorio),
        {"type": "divider"},
        criar_bloco_campos(metricas),
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "📍 Gerado via AI-Ops Engine v5.0"}]
        }
    ]
    
    return layout
def construir_payload_visual(pmo_msg: str, url_doc: str) -> Dict[str, list[Dict[str,any]]]:
    """
    Constrói um payload visual estruturado para mensagens do Slack usando blocos.

    Cria uma mensagem formatada com cabeçalho, corpo de texto e botão de ação,
    seguindo as melhores práticas de design do Slack para notificações visuais.

    Args:
        pmo_msg (str): Mensagem principal a ser exibida no corpo da notificação.
        url_doc (str): URL do documento (ex.: link para o relatório Excel) para o botão.

    Returns:
        dict: Payload estruturado em formato de blocos do Slack, pronto para envio.
    """
    cabecalho:Dict[str, any]={
        "type": "header",
        "text": {"type": "plain_text", "text": "📊 Relatório de Operações PMO"}
    }

    corpo = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": f"*{pmo_msg}*"}
    }

    acoes = {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "📁 Ver no Excel"},
                "url": url_doc,
                "style": "primary"
            }
        ]
    }

    return {"blocks": [cabecalho, corpo, acoes]}
def gerar_layout_slack(status_emoji, taxa_risco, total_projetos):
    """
    CLEAN CODE: Data-to-UI Mapping.
    Constrói a estrutura de blocos (Nested Dictionaries) para a API do Slack.
    """
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{status_emoji} Relatório de Saúde do Portfólio*"
            }
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Taxa de Risco:*\n{taxa_risco:.1f}%"},
                {"type": "mrkdwn", "text": f"*Projetos Ativos:*\n{total_projetos:.1f}%"}
            ]
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "📍 Gerado automaticamente pelo AI-Ops Agent v4.0"}
            ]
        }
    ]


def enviar_alerta_slack(mensagem,layout):
    """
    Envia uma mensagem de alerta para o Slack via webhook.

    Suporta tanto mensagens de texto simples quanto payloads estruturados em blocos.
    Valida a configuração do webhook antes do envio e trata erros de API.

    Args:
        mensagem (str or dict): Conteúdo da mensagem. Pode ser uma string de texto
            simples ou um dicionário com payload estruturado (ex.: blocos do Slack).

    Returns:
        None: Esta função não retorna valores, apenas envia a notificação.

    Raises:
        ValueError: Se a URL do webhook não estiver configurada.
        requests.exceptions.RequestException: Para erros de rede ou HTTP.
    """
    cfg = obter_configuracoes_slack()
    webhook_url = cfg["webhook_url"]

    if not webhook_url:
        logging.error("URL do Slack não encontrada no ficheiro .env")
        raise ValueError("URL do Slack não configurada")
    if layout:
        payload= {"text": mensagem,"blocks":layout}
    elif isinstance(mensagem, dict):
        payload = mensagem 
           
   
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logging.info("✅ Notificação enviada para o Slack com sucesso!")
        else:
            logging.warning(f"⚠️ Falha no Slack: {response.status_code} - {response.text}")
            response.raise_for_status()
    except Exception as e:
        logging.error(f"💥 Erro crítico na API do Slack: {e}")


def enviar_ficheiro_slack(caminho_local, canal=None):
    """
    Envia um arquivo para um canal do Slack usando a API de arquivos.

    Faz upload de um arquivo local para o Slack, especificando um comentário inicial
    e título. Suporta especificar um canal diferente do padrão.

    Args:
        caminho_local (str): Caminho absoluto ou relativo para o arquivo a ser enviado.
        canal (str, optional): ID do canal do Slack. Se não fornecido, usa o canal
            padrão configurado no .env.

    Returns:
        None: Esta função não retorna valores, apenas faz upload do arquivo.

    Raises:
        ValueError: Se o ID do canal não estiver configurado.
        SlackApiError: Para erros específicos da API do Slack, como bot não estar no canal.
        FileNotFoundError: Se o arquivo especificado não existir no caminho_local.
    """
    cfg = obter_configuracoes_slack()
    token = cfg["token"]
    canal_id = canal or cfg["canal_id"]
    

    if not canal_id:
        raise ValueError("ID do canal Slack não configurado")

    client = configurar_cliente_slack(token)

    try:
        logging.info(f"🔍 Enviando ficheiro '{caminho_local}' para o canal '{canal_id}' no Slack...")
        response = client.files_upload_v2(
            channel=canal_id,
            file=caminho_local,
            title="Relatório PMO Semanal",
            initial_comment="📊 Aqui está o Excel atualizado com as métricas de Ops."
        )

        if response.get("ok"):
            logging.info("✅ Upload V2 concluído com sucesso!")
        else:
            erro = response.get("error", "desconhecido")
            logging.error(f"❌ Erro na API do Slack ao enviar ficheiro: {erro}")

    except SlackApiError as e:
        erro = e.response.get("error", "desconhecido")
        if erro == "not_in_channel":
            logging.error(f"⚠️ Convida o Bot para o canal {canal_id} antes de enviar!")
        else:
            logging.error(f"❌ Erro na API do Slack: {erro}")
            logging.error(f"💥 Ficheiro não encontrado no caminho: {caminho_local}")


def main():
    """
    Função principal para demonstração e teste das funcionalidades de notificação do Slack.

    Executa uma sequência de testes incluindo validação de configuração,
    envio de mensagem visual e upload de arquivo. Serve como exemplo de uso
    das funções do módulo.

    Returns:
        None: Esta função não retorna valores, apenas executa operações de teste.
    """
    
    test_api_configuration()
    msg_texto = "O script detetou 3 tarefas em atraso no relatório de Terça-feira."
    link_dummy = "https://www.exemplo.com/relatorio-pmo.xlsx"
    msg_payload = construir_payload_visual(msg_texto, link_dummy)
    Layout= gerar_layout_slack(":)","22,5%", 15)
    metricas_semana=(":)", "15%", 16)
    layout_final = gerar_report_pmo("diario", metricas_semana)
    enviar_alerta_slack(msg_payload, layout_final)
    caminho_excel = "Relatorio_Formatado_pmo.xlsx"
    enviar_ficheiro_slack(caminho_excel)
   



if __name__ == "__main__":
    main()
