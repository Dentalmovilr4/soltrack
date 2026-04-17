import requests
import json
import time

# Dirección de contrato de tu moneda DMR4
DMR4_MINT = "3CThGZU6DA6CdRMeYqnW12rtpudL9TgQPFT7qqu4NJ84"
SOL_MINT = "So11111111111111111111111111111111111111112"

def obtener_precio(mint_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{mint_address}"
    try:
        response = requests.get(url)
        datos = response.json()
        
        # Extraer información del par principal
        if datos['pairs']:
            par = datos['pairs'][0]
            precio = par['priceUsd']
            cambio_24h = par['priceChange']['h24']
            return precio, cambio_24h
        return None, None
    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")
        return None, None

def monitor():
    print(f"🚀 Iniciando SolTrack para DMR4...")
    print("-" * 30)
    
    while True:
        precio, cambio = obtener_precio(DMR4_MINT)
        
        if precio:
            print(f"💎 DMR4 Coin: ${precio} USD | 24h: {cambio}%")
        else:
            print("⏳ Buscando liquidez en el DEX...")
            
        time.sleep(30) # Consulta cada 30 segundos

if __name__ == "__main__":
    monitor()
