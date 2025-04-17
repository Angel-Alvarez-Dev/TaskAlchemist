from jinja2 import Template
from pathlib import Path

def generate_tex(tarea):
    with open("document_generator/template.tex", "r") as file:
        template = Template(file.read())
    
    contenido = tarea.get("Resumen", "Sin contenido")
    rendered = template.render(contenido=contenido)
    
    output_path = Path("reporte.tex")
    with open(output_path, "w") as f:
        f.write(rendered)
    
    return output_path
