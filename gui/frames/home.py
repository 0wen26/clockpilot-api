#clockpilot/gui/frames/home.py
import tkinter as tk
from PIL import Image, ImageTk
from core.constants import IMAGE_DIR
import os
import sys

def create_home_frame(root):
    frame_home = tk.Frame(root, bg="#f0f0f0")
    frame_home.grid(row=0, column=0, sticky="nsew")

    # Configurar el grid para que se expanda y centre el contenido
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame_home.grid_rowconfigure(0, weight=1)
    frame_home.grid_rowconfigure(6, weight=1)
    frame_home.grid_columnconfigure(0, weight=1)

    # Título del programa
    title_label = tk.Label(
        frame_home,
        text="Bienvenido al Procesador de Turnos",
        font=("Segoe UI", 28, "bold"),
        bg="#f0f0f0",
        fg="#333333"
    )
    title_label.grid(row=1, column=0, pady=(20, 10), sticky="n")

    # Información del creador
    creator_label = tk.Label(
        frame_home,
        text="Desarrollado por Rubén H",
        font=("Segoe UI", 22, "bold"),
        bg="#f0f0f0",
        fg="#555555"
    )
    creator_label.grid(row=2, column=0, pady=(0, 20), sticky="n")

    # Descripción breve (texto multilínea)
    description_label = tk.Label(
        frame_home,
        text="Esta aplicación te ayuda a calcular y gestionar tus horas de trabajo,\n"
             "incluyendo pluses como horas nocturnas, festivas y dominicales.",
        font=("Segoe UI", 20),
        bg="#f0f0f0",
        fg="#555555",
        justify="center"
    )
    description_label.grid(row=3, column=0, pady=(0, 10), sticky="n")

    # Título de la sección de pluses (en negrita y más grande)
    pluses_title_label = tk.Label(
        frame_home,
        text="Pluses y cuándo se cobran:",
        font=("Segoe UI", 18, "bold"),
        bg="#f0f0f0",
        fg="#333333",
        justify="left"
    )
    pluses_title_label.grid(row=4, column=0, pady=(10, 5), sticky="n")

    # Lista de pluses (con íconos y texto normal)
    pluses_list_label = tk.Label(
        frame_home,
        text="-✈️Horas Perentorias: Mes vencido\n"
             "-🎉 Horas Festivas: Mes vencido\n"
             "-📅 Horas Domingos: Mes vencido\n"
             "-🌙 Horas Nocturnas: Mes vencido\n"
             "-🌅 Madrugues: Mes vencido\n"
             "-🍴 Manutención: Mes vencido\n"
             "-⏸️ Fraccionadas: Mes vencido\n"
             "-➕ Horas Complementarias: Mismo mes",
        font=("Segoe UI", 16),
        bg="#f0f0f0",
        fg="#555555",
        justify="left"
    )
    pluses_list_label.grid(row=5, column=0, pady=(0, 20), sticky="n")

    # Botón de inicio
    btn_comenzar = tk.Button(
        frame_home,
        text="Comenzar",
        font=("Segoe UI", 14),
        bg="#2196F3",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=lambda: frame_home.show_frame(frame_home.upload_frame)
    )
    btn_comenzar.grid(row=6, column=0, pady=(0, 50), sticky="n")

    # Opcional: Agregar una imagen o logo
    try:
        # Cargar la imagen desde la carpeta assets/images
        image_path = os.path.join(IMAGE_DIR, "logo.png")
        image = Image.open(image_path)
        # Usar Image.Resampling.LANCZOS en lugar de Image.ANTIALIAS
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(frame_home, image=img, bg="#f0f0f0")
        img_label.image = img
        img_label.grid(row=0, column=0, pady=(50, 20), sticky="n")
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo 'logo.png' en {IMAGE_DIR}. Omite la imagen.")

    return frame_home