# Crea: core/document_manager/pdf_converter.py

import os
import platform
import subprocess
from pathlib import Path
import logging
from typing import Optional, Union
import shutil

logger = logging.getLogger(__name__)


class PdfAlchemist:
    """
    Alquimista especializado en la transmutación de documentos a PDF.
    Soporta múltiples plataformas y métodos de conversión.
    """

    def __init__(self):
        self.platform = platform.system().lower()
        self._initialize_converters()

    def transmute_to_pdf(self, source_path: Union[str, Path]) -> str:
        """
        Convierte documentos a PDF usando el método más apropiado para la plataforma.

        Args:
            source_path: Ruta al documento original

        Returns:
            str: Ruta al archivo PDF generado

        Raises:
            AlchemyError: Si hay errores en la conversión
        """
        source_path = Path(source_path)
        if not source_path.exists():
            raise AlchemyError(
                f"¡El documento origen no existe!: {source_path}")

        # Verificar extensión soportada
        if source_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise AlchemyError(f"Formato no soportado: {source_path.suffix}")

        # Crear directorio de salida si no existe
        pdf_path = source_path.with_suffix('.pdf')
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if self.platform == 'windows':
                return self._transmute_windows(source_path, pdf_path)
            else:
                return self._transmute_unix(source_path, pdf_path)
        except Exception as e:
            logger.error(f"Error en la transmutación: {str(e)}")
            raise AlchemyError(f"Fallo en la transmutación PDF: {str(e)}")

    def _transmute_windows(self, source_path: Path, pdf_path: Path) -> str:
        """Transmutación usando Microsoft Word en Windows"""
        try:
            import pythoncom
            from docx2pdf import convert

            pythoncom.CoInitialize()
            try:
                convert(str(source_path), str(pdf_path))
                logger.info(f"Conversión exitosa usando Word: {pdf_path}")
                return str(pdf_path)
            finally:
                pythoncom.CoUninitialize()

        except ImportError:
            logger.warning(
                "docx2pdf no disponible, intentando con LibreOffice...")
            return self._transmute_libreoffice(source_path, pdf_path)

    def _transmute_unix(self, source_path: Path, pdf_path: Path) -> str:
        """Transmutación en sistemas Unix usando LibreOffice o alternativas"""
        # Intentar primero con LibreOffice
        if self._check_libreoffice():
            return self._transmute_libreoffice(source_path, pdf_path)

        # Intentar con unoconv si está disponible
        elif self._check_unoconv():
            return self._transmute_unoconv(source_path, pdf_path)

        raise AlchemyError("No se encontró ningún conversor compatible")

    def _transmute_libreoffice(self, source_path: Path, pdf_path: Path) -> str:
        """Transmutación usando LibreOffice"""
        soffice_path = self._get_soffice_path()
        if not soffice_path:
            raise AlchemyError("LibreOffice no encontrado")

        cmd = [
            soffice_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(pdf_path.parent),
            str(source_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Conversión exitosa usando LibreOffice: {pdf_path}")
            return str(pdf_path)
        except subprocess.CalledProcessError as e:
            raise AlchemyError(f"Error en LibreOffice: {e.stderr}")

    def _transmute_unoconv(self, source_path: Path, pdf_path: Path) -> str:
        """Transmutación usando unoconv"""
        try:
            subprocess.run(
                ['unoconv', '-f', 'pdf', '-o',
                    str(pdf_path), str(source_path)],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Conversión exitosa usando unoconv: {pdf_path}")
            return str(pdf_path)
        except subprocess.CalledProcessError as e:
            raise AlchemyError(f"Error en unoconv: {e.stderr}")

    def _get_soffice_path(self) -> Optional[str]:
        """Encuentra la ruta al ejecutable de LibreOffice"""
        if self.platform == 'windows':
            possible_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]
        else:
            possible_paths = [
                "/usr/bin/soffice",
                "/usr/lib/libreoffice/program/soffice",
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _check_libreoffice(self) -> bool:
        """Verifica si LibreOffice está disponible"""
        return bool(self._get_soffice_path())

    def _check_unoconv(self) -> bool:
        """Verifica si unoconv está disponible"""
        return bool(shutil.which('unoconv'))

    def _initialize_converters(self):
        """Inicializa las configuraciones según la plataforma"""
        self.SUPPORTED_EXTENSIONS = ['.docx', '.doc', '.odt', '.rtf']

        # Detectar conversores disponibles
        self.available_converters = []

        if self.platform == 'windows':
            try:
                import docx2pdf
                self.available_converters.append('word')
            except ImportError:
                pass

        if self._check_libreoffice():
            self.available_converters.append('libreoffice')

        if self._check_unoconv():
            self.available_converters.append('unoconv')

        if not self.available_converters:
            logger.warning("No se encontraron conversores PDF disponibles")


class AlchemyError(Exception):
    """Excepción personalizada para errores en el proceso de alquimia"""
    pass
