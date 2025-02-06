"""
TaskAlchemist Core
-----------------
Módulo principal que contiene la lógica de negocio para la gestión de documentos académicos.
"""

__version__ = '0.1.0'
__author__ = 'Tu Nombre'
__email__ = 'tu@email.com'

# Importar componentes principales para facilitar su uso
from .notion_api.client import NotionConnector
from .document_manager.file_generator import DocumentAlchemist
from .document_manager.pdf_converter import PdfAlchemist, AlchemyError
