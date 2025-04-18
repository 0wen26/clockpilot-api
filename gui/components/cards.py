#clockpilot/gui/components/cards.py
import tkinter as tk
from PIL import Image, ImageTk

def create_card(parent, text, value, color, image_path, row, col):
    """Crea una tarjeta de datos con imagen y texto."""
    card = tk.Frame(parent, bg=color, bd=2, relief="solid", padx=5, pady=5)
    card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    inner_frame = tk.Frame(card, bg=color)
    inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # Cargar imagen
    try:
        image = Image.open(image_path).resize((40, 40))
        img = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Advertencia: No se pudo cargar la imagen {image_path}. Error: {e}")
        img = None

    img_label = tk.Label(inner_frame, image=img, bg=color)
    img_label.image = img
    img_label.pack(side="left", padx=5)

    text_label = tk.Label(inner_frame, text=text, font=("Helvetica", 15, "bold"), bg=color, fg="black")
    text_label.pack(side="left", padx=5)

    value_label = tk.Label(card, text=value, font=("Helvetica", 18), bg=color, fg="black")
    value_label.pack(pady=2)

    return value_label