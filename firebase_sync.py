import firebase_admin
from firebase_admin import credentials, db

# Inicializa la conexión con Firebase
def inicializar_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'TU_URL_DE_FIREBASE_AQUI'
            })
            print("Conexión exitosa con Firebase Realtime DB")
        except Exception as e:
            print(f"Error al conectar con Firebase: {e}")

# Actualiza el precio en la base de datos
def actualizar_precio_dmr4(precio):
    try:
        ref = db.reference('assets/solana/dmr4')
        ref.update({
            'precio': precio,
            'status': 'Online',
            'last_update': 'Sincronizado desde Google Cloud'
        })
        print("Precio actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar precio: {e}")

if __name__ == "__main__":
    inicializar_firebase()
    actualizar_precio_dmr4(1.23)  # Cambia este valor por el precio real
