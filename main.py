from core.notion.manager import NotionManager
from core.documents.docx_builder import DocxBuilder


def run():
    """
    Ejecuta el flujo principal de TaskAlchemist:
    1. Obtiene tareas pendientes desde Notion
    2. Genera documentos .docx para cada tarea
    3. Actualiza el estado y la ruta del archivo en Notion
    """
    manager = NotionManager()
    tareas = manager.get_tasks(filter_estado="Pendiente")

    for tarea in tareas:
        # Genera el documento .docx a partir de los datos de la tarea
        doc_path = DocxBuilder(tarea).generate()

        # Marca la tarea como completada en Notion
        manager.update_task_status(task_id=tarea["id"], new_status="Completado")

        # Actualiza la ruta del archivo generado
        manager.update_file_metadata(task_id=tarea["id"], file_url=doc_path)


if __name__ == "__main__":
    run()
