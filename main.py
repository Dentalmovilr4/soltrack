import os
import time
import json
import requests
import firebase_admin
from firebase_admin import credentials, db

# -------- CONFIG --------
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"

# -------- FIREBASE (REPLIT SECRETS) --------
firebase_url = os.environ['FIREBASE_DB_URL']
service_account_info = json.loads(os.environ['FIREBASE_JSON_DATA'])

if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        'databaseURL': firebase_url
    })

# -------- API --------
def obtener_precio():
    url = f"https://api.dexscreener.com/latest/dex/tokens/{DMR4_MINT}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("pairs"):
            par = data["pairs"][0]
            precio = par.get("priceUsd")
            cambio = par.get("priceChange", {}).get("h24")
            liquidez = par.get("liquidity", {}).get("usd")

            return precio, cambio, liquidez

        return None, None, None

    except Exception as e:
        print(f"⚠️ Error API: {e}")
        return None, None, None

# -------- SYNC --------
def sincronizar_activos():
    ref = db.reference('assets/solana/dmr4')
    print("🚀 Agente Dentalmovilr4 activo en Replit Cloud")
    print("-" * 40)

    while True:
        try:
            precio, cambio, liquidez = obtener_precio()

            if precio:
                ref.update({
                    'precio_usd': float(precio),
                    'cambio_24h': float(cambio) if cambio else 0,
                    'liquidez_usd': float(liquidez) if liquidez else 0,
                    'last_update': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'server': 'Replit-Cloud',
                    'status': 'Online'
                })

                print(f"💎 ${precio} | 24h: {cambio}% | Liquidez: ${liquidez}")
            else:
                print("⏳ Sin datos aún (token sin liquidez en DEX)")

        except Exception as e:
            print(f"⚠️ Error en ciclo: {e}")

        time.sleep(300)  # 5 minutos

# -------- MAIN --------
if __name__ == "__main__":
    sincronizar_activos()