# Classwork 13 - Error Handling: Numerical Integration

import math

#INPUT
# Get and validate left endpoint
valid = False
while not valid:
    try:
        a = input("Write the left endpoint of the interval: ")
        if "pi" in a:
            a = eval(a.replace("pi", str(math.pi)))
        else:
            a = float(a)
        valid = True
    except ValueError:
        print("Input error: please enter a valid number or expression (e.g. 0, pi/2).")

# Get and validate right endpoint
valid = False
while not valid:
    try:
        b = input("Write the right endpoint of the interval: ")
        if "pi" in b:
            b = eval(b.replace("pi", str(math.pi)))
        else:
            b = float(b)
        if b <= a:
            raise ValueError("Right endpoint must be greater than left endpoint.")
        valid = True
    except ValueError as e:
        print(f"Input error: {e}")

# Get function
f_x = input("Write the function to integrate (use 'x'): ")

# Get and validate method
valid = False
while not valid:
    method = input("Write the integration method (LRM/RRM/MRM/TRAP): ").upper()
    if method in ("LRM", "RRM", "MRM", "TRAP"):
        valid = True
    else:
        print("Input error: method must be LRM, RRM, MRM, or TRAP.")

#PROCESS 
try:
    n        = 1000
    h        = (b - a) / n
    area     = 0.0
    constant = 0
    shift    = 0

    if method == "RRM":
        shift = 1
    if method == "MRM":
        constant = h / 2

    if method == "TRAP":
        f_0   = f_x.replace("x", str(a))
        area += (h / 2) * eval(f_0)

        for i in range(1, n):
            xi   = a + i * h
            f_xi = f_x.replace("x", str(xi))
            area += (h / 2) * 2 * eval(f_xi)

        f_xn  = f_x.replace("x", str(b))
        area += (h / 2) * eval(f_xn)

    else:
        for i in range(shift, n + shift):
            xi     = a + i * h
            height = f_x.replace("x", str(xi + constant))
            area  += h * eval(height)

except ZeroDivisionError:
    print("Processing error: division by zero in the function.")
    area = None
except SyntaxError:
    print("Processing error: invalid function syntax. Use valid Python math (e.g. x**2, x+1).")
    area = None
except Exception as e:
    print(f"Processing error: {e}")
    area = None

#OUTPUT
if area is not None:
    print(f"\nThe integration of {f_x} from {a} to {b} is: {area}")
else:
    print("Could not compute the integral due to an error.")