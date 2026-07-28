"""
Classwork #16 - Recursive Functions
File: recursive_functions.py
"""


# 1. Countdown recursion — recursiva(n)

def recursiva(n):
    """
    Imprime números desde n hasta 1 y retorna 'Done!'.
    Maneja errores si n no es un entero no negativo o si no es de tipo int.
    """
    try:
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("El parámetro 'n' debe ser un número entero.")
        if n < 0:
            raise ValueError("El parámetro 'n' debe ser un entero mayor o igual a 0.")

        # BASE CASE
        if n == 0:
            return "Done!"
        else:
            print(n)
            return recursiva(n - 1)

    except (TypeError, ValueError, RecursionError) as e:
        print(f"Error en recursiva(): {e}")
        return None


# 2. Fibonacci — fibonacci(n)

def fibonacci(n):
    """
    Calcula el n-ésimo número de Fibonacci.
    Maneja números negativos y tipos de datos inválidos.
    """
    try:
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("El parámetro 'n' debe ser un número entero.")
        if n < 0:
            raise ValueError("El parámetro 'n' no puede ser negativo.")

        # BASE CASE
        if n == 0 or n == 1:
            return n
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    except (TypeError, ValueError, RecursionError) as e:
        print(f"Error en fibonacci(): {e}")
        return None



# 3. Factorial — factorial(n)

def factorial(n):
    """
    Calcula el factorial de n.
    Maneja enteros negativos y números decimales/tipos no enteros.
    """
    try:
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("El parámetro 'n' debe ser un entero.")
        if n < 0:
            raise ValueError("El factorial no está definido para enteros negativos.")

        # BASE CASE
        if n == 0 or n == 1:
            return 1
        else:
            return factorial(n - 1) * n

    except (TypeError, ValueError, RecursionError) as e:
        print(f"Error en factorial(): {e}")
        return None


# 4. Recursive multiplication — multiplicacion_recursiva(n, m)
def multiplicacion_recursiva(n, m):
    """
    Multiplica dos números mediante sumas recursivas.
    Soporta multiplicadores negativos ajustando el signo.
    """
    try:
        if not (isinstance(n, (int, float)) and isinstance(m, (int, float))) or isinstance(n, bool) or isinstance(m, bool):
            raise TypeError("Los parámetros deben ser numéricos (int o float).")

        # Manejo de m negativo para evitar recursión infinita
        if m < 0:
            return -multiplicacion_recursiva(n, -m)

        # BASE CASE
        if m == 0:
            return 0
        else:
            return multiplicacion_recursiva(n, m - 1) + n

    except (TypeError, RecursionError) as e:
        print(f"Error en multiplicacion_recursiva(): {e}")
        return None



# 5. Integer division — division_entera_recursiva(dividendo, divisor)

def division_entera_recursiva(dividendo, divisor):
    """
    Realiza la división entera de forma recursiva mediante restas repetidas.
    Maneja división entre cero y valores negativos.
    """
    try:
        if not (isinstance(dividendo, int) and isinstance(divisor, int)) or isinstance(dividendo, bool) or isinstance(divisor, bool):
            raise TypeError("Los argumentos deben ser enteros.")
        if divisor == 0:
            raise ZeroDivisionError("No se puede dividir entre cero.")

        # Manejo de signos para números negativos
        if dividendo < 0 and divisor < 0:
            return division_entera_recursiva(-dividendo, -divisor)
        if dividendo < 0:
            return -division_entera_recursiva(-dividendo, divisor)
        if divisor < 0:
            return -division_entera_recursiva(dividendo, -divisor)

        # BASE CASE
        if dividendo - divisor < 0:
            return 0
        else:
            return division_entera_recursiva(dividendo - divisor, divisor) + 1

    except (TypeError, ZeroDivisionError, RecursionError) as e:
        print(f"Error en division_entera_recursiva(): {e}")
        return None



# 6. Power — potencia_recursiva(base, exponente)

