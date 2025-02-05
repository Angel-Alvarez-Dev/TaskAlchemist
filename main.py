# main.py

from typing import Dict, Any  # Import necesario para type hints
from core.notion_api.client import NotionConnector
from core.document_manager.file_generator import DocumentAlchemist
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    try:
        notion = NotionConnector()
        alchemist = DocumentAlchemist()

        tasks = notion.get_pending_tasks()
        print(f"🔮 {len(tasks)} tareas listas para transformación")

        for task in tasks:
            task_data = parse_notion_task(task)
            file_path = alchemist.create_document(task_data)
            print(f"⚗️ Documento alquimizado: {file_path}")
            notion.mark_task_processed(task['id'], file_path)

    except Exception as e:
        print(f"🔥 Error en el proceso alquímico: {str(e)}")


def parse_notion_task(raw_task: Dict[str, Any]) -> Dict[str, str]:
    """Transforma la respuesta cruda de Notion en datos útiles"""
    props = raw_task.get('properties', {})
    return {
        'name': _get_title_prop(props, 'Name'),
        'subject': _get_select_prop(props, 'Subject'),
        'responsible': _get_multi_select_prop(props, 'Responsible'),
        'file_type': _get_select_prop(props, 'FileType', default='docx')
    }


def _get_title_prop(props: dict, field: str) -> str:
    return props.get(field, {}).get('title', [{}])[0].get('text', {}).get('content', '')


def _get_select_prop(props: dict, field: str, default: str = '') -> str:
    return props.get(field, {}).get('select', {}).get('name', default)


def _get_multi_select_prop(props: dict, field: str) -> str:
    return ", ".join([item['name'] for item in props.get(field, {}).get('multi_select', [])])


if __name__ == "__main__":
    main()
