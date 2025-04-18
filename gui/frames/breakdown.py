#clockpilot/gui/frames/breakdown.py
import tkinter as tk
from tkinter import ttk
from services.data_io import load_from_json
from core.constants import OUTPUT_JSON

def create_breakdown_frame(root):
    """Crea la pantalla con el desglose detallado de pluses por día usando tarjetas con colores."""
    frame_breakdown = tk.Frame(root, bg="#f5f5f5")  # Fondo claro
    frame_breakdown.grid(row=0, column=0, sticky="nsew")

    # Configurar el grid para que se expanda
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Frame para el título y el botón "Volver"
    title_frame = tk.Frame(frame_breakdown, bg="#f5f5f5")
    title_frame.pack(fill="x", pady=10)

    # Botón para volver (a la izquierda)
    btn_volver = tk.Button(
        title_frame,
        text="⬅️ Volver",
        font=("Helvetica", 12),  # Fuente más pequeña
        bg="#4CAF50",  # Verde
        fg="white",
        bd=0,
        padx=10,
        pady=5,
        command=lambda: root.show_frame(root.results_frame)
    )
    btn_volver.pack(side="left", padx=(10, 0))  # Botón a la izquierda

    # Título (centrado)
    title_label = tk.Label(
        title_frame,
        text="Desglose Detallado de Pluses",
        font=("Helvetica", 18, "bold"),  # Fuente más pequeña
        bg="#f5f5f5",
        fg="#333333"
    )
    title_label.pack(side="left", padx=(10, 0), expand=True)  # Título centrado

    # Frame para contener las tarjetas (con scrollbar)
    canvas = tk.Canvas(frame_breakdown, bg="#f5f5f5", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame_breakdown, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    def update_report():
        """Carga los datos desde el JSON y actualiza las tarjetas."""
        try:
            data = load_from_json(OUTPUT_JSON)
            if not data:
                return

            # Limpiar tarjetas anteriores
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            # Procesar los detalles (datos diarios)
            detalles = data.get("detalles", {})
            row, col = 0, 0
            max_columns = 6  # 5 columnas

            for fecha, valores in detalles.items():
                # Omitir días vacíos (Total Horas es "00:00")
                if valores.get("duracion_total", "00:00") == "00:00":
                    continue

                # Crear una tarjeta para el día
                card = tk.Frame(
                    scrollable_frame,
                    bd=2,
                    relief="groove",
                    padx=10,
                    pady=10,
                    bg="#ffffff"  # Fondo blanco
                )
                card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                # Título de la tarjeta (fecha)
                tk.Label(
                    card,
                    text=f"Fecha: {fecha}",
                    font=("Helvetica", 16, "bold"),  # Fuente más pequeña
                    bg="#4CAF50",  # Verde
                    fg="white"
                ).pack(fill="x", pady=(0, 5))

                # Mostrar solo los pluses que no son 0
                campos = [
                    ("Total Horas", valores.get("duracion_total", "00:00"), "#2196F3"),  # Azul
                    ("Horas HR", valores.get("horas_perentorias", "00:00"), "#FF9800"),  # Naranja
                    ("Horas Festivas", valores.get("festive_hours", "00:00"), "#E91E63"),  # Rosa
                    ("Horas Domingos", valores.get("horas_domingos", "00:00"), "#9C27B0"),  # Morado
                    ("Horas Madrugue", valores.get("horas_madrugue", "00:00"), "#00BCD4"),  # Cyan
                    ("Horas Nocturnas", valores.get("horas_nocturnas", "00:00"), "#673AB7"),  # Índigo
                    ("Manutención", valores.get("manutencion", 0), "#FF5722"),  # Rojo oscuro
                    ("Fraccionadas", valores.get("fraccionadas", 0), "#795548")  # Marrón
                ]

                for nombre, valor, color in campos:
                    if valor != "00:00" and valor != 0:  # Omitir valores vacíos o 0
                        # Frame para cada plus
                        plus_frame = tk.Frame(card, bg=color, bd=1, relief="solid")
                        plus_frame.pack(fill="x", pady=2)

                        # Etiqueta con el nombre y valor del plus
                        tk.Label(
                            plus_frame,
                            text=f"{nombre}: {valor}",
                            font=("Helvetica", 14),  # Fuente más pequeña
                            bg=color,
                            fg="white"
                        ).pack(padx=5, pady=2)

                # Actualizar la posición de la siguiente tarjeta
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

        except Exception as e:
            print(f"Error en update_report: {e}")

    # Asignar la función update_report al frame
    frame_breakdown.update_report = update_report

    # Actualizar las tarjetas al cargar la pantalla
    update_report()

    return frame_breakdown