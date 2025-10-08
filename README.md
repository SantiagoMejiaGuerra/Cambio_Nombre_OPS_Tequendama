# 📂 Renombrador de Archivos Vallesalud (OPS Organizer)

![Python Tkinter GUI](https://img.shields.io/badge/Tecnología-Python%20%26%20Tkinter-blue)
![Automatización de Documentos](https://img.shields.io/badge/Función-Automatización%20de%20Documentos-green)

Esta herramienta de escritorio fue diseñada para **automatizar y agilizar el proceso de renombrado y organización** de archivos PDF y carpetas asociados a órdenes de servicio (OPS) y números de trámite (T).

El objetivo principal es estandarizar la nomenclatura, garantizando que tanto los archivos como las carpetas sigan el formato correcto requerido por el sistema.

***

## ✨ Características Principales

* **Renombrado de Carpetas:** Las carpetas de origen (que inician con "OPS") son renombradas automáticamente al formato **`T[Número]`** (ej. `T56789`).
* **Renombrado de Archivos PDF:** Los archivos PDF dentro de estas carpetas son renombrados utilizando el prefijo tipográfico correcto (según el mapeo de `DIC_TIPOGRAFICO`) seguido del número de Trámite (T).
* **Interfaz Gráfica (GUI):** Interfaz amigable e intuitiva desarrollada con **Tkinter**.
* **Gestión Dinámica:** Permite al usuario **agregar o eliminar dinámicamente** campos de entrada para múltiples pares de números OPS y T en una sola ejecución.
* **Validación:** Limpieza y validación básica de las entradas numéricas.

***

## 🛠️ Instalación y Requisitos

### Requisitos

Necesitas tener **Python 3.x** instalado en tu sistema operativo. Las librerías utilizadas (como `os`, `tkinter`) son estándar de Python.

### Ejecución del Script

1.  Abre tu terminal o línea de comandos.
2.  Navega hasta el directorio donde se encuentra el script principal del proyecto.
3.  Ejecuta la aplicación usando el comando:

    ```bash
    python nombre_de_tu_script.py
    ```
    *(Asegúrate de reemplazar `nombre_de_tu_script.py` con el nombre de tu archivo).*

***

## 🚀 Guía de Uso

La aplicación funciona en tres sencillos pasos:

### 1. Seleccionar la Carpeta Principal

Haz clic en el botón **"Seleccionar Carpeta"** y elige el directorio que contiene las carpetas a procesar (las que inician con el prefijo "OPS").

### 2. Ingresar Pares de OPS y T

* Utiliza el botón **"✚ Agregar par de OPS/T"** para añadir las filas de entrada necesarias.
* Ingresa el **Número de OPS** que deseas buscar en la primera casilla.
* Ingresa el **Número de la T** (Trámite) correspondiente en la segunda casilla. Este número se utilizará para renombrar tanto los archivos como la carpeta.

### 3. Ejecutar el Proceso

Haz clic en el botón **"► Ejecutar Renombrado"**. El sistema procesará las carpetas y archivos en la ruta seleccionada y mostrará un resumen con los resultados de la operación (archivos procesados, carpetas renombradas y advertencias).

***

## ⚙️ Detalle Técnico del Renombrado

La lógica de renombrado se basa en dos transformaciones clave:

### 1. Renombrado de Archivos PDF

El archivo PDF es renombrado siguiendo un mapeo estricto basado en su prefijo actual (ej. `DFU`, `FAC`). La estructura final del nombre del archivo es:

**`[Prefijo_Correcto][Número_T][Extensión]`**

Ejemplo de mapeo (Diccionario `DIC_TIPOGRAFICO`):
* Un archivo que contenga **`DFU`** será renombrado a: `FEV_900847382_T[Número_T].pdf`

### 2. Renombrado de Carpetas

La carpeta es renombrada a la nomenclatura final:

**`T[Número_T]`**

Donde `[Número_T]` es el valor que el usuario ingresó para ese OPS.