def potencia_recursiva(base, exponente):
    """
    Calcula base^exponente recursivamente.
    Soporta exponentes negativos.
    """
    try:
        if not (isinstance(base, (int, float)) and isinstance(exponente, int)) or isinstance(base, bool) or isinstance(exponente, bool):
            raise TypeError("La base debe ser numérica y el exponente debe ser un entero.")

        # Soporte para exponentes negativos (matemáticamente correcto)
        if exponente < 0:
            if base == 0:
                raise ZeroDivisionError("Cero no puede ser elevado a un exponente negativo.")
            return 1 / potencia_recursiva(base, -exponente)

        # BASE CASE
        if exponente == 0:
            return 1
        else:
            return potencia_recursiva(base, exponente - 1) * base

    except (TypeError, ZeroDivisionError, RecursionError) as e:
        print(f"Error en potencia_recursiva(): {e}")
        return None



# 7. Collatz sequence — serie_collatz(n)

def serie_collatz(n):
    """
    Genera e imprime la secuencia de Collatz hasta llegar a 1.
    Maneja enteros <= 0 e insumos no enteros.
    """
    try:
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("El valor de 'n' debe ser un número entero.")
        if n <= 0:
            raise ValueError("La serie de Collatz solo está definida para enteros estrictamente positivos (n >= 1).")

        # BASE CASE
        if n == 1:
            print("END!")
            return 0
        else:
            if n % 2 == 0:
                print(n // 2)
                return serie_collatz(n // 2)
            else:
                print(3 * n + 1)
                return serie_collatz(3 * n + 1)

    except (TypeError, ValueError, RecursionError) as e:
        print(f"Error en serie_collatz(): {e}")
        return None



# 8. Flattening a JSON — aplanar_json(diccionario, clave_padre, separador)

def aplanar_json(diccionario, clave_padre='', separador='.'):
    """
    Aplanar un diccionario anidado.
    Maneja listas de forma recursiva e insumos que no sean diccionarios.
    """
    try:
        if not isinstance(diccionario, (dict, list)):
            raise TypeError("El insumo principal debe ser un diccionario o una lista.")

        elementos = []

        # Si el nivel superior o valor actual es una lista
        if isinstance(diccionario, list):
            for i, item in enumerate(diccionario):
                nueva_llave = f"{clave_padre}{separador}{i}" if clave_padre else str(i)
                if isinstance(item, (dict, list)):
                    res = aplanar_json(item, nueva_llave, separador)
                    if res is not None:
                        elementos.extend(res.items())
                else:
                    elementos.append((nueva_llave, item))
            return dict(elementos)

        # Si el valor actual es un diccionario
        for key, value in diccionario.items():
            nueva_llave = f"{clave_padre}{separador}{key}" if clave_padre else str(key)
            if isinstance(value, (dict, list)):
                res = aplanar_json(value, nueva_llave, separador)
                if res is not None:
                    elementos.extend(res.items())
            else:
                elementos.append((nueva_llave, value))

        return dict(elementos)

    except (TypeError, AttributeError, RecursionError) as e:
        print(f"Error en aplanar_json(): {e}")
        return None



# Pruebas Rápidas (Main Block)

if __name__ == "__main__":
    print("--- 1. recursiva ---")
    recursiva(3)
    recursiva(-3)  # Maneja error sin crash

    print("\n--- 2. fibonacci ---")
    print(f"fibonacci(7): {fibonacci(7)}")
    fibonacci(-1)  # Maneja error sin crash

    print("\n--- 3. factorial ---")
    print(f"factorial(5): {factorial(5)}")
    factorial(1.5)  # Maneja error sin crash

    print("\n--- 4. multiplicacion_recursiva ---")
    print(f"4 * 3: {multiplicacion_recursiva(4, 3)}")
    print(f"4 * -3: {multiplicacion_recursiva(4, -3)}")

    print("\n--- 5. division_entera_recursiva ---")
    print(f"17 // 5: {division_entera_recursiva(17, 5)}")
    division_entera_recursiva(10, 0)  # Maneja error sin crash

    print("\n--- 6. potencia_recursiva ---")
    print(f"2^5: {potencia_recursiva(2, 5)}")
    print(f"2^-2: {potencia_recursiva(2, -2)}")

    print("\n--- 7. serie_collatz ---")
    serie_collatz(6)
    serie_collatz(-6)  # Maneja error sin crash

    print("\n--- 8. aplanar_json ---")
    json_prueba = {
        "a": 1,
        "b": {"c": 2, "d": {"e": 3}},
        "f": [1, 2, 3],
        "g": [{"h": 4}, {"i": 5}],
        "j": {"k": [6, 7, {"l": 8}]},
        "m": None,
        "n": True,
        "o": []
    }
    print(aplanar_json(json_prueba))