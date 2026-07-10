
# Classwork 13 - Error Handling: Verifier Digit

#INPUT 
valid = False
while not valid:
    try:
        rol_input = input("Enter the UTFSM rol (no hyphen, no verifier digit): ")

        # Must contain only digits
        if not rol_input.isdigit():
            raise ValueError("The rol must contain only numbers.")
        if len(rol_input) == 0:
            raise ValueError("The rol cannot be empty.")

        valid = True

    except ValueError as e:
        print(f"Input error: {e}. Please try again.")

#PROCESS 
try:
    rol = rol_input.strip()

    # Step 1: Reverse the rol string
    rol_invertido = rol[::-1]

    # Step 2: Multiply each digit by cycling sequence 2,3,4,5,6,7
    sequence = [2, 3, 4, 5, 6, 7]
    total = 0

    for i, digit_char in enumerate(rol_invertido):
        digit      = int(digit_char)
        multiplier = sequence[i % len(sequence)]
        total     += digit * multiplier

    # Step 3: Modulo 11
    resto = total % 11

    # Step 4: Subtract from 11
    diferencia = 11 - resto

    # Step 5: Determine verifier digit
    if diferencia == 11:
        digito_verificador = "0"
    elif diferencia == 10:
        digito_verificador = "K"
    else:
        digito_verificador = str(diferencia)

except Exception as e:
    print(f"Processing error: {e}")
    digito_verificador = "ERROR"

#OUTPUT
print(f"\n--- Result ---")
print(f"Rol entered       : {rol}")
print(f"Reversed rol      : {rol_invertido}")
print(f"Total sum         : {total}")
print(f"Modulo 11         : {total} % 11 = {resto}")
print(f"11 - {resto:<2}          = {diferencia}")
print(f"Verifier digit    : {digito_verificador}")
print(f"Complete rol      : {rol}-{digito_verificador}")