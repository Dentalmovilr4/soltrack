import os
import time
import json
import requests
import firebase_admin
from firebase_admin import credentials, db

# 1. Cargar secretos desde la nube de Replit
firebase_url = os.environ['FIREBASE_DB_URL']
service_account_info = json.loads(os.environ['FIREBASE_JSON_DATA'])

# 2. Inicializar Firebase (Aquí no hay error de memoria, Replit aguanta)
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        'databaseURL': firebase_url
    })

def sincronizar_activos():
    ref = db.reference('assets/solana/dmr4')
    print("🚀 Agente Dentalmovilr4 activo en la nube...")
    
    while True:
        try:
            # Aquí irá tu lógica de SolTrack para obtener el precio real
            # Por ahora usamos un placeholder para probar la conexión
            precio_actual = 0.0052 
            
            ref.update({
                'precio': precio_actual,
                'last_update': time.ctime(),
                'server': 'Replit-Cloud'
            })
            print(f"✅ Sincronizado correctamente a las {time.ctime()}")
            
        except Exception as e:
            print(f"⚠️ Error en el ciclo: {e}")
        
        time.sleep(300) # Actualiza cada 5 minutos para ahorrar recursos

if __name__ == "__main__":
    sincronizar_activos()
