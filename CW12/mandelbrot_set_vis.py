# Classwork #12 - The Mandelbrot Set


from PIL import Image


# INPUT


# Configuration constants (adjust dimensions if your original grid used different limits)
width = 800
height = 600
max_iter = 100

# Open and read the raw Mandelbrot data generated in Classwork 12
try:
    archivo = open(r'C:\Users\Surface\Documents\GitHub\Erazo23-UPY-PROGRAMMING-SCARLET-ERAZO-Q2-2026\CW12\mandelbrot12.csv', 'r')
    lineas = archivo.readlines()
    archivo.close()
except FileNotFoundError:
    print("Error: 'mandelbrot12.csv' not found. Please run your Classwork 11 script first.")
    exit()

# Skip the header row to extract data
datos = lineas[1:]

# Create a new grayscale ('L') image canvas
img = Image.new('L', (width, height))


# PROCESS


for linea in datos:
    # Clean string and extract the row, column, and iteration values
    fila, columna, iteraciones = linea.strip().split(',')
    fila = int(fila)
    columna = int(columna)
    iteraciones = int(iteraciones)
    
    # Calculate pixel brightness: 0 (black) if inside the set, normalized 0-255 if outside
    if iteraciones == max_iter:
        brillo = 0
    else:
        brillo = int((iteraciones / max_iter) * 255)
    
    # Map data to the image canvas. Note: (x, y) correlates to (columna, fila)
    img.putpixel((columna, fila), brillo)


# OUTPUT


# Save the finalized visual presentation to disk
img.save('mandelbrot.png')
print("Success: 'mandelbrot.png' has been successfully generated and saved.")