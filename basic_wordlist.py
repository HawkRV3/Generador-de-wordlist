#Creación de wordlist basica
import itertools
import re

def limpiar_texto(texto):
    """Elimina espacios adicionales y caracteres no deseados."""
    return texto.strip()

def obtener_datos():
    # Solicitar datos básicos
    nombre = limpiar_texto(input("Ingrese el nombre del objetivo: "))
    apellido = limpiar_texto(input("Ingrese el apellido del objetivo: "))
    
    # Fecha de nacimiento: se espera el formato dd/mm/yyyy
    fecha_nac = limpiar_texto(input("Ingrese la fecha de nacimiento (dd/mm/yyyy): "))
    dia, mes, anio = None, None, None
    if re.match(r"\d{1,2}/\d{1,2}/\d{4}", fecha_nac):
        dia, mes, anio = fecha_nac.split('/')
    else:
        print("Formato de fecha no reconocido. Se omite este dato.")

    # Otros datos personales
    apodo = limpiar_texto(input("Ingrese un apodo o alias (de ser aplicable): "))
    pareja = limpiar_texto(input("Ingrese el nombre de la pareja (si aplica): "))
    mascota = limpiar_texto(input("Ingrese el nombre de alguna mascota (si aplica): "))
    nacimiento_lugar = limpiar_texto(input("Ingrese el lugar de nacimiento (si aplica): "))
    
    # Datos extendidos: familiares, hobbies, eventos importantes
    familiares = limpiar_texto(input("Ingrese nombres de familiares (separados por comas): ")).split(',')
    hobbies = limpiar_texto(input("Ingrese hobbies o intereses (separados por comas): ")).split(',')
    eventos = limpiar_texto(input("Ingrese eventos o fechas importantes (separados por comas, ej: 'graduacion2020, boda'): ")).split(',')
    
    # Limpiar listas removiendo espacios y elementos vacíos
    familiares = [limpiar_texto(x) for x in familiares if x.strip()]
    hobbies = [limpiar_texto(x) for x in hobbies if x.strip()]
    eventos = [limpiar_texto(x) for x in eventos if x.strip()]
    
    datos = {
        "nombre": nombre,
        "apellido": apellido,
        "dia": dia,
        "mes": mes,
        "anio": anio,
        "apodo": apodo,
        "pareja": pareja,
        "mascota": mascota,
        "lugar": nacimiento_lugar,
        "familiares": familiares,
        "hobbies": hobbies,
        "eventos": eventos,
    }
    return datos

def generar_lista_palabras(datos):
    """Genera una lista base de palabras a partir de los datos ingresados."""
    lista = []

    # Datos básicos
    for campo in ['nombre', 'apellido', 'apodo', 'pareja', 'mascota', 'lugar']:
        if datos[campo]:
            lista.append(datos[campo])

    # Fecha de nacimiento y sus partes
    if datos["dia"]:
        lista.append(datos["dia"])
    if datos["mes"]:
        lista.append(datos["mes"])
    if datos["anio"]:
        lista.append(datos["anio"])
        # Algunas combinaciones con año corto
        lista.append(datos["anio"][-2:])

    # Combinar nombre y apellido en distintos órdenes
    if datos["nombre"] and datos["apellido"]:
        lista.append(datos["nombre"] + datos["apellido"])
        lista.append(datos["apellido"] + datos["nombre"])

    # Agregar elementos de las listas
    lista.extend(datos["familiares"])
    lista.extend(datos["hobbies"])
    lista.extend(datos["eventos"])
    
    # Eliminar duplicados y limpiar
    lista = list(set([x for x in lista if x]))
    return lista

def generar_variantes(base_words):
    """Genera variantes de cada palabra (minúsculas, mayúsculas, capitalizadas) y algunas con caracteres especiales."""
    variantes = set()
    caracteres_especiales = ['!', '@', '#', '$', '']
    
    for word in base_words:
        # Variantes básicas
        variantes.add(word.lower())
        variantes.add(word.upper())
        variantes.add(word.capitalize())
        
        # Variantes con agregados de caracteres especiales al final y al principio
        for char in caracteres_especiales:
            variantes.add(char + word.lower())
            variantes.add(word.lower() + char)
    return variantes

def generar_combinaciones(variantes):
    """Genera combinaciones simples entre dos o tres elementos y añade números."""
    contraseñas = set()
    
    # Agregar variantes individuales
    contraseñas.update(variantes)
    
    # Combinaciones de dos elementos
    for a, b in itertools.product(variantes, repeat=2):
        if a != b:
            contraseñas.add(a + b)
            contraseñas.add(a + "_" + b)
            contraseñas.add(a + "@" + b)
    
    # Combinaciones de tres elementos
    for a, b, c in itertools.product(variantes, repeat=3):
        contraseñas.add(a + b + c)
        contraseñas.add(a + "_" + b + "_" + c)
    
    # Añadir combinaciones con números al final (por ejemplo, 0-99)
    numeros = [str(i) for i in range(0, 100)]
    contraseñas_num = set()
    for pwd in contraseñas:
        for num in numeros:
            contraseñas_num.add(pwd + num)
    contraseñas.update(contraseñas_num)
    
    return contraseñas

def guardar_diccionario(contraseñas, filename="dictionary.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for pwd in contraseñas:
            f.write(pwd + "\n")
    print(f"Diccionario generado con {len(contraseñas)} contraseñas y guardado en '{filename}'.")

def main():
    print("=== Herramienta de generación de contraseñas ===")
    datos = obtener_datos()
    base_words = generar_lista_palabras(datos)
    variantes = generar_variantes(base_words)
    contraseñas = generar_combinaciones(variantes)
    guardar_diccionario(contraseñas)

if __name__ == "__main__":
    main()
