import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from core.notion_api.client import NotionConnector
from core.document_manager.file_generator import DocumentAlchemist
from core.document_manager.pdf_converter import PdfAlchemist, AlchemyError

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar logging: registra mensajes tanto en consola como en un archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("task_alchemist.log"),
        logging.StreamHandler()
    ]
)

def main():
    try:
        # Inicializar los conectores y gestores de documentos
        notion = NotionConnector()
        alchemist = DocumentAlchemist()
        pdf_alchemist = PdfAlchemist()

        # Obtener las tareas pendientes desde Notion
        tasks = notion.get_pending_tasks()
        logging.info(f"🔮 {len(tasks)} tareas listas para transformación")

        for task in tasks:
            try:
                # Procesar cada tarea: extraer datos y crear el documento
                task_data = parse_notion_task(task)
                file_path = alchemist.create_document(task_data)
                logging.info(f"⚗️ Documento alquimizado: {file_path}")

                # Marcar la tarea como procesada y guardar la ruta del archivo generado
                notion.mark_task_processed(task['id'], file_path)

                # Si la tarea requiere conversión a PDF, realizarla y actualizar Notion
                if task_data.get('convert_to_pdf', False):
                    pdf_path = pdf_alchemist.transmute_to_pdf(file_path)
                    logging.info(f"📜 PDF creado: {pdf_path}")
                    notion.update_task_property(task['id'], "PDF_Path", pdf_path)

            except AlchemyError as ae:
                # Registrar errores específicos en la conversión o generación de documentos
                logging.error(f"🧪 Error procesando tarea {task_data.get('name', 'unknown')}: {str(ae)}")
                continue  # Continuar con la siguiente tarea

    except Exception as e:
        # Registrar cualquier otro error crítico, mostrando la traza completa
        logging.critical(f"🔥 Error en el proceso alquímico: {str(e)}", exc_info=True)

def parse_notion_task(raw_task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforma la respuesta cruda de Notion en datos útiles para generar el documento.

    Args:
        raw_task (Dict[str, Any]): Tarea sin procesar de Notion

    Returns:
        Dict[str, Any]: Datos procesados de la tarea
    """
    props = raw_task.get('properties', {})
    return {
        'name': _get_title_prop(props, 'Name'),
        'subject': _get_select_prop(props, 'Subject'),
        'responsible': _get_multi_select_prop(props, 'Responsible'),
        'file_type': _get_select_prop(props, 'FileType', default='docx'),
        'convert_to_pdf': _get_checkbox_prop(props, 'ConvertToPDF', default=False)
    }

def _get_title_prop(props: dict, field: str) -> str:
    """Extrae el valor de una propiedad de tipo título."""
    return props.get(field, {}).get('title', [{}])[0].get('text', {}).get('content', '') or 'Sin título'

def _get_select_prop(props: dict, field: str, default: str = '') -> str:
    """Extrae el valor de una propiedad de tipo select."""
    return props.get(field, {}).get('select', {}).get('name', default) or default

def _get_multi_select_prop(props: dict, field: str) -> str:
    """Extrae y concatena los valores de una propiedad de tipo multi-select."""
    return ", ".join([item.get('name', 'Desconocido') for item in props.get(field, {}).get('multi_select', [])]) or 'Sin responsables'

def _get_checkbox_prop(props: dict, field: str, default: bool = False) -> bool:
    """Extrae el valor de una propiedad de tipo checkbox."""
    return props.get(field, {}).get('checkbox', default)

if __name__ == "__main__":
    main()
