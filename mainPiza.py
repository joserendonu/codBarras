import cv2
import os
from pyzbar.pyzbar import decode
from playsound import playsound
import numpy as np

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = "media"

# Diccionario para almacenar los códigos detectados y su conteo
detecciones = {'0123456789012': 0}

# Itera sobre todas las imágenes en la carpeta
for archivo in os.listdir(carpeta_imagenes):
    # Construye la ruta completa del archivo
    ruta_imagen = os.path.join(carpeta_imagenes, archivo)

    # Lee la imagen
    frame = cv2.imread(ruta_imagen)
    if frame is None:
        print(f"No se pudo leer la imagen: {ruta_imagen}")
        continue

    # Detecta y decodifica códigos de barras en la imagen
    barcodes = decode(frame)  # Usa pyzbar para detectar códigos de barras
    if barcodes:
        for barcode in barcodes:
            # Extrae los datos decodificados y las coordenadas
            codigo = barcode.data.decode("utf-8")  # Convierte los datos a texto
            puntos = barcode.polygon  # Coordenadas del polígono

            # Dibuja un polígono alrededor del código de barras detectado
            if len(puntos) > 0:
                pts = [(point.x, point.y) for point in puntos]
                pts = np.array(pts, dtype=np.int32)
                frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            # Procesa el código detectado
            if codigo in detecciones:
                detecciones[codigo] += 1
                if detecciones[codigo] >= 1:  # Cambia el umbral según sea necesario
                    print("Detección exitosa:", codigo)
                    playsound("beep.mp3")
                    detecciones.clear()
            else:
                detecciones[codigo] = 1

    else:
        print(f"No se detectaron códigos de barras en la imagen: {ruta_imagen}")

    # Muestra la imagen procesada (opcional)
    cv2.imshow("Resultado", frame)
    cv2.waitKey(1000)  # Muestra cada imagen durante 1 segundo

# Cierra todas las ventanas de OpenCV
cv2.destroyAllWindows()