# Classwork 13 - Error Handling: Spanish Verb Conjugator



#PROCESS: Required structures

pronombres = ['yo', 'tu', 'el', 'nosotros', 'vosotros', 'ellos']

terminaciones = {
    'ar': ['o', 'as', 'a', 'amos', 'ais', 'an'],
    'er': ['o', 'es', 'e', 'emos', 'eis', 'en'],
    'ir': ['o', 'es', 'e', 'imos', 'is', 'en']
}

#INPUT
valid = False
while not valid:
    try:
        verbo = input("Ingrese verbo: ").strip().lower()

        # Must be at least 3 characters
        if len(verbo) < 3:
            raise ValueError("The verb is too short.")

        # Must end in -ar, -er, or -ir
        ending = verbo[-2:]
        if ending not in terminaciones:
            raise ValueError(f"'{verbo}' does not end in -ar, -er, or -ir.")

        # Must contain only letters
        if not verbo.isalpha():
            raise ValueError("The verb must contain only letters.")

        valid = True

    except ValueError as e:
        print(f"Input error: {e} Please try again.")

#PROCESS
try:
    stem         = verbo[:-2]
    endings_list = terminaciones[ending]

except KeyError:
    print(f"Processing error: no endings found for '-{ending}'.")
    endings_list = None

except Exception as e:
    print(f"Processing error: {e}")
    endings_list = None

#OUTPUT
if endings_list is not None:
    for i in range(len(pronombres)):
        print(pronombres[i], stem + endings_list[i])
else:
    print("Could not conjugate the verb due to an error.")