import requests
import time
import os
import json
import firebase_admin
from firebase_admin import credentials, db

# -------- CONFIG --------
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"
DB_URL = "https://miproyectoreact-55e39-default-rtdb.firebaseio.com/"

# -------- INIT FIREBASE --------
def init_firebase():
    try:
        if not firebase_admin._apps:
            if os.path.exists("serviceAccountKey.json"):
                cred = credentials.Certificate("serviceAccountKey.json")
            else:
                cred = credentials.Certificate(json.loads(os.environ['FIREBASE_JSON']))

            firebase_admin.initialize_app(cred, {
                'databaseURL': DB_URL
            })

        print("✅ Firebase conectado")

    except Exception as e:
        print(f"❌ Error Firebase: {e}")

# -------- DATA --------
def obtener_datos():
    try:
        data = {}

        # COINGECKO
        url_cg = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url_cg, timeout=10).json()

        data['btc'] = {"precio": r['bitcoin']['usd'], "cambio24h": round(r['bitcoin']['usd_24h_change'], 2)}
        data['eth'] = {"precio": r['ethereum']['usd'], "cambio24h": round(r['ethereum']['usd_24h_change'], 2)}
        data['sol'] = {"precio": r['solana']['usd'], "cambio24h": round(r['solana']['usd_24h_change'], 2)}
        data['bnb'] = {"precio": r['binancecoin']['usd'], "cambio24h": round(r['binancecoin']['usd_24h_change'], 2)}

        # DEXSCREENER
        url_dex = f"https://api.dexscreener.com/latest/dex/tokens/{DMR4_MINT}"
        r_dex = requests.get(url_dex, timeout=10).json()

        if r_dex.get('pairs'):
            mejor = max(
                r_dex['pairs'],
                key=lambda x: float(x.get('liquidity', {}).get('usd', 0))
            )

            data["dmr4"] = {
                "precio": float(mejor.get('priceUsd', 0)),
                "cambio24h": float(mejor.get('priceChange', {}).get('h24', 0)),
                "liquidez": float(mejor.get('liquidity', {}).get('usd', 0))
            }
        else:
            data["dmr4"] = {"precio": 0, "cambio24h": 0, "liquidez": 0}

        return data

    except Exception as e:
        print(f"⚠️ Error datos: {e}")
        return None

# -------- MAIN --------
init_firebase()
print("🚀 Motor SolTrack activo")

while True:
    precios = obtener_datos()

    if precios:
        try:
            db.reference('mercado').set(precios)
            print(f"📊 {time.strftime('%H:%M:%S')} BTC: ${precios['btc']['precio']} DMR4: ${precios['dmr4']['precio']}")
        except Exception as e:
            print(f"❌ Error Firebase write: {e}")

    time.sleep(30)