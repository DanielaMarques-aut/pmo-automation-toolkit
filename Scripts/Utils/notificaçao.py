"""Slack Notification and Alert System for PMO Reporting

Provides comprehensive integration with Slack for sending PMO reports, alerts, and metrics.
Includes functions for:
- Slack API configuration and validation
- Report generation with custom layouts and metrics
- Webhook-based message sending
- File uploads to Slack channels
- Structured message blocks for professional reporting

All notifications are logged with timestamps for audit purposes.
"""

import requests
import os
import logging
from typing import Optional, Dict, List, Union, Any
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configure professional logging for production monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Report configuration templates with emoji and styling
CONFIG_RELATORIOS: Dict[str, Dict[str, str]] = {
    "diario": {"emoji": "📅", "titulo": "Status Diário de Ops", "cor": "primary"},
    "semanal": {"emoji": "📊", "titulo": "Relatório Semanal PMO", "cor": "primary"},
    "urgente": {"emoji": "🚨", "titulo": "ALERTA CRÍTICO: Risco Elevado", "cor": "danger"}
}


def obter_configuracoes_slack() -> Dict[str, Optional[str]]:
    """
    Load and validate Slack API configuration from environment variables.

    Loads configuration from .env file including webhook URL, API token, and channel ID.
    Validates that all required variables are present and logs missing configurations.

    Returns:
        Dict[str, Optional[str]]: Configuration dictionary with keys:
            - 'webhook_url': Slack incoming webhook URL for message posting
            - 'token': Slack API token for WebClient authentication
            - 'canal_id': Default Slack channel ID for file uploads

    Note:
        - Logs error if .env file is not found
        - Logs error for each missing environment variable
        - Returns a dict even if some values are None (caller must validate)

    Example:
        >>> config = obter_configuracoes_slack()
        >>> if config['token']:
        ...     client = configurar_cliente_slack(config['token'])
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


def configurar_cliente_slack(token: str) -> WebClient:
    """
    Configure and return Slack API WebClient instance with authentication.

    Creates a WebClient instance using the provided authentication token.
    Validates token before instantiation.

    Args:
        token: Slack API authentication token (Bot User OAuth Token).
               Must be a valid token starting with 'xoxb-' or 'xoxp-'.

    Returns:
        WebClient: Configured Slack WebClient instance ready for API calls.

    Raises:
        ValueError: If token is empty, None, or not provided.
        Exception: If WebClient instantiation fails (invalid format, auth error).

    Example:
        >>> client = configurar_cliente_slack('xoxb-your-token-here')
        >>> response = client.chat_postMessage(channel='#general', text='Hello')
    """
    if not token:
        raise ValueError("Token do Slack não configurado")
    try:
        return WebClient(token)
    except Exception as e:
        logging.error(f"🔥 Erro ao instanciar o WebClient: {str(e)}")
        raise


def test_api_configuration() -> None:
    """
    Test Slack API configuration by validating environment variables.

    Loads Slack configuration and checks each required variable. Logs status
    of each configuration item, showing first 5 characters of secrets for safety.
    Useful for debugging and pre-flight validation before using the API.

    Returns:
        None: Only logs information about configuration status.

    Note:
        - Does not raise exceptions (for safe use in tests)
        - Shows truncated tokens/URLs for security (first 5 chars only)
        - Logs both success and missing items to help with troubleshooting
    """
    logging.info("🔍 A testar a configuração da API do Slack...")
    cfg: Dict[str, Optional[str]] = obter_configuracoes_slack()

    for chave in ["webhook_url", "token", "canal_id"]:
        valor: Optional[str] = cfg[chave]
        if valor:
            logging.info(f"{chave}: Configurado (Primeiros 5 caracteres: {valor[:5]}...)")
        else:
            logging.error(f"{chave}: NÃO CONFIGURADO. Verifica .env")


# Helper functions for Slack block construction
def criar_bloco_cabecalho(tipo: str) -> Dict[str, Any]:
    """
    Create a Slack header block with emoji and title based on report type.

    Builds a header block using the Slack Block Kit format, selecting emoji and title
    from CONFIG_RELATORIOS based on the provided type. Falls back to 'diario' if type
    not found.

    Args:
        tipo: Report type key ('diario', 'semanal', or 'urgente').
              Unknown types default to 'diario' configuration.

    Returns:
        Dict[str, Any]: Slack header block dictionary ready for inclusion in blocks array.
                       Format: {"type": "header", "text": {...}}

    Example:
        >>> block = criar_bloco_cabecalho('urgente')
        >>> block['text']['text']
        '🚨 ALERTA CRÍTICO: Risco Elevado'
    """
    conf: Dict[str, str] = CONFIG_RELATORIOS.get(tipo, CONFIG_RELATORIOS["diario"])
    return {
        "type": "header",
        "text": {"type": "plain_text", "text": f"{conf['emoji']} {conf['titulo']}"}
    }


def criar_bloco_campos(dados_campos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create Slack section block with key-value fields from provided data.

    Transforms a dictionary of data into a Slack section block with formatted fields.
    Automatically handles numeric values with percentage formatting (one decimal place).

    Args:
        dados_campos: Dictionary mapping field names (keys) to field values.
                     Values can be numbers (formatted as %) or strings (shown as-is).
                     Example: {'Taxa de Risco': 45.6, 'Status': 'Normal'}

    Returns:
        Dict[str, Any]: Slack section block with mrkdwn formatted fields.
                       Format: {"type": "section", "fields": [...]}

    Note:
        - Numeric values are formatted with one decimal place and '%' suffix
        - String values are displayed as-is
        - Strings are bolded (mrkdwn *text* syntax)

    Example:
        >>> data = {'Taxa de Risco': 35.4, 'Projetos': 'Em Progresso'}
        >>> block = criar_bloco_campos(data)
        >>> block['fields'][0]['text']
        '*Taxa de Risco:*\n35.4%'
    """
    fields: List[Dict[str, str]] = []
    for k, v in dados_campos.items():
        # Format numbers with percentage; keep other types as strings
        if isinstance(v, (int, float)):
            val_str: str = f"{v:.1f}%"
        else:
            val_str = str(v)

        fields.append({
            "type": "mrkdwn",
            "text": f"*{k}:*\n{val_str}"
        })

    return {"type": "section", "fields": fields}


