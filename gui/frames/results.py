#clockpilot/gui/frames/results.py
import tkinter as tk
from tkinter import messagebox
import os
from gui.components.cards import create_card
from core.constants import CARD_COLORS, IMAGE_DIR, DATA, OUTPUT_JSON
from services.data_io import load_from_json, json_exists
from core.calculations.complementary_hours import calculate_complementary_hours
from core.utils import hh_mm_to_decimal  # Importar la función de conversión

def create_results_frame(root):
    frame_results = tk.Frame(root, bg="#e0e0e0")
    frame_results.grid(row=0, column=0, sticky="nsew")

    # Configurar el grid para que se expanda y centre el contenido
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame_results.grid_rowconfigure(0, weight=1)
    frame_results.grid_rowconfigure(2, weight=1)
    frame_results.grid_columnconfigure(0, weight=1)

    # Título
    title_label = tk.Label(
        frame_results,
        text="Resultados del Procesamiento",
        font=("Segoe UI", 24, "bold"),
        bg="#e0e0e0",
        fg="#222222"
    )
    title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    # Frame para los botones
    button_frame = tk.Frame(frame_results, bg="#e0e0e0")
    button_frame.grid(row=1, column=0, pady=(10, 20), sticky="n")

    # Botón "Volver"
    btn_volver = tk.Button(
        button_frame,
        text="Volver",
        font=("Segoe UI", 14),
        bg="#2196F3",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=lambda: root.show_frame(root.upload_frame)
    )
    btn_volver.grid(row=0, column=0, padx=(0, 10), sticky="n")

    # Botón "Ver Informe"
    btn_ver_informe = tk.Button(
        button_frame,
        text="Ver Informe",
        font=("Segoe UI", 14),
        bg="#4CAF50",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=lambda: ver_informe(root)
    )
    btn_ver_informe.grid(row=0, column=1, sticky="n")

    # Frame para las tarjetas
    card_frame = tk.Frame(frame_results, bg="#e0e0e0")
    card_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    # Crear tarjetas dinámicamente
    cards_per_row = 4
    card_widgets = {}

    # Texto explicativo para cada tarjeta
    explanations = {
        "Horas Contrato": "Las horas que tienes asignadas según tu contrato.",
        "Total Horas": "El número total de horas trabajadas este mes.",
        "Horas Complementarias": "Horas trabajadas de + mes que se pagan en el mismo mes.",
        "Horas Perentorias": "Horas de retraso de avión que se pagan a mes vencido.",
        "Horas Festivas": "Horas trabajadas en días festivos.",
        "Horas Domingos": "Horas trabajadas en domingos.",
        "Horas Nocturnas": "Horas trabajadas entre las 22:00 y las 06:00.",
        "Madrugues": "Días que empiezas entre las 4:00 y las 6:55 horas.",
        "Manutención": "Se paga si el turno incluye completamente el tramo de 14:00 a 16:00 o de 21:00 a 23:00 horas.",
        "Fraccionadas": "Jornada fraccionada: trabajas en dos períodos con una interrupción de 1 a 5 horas."
    }

    # Íconos para las explicaciones
    icons = {
        "Horas Contrato": "📄",
        "Total Horas": "⏰",
        "Horas Complementarias": "➕",
        "Horas Perentorias": "✈️",
        "Horas Festivas": "🎉",
        "Horas Domingos": "📅",
        "Horas Nocturnas": "🌙",
        "Madrugues": "🌅",
        "Manutención": "🍴",
        "Fraccionadas": "⏸️"
    }

    # Crear las tarjetas y las explicaciones
    for index, (text, value, image_file) in enumerate(DATA):
        row = (index // cards_per_row) * 2
        col = index % cards_per_row
        image_path = os.path.join(IMAGE_DIR, image_file)

        # Crear la explicación arriba de la tarjeta
        explanation_frame = tk.Frame(card_frame, bg="#ffffff", bd=2, relief="groove")
        explanation_frame.grid(row=row, column=col, pady=(10, 5), sticky="nsew")

        # Ícono
        icon_label = tk.Label(
            explanation_frame,
            text=icons.get(text, ""),
            font=("Segoe UI", 16),
            bg="#ffffff",
            fg="#333333"
        )
        icon_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

        # Texto explicativo
        explanation_label = tk.Label(
            explanation_frame,
            text=explanations.get(text, ""),
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#555555",
            wraplength=150,
            justify="left"
        )
        explanation_label.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Crear la tarjeta debajo de la explicación
        card = create_card(card_frame, text, value, CARD_COLORS[text], image_path, row + 1, col)
        card_widgets[text] = card

    def update_results():
        """Carga el JSON y actualiza las tarjetas con los resultados en formato decimal."""
        try:
            data = load_from_json(OUTPUT_JSON)
            if not data:
                # Valores por defecto
                card_widgets["Total Horas"].config(text="Total Horas: 0.00 h")
                card_widgets["Horas Contrato"].config(text="Horas Contrato: 0")
                card_widgets["Horas Perentorias"].config(text="Horas Perentorias: 0.00 h")
                card_widgets["Horas Complementarias"].config(text="Horas Complementarias: 0.00 h")
                card_widgets["Horas Festivas"].config(text="Horas Festivas: 0.00 h")
                card_widgets["Horas Domingos"].config(text="Horas Domingos: 0.00 h")
                card_widgets["Madrugues"].config(text="Madrugues: 0 días")
                card_widgets["Manutención"].config(text="Manutención: 0 días")
                card_widgets["Fraccionadas"].config(text="Fraccionadas: 0 días")
                card_widgets["Horas Nocturnas"].config(text="Horas Nocturnas: 0.00 h")
                return

            # Leer valores del JSON
            totales = data.get("totales", {})
            horas_contrato = data.get("horas_contrato", 0)

            # Obtener valores y convertir a decimal
            total_hours = hh_mm_to_decimal(totales.get("total_hours", "00:00"))
            total_hr_hours = hh_mm_to_decimal(totales.get("total_hr_hours", "00:00"))
            total_festive_hours = hh_mm_to_decimal(totales.get("total_festive_hours", "00:00"))
            total_sundays_hours = hh_mm_to_decimal(totales.get("total_sundays_hours", "00:00"))
            night_hours = hh_mm_to_decimal(totales.get("total_night_hours", "00:00"))
            
            # Valores que no requieren conversión (días)
            madrugue_hours = totales.get("total_madrugue_days", 0)
            meal_allowance = totales.get("total_meal_allowance", 0)
            split_shifts = totales.get("total_split_shifts", 0)

            # Calcular horas complementarias (ya en decimal)
            complementary_hours = calculate_complementary_hours(
                horas_contrato, 
                f"{int(total_hours)}:{int((total_hours % 1) * 60):02d}",  # Convertir a HH:MM temporalmente
                f"{int(total_hr_hours)}:{int((total_hr_hours % 1) * 60):02d}"
            )
            complementary_hours_decimal = hh_mm_to_decimal(complementary_hours)

            # Actualizar las tarjetas con valores decimales
            card_widgets["Total Horas"].config(text=f"Total Horas: {total_hours:.2f} h")
            card_widgets["Horas Contrato"].config(text=f"Horas Contrato: {horas_contrato}")
            card_widgets["Horas Perentorias"].config(text=f"Horas Perentorias: {total_hr_hours:.2f} h")
            card_widgets["Horas Complementarias"].config(text=f"Horas Complementarias: {complementary_hours_decimal:.2f} h")
            card_widgets["Horas Festivas"].config(text=f"Horas Festivas: {total_festive_hours:.2f} h")
            card_widgets["Horas Domingos"].config(text=f"Horas Domingos: {total_sundays_hours:.2f} h")
            card_widgets["Horas Nocturnas"].config(text=f"Horas Nocturnas: {night_hours:.2f} h")
            
            # Tarjetas que no requieren conversión (días)
            card_widgets["Madrugues"].config(text=f"Madrugues: {madrugue_hours} días")
            card_widgets["Manutención"].config(text=f"Manutención: {meal_allowance} días")
            card_widgets["Fraccionadas"].config(text=f"Fraccionadas: {split_shifts} días")

        except Exception as e:
            print(f"Error en update_results: {e}")
            card_widgets["Total Horas"].config(text=f"Error: {e}")

    def ver_informe(root):
        """Verifica si el JSON existe antes de mostrar el informe."""
        if not json_exists():
            messagebox.showwarning(
                "Advertencia",
                "No se ha generado el archivo JSON. Procesa un PDF primero."
            )
        else:
            root.show_frame(root.breakdown_frame)
            root.breakdown_frame.update_report()

    frame_results.update_results = update_results

    return frame_results