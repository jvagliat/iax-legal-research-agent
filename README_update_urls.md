# Script de Actualización de URLs para Documentos Legales

Este script Python actualiza las URLs en el archivo JSON de tesis legales, reemplazando las URLs actuales con un nuevo formato que apunta a los documentos PDF almacenados en IATraxia.

## Funcionalidad

El script:
1. **Encuentra** el archivo `tesis_from_csv_to_ingest_claude_enhanced.json`
2. **Crea un backup** automático del archivo original (`.backup`)
3. **Lee** los documentos JSON con estructura:
   ```json
   {
     "page_content": "...",
     "metadata": {
       "ius": "2030758",
       "url": "https://sjf2.scjn.gob.mx/detalle/tesis/2030758Pág."
     }
   }
   ```
4. **Reemplaza** las URLs con el formato:
   ```
   @https://iattraxia.com/files/iax-legal-documents-mx/{ius}.pdf
   ```
5. **Guarda** el archivo actualizado

## Uso

### Método 1: Ejecución automática
```bash
python update_urls.py
```

El script automáticamente buscará el archivo en:
`src/iax_legal_lg_rag_research_agent/tesis_from_csv_to_ingest_claude_enhanced.json`

### Método 2: Especificar archivo manualmente
Si el archivo no se encuentra en la ubicación por defecto, el script te pedirá la ruta:
```
Ingresa la ruta del archivo JSON: /ruta/a/tu/archivo.json
```

## Características de Seguridad

- ✅ **Backup automático**: Se crea un archivo `.backup` antes de cualquier modificación
- ✅ **Verificación de archivos**: Valida que el archivo existe antes de procesarlo
- ✅ **Manejo de errores**: Informa sobre problemas de JSON o archivos
- ✅ **Preserva encoding**: Mantiene caracteres especiales UTF-8
- ✅ **Formato legible**: Guarda el JSON con indentación

## Ejemplo de Transformación

**Antes:**
```json
{
  "metadata": {
    "ius": "2030758",
    "url": "https://sjf2.scjn.gob.mx/detalle/tesis/2030758Pág."
  }
}
```

**Después:**
```json
{
  "metadata": {
    "ius": "2030758",
    "url": "@https://iattraxia.com/files/iax-legal-documents-mx/2030758.pdf"
  }
}
```

## Requisitos

- Python 3.6+
- No requiere bibliotecas externas (usa solo la biblioteca estándar)

## Archivos Generados

- `archivo_original.json.backup` - Respaldo del archivo original
- `archivo_original.json` - Archivo actualizado con las nuevas URLs

## Recuperación

Si necesitas restaurar el archivo original:
```bash
cp archivo_original.json.backup archivo_original.json
``` 