import pyautogui
import pyperclip
import time
import re

# Código a ingresar en el campo de búsqueda
codigo_producto = "10066741003"

# Esperar 5 segundos antes de iniciar
time.sleep(5)

# Paso 1: Buscar el campo de búsqueda y escribir el código
campo_busqueda = pyautogui.locateCenterOnScreen('campo_busqueda.png', confidence=0.8)
if campo_busqueda:
    pyautogui.click(campo_busqueda)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(codigo_producto)
else:
    exit()

# Paso 2: Buscar el botón "Buscar" y hacer clic
buscar_button = pyautogui.locateCenterOnScreen('buscar.png', confidence=0.8)
if buscar_button:
    pyautogui.click(buscar_button)
else:
    exit()

# Paso 3: Hacer clic en el enlace de la columna "Identificación"
time.sleep(5)
identificacion_link = pyautogui.locateCenterOnScreen('identificacion.png', confidence=0.6)
if identificacion_link:
    pyautogui.click(identificacion_link.x, identificacion_link.y + 20)
    time.sleep(3)

    # Paso 4: Clic directo en el centro de la pantalla para asegurar el foco en la web
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(1)

    # Paso 5: Seleccionar todo y copiar
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    # Paso 6: Extraer e imprimir solo la sección de "Imágenes:"
    texto_copiado = pyperclip.paste()
    match = re.search(r'Imágenes:\s*(.*?)\n', texto_copiado, re.DOTALL)
    if match:
        print("Imágenes:", match.group(1).strip())
    else:
        print("No se encontró la sección de 'Imágenes:'.")
    
    # Paso 7: Hacer clic en la imagen de Salesforce después de imprimir el texto
    time.sleep(2)
    salesforce_logo = pyautogui.locateCenterOnScreen('salesforce_logo.png', confidence=0.8)
    if salesforce_logo:
        pyautogui.click(salesforce_logo)
        time.sleep(2)
        
        # Paso 8: Hacer clic en la nueva imagen de Productos
        productos_icon = pyautogui.locateCenterOnScreen('productos_icon.png', confidence=0.8)
        if productos_icon:
            pyautogui.click(productos_icon)
        else:
            print("No se encontró la imagen de Productos.")
    else:
        print("No se encontró la imagen de Salesforce.")
else:
    exit()
