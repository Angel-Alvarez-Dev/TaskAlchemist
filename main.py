from core.notion.manager import NotionManager
from core.documents.docx_builder import DocxBuilder

def run():
    manager = NotionManager()
    tareas = manager.get_tasks(filter_estado="Pendiente")

    for tarea in tareas:
        doc_path = DocxBuilder(tarea).generate()
        manager.update_task_status(tarea["id"], "Completado")
        manager.update_file_metadata(tarea["id"], doc_path)

if __name__ == "__main__":
    run()
