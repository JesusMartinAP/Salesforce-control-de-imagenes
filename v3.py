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
    exit()

# Paso 3: Buscar y hacer clic en el enlace de la columna "Identificación"
time.sleep(3)  # Esperar a que cargue la tabla
identificacion_link = pyautogui.locateCenterOnScreen('identificacion.png', confidence=0.8)
if identificacion_link:
    pyautogui.click(identificacion_link.x, identificacion_link.y + 20)
    print("Clic en los dígitos de la columna 'Identificación' realizado correctamente.")
else:
    print("No se encontró el enlace de identificación. Verifica la imagen 'identificacion.png'.")

# Paso 4: Hacer 2 scroll hacia abajo
print("Realizando scroll hacia abajo...")
pyautogui.scroll(-800)
time.sleep(1)
pyautogui.scroll(-800)
time.sleep(2)

# Paso 5: Buscar el apartado de imágenes y seleccionar el texto
print("Buscando el apartado de imágenes...")
apartado_imagen = pyautogui.locateCenterOnScreen('apartado_imagen.png', confidence=0.8)
if apartado_imagen:
    # Mover el cursor al texto a la derecha de la imagen y seleccionar
    pyautogui.moveTo(apartado_imagen.x + 150, apartado_imagen.y)
    pyautogui.mouseDown()
    pyautogui.moveRel(300, 0)  # Seleccionar el texto hacia la derecha
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')  # Copiar el texto seleccionado
    time.sleep(1)
    texto_copiado = pyautogui.paste()  # Obtener el texto copiado
    print("Texto del apartado de imágenes:", texto_copiado.strip())
else:
    print("No se encontró el apartado de imágenes. Verifica 'apartado_imagen.png'.")
