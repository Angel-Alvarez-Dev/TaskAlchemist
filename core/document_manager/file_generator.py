# core/document_manager/file_generator.py

import os
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from typing import Dict, Optional, Union
import logging
from pptx import Presentation
from pptx.util import Inches as PptxInches

logger = logging.getLogger(__name__)


class DocumentTemplates:
    """Plantillas predefinidas para diferentes tipos de documentos"""

    @staticmethod
    def get_word_styles() -> Dict:
        return {
            'title': {'size': 24, 'bold': True, 'align': WD_ALIGN_PARAGRAPH.CENTER},
            'subtitle': {'size': 16, 'bold': True},
            'heading1': {'size': 14, 'bold': True},
            'normal': {'size': 12},
            'footer': {'size': 10, 'italic': True}
        }

    @staticmethod
    def get_document_sections() -> Dict:
        return {
            'academic': ['Introduction', 'Development', 'Conclusion', 'References'],
            'report': ['Executive Summary', 'Methods', 'Results', 'Discussion', 'References'],
            'presentation': ['Overview', 'Content', 'Summary']
        }


class DocumentAlchemist:
    def __init__(self, base_path: str = os.getenv("DOCUMENTS_DIR", "documents")):
        """
        Inicializa el alquimista de documentos

        Args:
            base_path (str): Ruta base para almacenar documentos
        """
        self.base_path = Path(os.path.expanduser(base_path))
        self.templates = DocumentTemplates()
        self._ensure_base_path()

    def create_document(self, task_data: Dict) -> str:
        """
        Transforma los datos de la tarea en un documento estructurado

        Args:
            task_data (Dict): Datos de la tarea de Notion

        Returns:
            str: Ruta del archivo creado

        Raises:
            ValueError: Si el tipo de archivo no es soportado
            OSError: Si hay problemas al crear el archivo
        """
        try:
            file_type = task_data.get('file_type', 'docx').lower()
            subject = task_data.get('subject', 'Uncategorized')
            task_name = self._sanitize_filename(
                task_data.get('name', 'Untitled'))
            responsible = task_data.get('responsible', 'Anonymous')

            # Crear estructura de directorios
            file_path = self._generate_file_path(
                subject, task_name, responsible, file_type)

            # Crear documento según el tipo
            creator_method = getattr(self, f'_create_{file_type}', None)
            if creator_method is None:
                raise ValueError(f"Unsupported file type: {file_type}")

            creator_method(file_path, task_data)
            logger.info(f"Document created successfully: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            raise

    def _create_docx(self, path: Path, data: Dict):
        """Crea un documento Word estructurado"""
        doc = Document()
        styles = self.templates.get_word_styles()

        # Configurar página
        section = doc.sections[0]
        section.page_height = Inches(11)
        section.page_width = Inches(8.5)
        section.left_margin = section.right_margin = Inches(1)
        section.top_margin = section.bottom_margin = Inches(1)

        # Portada
        title = doc.add_heading(data['name'], 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Información del documento
        info_table = doc.add_table(rows=4, cols=2)
        info_cells = [
            ('Subject:', data['subject']),
            ('Responsible:', data['responsible']),
            ('Created:', datetime.now().strftime('%Y-%m-%d %H:%M')),
            ('Due Date:', data.get('due_date', 'Not specified'))
        ]

        for i, (label, value) in enumerate(info_cells):
            row = info_table.rows[i]
            row.cells[0].text = label
            row.cells[1].text = str(value)

        doc.add_page_break()

        # Secciones de contenido
        document_type = data.get('document_type', 'academic')
        sections = self.templates.get_document_sections()[document_type]

        for section in sections:
            doc.add_heading(section, 1)
            if section == 'References':
                doc.add_paragraph("• ")
            else:
                doc.add_paragraph()

        doc.save(path)

    def _create_pptx(self, path: Path, data: Dict):
        """Crea una presentación PowerPoint estructurada"""
        prs = Presentation()

        # Slide de título
        title_slide = prs.slides.add_slide(prs.slide_layouts[0])
        title_slide.shapes.title.text = data['name']
        title_slide.placeholders[1].text = f"{
            data['subject']}\n{data['responsible']}"

        # Slides de contenido
        sections = self.templates.get_document_sections()['presentation']

        for section in sections:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = section

        prs.save(path)

    def _generate_file_path(self, subject: str, task_name: str, responsible: str, file_type: str) -> Path:
        """Genera la ruta del archivo con control de versiones"""
        base_dir = self.base_path / subject / task_name
        base_dir.mkdir(parents=True, exist_ok=True)

        # Control de versiones
        version = 1
        while True:
            file_path = base_dir / f"{responsible}_v{version}.{file_type}"
            if not file_path.exists():
                return file_path
            version += 1

    def _ensure_base_path(self):
        """Asegura que existe el directorio base"""
        self.base_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Sanitiza el nombre del archivo"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()

    def get_document_path(self, subject: str, task_name: str, responsible: str, file_type: str) -> str:
        """Obtiene la ruta de un documento existente"""
        directory = self.base_path / subject / task_name
        if not directory.exists():
            return None

        files = list(directory.glob(f"{responsible}_v*{file_type}"))
        return str(files[-1]) if files else None
