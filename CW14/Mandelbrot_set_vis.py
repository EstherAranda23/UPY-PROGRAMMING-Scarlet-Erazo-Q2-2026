# Classwork 14 - Error Handling: Mandelbrot Set Vis (CW12)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library not found. Run: pip install Pillow")
    exit()

#INPUT
try:
    archivo = open('mandelbrot.csv', 'r')
    lineas  = archivo.readlines()
    archivo.close()

    if len(lineas) < 2:
        raise ValueError("CSV file is empty or missing data rows.")

    datos = lineas[1:]  # skip header

except FileNotFoundError:
    print("Error: 'mandelbrot.csv' not found. Run mandelbrot_set_math.py first.")
    exit()

except ValueError as e:
    print(f"File error: {e}")
    exit()

except IOError as e:
    print(f"File read error: {e}")
    exit()

#PROCESS

try:
    max_iter = 100

    # Determine image dimensions
    ancho, alto = 0, 0
    for linea in datos:
        partes = linea.strip().split(',')
        if len(partes) != 3:
            continue
        fila    = int(partes[0])
        columna = int(partes[1])
        if fila + 1 > alto:
            alto = fila + 1
        if columna + 1 > ancho:
            ancho = columna + 1

    if ancho == 0 or alto == 0:
        raise ValueError("Could not determine image dimensions from CSV.")

    # Create grayscale image
    img = Image.new('L', (ancho, alto))

    for linea in datos:
        partes = linea.strip().split(',')
        if len(partes) != 3:
            continue

        fila        = int(partes[0])
        columna     = int(partes[1])
        iteraciones = int(partes[2])

        # Convert iterations to brightness
        if iteraciones == max_iter:
            brillo = 0
        else:
            brillo = int((iteraciones / max_iter) * 255)

        img.putpixel((columna, fila), brillo)

except ValueError as e:
    print(f"Processing error: {e}")
    exit()

except Exception as e:
    print(f"Unexpected processing error: {e}")
    exit()

#OUTPUT
try:
    img.save('mandelbrot.png')
    print(f"Image saved: mandelbrot.png  ({ancho} x {alto} px)")

except IOError as e:
    print(f"File save error: {e}")
except Exception as e:
    print(f"Unexpected output error: {e}")