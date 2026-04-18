import requests
import time
import firebase_admin
from firebase_admin import credentials, db

# 1. CONFIGURACIÓN
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"
DB_URL = "https://miproyectoreact-55e39-default-rtdb.firebaseio.com/"

# 2. INICIALIZAR FIREBASE
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})
    print("✅ Conectado a Firebase correctamente")
except Exception as e:
    print(f"❌ Error al conectar Firebase: {e}")

def obtener_datos_dex():
    url = f"https://api.dexscreener.com/latest/dex/tokens/{DMR4_MINT}"
    try:
        response = requests.get(url)
        datos = response.json()
        if 'pairs' in datos and datos['pairs']:
            par = datos['pairs'][0]
            return {
                "precio": par.get('priceUsd', "0"),
                "cambio24h": par.get('priceChange', {}).get('h24', 0),
                "volumen": par.get('volume', {}).get('h24', 0),
                "actualizado": time.strftime('%Y-%m-%d %H:%M:%S')
            }
        return None
    except Exception as e:
        print(f"⚠️ Error de red: {e}")
        return None

# 3. BUCLE DE ACTUALIZACIÓN
print("🚀 SolTrack en marcha para Dentalmovilr4...")
while True:
    info = obtener_datos_dex()
    if info:
        # Enviamos los datos a la rama 'activos/dmr4'
        ref = db.reference('activos/dmr4')
        ref.set(info)
        print(f"📊 Actualizado en Firebase: ${info['precio']} ({info['cambio24h']}%)")
    else:
        print("🔍 Buscando datos en la blockchain...")
    
    time.sleep(30) # Actualiza cada 30 segundos para no saturar
