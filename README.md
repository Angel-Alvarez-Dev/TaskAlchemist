## 🔮 TaskAlchemist

TaskAlchemist es una herramienta que automatiza la creación y conversión de documentos académicos a partir de tareas registradas en **Notion**. Convierte tareas en documentos `.docx` y, si es necesario, en **PDF**, permitiendo un flujo de trabajo más eficiente y organizado.

### 🚀 Características

✅ **Integración con Notion** → Obtiene tareas y actualiza su estado automáticamente.  
✅ **Generación de documentos** → Crea archivos `.docx` listos para entrega.  
✅ **Conversión a PDF** → Opción para convertir documentos a PDF en segundos.  
✅ **Automatización total** → Marca tareas como procesadas y almacena las rutas de los archivos generados.  
✅ **Organización por asignaturas** → Guarda documentos en carpetas específicas según la materia.  
✅ **Manejo de excepciones** → Control de errores en la conversión y generación de archivos.  

---

### 🛠 Instalación

1. **Clonar el repositorio**  
```bash
   git clone https://github.com/tu_usuario/TaskAlchemist.git
   cd TaskAlchemist
```

2. **Crear un entorno virtual** (opcional pero recomendado)  
```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/macOS
   venv\Scripts\activate      # En Windows
```

3. **Instalar dependencias**  
```bash
   pip install -r requirements.txt
```

4. **Configurar variables de entorno**  
   Renombra `.env.example` a `.env` y añade tu clave de API de Notion:  
```ini
   NOTION_API_KEY="tu_clave_secreta"
   DATABASE_ID="tu_database_id"
```

### 🏗 Estructura del Proyecto

```bash
TaskAlchemist/
│── core/
│   ├── notion_api/
│   │   ├── client.py  # Conexión con Notion
│   ├── document_manager/
│   │   ├── file_generator.py  # Creación de documentos
│   │   ├── pdf_converter.py   # Conversión a PDF
│   ├── utils/
│   │   ├── error_handler.py   # Manejo de errores
│── main.py  # Punto de entrada
│── requirements.txt  # Dependencias
│── .gitignore
│── README.md  # Este archivo
```

---

### 🧙 Contribución

¡Las mejoras son bienvenidas! Si quieres contribuir:  

1. **Haz un fork** del repositorio.  
2. Crea una nueva **rama**: `git checkout -b feature-nueva-funcionalidad`  
3. **Haz commits** con mensajes claros: `git commit -m "Añadir nueva funcionalidad"`  
4. **Envía un Pull Request** 🎉  

---

### 📝 Licencia

Este proyecto está bajo la **Licencia MIT**, lo que significa que puedes modificarlo y distribuirlo libremente.
