import requests
import time
import firebase_admin
from firebase_admin import credentials, db

# CONFIGURACIÓN
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"
DB_URL = "https://miproyectoreact-55e39-default-rtdb.firebaseio.com/"

# INICIALIZAR FIREBASE
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
    print("✅ Conexión estable")
except Exception as e:
    print(f"❌ Error Firebase: {e}")

def obtener_datos():
    data = {}
    try:
        # Precios de Mercado (Capa 1)
        url_cg = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url_cg).json()
        
        # Mapeo para index.html
        data['btc'] = {"precio": r['bitcoin']['usd'], "cambio24h": round(r['bitcoin']['usd_24h_change'], 2)}
        data['eth'] = {"precio": r['ethereum']['usd'], "cambio24h": round(r['ethereum']['usd_24h_change'], 2)}
        data['sol'] = {"precio": r['solana']['usd'], "cambio24h": round(r['solana']['usd_24h_change'], 2)}
        data['bnb'] = {"precio": r['binancecoin']['usd'], "cambio24h": round(r['binancecoin']['usd_24h_change'], 2)}

        # DMR4 (DexScreener)
        url_dex = f"https://api.dexscreener.com/latest/dex/tokens/{DMR4_MINT}"
        r_dex = requests.get(url_dex).json()
        if 'pairs' in r_dex and r_dex['pairs']:
            p = r_dex['pairs'][0]
            data["dmr4"] = {"precio": p.get('priceUsd', "0"), "cambio24h": p.get('priceChange', {}).get('h24', 0)}
        else:
            data["dmr4"] = {"precio": "0.0000", "cambio24h": 0}
            
        return data
    except:
        return None

# BUCLE INFINITO
print("🚀 Motor SolTrack Dentalmovilr4 encendido...")
while True:
    precios = obtener_datos()
    if precios:
        db.reference('mercado').set(precios)
        print(f"📊 Sincronizado {time.strftime('%H:%M:%S')} | BTC: ${precios['btc']['precio']}")
    time.sleep(30)

