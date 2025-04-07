import os
from notion_client import Client
from typing import List, Dict
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

class NotionManager:
    def __init__(self):
        # Inicializa el cliente de Notion con el token de la API
        self.client = Client(auth=os.getenv("NOTION_API_KEY"))
        # ID de la base de datos de Notion donde se encuentran las tareas
        self.database_id = os.getenv("DATABASE_ID")

    def get_tasks(self, filter_estado: str = "Pendiente") -> List[Dict]:
        """
        Obtiene tareas desde Notion con un estado específico.

        Args:
            filter_estado (str): Estado de las tareas a filtrar (por defecto 'Pendiente')

        Returns:
            List[Dict]: Lista de tareas con propiedades procesadas
        """
        response = self.client.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Estado",
                "select": {"equals": filter_estado}
            }
        )

        tasks = []
        for result in response.get("results", []):
            # Extrae propiedades clave de cada tarea
            tarea = {
                "id": result["id"],
                # Accede al texto plano del título de la tarea
                "nombre": result["properties"]["Tareas"]["title"][0]["plain_text"],
                # Toma el primer valor del multi-select de asignaturas
                "asignatura": result["properties"]["Asignaturas"]["multi_select"][0]["name"],
                "tipo_archivo": result["properties"]["Tipo de archivo"]["select"]["name"],
                "fecha_entrega": result["properties"]["Fecha de entrega"]["date"]["start"],
                # Obtiene la primera nota o una cadena vacía si no existe
                "nota": result["properties"].get("Nota", {}).get("rich_text", [{}])[0].get("plain_text", "")
            }
            tasks.append(tarea)
        return tasks

    def update_task_status(self, task_id: str, new_status: str) -> None:
        """
        Actualiza el estado de una tarea en Notion.

        Args:
            task_id (str): ID de la página de la tarea
            new_status (str): Nuevo valor del campo Estado (ej: 'Completado')
        """
        self.client.pages.update(
            page_id=task_id,
            properties={
                "Estado": {"select": {"name": new_status}}
            }
        )

    def update_file_metadata(self, task_id: str, file_url: str) -> None:
        """
        Actualiza la propiedad de URL de archivo en la tarea.

        Args:
            task_id (str): ID de la página de la tarea
            file_url (str): URL o ruta local del archivo generado
        """
        self.client.pages.update(
            page_id=task_id,
            properties={
                "Ruta del archivo": {"url": file_url}
            }
        )