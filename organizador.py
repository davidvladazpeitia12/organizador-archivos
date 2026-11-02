"""
Módulo: Organizador de Archivos
Propósito: Automatizar la clasificación de archivos por extensión.
"""
import os
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

def mostrar_cabecera(consola):
    """Muestra la cabecera principal del programa."""
    panel = Panel(
        "[bold cyan]Organizador Automático de Archivos[/bold cyan]\n"
        "Clasifica tus archivos por extensión de forma recursiva.",
        border_style="cyan",
        expand=False
    )
    consola.print(panel)

def obtener_extension(nombre_archivo):
    """Obtiene la extensión de un archivo en minúsculas y sin el punto inicial."""
    _, ext = os.path.splitext(nombre_archivo)
    if ext:
        return ext.lower().replace(".", "")
    return "sin_extension"

def tamano_legible(tamano_bytes):
    """Convierte un tamaño en bytes a su unidad legible más adecuada."""
    unidades = ["bytes", "KB", "MB", "GB"]
    indice = 0
    valor = float(tamano_bytes)
    
    while valor >= 1024 and indice < len(unidades) - 1:
        valor /= 1024
        indice += 1
        
    if indice == 0:
        return f"{int(valor)} {unidades[indice]}"
    return f"{valor:.2f} {unidades[indice]}"

def una_dentro_de_otra(ruta_a, ruta_b):
    """Comprueba si dos rutas son la misma carpeta o si una está dentro de la otra."""
    abs_a = os.path.abspath(ruta_a) + os.sep
    abs_b = os.path.abspath(ruta_b) + os.sep
    return abs_a.startswith(abs_b) or abs_b.startswith(abs_a)

def nombre_disponible(ruta_destino, nombre_archivo):
    """Devuelve un nombre de archivo que no exista en la carpeta de destino."""
    ruta_completa = os.path.join(ruta_destino, nombre_archivo)
    if not os.path.exists(ruta_completa):
        return nombre_archivo
        
    nombre_base, ext = os.path.splitext(nombre_archivo)
    contador = 1
    
    while True:
        nuevo_nombre = f"{nombre_base}_{contador}{ext}"
        if not os.path.exists(os.path.join(ruta_destino, nuevo_nombre)):
            return nuevo_nombre
        contador += 1

def clasificar_archivo(ruta_origen, nombre_archivo, ruta_destino, historial):
    """Mueve un archivo a su subcarpeta correspondiente y lo añade al historial."""
    ruta_archivo_origen = os.path.join(ruta_origen, nombre_archivo)
    tamano = os.path.getsize(ruta_archivo_origen)
    
    ext = obtener_extension(nombre_archivo)
    carpeta_ext = os.path.join(ruta_destino, ext)
    
    os.makedirs(carpeta_ext, exist_ok=True)
    nuevo_nombre = nombre_disponible(carpeta_ext, nombre_archivo)
    ruta_archivo_destino = os.path.join(carpeta_ext, nuevo_nombre)
    
    shutil.move(ruta_archivo_origen, ruta_archivo_destino)
    historial.append(f"{ruta_archivo_origen} → {ext}/{nuevo_nombre}")
    
    return tamano

def clasificar_carpeta_recursivo(ruta_origen, ruta_destino, historial):
    """Recorre recursivamente una carpeta para clasificar todos sus archivos."""
    total_bytes = 0
    try:
        elementos = os.listdir(ruta_origen)
    except PermissionError:
        return 0

    for elemento in elementos:
        ruta_elemento = os.path.join(ruta_origen, elemento)
        # Caso recursivo: es un directorio
        if os.path.isdir(ruta_elemento):
            total_bytes += clasificar_carpeta_recursivo(ruta_elemento, ruta_destino, historial)
        # Caso base: es un archivo
        elif os.path.isfile(ruta_elemento):
            total_bytes += clasificar_archivo(ruta_origen, elemento, ruta_destino, historial)
            
    return total_bytes

def contar_archivos_recursivo(ruta):
    """Recorre recursivamente una carpeta para contar el número total de archivos."""
    total_archivos = 0
    if not os.path.exists(ruta):
        return 0
        
    try:
        elementos = os.listdir(ruta)
    except PermissionError:
        return 0

    for elemento in elementos:
        ruta_elemento = os.path.join(ruta, elemento)
        # Caso recursivo
        if os.path.isdir(ruta_elemento):
            total_archivos += contar_archivos_recursivo(ruta_elemento)
        # Caso base
        elif os.path.isfile(ruta_elemento):
            total_archivos += 1
            
    return total_archivos

def main():
    consola = Console()
    mostrar_cabecera(consola)
    
    ruta_origen = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de origen[/bold yellow]")
    ruta_destino = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de destino[/bold yellow]")
    
    if not os.path.isdir(ruta_origen):
        consola.print(Panel("La carpeta de origen no existe o no es una carpeta.", border_style="red"))
        return
        
    if os.path.exists(ruta_destino) and not os.path.isdir(ruta_destino):
        consola.print(Panel("La ruta de destino ya existe y no es una carpeta.", border_style="red"))
        return
        
    if una_dentro_de_otra(ruta_origen, ruta_destino):
        consola.print(Panel("Origen y destino no pueden ser la misma carpeta ni estar una dentro de la otra.", border_style="red"))
        return

if __name__ == "__main__":
    main()