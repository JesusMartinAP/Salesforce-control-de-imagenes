import pyautogui
import pyperclip
import time
import re
import pandas as pd
import os
from datetime import datetime

# Lista de códigos de productos (Ejemplo)
codigos_productos = [
    "10066135001",
    "10066741003",
    "10066742003",
    "10066743003"
]

# Inicializar lista para almacenar los resultados
datos_productos = []

# Función para esperar a que un elemento aparezca en pantalla
def esperar_imagen(imagen, confianza=0.8, intentos=10, espera=2):
    for intento in range(intentos):
        ubicacion = pyautogui.locateCenterOnScreen(imagen, confidence=confianza)
        if ubicacion:
            return ubicacion
        time.sleep(espera)
    return None

# Función para guardar los datos en Excel
def guardar_excel(datos):
    df = pd.DataFrame(datos, columns=["Artículo", "Imágenes"])
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"Salesforce control de imagenes {fecha_hora}.xlsx"
    ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
    df.to_excel(ruta_archivo, index=False)
    print(f"Datos guardados en: {ruta_archivo}")

# Esperar antes de iniciar
time.sleep(5)

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
    exit()

# Guardar los datos en Excel después de completar el proceso
guardar_excel(datos_productos)
