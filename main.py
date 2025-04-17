from notion_client import database
from document_generator import latex_generator, pdf_exporter

def main():
    tarea = database.get_pending_tasks()[0]
    tex_path = latex_generator.generate_tex(tarea)
    pdf_exporter.export_pdf(tex_path)
    database.mark_task_as_done(tarea["id"])

if __name__ == "__main__":
    main()
