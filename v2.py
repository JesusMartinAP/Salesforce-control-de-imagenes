import pyautogui
import pytesseract
import time
from PIL import ImageGrab

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

# Paso 4: Hacer scroll hasta encontrar la imagen y capturar el texto
print("Buscando la imagen de referencia...")
for _ in range(10):  # Limitar el número de desplazamientos
    imagen_referencia = pyautogui.locateCenterOnScreen('imagenes.png', confidence=0.8)
    if imagen_referencia:
        # Definir región alrededor de la imagen para capturar el texto
        region = (imagen_referencia.x + 50, imagen_referencia.y, imagen_referencia.x + 400, imagen_referencia.y + 50)
        captura = ImageGrab.grab(bbox=region)
        texto_extraido = pytesseract.image_to_string(captura, lang='spa')
        print("Texto encontrado:", texto_extraido.strip())
        break
    else:
        pyautogui.scroll(-500)  # Desplazar hacia abajo
        time.sleep(1)
else:
    print("No se encontró la imagen de referencia. Verifica 'imagenes.png'.")
