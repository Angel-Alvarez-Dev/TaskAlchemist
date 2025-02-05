# main.py
from core.notion_api.client import NotionConnector
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()


def main():
    """Punto de entrada principal del alquimista digital"""
    try:
        # Inicializar conexión con Notion
        connector = NotionConnector()

        # Obtener tareas de la base de datos
        database_id = os.getenv("NOTION_DATABASE_ID")
        tasks = connector.get_database(database_id)

        # TODO: Procesamiento alquímico de tareas
        print(f"🔮 {len(tasks)} tareas listas para transformación")

    except Exception as e:
        print(f"⚡ Error en el ritual: {str(e)}")


if __name__ == "__main__":
    main()
