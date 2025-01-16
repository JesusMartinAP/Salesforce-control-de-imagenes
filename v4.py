import tkinter as tk
from tkinter import messagebox
import pyautogui
import pyperclip
import time
import re
import pandas as pd
import os
from datetime import datetime

def esperar_imagen(imagen, confianza=0.8, intentos=10, espera=2):
    """
    Espera hasta que la imagen aparezca en pantalla.
    Retorna la ubicación (x, y) del centro de la imagen si la encuentra,
    de lo contrario retorna None.
    """
    for _ in range(intentos):
        ubicacion = pyautogui.locateCenterOnScreen(imagen, confidence=confianza)
        if ubicacion:
            return ubicacion
        time.sleep(espera)
    return None

def guardar_excel(datos):
    """
    Guarda en un archivo Excel la lista de datos proporcionada.
    """
    df = pd.DataFrame(datos, columns=["Artículo", "Imágenes"])
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"Salesforce control de imagenes {fecha_hora}.xlsx"
    ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
    df.to_excel(ruta_archivo, index=False)
    print(f"Datos guardados en: {ruta_archivo}")

def procesar_codigos(codigos_productos):
    """
    Realiza todo el proceso para cada código y devuelve la lista con los resultados.
    """
    datos_productos = []
    
    # Esperar unos segundos antes de iniciar (opcional, para acomodar la pantalla)
    time.sleep(2)

    try:
        for codigo_producto in codigos_productos:
            # Paso 1: Esperar y buscar el campo de búsqueda
            campo_busqueda = esperar_imagen('campo_busqueda.png', confianza=0.8)
            if campo_busqueda:
                pyautogui.click(campo_busqueda)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                pyautogui.write(codigo_producto)
            else:
                print(f"Error: No se encontró el campo de búsqueda para el código {codigo_producto}")
                continue

            # Paso 2: Esperar y hacer clic en el botón "Buscar"
            buscar_button = esperar_imagen('buscar.png', confianza=0.8)
            if buscar_button:
                pyautogui.click(buscar_button)
                time.sleep(5)
            else:
                print(f"Error: No se encontró el botón 'Buscar' para el código {codigo_producto}")
                continue

            # Paso 3: Esperar y hacer clic en el enlace de "Identificación"
            identificacion_link = esperar_imagen('identificacion.png', confianza=0.6)
            if identificacion_link:
                # A veces el texto de "Identificación" se ve un poco más abajo
                pyautogui.click(identificacion_link.x, identificacion_link.y + 20)
                time.sleep(5)
            else:
                print(f"Error: No se encontró el enlace de identificación para el código {codigo_producto}")
                continue

            # Paso 4: Asegurar el foco en la página
            screen_width, screen_height = pyautogui.size()
            pyautogui.click(screen_width // 2, screen_height // 2)
            time.sleep(2)

            # Paso 5: Seleccionar todo el contenido y copiar
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)

            # Paso 6: Extraer la sección "Imágenes:"
            texto_copiado = pyperclip.paste()
            match = re.search(r'Imágenes:\s*(.*?)\n', texto_copiado, re.DOTALL)
            if match:
                imagenes_texto = match.group(1).strip()
                print(f"{codigo_producto}: {imagenes_texto}")
            else:
                imagenes_texto = "No se encontró la sección de 'Imágenes'."
                print(f"{codigo_producto}: {imagenes_texto}")

            # Agregar datos a la lista
            datos_productos.append([codigo_producto, imagenes_texto])

            # Paso 7: Volver al inicio (Salesforce)
            salesforce_logo = esperar_imagen('salesforce_logo.png', confianza=0.6)
            if salesforce_logo:
                pyautogui.click(salesforce_logo)
                time.sleep(3)

                # Paso 8: Hacer clic en la imagen de "Productos"
                productos_icon = esperar_imagen('productos_icon.png', confianza=0.6)
                if productos_icon:
                    pyautogui.click(productos_icon)
                    time.sleep(5)
                else:
                    print(f"Error: No se encontró la imagen de Productos para el código {codigo_producto}")
            else:
                print(f"Error: No se encontró el logo de Salesforce para el código {codigo_producto}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        guardar_excel(datos_productos)
        return datos_productos

    return datos_productos

def iniciar_proceso():
    """
    Función que se ejecuta al presionar el botón.
    Obtiene los códigos de la caja de texto, los procesa y al final
    muestra un mensaje de finalización.
    """
    # Obtener texto (códigos) del widget de Tkinter
    codigos_str = text_codigos.get("1.0", tk.END)
    # Separar por cualquier espacio en blanco
    codigos_productos = codigos_str.split()

    if not codigos_productos:
        messagebox.showwarning("Advertencia", "No se ingresaron códigos.")
        return

    # Ejecutar el proceso con los códigos ingresados
    datos_productos = procesar_codigos(codigos_productos)

    # Guardar en Excel
    guardar_excel(datos_productos)

    # Mostrar alerta de finalización
    messagebox.showinfo("Proceso finalizado", "El proceso ha concluido exitosamente.")

# ---------------------- INTERFAZ GRÁFICA (TKINTER) ----------------------
ventana = tk.Tk()
ventana.title("Control de Imágenes en Salesforce")

# Frame o etiqueta para indicar al usuario
lbl_instruccion = tk.Label(ventana, text="Pega aquí los códigos (separados por espacios):")
lbl_instruccion.pack(padx=10, pady=5)

# Caja de texto para pegar los códigos
text_codigos = tk.Text(ventana, width=60, height=10)
text_codigos.pack(padx=10, pady=5)

# Botón para iniciar proceso
btn_iniciar = tk.Button(ventana, text="Iniciar proceso", command=iniciar_proceso, bg="lightblue")
btn_iniciar.pack(pady=10)

ventana.mainloop()
