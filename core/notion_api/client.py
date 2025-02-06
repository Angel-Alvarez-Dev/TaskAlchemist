# core/notion_api/client.py
from notion_client import Client
import os
from dotenv import load_dotenv


class NotionClient:
    def __init__(self):
        load_dotenv()
        self.client = Client(auth=os.getenv('NOTION_TOKEN'))
        self.database_id = os.getenv('NOTION_DATABASE_ID')

    def get_tasks(self):
        """Obtiene todas las tareas de la base de datos de Notion"""
        try:
            response = self.client.databases.query(
                database_id=self.database_id
            )
            return response['results']
        except Exception as e:
            print(f"Error al obtener tareas: {e}")
            return []

    def create_task(self, task_data):
        """Crea una nueva tarea en la base de datos de Notion"""
        try:
            properties = {
                "Nombre": {"title": [{"text": {"content": task_data['nombre']}}]},
                "Asignatura": {"select": {"name": task_data['asignatura']}},
                "Fecha Entrega": {"date": {"start": task_data['fecha_entrega']}},
                "Responsables": {"multi_select": [{"name": r} for r in task_data['responsables']]},
                "Estado": {"select": {"name": task_data['estado']}},
                "Tipo Archivo": {"select": {"name": task_data['tipo_archivo']}},
                "Ruta": {"rich_text": [{"text": {"content": task_data.get('ruta', '')}}]}
            }

            self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            return True
        except Exception as e:
            print(f"Error al crear tarea: {e}")
            return False
