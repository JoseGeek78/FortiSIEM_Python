"""
Script para FortiSIEM: Consulta IPs con VirusTotal y envía alertas a Telegram.

📌 Requisitos previos:
1. Tener una API Key válida de VirusTotal (https://www.virustotal.com/gui/join-us).
2. Exportar eventos de FortiSIEM en formato CSV que contenga la columna 'src_ip' o 'dst_ip'.
3. Crear un bot en Telegram (https://t.me/BotFather) y obtener:
    - BOT_TOKEN
    - CHAT_ID (puedes obtenerlo usando: https://api.telegram.org/bot<BOT_TOKEN>/getUpdates)

📦 Librerías necesarias:
- pandas
- requests
"""

import pandas as pd
import requests

# === CONFIGURACIÓN ===
VT_API_KEY = "TU_API_KEY_DE_VIRUSTOTAL"
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TU_CHAT_ID"
CSV_PATH = "export_fortisiem.csv"  # Exportado desde FortiSIEM (con columna src_ip o dst_ip)

# === FUNCIONES ===

def consultar_virustotal(ip):
    """
    Consulta una dirección IP en VirusTotal y devuelve:
    - Número de motores que la marcan como maliciosa
    - Número total de motores analizados
    - Categoría general (malicious, suspicious, harmless, etc.)
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "x-apikey": VT_API_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]
        stats = data["attributes"]["last_analysis_stats"]
        category = data["attributes"].get("reputation", "N/A")

        maliciosos = stats.get("malicious", 0)
        total = sum(stats.values())

        return maliciosos, total, data["attributes"].get("country", "N/A")
    else:
        print(f"[!] Error al consultar {ip} en VirusTotal: {response.status_code}")
        return None, None, None

def enviar_telegram(mensaje):
    """
    Envía un mensaje a Telegram usando el bot y chat ID configurado.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

# === LECTURA DE ARCHIVO ===
df = pd.read_csv(CSV_PATH)
ips = df['src_ip'].dropna().unique()  # Cambia a 'dst_ip' si es necesario

# === PROCESAMIENTO DE CADA IP ===
for ip in ips:
    maliciosos, total, pais = consultar_virustotal(ip)
    if maliciosos is not None and maliciosos >= 3:  # Umbral configurable
        mensaje = (
            f"⚠️ *Alerta IOC desde FortiSIEM*\n"
            f"*IP:* {ip}\n"
            f"*País:* {pais}\n"
            f"*Motores maliciosos:* {maliciosos}/{total}\n"
            f"*Fuente:* VirusTotal"
        )
        print(f"[!] IP sospechosa detectada: {ip} ({maliciosos}/{total})")
        enviar_telegram(mensaje)
    else:
        print(f"[✓] IP {ip} no es sospechosa ({maliciosos}/{total})")