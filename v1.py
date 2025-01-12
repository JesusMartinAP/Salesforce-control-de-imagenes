import pyautogui
import time

# Código a ingresar en el campo de búsqueda
codigo_producto = "10066741003"

print("El script comenzará en 5 segundos...")

# Esperar 5 segundos antes de iniciar
time.sleep(5)

# Paso 1: Buscar el campo de búsqueda mediante imagen
campo_busqueda = pyautogui.locateCenterOnScreen('campo_busqueda.png', confidence=0.8)
if campo_busqueda:
    pyautogui.click(campo_busqueda)  # Clic en el campo de búsqueda
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')  # Seleccionar texto previo (si lo hubiera)
    pyautogui.press('backspace')   # Borrar cualquier texto existente
    pyautogui.write(codigo_producto)
    print("Código ingresado correctamente.")
else:
    print("No se encontró el campo de búsqueda. Verifica la imagen 'campo_busqueda.png'.")
    exit()

# Paso 2: Buscar el botón "Buscar" mediante imagen y hacer clic
buscar_button = pyautogui.locateCenterOnScreen('buscar.png', confidence=0.8)
if buscar_button:
    pyautogui.click(buscar_button)
    print("Búsqueda realizada correctamente.")
else:
    print("No se encontró el botón 'Buscar'. Verifica la imagen 'buscar.png'.")
