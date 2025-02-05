# core/document_manager/file_generator.py
import os
from pathlib import Path
from docx import Document
from datetime import datetime
from typing import Dict


class DocumentAlchemist:
    def __init__(self, base_path: str = os.getenv("DOCUMENTS_DIR", "documents")):
        self.base_path = Path(os.path.expanduser(base_path))

    def create_document(self, task_data: Dict) -> str:
        """Transform task data into a structured document"""
        file_type = task_data.get('file_type', 'docx')
        subject = task_data.get('subject', 'Uncategorized')
        task_name = task_data.get('name', 'Untitled')
        responsible = task_data.get('responsible', 'Anonymous')

        # Create directory structure
        file_path = self.base_path / subject / \
            task_name / f"{responsible}_v1.{file_type}"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create document based on type
        if file_type == 'docx':
            self._create_word_doc(file_path, task_data)
        elif file_type == 'pptx':
            self._create_powerpoint(file_path, task_data)
        # Add other formats here...

        return str(file_path)

    def _create_word_doc(self, path: Path, data: Dict):
        """Alchemize data into a structured Word document"""
        doc = Document()

        # Add cover page
        doc.add_heading(data['name'], 0)
        doc.add_paragraph(f"Subject: {data['subject']}")
        doc.add_paragraph(f"Responsible: {data['responsible']}")
        doc.add_paragraph(
            f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        doc.add_page_break()

        # Add content sections
        doc.add_heading("Main Content", 1)
        doc.add_paragraph("Start your magical work here...")

        # Add references section
        doc.add_heading("References", 1)
        doc.add_paragraph("• Insert your sources here")

        doc.save(path)
