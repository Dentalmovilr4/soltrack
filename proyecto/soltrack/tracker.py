import requests
import time
import firebase_admin
from firebase_admin import credentials, db

# -------- CONFIG --------
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"

# -------- FIREBASE --------
def inicializar_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'TU_URL_DE_FIREBASE_AQUI'
            })
            print("✅ Firebase conectado")
        except Exception as e:
            print(f"❌ Error Firebase: {e}")

def actualizar_precio_firebase(precio, cambio):
    try:
        ref = db.reference('assets/solana/dmr4')
        ref.update({
            'precio_usd': float(precio),
            'cambio_24h': float(cambio),
            'status': 'Online',
            'last_update': time.strftime("%Y-%m-%d %H:%M:%S")
        })
        print("📡 Datos enviados a Firebase")
    except Exception as e:
        print(f"❌ Error al actualizar Firebase: {e}")

# -------- API --------
def obtener_precio(mint_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{mint_address}"
    try:
        response = requests.get(url)
        datos = response.json()

        if datos.get('pairs'):
            par = datos['pairs'][0]
            precio = par.get('priceUsd')
            cambio_24h = par.get('priceChange', {}).get('h24')
            return precio, cambio_24h

        return None, None
    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")
        return None, None

# -------- MONITOR --------
def monitor():
    print("🚀 Iniciando SolTrack DMR4 + Firebase")
    print("-" * 40)

    while True:
        precio, cambio = obtener_precio(DMR4_MINT)

        if precio and cambio:
            print(f"💎 DMR4: ${precio} USD | 24h: {cambio}%")
            actualizar_precio_firebase(precio, cambio)
        else:
            print("⏳ Sin datos aún en el DEX...")

        time.sleep(30)

# -------- MAIN --------
if __name__ == "__main__":
    inicializar_firebase()
    monitor()