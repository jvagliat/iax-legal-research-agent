#!/usr/bin/env python3
"""
Script para actualizar las URLs en el archivo JSON de tesis legales.
Reemplaza las URLs actuales con el formato: @https://iattraxia.com/files/iax-legal-documents-mx/{ius}.pdf
"""

import json
import os
from typing import Dict, Any, Optional

def update_url_format(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza el formato de URL usando el valor de 'ius' de los metadatos.
    
    Args:
        data: Diccionario que representa un documento con metadata
        
    Returns:
        Diccionario actualizado con la nueva URL
    """
    if "metadata" in data and "ius" in data["metadata"]:
        ius_value = data["metadata"]["ius"]
        new_url = f"@https://iattraxia.com/files/iax-legal-documents-mx/{ius_value}.pdf"
        data["metadata"]["url"] = new_url
        print(f"Actualizada URL para IUS {ius_value}: {new_url}")
    
    return data

def process_json_file(input_file: str, output_file: Optional[str] = None) -> None:
    """
    Procesa el archivo JSON y actualiza las URLs.
    
    Args:
        input_file: Ruta del archivo JSON de entrada
        output_file: Ruta del archivo JSON de salida (opcional, por defecto sobrescribe el original)
    """
    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe.")
        return
    
    # Crear backup del archivo original
    backup_file = f"{input_file}.backup"
    original_input = input_file
    if not os.path.exists(backup_file):
        os.rename(input_file, backup_file)
        print(f"Backup creado: {backup_file}")
        input_file = backup_file
    
    try:
        # Leer el archivo JSON
        print(f"Leyendo archivo: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar si es una lista de documentos
        if isinstance(data, list):
            print(f"Procesando {len(data)} documentos...")
            updated_data = [update_url_format(doc) for doc in data]
        else:
            print("Procesando documento único...")
            updated_data = update_url_format(data)
        
        # Determinar archivo de salida
        if output_file is None:
            output_file = original_input
        
        # Escribir el archivo actualizado
        print(f"Escribiendo archivo actualizado: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Proceso completado exitosamente!")
        print(f"📁 Archivo original respaldado en: {backup_file}")
        print(f"📁 Archivo actualizado guardado en: {output_file}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el archivo JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal del script."""
    print("🔄 Script de actualización de URLs para documentos legales")
    print("=" * 60)
    
    # Archivo por defecto basado en la estructura del proyecto
    default_file = "src/iax_legal_lg_rag_research_agent/tesis_from_csv_to_ingest_claude_enhanced.json"
    
    # Verificar si existe el archivo por defecto
    if os.path.exists(default_file):
        print(f"📄 Archivo encontrado: {default_file}")
        process_json_file(default_file)
    else:
        print(f"❌ Archivo no encontrado: {default_file}")
        print("Por favor, especifica la ruta correcta del archivo.")
        
        # Solicitar ruta del archivo al usuario
        file_path = input("Ingresa la ruta del archivo JSON: ").strip()
        if file_path and os.path.exists(file_path):
            process_json_file(file_path)
        else:
            print("❌ Archivo no válido o no existe.")

if __name__ == "__main__":
    main() 