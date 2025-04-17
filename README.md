# TaskAlchemist

Automatiza la generación de reportes académicos a partir de tareas registradas en Notion.

## Cómo usar

1. Crea una base de datos en Notion con propiedades `Estado` y `Resumen`.
2. Llena el archivo `.env` con tu token y el ID de la base de datos.
3. Ejecuta el script:

```bash
python main.py
```

Generará un PDF con el contenido de la primera tarea pendiente.

