import requests
import time
import firebase_admin
from firebase_admin import credentials, db

# 1. CONFIGURACIÓN (Dentalmovilr4)
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"
DB_URL = "https://miproyectoreact-55e39-default-rtdb.firebaseio.com/"
CRYPTO_IDS = "bitcoin,ethereum,solana,binancecoin"

# 2. INICIALIZAR FIREBASE (Evita errores si ya está inicializado)
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
    print("✅ Conectado a Firebase correctamente")
except Exception as e:
    print(f"❌ Error al conectar Firebase: {e}")

def obtener_datos():
    data_final = {}
    # Diccionario para convertir nombres largos a cortos (para tu index.html)
    nombres_cortos = {
        "bitcoin": "btc",
        "ethereum": "eth",
        "solana": "sol",
        "binancecoin": "bnb"
    }
    
    try:
        # A. Obtener Precios del Mercado (BTC, ETH, SOL, BNB)
        cg_url = f"https://api.coingecko.com/api/v3/simple/price?ids={CRYPTO_IDS}&vs_currencies=usd&include_24hr_change=true"
        res_cg = requests.get(cg_url).json()

        for coin in res_cg:
            nombre_web = nombres_cortos.get(coin, coin)
            data_final[nombre_web] = {
                "precio": res_cg[coin]['usd'],
                "cambio24h": round(res_cg[coin]['usd_24h_change'], 2)
            }

        # B. Obtener Precio de DMR4 (DexScreener)
        dex_url = f"https://api.dexscreener.com/latest/dex/tokens/{DMR4_MINT}"
        res_dex = requests.get(dex_url).json()

        if 'pairs' in res_dex and res_dex['pairs']:
            par = res_dex['pairs'][0]
            data_final["dmr4"] = {
                "precio": par.get('priceUsd', "0"),
                "cambio24h": par.get('priceChange', {}).get('h24', 0)
            }
        else:
            data_final["dmr4"] = {"precio": "0.0000", "cambio24h": 0}

        return data_final
    except Exception as e:
        print(f"⚠️ Error capturando datos: {e}")
        return None

# 3. BUCLE DE ACTUALIZACIÓN 24/7
print("🚀 Motor SolTrack Dentalmovilr4 a toda marcha...")
while True:
    datos = obtener_datos()
    if datos:
        # Guardamos todo en la rama 'mercado' para que la web lo lea
        db.reference('mercado').set(datos)
        # Log simplificado para la terminal
        print(f"📊 {time.strftime('%H:%M:%S')} | BTC: ${datos['btc']['precio']} | DMR4: ${datos['dmr4']['precio']}")
    else:
        print("🔍 Reintentando conexión en el próximo ciclo...")

    time.sleep(30) # Actualiza cada 30 segundos

