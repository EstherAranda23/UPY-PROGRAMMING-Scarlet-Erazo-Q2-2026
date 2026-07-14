# Classwork 14 - Error Handling: Mandelbrot Set Math (CW11)

#INPUT

try:
    archivo = open('config.txt', 'r')
    lineas  = archivo.readlines()
    archivo.close()

    config = {}
    for linea in lineas:
        linea = linea.strip()
        if '=' in linea and not linea.startswith('#'):
            key, value = linea.split('=', 1)
            config[key.strip()] = value.strip()

    ancho    = int(config['ancho'])
    alto     = int(config['alto'])
    max_iter = int(config['max_iter'])
    xmin     = float(config['xmin'])
    xmax     = float(config['xmax'])
    ymin     = float(config['ymin'])
    ymax     = float(config['ymax'])

    if ancho <= 0 or alto <= 0:
        raise ValueError("Width and height must be positive integers.")
    if max_iter <= 0:
        raise ValueError("max_iter must be a positive integer.")
    if xmin >= xmax or ymin >= ymax:
        raise ValueError("Invalid coordinate range: min must be less than max.")

except FileNotFoundError:
    print("Error: 'config.txt' not found. Using default values.")
    ancho, alto, max_iter = 400, 300, 100
    xmin, xmax = -2.5, 1.0
    ymin, ymax = -1.2, 1.2

except KeyError as e:
    print(f"Config error: missing parameter {e}. Using default values.")
    ancho, alto, max_iter = 400, 300, 100
    xmin, xmax = -2.5, 1.0
    ymin, ymax = -1.2, 1.2

except ValueError as e:
    print(f"Config value error: {e}. Using default values.")
    ancho, alto, max_iter = 400, 300, 100
    xmin, xmax = -2.5, 1.0
    ymin, ymax = -1.2, 1.2

#PROCESS 

try:
    resultados = []

    for fila in range(alto):
        for columna in range(ancho):
            # Map pixel to complex plane
            cr = xmin + columna * (xmax - xmin) / ancho
            ci = ymin + fila    * (ymax - ymin) / alto

            # Mandelbrot iteration: z = z² + c
            zr, zi, iteraciones = 0.0, 0.0, 0
            while zr * zr + zi * zi <= 4.0 and iteraciones < max_iter:
                zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
                iteraciones += 1

            resultados.append((fila, columna, iteraciones))

except ZeroDivisionError:
    print("Processing error: division by zero — check width/height values.")
    resultados = []

except Exception as e:
    print(f"Processing error: {e}")
    resultados = []

#OUTPUT

try:
    if not resultados:
        raise RuntimeError("No data to write — computation failed.")

    archivo = open('mandelbrot.csv', 'w')
    archivo.write('fila,columna,iteraciones\n')
    for fila, columna, iteraciones in resultados:
        archivo.write(f'{fila},{columna},{iteraciones}\n')
    archivo.close()

    print(f"CSV saved: mandelbrot.csv  ({ancho}x{alto} px, max_iter={max_iter})")

except IOError as e:
    print(f"File write error: {e}")
except RuntimeError as e:
    print(f"Output error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")