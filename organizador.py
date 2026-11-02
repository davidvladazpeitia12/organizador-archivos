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
    """
    Obtiene la extensión de un archivo en minúsculas y sin el punto inicial.
    Si el archivo no tiene extensión, devuelve 'sin_extension'.
    """
    _, ext = os.path.splitext(nombre_archivo)
    if ext:
        return ext.lower().replace(".", "")
    return "sin_extension"

def tamano_legible(tamano_bytes):
    """
    Convierte un tamaño en bytes a su unidad legible más adecuada (bytes, KB, MB, GB).
    Se divide sucesivamente entre 1024.
    """
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
    """
    Comprueba si dos rutas son la misma carpeta o si una está dentro de la otra.
    """
    abs_a = os.path.abspath(ruta_a) + os.sep
    abs_b = os.path.abspath(ruta_b) + os.sep
    return abs_a.startswith(abs_b) or abs_b.startswith(abs_a)

def main():
    consola = Console()
    mostrar_cabecera(consola)
    
    ruta_origen = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de origen[/bold yellow]")
    ruta_destino = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de destino[/bold yellow]")
    
    # Comprobaciones de seguridad
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