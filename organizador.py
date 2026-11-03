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

def mostrar_informe(consola, movidos, tamano_total, en_origen, en_destino, historial):
    """Genera tablas resumen usando rich con las estadísticas finales."""
    tabla_resumen = Table(title="Resumen de la Clasificación", show_header=True, header_style="bold magenta")
    tabla_resumen.add_column("Métrica", style="cyan")
    tabla_resumen.add_column("Valor", style="white")
    
    color_origen = "[green]" if en_origen == 0 else "[red]"
    
    tabla_resumen.add_row("Archivos movidos", str(movidos))
    tabla_resumen.add_row("Tamaño total procesado", tamano_legible(tamano_total))
    tabla_resumen.add_row("Archivos restantes en origen", f"{color_origen}{en_origen}[/]")
    tabla_resumen.add_row("Total de archivos en destino", str(en_destino))
    
    consola.print(tabla_resumen)
    consola.print("\n")
    
    if historial:
        tabla_historial = Table(title="Historial de Movimientos", show_header=True, header_style="bold magenta")
        tabla_historial.add_column("Nº", justify="right", style="cyan", width=4)
        tabla_historial.add_column("Movimiento", style="white")
        
        for i, movimiento in enumerate(historial, 1):
            tabla_historial.add_row(str(i), movimiento)
            
        consola.print(tabla_historial)

def main():
    consola = Console()
    mostrar_cabecera(consola)
    
    ruta_origen = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de origen[/bold yellow]")
    ruta_destino = Prompt.ask("[bold yellow]Introduce la ruta de la carpeta de destino[/bold yellow]")
    
    # Comprobaciones de seguridad
    if not os.path.exists(ruta_origen) or not os.path.isdir(ruta_origen):
        consola.print(Panel("La carpeta de origen no existe o no es una carpeta válida.", border_style="red"))
        return
        
    if os.path.exists(ruta_destino) and not os.path.isdir(ruta_destino):
        consola.print(Panel("La ruta de destino ya existe y no es una carpeta.", border_style="red"))
        return
        
    if una_dentro_de_otra(ruta_origen, ruta_destino):
        consola.print(Panel("Origen y destino no pueden ser la misma carpeta ni estar una dentro de la otra.", border_style="red"))
        return
        
    historial = []
    
    # Animación de carga mientras clasifica
    with consola.status("[bold green]Organizando archivos...[/bold green]"):
        tamano_total = clasificar_carpeta_recursivo(ruta_origen, ruta_destino, historial)
        
    # Cálculos post-clasificación
    archivos_movidos = len(historial)
    archivos_en_origen = contar_archivos_recursivo(ruta_origen)
    archivos_en_destino = contar_archivos_recursivo(ruta_destino)
    
    # Mostrar el informe final
    mostrar_informe(consola, archivos_movidos, tamano_total, archivos_en_origen, archivos_en_destino, historial)

if __name__ == "__main__":
    main()