def gerar_report_pmo(tipo_relatorio: str, metricas: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate complete PMO report layout with header, metrics, and footer.

    Combines header block, divider, metrics fields, and footer context into a complete
    report layout ready for Slack messaging. Supports multiple report types with
    appropriate styling.

    Args:
        tipo_relatorio: Type of report ('diario', 'semanal', 'urgente').
                       Determines header emoji, title, and styling.
        metricas: Dictionary of metric names (keys) and values to display.
                 Example: {'Taxa de Risco': 42.5, 'Projetos Ativos': 15}

    Returns:
        List[Dict[str, Any]]: Array of Slack blocks ready for message sending.
                             Includes header, divider, metrics section, and footer.

    Example:
        >>> metrics = {'Taxa de Risco': 35.0, 'Conclusão': 65.0}
        >>> layout = gerar_report_pmo('urgente', metrics)
        >>> len(layout)
        4  # header, divider, section, context
    """
    layout: List[Dict[str, Any]] = [
        criar_bloco_cabecalho(tipo_relatorio),
        {"type": "divider"},
        criar_bloco_campos(metricas),
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "📍 Gerado via AI-Ops Engine v5.0"}]
        }
    ]

    return layout


def construir_payload_visual(pmo_msg: str, url_doc: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Build structured Slack payload with message, action button, and professional styling.

    Creates a complete message payload with header, message body, and call-to-action button.
    Follows Slack Block Kit best practices for professional notification design.

    Args:
        pmo_msg: Main message text to display in the notification body.
                Should be concise and actionable (max 300 chars recommended).
        url_doc: URL for the action button (e.g., link to Excel report or dashboard).
                Must be a valid HTTP/HTTPS URL.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Complete Slack payload with blocks array.
                                        Ready to send via webhook or client.send() method.

    Note:
        - Header is fixed: "📊 Relatório de Operações PMO"
        - Button text: "📁 Ver no Excel"
        - Button style: primary (blue)
        - Message text is bolded for emphasis

    Example:
        >>> payload = construir_payload_visual(
        ...     'Novo alerta de risco detectado',
        ...     'https://example.com/report.xlsx'
        ... )
        >>> # payload ready to send to Slack webhook
    """
    cabecalho: Dict[str, Any] = {
        "type": "header",
        "text": {"type": "plain_text", "text": "📊 Relatório de Operações PMO"}
    }

    corpo: Dict[str, Any] = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": f"*{pmo_msg}*"}
    }

    acoes: Dict[str, Any] = {
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


def gerar_layout_slack(status_emoji: str, taxa_risco: float, total_projetos: float) -> List[Dict[str, Any]]:
    """
    Generate portfolio health status layout for Slack display.

    Creates a formatted Slack block layout showing portfolio health metrics with
    risk percentage and project count. Uses data-to-UI mapping for clean separation.

    Args:
        status_emoji: Emoji to display in header (e.g., '😟', '😐', '😊').
        taxa_risco: Risk percentage (0-100). Usually from portfolio health calculation.
        total_projetos: Number or percentage of active projects.

    Returns:
        List[Dict[str, Any]]: Array of Slack blocks with header, divider, metrics, and footer.

    Example:
        >>> layout = gerar_layout_slack('😟', 45.3, 12.0)
        >>> # layout shows: "😟 Relatório de Saúde...", divider, metrics, footer
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


def enviar_alerta_slack(mensagem: Union[str, Dict[str, Any]], layout: Optional[List[Dict[str, Any]]] = None) -> None:
    """
    Send alert message to Slack via webhook with optional structured blocks.

    Posts a message to Slack using the configured webhook URL. Supports both
    simple text messages and complex structured payloads with Slack blocks.

    Args:
        mensagem: Message content. Can be:
                 - String: Simple text message
                 - Dict: Structured payload (for complex designs)
        layout: Optional list of Slack blocks for structured formatting.
               If provided, creates payload with both text fallback and blocks.

    Returns:
        None: Sends message as side effect. Logs success or failure.

    Raises:
        ValueError: If webhook URL is not configured (.env missing).
        requests.exceptions.RequestException: Network/HTTP errors during POST.

    Note:
        - Logs all responses (success or failure) for audit trail
        - Webhook URL must be configured in .env as 'url_slack'
        - Status code 200 indicates success; warnings logged for other codes
        - All exceptions are logged but not re-raised (fail-safe behavior)

    Example:
        >>> layout = gerar_report_pmo('urgente', {'Risco': 95.0})
        >>> enviar_alerta_slack('Alerta Crítico!', layout)
    """
    cfg: Dict[str, Optional[str]] = obter_configuracoes_slack()
    webhook_url: Optional[str] = cfg["webhook_url"]

    if not webhook_url:
        logging.error("URL do Slack não encontrada no ficheiro .env")
        raise ValueError("URL do Slack não configurada")

    if layout:
        payload: Dict[str, Any] = {"text": mensagem, "blocks": layout}
    elif isinstance(mensagem, dict):
        payload = mensagem
    else:
        payload = {"text": mensagem}

    try:
        response: requests.Response = requests.post(webhook_url, json=payload)
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
