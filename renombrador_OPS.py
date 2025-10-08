# Se realizara un proyecto en el que la idea es cambiar el nombre de los archivos de forma más automatica y agil sin intervención humana
# 
# Por ende es evitar que hayan espacios en sus nombre o dobles '__' (rayas al piso) en el nombre del archivo, además este tambien debe cambiarse el nombre de la carpeta

import os
import tkinter as tk 
from tkinter import filedialog, messagebox
from tkinter import font as tkFont

# Agregamos algunos colores para la interfaz de usuario

COLOR_PRIMARY_BLUE = "#2196F3"
COLOR_DARK_BLUE = "#1976D2"
COLOR_LIGHT_BLUE = "#E3F2FD"
COLOR_ACCENT_GREEN = "#4CAF50"
COLOR_TEXT_DARK = "#212121"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_BACKGROUND_APP = "#F5F5F5"
COLOR_BORDER_GRAY = "#DEDEDE"
COLOR_DELETE_RED = "#E53935"

# Luego de importar las librerias que usaremos como 'os' y 'tkinter' para realizar una interfaz de usuario y además pueda ir al sistema a realizar los procesos que debemos hacer.
# Realizaremos un diccionario con la tipografia 'incorrecta' y la 'correcta' sobre los nombres de los archivos.

DIC_TIPOGRAFICO = {
    "DFU" : "FEV_900847382_T",
    "FAC" : "CRC_900847382_T",
    "HCE" : "HEV_900847382_T",
    "LAB" : "PDX_900847382_T",
    "AYD" : "PDX_900847382_T",
    "NCD" : "PDE_900847382_T"
}

# Luego realizaremos la asignación de las variables globales para la interfaz una que almacenara la ruta de la carpeta principal que almacena las subcarpetas y otra variable que almacenara un listado con los campos de entrada de la interfaz (Numero de OPS y T)
ruta_principal= "" # Almacena la ruta de la carpeta
num_entradas = [] # Almacena los numeros que ingresaran de las OPS y de la T

# Crearemos dos funciones:
# 
# 1. La primera función sera para realizar un cuadro de dialogo para la selección de la carpeta principal
# 2. La segunda función sera para agregar un nuevo campo de entrada para ingresar los numero de la OPS y el numero de la T correspondiente

def seleccion_principal():
    """
    Función que abrira cuadro de diálogo para seleccionar la carpeta principal 
    """
    global ruta_principal
    ruta_principal = filedialog.askdirectory()
    if ruta_principal:
        # Esta variable esta en al función de tkinter que es el texto que se actualiza para mostrar al usuario
        label_estado.config(text=f"Carpeta seleccionada: {ruta_principal}")
    else: 
        label_estado.config(text="Carpeta no seleccionada", fg=COLOR_TEXT_DARK)

def filas_entrada():
    """
    Función que servira para agregar una nueva fila de campos para la entrada de datos para la OPS y la T
    """
    # Frame_campos esta en la función de tkinter 
    fr_entrada = tk.Frame(frame_campos, bg=COLOR_LIGHT_BLUE, bd=1, relief=tk.FLAT, padx=5, pady=5)
    fr_entrada.pack(pady=5, fill=tk.X)

    # INgreso del numero de la OPS
    label_ops = tk.Label(fr_entrada, text="Número de OPS:", bg=COLOR_LIGHT_BLUE, fg=COLOR_TEXT_DARK, font=small_font)
    label_ops.pack(side=tk.LEFT, padx=5)

    entry_ops = tk.Entry(fr_entrada, width=15, bd=1, relief=tk.SOLID, font=entry_font)
    entry_ops.pack(side=tk.LEFT, padx=5, ipady=2)

    # Ingreso de el numero de la T
    label_t = tk.Label(fr_entrada, text="Número de la T:", bg= COLOR_LIGHT_BLUE, fg=COLOR_TEXT_DARK, font=small_font)
    label_t.pack(side=tk.LEFT, padx=5)

    entry_t = tk.Entry(fr_entrada, width=15, bd=1, relief=tk.SOLID, font=entry_font)
    entry_t.pack(side=tk.LEFT, padx=5, ipady=2)

    # Boton eliminación de filas
    btn_delete_row = tk.Button(fr_entrada, text="🗑️", command=lambda: eliminar_fila(fr_entrada, entry_ops, entry_t),
                                bg=COLOR_DELETE_RED, fg=COLOR_TEXT_LIGHT, font=small_font,
                                activebackground="#C52828", activeforeground=COLOR_TEXT_LIGHT,
                                relief=tk.RAISED, bd=1, padx=5, pady=2, cursor="hand2")
    btn_delete_row.pack(side=tk.RIGHT, padx=5)

    # Filas que se pueden ingresar
    num_entradas.append({"frame": fr_entrada, "ops_entry": entry_ops, "t_entry":entry_t})

    canvas_entries.update_idletasks()
    canvas_entries.config(scrollregion=canvas_entries.bbox("all"))

