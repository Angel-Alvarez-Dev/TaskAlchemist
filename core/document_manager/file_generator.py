# core/document_manager/file_generator.py
import os
from datetime import datetime


class FileGenerator:
    def __init__(self, base_path):
        self.base_path = base_path

    def create_document(self, task_data):
        """Crea un nuevo documento basado en el tipo de archivo y los datos de la tarea"""
        asignatura = task_data['asignatura']
        nombre = task_data['nombre']
        responsables = '-'.join(task_data['responsables'])
        grupo = task_data.get('grupo', '')

        # Crear nombre del archivo
        filename = f"{nombre}_{grupo}_{responsables}"

        # Asegurar que existe el directorio de la asignatura
        folder_path = os.path.join(self.base_path, asignatura)
        os.makedirs(folder_path, exist_ok=True)

        # Crear archivo según el tipo
        file_path = ""
        if task_data['tipo_archivo'].lower() == 'word':
            file_path = self._create_word_document(
                folder_path, filename, task_data)
        elif task_data['tipo_archivo'].lower() == 'powerpoint':
            file_path = self._create_powerpoint(
                folder_path, filename, task_data)

        return file_path

    def _create_word_document(self, folder_path, filename, task_data):
        """Crea un documento de Word con la plantilla básica"""
        # Aquí implementarías la lógica para crear el documento Word
        # Usando python-docx u otra biblioteca similar
        pass

    def _create_powerpoint(self, folder_path, filename, task_data):
        """Crea una presentación de PowerPoint con la plantilla básica"""
        # Aquí implementarías la lógica para crear la presentación
        # Usando python-pptx u otra biblioteca similar
        pass
