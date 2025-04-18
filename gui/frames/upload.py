#clockpilot/gui/frames/upload.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from services.pdf.pdf_transformer import parse_pdf_to_json
from core.constants import OUTPUT_JSON
from core.validators import validate_pdf_path, validate_contract_hours
from services.data_io import delete_json

def create_upload_frame(root):
    frame_upload = tk.Frame(root, bg="#e0e0e0")  # Fondo un poco más oscuro
    frame_upload.grid(row=0, column=0, sticky="nsew")  # Usar grid para expandir el frame

    # Configurar el grid para que se expanda y centre el contenido
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame_upload.grid_rowconfigure(0, weight=1)  # Espacio arriba
    frame_upload.grid_rowconfigure(6, weight=1)  # Espacio abajo
    frame_upload.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente

    # Título
    title_label = tk.Label(
        frame_upload,
        text="Carga de Archivo y Configuración",
        font=("Segoe UI", 25, "bold"),  # Fuente más grande
        bg="#e0e0e0",
        fg="#222222"  # Color de texto más oscuro
    )
    title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")  # Centrado

    # Frame para el contenido principal
    content_frame = tk.Frame(frame_upload, bg="#e0e0e0")
    content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    # Campo para seleccionar archivo PDF
    pdf_frame = tk.Frame(content_frame, bg="#e0e0e0")
    pdf_frame.grid(row=0, column=0, pady=(0, 20), sticky="w")

    pdf_label = tk.Label(
        pdf_frame,
        text="1. Selecciona tu archivo PDF:",
        font=("Segoe UI", 14),  # Fuente más grande
        bg="#e0e0e0",
        fg="#333333"  # Color de texto más oscuro
    )
    pdf_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

    pdf_help_label = tk.Label(
        pdf_frame,
        text="Haz clic en 'Buscar' para seleccionar el archivo PDF de tu horario.",
        font=("Segoe UI", 14),  # Fuente más grande
        bg="#e0e0e0",
        fg="#555555",  # Color de texto más oscuro
        justify="left"
    )
    pdf_help_label.grid(row=1, column=0, pady=(0, 10), sticky="w")

    entry_pdf_path = tk.Entry(pdf_frame, width=50, font=("Segoe UI", 12), bd=2, relief="groove")
    entry_pdf_path.grid(row=2, column=0, pady=(0, 5), sticky="w")

    btn_buscar = tk.Button(
        pdf_frame,
        text="Buscar",
        font=("Segoe UI", 12),
        bg="#4CAF50",  # Verde
        fg="white",
        bd=0,
        padx=20,
        pady=5,
        command=lambda: [entry_pdf_path.delete(0, tk.END), entry_pdf_path.insert(0, filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")]))]
    )
    btn_buscar.grid(row=3, column=0, pady=(0, 10), sticky="w")

    # Campo de entrada para las horas de contrato
    contract_frame = tk.Frame(content_frame, bg="#e0e0e0")
    contract_frame.grid(row=1, column=0, pady=(0, 20), sticky="w")

    contract_label = tk.Label(
        contract_frame,
        text="2. Ingresa tus horas de contrato:",
        font=("Segoe UI", 14),  # Fuente más grande
        bg="#e0e0e0",
        fg="#333333"  # Color de texto más oscuro
    )
    contract_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

    contract_help_label = tk.Label(
        contract_frame,
        text="Ingresa el número total de horas que debes trabajar según tu contrato.",
        font=("Segoe UI", 12),  # Fuente más grande
        bg="#e0e0e0",
        fg="#555555",  # Color de texto más oscuro
        justify="left"
    )
    contract_help_label.grid(row=1, column=0, pady=(0, 10), sticky="w")

    entry_horas_contrato = tk.Entry(contract_frame, width=10, font=("Segoe UI", 12), bd=2, relief="groove")
    entry_horas_contrato.grid(row=2, column=0, pady=(0, 5), sticky="w")

    # Campo para seleccionar el año
    year_frame = tk.Frame(content_frame, bg="#e0e0e0")
    year_frame.grid(row=2, column=0, pady=(0, 20), sticky="w")

    year_label = tk.Label(
        year_frame,
        text="3. Selecciona el año:",
        font=("Segoe UI", 14),  # Fuente más grande
        bg="#e0e0e0",
        fg="#333333"  # Color de texto más oscuro
    )
    year_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

    year_help_label = tk.Label(
        year_frame,
        text="Selecciona el año correspondiente a tu horario.",
        font=("Segoe UI", 12),  # Fuente más grande
        bg="#e0e0e0",
        fg="#555555",  # Color de texto más oscuro
        justify="left"
    )
    year_help_label.grid(row=1, column=0, pady=(0, 10), sticky="w")

    year_var = tk.StringVar(value="2024")
    year_dropdown = ttk.Combobox(year_frame, textvariable=year_var, values=["2024", "2025"], font=("Segoe UI", 12), state="readonly")
    year_dropdown.grid(row=2, column=0, pady=(0, 5), sticky="w")

    # Botón para procesar el PDF
    btn_procesar = tk.Button(
        content_frame,
        text="Procesar PDF",
        font=("Segoe UI", 14),  # Fuente más grande
        bg="#2196F3",  # Azul
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=lambda: process_pdf(entry_pdf_path, entry_horas_contrato, year_var, frame_upload)
    )
    btn_procesar.grid(row=3, column=0, pady=(20, 10), sticky="w")

    return frame_upload

def process_pdf(entry_pdf_path, entry_horas_contrato, year_var, frame_upload):
    """Procesa el PDF y guarda los datos en JSON."""
    # 1. Borrar el JSON existente
    delete_json()
    pdf_path = entry_pdf_path.get()
    horas_contrato = entry_horas_contrato.get()
    selected_year = year_var.get()

    # Validar el archivo PDF
    pdf_error = validate_pdf_path(pdf_path)
    if pdf_error:
        messagebox.showwarning("Archivo no válido", pdf_error)
        return

    # Validar las horas de contrato
    contract_error = validate_contract_hours(horas_contrato)
    if contract_error:
        messagebox.showwarning("Horas de Contrato", contract_error)
        return

    try:
        parse_pdf_to_json(pdf_path, OUTPUT_JSON, int(selected_year), int(horas_contrato))
        messagebox.showinfo("Éxito", "El archivo PDF fue procesado correctamente.")
        frame_upload.show_frame(frame_upload.results_frame)  # Ir a resultados
        frame_upload.results_frame.update_results()  # Actualizar resultados
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar el PDF: {e}")