def eliminar_fila(frame_destroy, ops_entry_remove, t_entry_remove):
    """
    Eliminar filas o campos de entrada de la interfaz
    """
    global num_entradas
    num_entradas = [item for item in num_entradas if not (item["ops_entry"] == ops_entry_remove and item["t_entry"] == t_entry_remove)]
    frame_destroy.destroy()
    canvas_entries.update_idletasks()
    canvas_entries.config(scrollregion=canvas_entries.bbox("all"))

# Al tener las funciones que almacenaran la información que el usuario ingresara, se realizara la función de la cual se basara nuestro sistema la que reenombrara los archivos y carpetas segun lo que ingrese el usuario

def renombramiento():
    """
    Función que realiza el inicio del renombre de los arhcivos y carpetas que esten escritas incorrectamente
    """

    # Verificamos que la carpeta exita si no lanzara la advertencia
    if not ruta_principal:
        messagebox.showwarning("ADVERTENCIA: ", "Por favor, seleccione una carpeta principal")
        return
    
    # Mapeamos los datos que se ingresen por medio de la interfaz de usuario
    data_user = {}
    for entry_data in num_entradas:
        try:
            ops_num = entry_data["ops_entry"].get()
            t_num = entry_data["t_entry"].get()
            if ops_num and t_num:
                # Relizaremos una limpieza quianto espacios y cualquier texto ingresado que no se numerico
                ops_num_clean = ''.join(filter(str.isdigit, ops_num))
                t_num_clean = ''.join(filter(str.isdigit, t_num))
                if ops_num_clean:
                    data_user[ops_num_clean] = t_num_clean
        except tk.TclError:
            # Si el widget no existe pasamos al siguiente
            continue
    if not data_user:
        messagebox.showwarning("ADVERTENCIA: ", "Por favor, ingresa los numeros de la OPS y la T")
        return
    
    # Lista para almacenar las rutas de las carpetas a renombrar
    folder_process = []

    # Recolección de datos
    try:
        for dirpath, dirnames, filenames in os.walk(ruta_principal):
            for dirname in dirnames:
                if dirname.startswith("OPS"):
                    ops_num = ''.join(filter(str.isdigit, dirname))
                    if ops_num in data_user:
                        t_num = data_user[ops_num]
                        path_subfolder= os.path.join(dirpath, dirname)
                        # Almacenamos la información en tupla
                        folder_process.append((path_subfolder, t_num, dirpath))
    
        # Ejecuta el renombramiento
        files_process = 0
        folders_renamed_count=0
        warnings_count=0

        for old_path_subfolder, t_num, parent_path in folder_process:
            #Renombramos los archivos de la subcarpeta
            for filename in os.listdir(old_path_subfolder):
                if filename.lower().endswith(".pdf"):
                    base_name, extension = os.path.splitext(filename)

                    for typo_incorrect, prefix_correct in DIC_TIPOGRAFICO.items():
                        if typo_incorrect in base_name:
                            new_name = f"{prefix_correct}{t_num}{extension}"
                            old_path = os.path.join(old_path_subfolder, filename)
                            new_path = os.path.join(old_path_subfolder, new_name)

                            if not os.path.exists(new_path):
                                os.rename(old_path, new_path)
                                files_process += 1
                            else:
                                print(f"Advertencia: El archivo {new_name} ya existe en {old_path_subfolder}. Se omite")
                                warnings_count += 1
                            break
            
            # Renonbramos la carpeta después de haber procesado los archivos
            new_folder_name = f"T{t_num}"
            new_path_subfolder = os.path.join(parent_path, new_folder_name)
            if not os.path.exists(new_path_subfolder):
                os.rename(old_path_subfolder, new_path_subfolder)
                folders_renamed_count += 1
            else:
                print(f"Advertencia: La carpeta {new_folder_name} ya existe en {parent_path}. La carpeta original {os.path.basename(old_path_subfolder)} no fue renombrada.")
                warnings_count += 1
        
        messagebox.showinfo("Proceso Completado", 
                            f"Proceso finalizado:\n"
                            f"- Archivos PDF procesados: {files_process}\n"
                            f"- Carpetas renombradas: {folders_renamed_count}\n"
                            f"- Advertencias (archivos/carpetas existentes): {warnings_count}")
    
    except Exception as e:
        messagebox.showerror("ERROR", f"Ocurrió un error inesperado durante el renombrado: {e}")

