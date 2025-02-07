import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()


class NotionConnector:
    """
    Conector para interactuar con la API de Notion y gestionar tareas académicas.
    """

    def __init__(self):
        # Obtiene la clave de API y el ID de la base de datos desde las variables de entorno
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.base_url = "https://api.notion.com/v1"

        # Define los encabezados necesarios para la autenticación y el tipo de contenido
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """
        Obtiene las tareas pendientes desde la base de datos de Notion.

        Returns:
            List[Dict[str, Any]]: Lista de tareas pendientes.
        """
        # Construir la URL para la consulta a la base de datos de Notion
        url = f"{self.base_url}/databases/{self.database_id}/query"

        # Definir el payload para filtrar las tareas cuyo estado sea "Pendiente"
        payload = {
            "filter": {
                "property": "Estado",
                "select": {"equals": "Pendiente"}
            }
        }

        # Realizar la solicitud POST a la API de Notion con los encabezados y el payload
        response = requests.post(url, headers=self.headers, json=payload)

        # Si la respuesta es exitosa, retorna la lista de tareas; en caso contrario, lanza una excepción
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            raise Exception(f"Error al obtener tareas: {response.text}")

    def mark_task_processed(self, task_id: str, file_path: str):
        """
        Marca una tarea como procesada y almacena la ruta del archivo generado.

        Args:
            task_id (str): ID de la tarea en Notion.
            file_path (str): Ruta del archivo generado.
        """
        # Construir la URL para actualizar la página correspondiente a la tarea
        url = f"{self.base_url}/pages/{task_id}"

        # Definir el payload con las propiedades a actualizar: cambiar el estado y asignar la ruta del archivo
        payload = {
            "properties": {
                "Estado": {"select": {"name": "Procesado"}},
                "Ruta Archivo": {"url": file_path}
            }
        }

        # Realizar la solicitud PATCH para actualizar la tarea en Notion
        response = requests.patch(url, headers=self.headers, json=payload)

        # Si la actualización falla, lanza una excepción con el mensaje de error
        if response.status_code != 200:
            raise Exception(f"Error al actualizar tarea {task_id}: {response.text}")

    def update_task_property(self, task_id: str, property_name: str, value: Any):
        """
        Actualiza una propiedad específica de una tarea en Notion.

        Args:
            task_id (str): ID de la tarea en Notion.
            property_name (str): Nombre de la propiedad a actualizar.
            value (Any): Nuevo valor para la propiedad.
        """
        # Construir la URL para la actualización de la tarea
        url = f"{self.base_url}/pages/{task_id}"

        # Estructurar el payload de acuerdo al tipo de dato que se pase en 'value'
        payload = {
            "properties": {
                property_name: {"url": value} if isinstance(value, str) else value
            }
        }

        # Realizar la solicitud PATCH para actualizar la propiedad especificada
        response = requests.patch(url, headers=self.headers, json=payload)

        # Si la actualización falla, lanza una excepción con el mensaje de error
        if response.status_code != 200:
            raise Exception(f"Error al actualizar propiedad {property_name} en {task_id}: {response.text}")
