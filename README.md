# 🧙 TaskAlchemist  
**Automatización académica inteligente con Notion**  
*Convierte tareas en documentos profesionales y sincroniza su estado automáticamente*

---

## 🌟 Características  
| Funcionalidad | Icono | Descripción |  
|---------------|-------|-------------|  
| **Sincronización en tiempo real** | 🔄 | Extrae tareas de Notion y actualiza su estado post-procesamiento |  
| **Generación de documentos** | 📄 | Crea archivos .docx con estructura académica estándar |  
| **Conversión a PDF** | 🖨️ | Exporta a PDF manteniendo formato y márgenes |  
| **Gestión de metadatos** | 🗃️ | Vincula documentos generados a través de URL y notas |  
| **Automatización de flujos** | 🤖 | Actualiza fechas, responsables y estados automáticamente |  

---

## 🛠️ Configuración Requerida en Notion  
### Esquema de la Base de Datos  
| Nombre Columna | Tipo Notion | Configuración Recomendada |  
|----------------|-------------|---------------------------|  
| **Tareas** | Título | Propiedad principal |  
| **Estado** | Select | Opciones: `Pendiente`/`En proceso`/`Completado` |  
| **Asignaturas** | Multi-select | Lista de materias (ej: Matemáticas, Literatura) |  
| **Tipo de archivo** | Select | Opciones: `DOCX`/`PDF` |  
| **Fecha de entrega** | Date | Formato: Fecha completa |  
| **Responsable** | Persona | Usuarios de tu workspace |  
| **Ruta del archivo** | URL | Campo para enlace al documento |  
| **Nota** | Texto | Notas adicionales (máx. 200 caracteres) |  

![Captura Base de Datos](https://ejemplo.com/db-preview.png) *Ejemplo visual de la configuración*

---

## ⚡ Instalación Rápida  
1. **Clonar repositorio**  
```bash  
git clone https://github.com/tu_usuario/TaskAlchemist.git  
cd TaskAlchemist  
```

2. **Configurar entorno**  
```bash  
python -m venv .venv && source .venv/bin/activate  # Linux/macOS  
pip install -r requirements.txt  
```

3. **Variables de entorno** (.env):  
```ini  
NOTION_API_KEY="secret_tu_token"  
DATABASE_ID="tu_db_id"  
DOCS_OUTPUT="./documentos"  
```

---

## 🚀 Uso Básico  
### 1. Sincronizar tareas  
```python  
from core.notion import NotionManager  

manager = NotionManager()  
tareas_pendientes = manager.get_tasks(filter_estado="Pendiente")  
```

### 2. Generar documento  
```python  
from core.documents import DocxBuilder  

for tarea in tareas_pendientes:  
    documento = DocxBuilder(tarea).generate()  
    manager.update_task_status(tarea.id, "Completado")  
```

### 3. Actualizar metadatos  
```python  
manager.update_file_metadata(  
    task_id=tarea.id,  
    file_url=f"{DOCS_OUTPUT}/{tarea.asignatura}/{tarea.nombre}.docx"  
)  
```

---

## 🔧 Estructura del Proyecto  
```  
taskalchemist/  
├── core/                  # Núcleo funcional  
│   ├── notion/           # Integración API  
│   ├── documents/        # Generadores de documentos  
│   └── utils/            # Herramientas auxiliares  
├── output/               # Documentos generados  
├── tests/                # Pruebas unitarias  
└── main.py               # Punto de entrada  
```

---

## 🚨 Solución de Problemas  
**Error común**: Permisos insuficientes en Notion  
```bash  
# Verificar que la integración tenga acceso a:  
- Lectura/escritura de bases de datos  
- Lectura de información de usuarios  
- Capacidad para editar contenido  
```

**Error en generación de PDF**:  
```python  
# Verificar dependencias:  
pip show python-docx pdfkit  # Deben estar instaladas  
```

---

## 🤝 Contribuir  
1. Implementa mejoras en ramas feature:  
```bash  
git checkout -b feature/nueva-funcionalidad  
```  
2. Sigue el estándar de código:  
- Type hints obligatorios  
- Docstrings en formato Google  
- Máx. 80 caracteres por línea  

---

## 📜 Licencia  
MIT License © 2023 Angel-Alvarez-Dev
---