# Al tener nuestra columna vertebral lista que sera la función de renombramiento realizaremos la interfaz de usuario con tkinter

app = tk.Tk()
app.title("Organizador de Archivos OPS")
app.geometry("700x600")
app.resizable(True, True)
app.config(bg=COLOR_BACKGROUND_APP)

# --- Definición de Fuentes Personalizadas ---
title_font = tkFont.Font(family="Arial", size=18, weight='bold')
header_font = tkFont.Font(family="Arial", size=12, weight='bold')
label_font = tkFont.Font(family="Arial", size=10)
small_font = tkFont.Font(family="Arial", size=9)
button_font = tkFont.Font(family="Arial", size=11, weight="bold")
entry_font = tkFont.Font(family="Arial", size=10)

# --- Frame Principal que contendrá todos los elementos de la vista ----
main_frame = tk.Frame(app, padx=20, pady=20, bg=COLOR_BACKGROUND_APP, bd=2, relief=tk.GROOVE)
main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Configurar grid para el main_frame
# main_frame.grid_rowconfigure(2, weight=1)  # La fila de entradas se expandirá
main_frame.grid_columnconfigure(0, weight=1)

# --- Título que llevará la aplicación ---
label_title = tk.Label(main_frame, text="Organizador de Documentos OPS", font=title_font,
                        fg=COLOR_DARK_BLUE, bg=COLOR_BACKGROUND_APP)
label_title.grid(row=0, column=0, pady=15, sticky="ew")

# ---- Sección #1 selección de carpeta ----
frame_selection = tk.LabelFrame(main_frame, text="1. Seleccione la carpeta principal: ",
                                font=header_font, fg=COLOR_PRIMARY_BLUE, bg=COLOR_LIGHT_BLUE,
                                padx=15, pady=15, bd=1, relief=tk.SOLID)
frame_selection.grid(row=1, column=0, pady=10, sticky="ew")

# Configurar grid interno para frame_selection
frame_selection.grid_columnconfigure(0, weight=1)

label_folder = tk.Label(frame_selection, text="Seleccione la carpeta que contiene las 'OPS'",
                        bg=COLOR_LIGHT_BLUE, fg=COLOR_TEXT_DARK, font=label_font)
label_folder.grid(row=0, column=0, pady=5)

btn_select = tk.Button(frame_selection, text="Seleccionar Carpeta", command=seleccion_principal,
                        bg=COLOR_PRIMARY_BLUE, fg=COLOR_TEXT_LIGHT, font=button_font,
                        activebackground=COLOR_DARK_BLUE, activeforeground=COLOR_TEXT_LIGHT,
                        relief=tk.RAISED, bd=2, padx=10, pady=5, cursor="hand2")
btn_select.grid(row=1, column=0, pady=10)

label_estado = tk.Label(frame_selection, text="Carpeta no seleccionada", fg=COLOR_TEXT_DARK,
                        bg=COLOR_LIGHT_BLUE, font=small_font)
label_estado.grid(row=2, column=0, pady=5)

