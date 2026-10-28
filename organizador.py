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
    )
    consola.print(panel)

def main():
    # El objeto Console se crea una sola vez según los requisitos
    consola = Console()
    mostrar_cabecera(consola)
    
    ruta_origen = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de origen[/bold yellow]")
    ruta_destino = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de destino[/bold yellow]")

if __name__ == "__main__":
    main()