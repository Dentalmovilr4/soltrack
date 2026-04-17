import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Esta función conectará tu código con la base de datos de Dentalmovilr4
def inicializar_firebase():
    # En la nube usaremos variables de entorno por seguridad
    # Por ahora, puedes probar con el archivo JSON de credenciales
    if not firebase_admin._apps:
        try:
            # Aquí buscaremos el archivo de llaves que subas luego
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'TU_URL_DE_FIREBASE_AQUI'
            })
            print("✅ Conexión exitosa con Firebase Realtime DB")
        except Exception as e:
            print(f"❌ Error al conectar con Firebase: {e}")

def actualizar_precio_dmr4(precio):
    ref = db.reference('assets/solana/dmr4')
    ref.update({
        'precio': precio,
        'status': 'Online',
        'last_update': 'Sincronizado desde Google Cloud'
    })

if __name__ == "__main__":
    inicializar_firebase()
