# INPUT
# Read configuration parameters from config.txt
config = {}

file = open("config.txt", "r")

for line in file:
    parameter, value = line.strip().split("=")
    config[parameter] = float(value) if "." in value else int(value)
file.close()

# Assign configuration values to descriptive variables
width = config["ancho"]
height = config["alto"]
max_iter = config["max_iter"]

# Prepare the output file structure
output = open("mandelbrot.csv", "w")
output.write("row,column,iterations\n")



# PROCESS & OUTPUT

# In this section, we process each pixel and output the results directly to the file

for row in range(height):
    for column in range(width):
        # PROCESS: Map screen pixels to the complex plane numbers
        real = config["real_min"] + (column / width) * (config["real_max"] - config["real_min"])
        imag = config["imag_min"] + (row / height) * (config["imag_max"] - config["imag_min"])
        c = complex(real, imag)
        
        z = 0 + 0j
        iterations = 0
        
        # PROCESS: Mandelbrot iteration loop
        while (abs(z) <= 2) and (iterations < max_iter):
            z = z * z + c
            iterations += 1
        
        # OUTPUT: Write the computed iteration results for the current pixel
        output.write(f"{row},{column},{iterations}\n")

# Close file after processing completes
output.close()