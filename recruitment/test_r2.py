from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_r2_connection():
    try:
        print("Iniciando prueba de conexión con R2...")
        # Crear archivo de prueba
        test_content = "Test content"
        path = default_storage.save('test.txt', ContentFile(test_content))
        print(f"Archivo creado: {path}")
        
        # Verificar existencia
        exists = default_storage.exists(path)
        print(f"¿Archivo existe? {exists}")
        
        # Eliminar archivo de prueba
        default_storage.delete(path)
        print("Archivo eliminado")
        
        print("¡Conexión exitosa!")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False