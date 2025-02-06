# database/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Task:
    """Modelo para representar una tarea académica"""
    id: str
    name: str
    subject: str
    responsible: List[str]
    due_date: datetime
    created_at: datetime
    status: str
    notes: Optional[str] = None
    file_type: str = 'docx'
    file_path: Optional[str] = None
    pdf_path: Optional[str] = None

    @classmethod
    def from_notion(cls, notion_data: dict) -> 'Task':
        """Crea una instancia de Task desde datos de Notion"""
        props = notion_data.get('properties', {})
        return cls(
            id=notion_data.get('id', ''),
            name=props.get('Name', {}).get('title', [{}])[
                0].get('text', {}).get('content', ''),
            subject=props.get('Subject', {}).get('select', {}).get('name', ''),
            responsible=[item['name'] for item in props.get(
                'Responsible', {}).get('multi_select', [])],
            due_date=datetime.fromisoformat(
                props.get('DueDate', {}).get('date', {}).get('start', '')),
            created_at=datetime.fromisoformat(
                notion_data.get('created_time', '')),
            status=props.get('Status', {}).get('select', {}).get('name', ''),
            notes=props.get('Notes', {}).get('rich_text', [{}])[
                0].get('text', {}).get('content', ''),
            file_type=props.get('FileType', {}).get(
                'select', {}).get('name', 'docx'),
            file_path=props.get('FilePath', {}).get('rich_text', [{}])[
                0].get('text', {}).get('content', ''),
            pdf_path=props.get('PDF_Path', {}).get('rich_text', [{}])[
                0].get('text', {}).get('content', '')
        )
