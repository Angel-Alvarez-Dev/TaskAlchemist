"""
TaskAlchemist Core
-----------------
Módulo principal que contiene la lógica de negocio para la gestión de documentos académicos.
"""

__author__ = 'Tu Nombre'
__email__ = 'tu@email.com'

# Importar componentes principales para facilitar su uso
from .notion_api.client import NotionConnector
from .document_manager.pdf_converter import PdfAlchemist, AlchemyError