# --- Sección #2 entrada de pares de OPS y T ---
frame_entries = tk.LabelFrame(main_frame, text="2. Ingresar Pares de OPS y T", font=header_font,
                            fg=COLOR_PRIMARY_BLUE, bg=COLOR_BACKGROUND_APP, padx=15, pady=15,
                            bd=1, relief=tk.SOLID, height=100)
frame_entries.grid(row=2, column=0, pady=10, sticky="nsew")

# Configurar grid interno para frame_entries
frame_entries.grid_rowconfigure(2, weight=1)  # El área scrollable se expandirá
frame_entries.grid_columnconfigure(0, weight=1)

label_entry_instruction = tk.Label(frame_entries, text="Agregue o elimine filas e ingrese los números correspondientes:",
                                bg=COLOR_BACKGROUND_APP, fg=COLOR_TEXT_DARK, font=label_font)
label_entry_instruction.grid(row=0, column=0, pady=10)

btn_add = tk.Button(frame_entries, text="✚ Agregar par de OPS/T", command=filas_entrada,
                    bg=COLOR_PRIMARY_BLUE, fg=COLOR_TEXT_LIGHT, font=button_font, 
                    activebackground=COLOR_DARK_BLUE, activeforeground=COLOR_TEXT_LIGHT, relief=tk.RAISED,
                    bd=2, padx=15, pady=7, cursor="hand2")
btn_add.grid(row=1, column=0, pady=10)

# --- Área scrollable para las entradas ---
frame_scrollable_area = tk.Frame(frame_entries, bg=COLOR_BACKGROUND_APP, height=90)
frame_scrollable_area.grid(row=2, column=0, sticky="ew", pady=(0, 10))
frame_scrollable_area.grid_propagate(False)

# Configurar grid para el área scrollable
frame_scrollable_area.grid_rowconfigure(0, weight=1)
frame_scrollable_area.grid_columnconfigure(0, weight=1)

canvas_entries = tk.Canvas(frame_scrollable_area, bg=COLOR_BACKGROUND_APP, bd=0, highlightthickness=0)
canvas_entries.grid(row=0, column=0, sticky="nsew")

scrollbar_entries = tk.Scrollbar(frame_scrollable_area, orient="vertical", command=canvas_entries.yview)
scrollbar_entries.grid(row=0, column=1, sticky="ns")

canvas_entries.configure(yscrollcommand=scrollbar_entries.set)

frame_campos = tk.Frame(canvas_entries, bg=COLOR_BACKGROUND_APP)
canvas_window_id = canvas_entries.create_window((0, 0), window=frame_campos, anchor="nw")

def on_canvas_configure(event):
    """
    Función que realizará el ajuste del ancho del frame de entradas para que se adapte al ancho del canvas
    """
    canvas_entries.itemconfig(canvas_window_id, width=event.width)
    canvas_entries.config(scrollregion=canvas_entries.bbox("all"))

def on_frame_configure(event):
    """
    Función que actualiza la región de scroll cuando cambia el contenido del frame
    """
    canvas_entries.config(scrollregion=canvas_entries.bbox("all"))

canvas_entries.bind('<Configure>', on_canvas_configure)
frame_campos.bind('<Configure>', on_frame_configure)

# --- Sección #3 Botón Ejecutar (AHORA VISIBLE) ---
execute_button_frame = tk.Frame(main_frame, bg=COLOR_BACKGROUND_APP)
execute_button_frame.grid(row=3, column=0, pady=5, sticky="ew")

# Configurar grid para centrar el botón
execute_button_frame.grid_columnconfigure(0, weight=1)

btn_execute = tk.Button(execute_button_frame, text="► Ejecutar Renombrado", command=renombramiento,
                        bg=COLOR_ACCENT_GREEN, fg=COLOR_TEXT_LIGHT, font=button_font,
                        activebackground="#388E3C", activeforeground=COLOR_TEXT_LIGHT,
                        relief=tk.RAISED, bd=2, padx=20, pady=5, cursor="hand2")
btn_execute.grid(row=0, column=0, pady=10)

# Agregar una fila inicial
filas_entrada()

app.mainloop()


