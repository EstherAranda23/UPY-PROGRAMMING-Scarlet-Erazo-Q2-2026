
# Classwork #11 - The Mandelbrot Set

# INPUT
print("Reading configuration...")

# Initialize an empty dictionary to store config options
config = {}

# Fix pathing issues: target config.txt in the same folder as this script
# We build the path manually to avoid using the forbidden 'os' library
# Open configuration file
file = open("config.txt", "r", encoding="utf-8-sig")
# Read configuration
for line in file:
    line = line.strip()

    if line != "":
        key, value = line.split("=")
        config[key] = float(value)

file.close()

print(config)
# Double check that the file actually contained data
if "width" not in config:
    print("ERROR: config.txt was found but it seems empty or formatted incorrectly!")
    print("Current dictionary contents:", config)
else:
    print("Configuration loaded.")

# Extract and convert parameters to proper types
width = int(config["width"])
height = int(config["height"])
max_iter = int(config["max_iter"])
real_min = config["real_min"]
real_max = config["real_max"]
imag_min = config["imag_min"]
imag_max = config["imag_max"]

# PROCESS & OUTPUT
print("Computing Mandelbrot Set...")
print("Saving CSV...")

# Open the output CSV file for writing data
csv_file = open("mandelbrot.csv", "w")

# Write the CSV column header line
csv_file.write("row,column,iterations\n")

# Loop over every pixel row by row
for row in range(height):
    for column in range(width):
        
        # Map pixel coordinates to the complex plane scale
        # Calculate real part fraction relative to total width
        real_fraction = column / (width - 1)
        real = real_min + real_fraction * (real_max - real_min)
        
        # Calculate imaginary part fraction relative to total height
        # Top rows map to max imaginary value down to min imaginary value
        imag_fraction = row / (height - 1)
        imag = imag_max - imag_fraction * (imag_max - imag_min)
        
        # Generate the complex number using Python's built-in type
        c = complex(real, imag)
        
        # Initialize variables for the Mandelbrot escape sequence math
        z = complex(0.0, 0.0)
        iterations = 0
        
        # Iterate sequence algorithm until it escapes boundary or hits maximum limit
        while abs(z) <= 2.0 and iterations < max_iter:
            z = z * z + c
            iterations = iterations + 1
            
        # Format dataset line as text string
        output_line = str(row) + "," + str(column) + "," + str(iterations) + "\n"
        
        # Save dataset line into the CSV output file
        csv_file.write(output_line)

# Close the CSV file to flush data safely to disk
csv_file.close()

print("Done!")
print("CSV file created successfully.")