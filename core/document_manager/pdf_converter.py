import os
from docx2pdf import convert

class PdfAlchemist:
    """
    Clase encargada de convertir documentos DOCX a PDF utilizando docx2pdf.
    """

    def __init__(self):
        # El constructor no requiere inicialización especial, pero se deja para futuras extensiones.
        pass

    def transmute_to_pdf(self, file_path: str) -> str:
        """
        Convierte un archivo DOCX en PDF y devuelve la ruta del PDF generado.

        Args:
            file_path (str): Ruta del archivo DOCX a convertir.

        Returns:
            str: Ruta del archivo PDF generado.

        Raises:
            AlchemyError: Si ocurre un error durante la conversión.
        """
        # Verifica que el archivo tenga extensión .docx (ignora mayúsculas/minúsculas)
        if not file_path.lower().endswith(".docx"):
            raise AlchemyError("El archivo no es un documento DOCX válido.")

        # Define la ruta de salida cambiando la extensión .docx por .pdf
        output_path = file_path.replace(".docx", ".pdf")

        try:
            # Ejecuta la conversión de DOCX a PDF usando la función convert de docx2pdf
            convert(file_path, output_path)

            # Verifica que el archivo PDF se haya generado correctamente
            if not os.path.exists(output_path):
                raise AlchemyError("La conversión a PDF falló. No se encontró el archivo generado.")

            # Devuelve la ruta del PDF generado
            return output_path
        except Exception as e:
            # En caso de cualquier excepción durante la conversión, se lanza una excepción personalizada
            raise AlchemyError(f"Error en la conversión de PDF: {str(e)}")

class AlchemyError(Exception):
    """
    Excepción personalizada para errores en la conversión de documentos.
    """
    pass
