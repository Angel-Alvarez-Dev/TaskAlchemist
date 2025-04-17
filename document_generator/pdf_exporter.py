import subprocess
from pathlib import Path

def export_pdf(tex_path: Path):
    subprocess.run(["pdflatex", str(tex_path)], check=True)
