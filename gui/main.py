#clockpilot/gui/main.py
import os
import sys
import tkinter as tk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from frames.home import create_home_frame
from frames.upload import create_upload_frame
from frames.results import create_results_frame
from frames.breakdown import create_breakdown_frame
from components.navigation import setup_navigation
from core.constants import IMAGE_DIR

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller."""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    root = tk.Tk()
    root.title("Procesador de Turnos")
    root.geometry("1280x1024")
    root.resizable(True, True)
    root.state("zoomed")  # Maximizar la ventana

    # Establecer el icono de la ventana (manejar errores si el archivo no existe)
    icon_path = os.path.join(IMAGE_DIR, "logo.ico")
    try:
        root.iconbitmap(icon_path)  # Usar el archivo .ico como icono de la ventana
    except Exception as e:
        print(f"Advertencia: No se pudo cargar el icono. Error: {e}")

    # Crear los frames
    home_frame = create_home_frame(root)
    upload_frame = create_upload_frame(root)
    results_frame = create_results_frame(root)
    breakdown_frame = create_breakdown_frame(root)

    # Asignar los frames a root para que estén disponibles globalmente
    root.home_frame = home_frame
    root.upload_frame = upload_frame
    root.results_frame = results_frame
    root.breakdown_frame = breakdown_frame

    # Configurar la navegación
    setup_navigation(root, {
        "home": home_frame,
        "upload": upload_frame,
        "results": results_frame,
        "breakdown": breakdown_frame,
    })

    # Mostrar la pantalla inicial
    home_frame.grid(row=0, column=0, sticky="nsew")
    home_frame.tkraise()

    root.mainloop()

if __name__ == "__main__":
    main()