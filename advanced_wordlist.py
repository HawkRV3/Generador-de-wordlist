#Creación de wordlist avanzada
import itertools
import re
import argparse
from typing import Set, List

# Diccionario de sustituciones: se pueden ampliar o modificar
SUBSTITUTIONS = {
    'a': ['@', '4'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['$', '5'],
    'l': ['1', '|']
}

def limpiar_texto(texto: str) -> str:
    """Elimina espacios extra y limpia el texto."""
    return texto.strip()

def obtener_datos_interactivo() -> dict:
    """Solicita datos de entrada al usuario mediante preguntas."""
    datos = {}
    datos["nombre"] = limpiar_texto(input("Ingrese el nombre: "))
    datos["apellido"] = limpiar_texto(input("Ingrese el apellido: "))
    datos["fecha_nac"] = limpiar_texto(input("Ingrese la fecha de nacimiento (dd/mm/yyyy): "))
    datos["apodo"] = limpiar_texto(input("Ingrese el apodo: "))
    datos["mascota"] = limpiar_texto(input("Ingrese el nombre de una mascota: "))
    datos["familiares"] = [limpiar_texto(x) for x in input("Nombres de familiares (separados por comas): ").split(',') if x]
    datos["hobbies"] = [limpiar_texto(x) for x in input("Hobbies o intereses (separados por comas): ").split(',') if x]
    return datos

def generar_lista_palabras(datos: dict) -> List[str]:
    """Genera una lista base de palabras a partir de los datos ingresados."""
    lista = []
    for campo in ["nombre", "apellido", "apodo", "mascota"]:
        if datos.get(campo):
            lista.append(datos[campo])
    if datos.get("fecha_nac"):
        match = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", datos["fecha_nac"])
        if match:
            dia, mes, anio = match.groups()
            lista.extend([dia, mes, anio, anio[-2:]])
    lista.extend(datos.get("familiares", []))
    lista.extend(datos.get("hobbies", []))
    if datos.get("nombre") and datos.get("apellido"):
        lista.append(datos["nombre"] + datos["apellido"])
        lista.append(datos["apellido"] + datos["nombre"])
    return list(set(lista))

def apply_substitutions(word: str, subs: dict = SUBSTITUTIONS) -> Set[str]:
    """Genera variantes de una palabra aplicando sustituciones (por ejemplo, 'a' → '@')."""
    variants = {word}
    for i, char in enumerate(word):
        lower_char = char.lower()
        if lower_char in subs:
            new_variants = set()
            for variant in variants:
                for sub in subs[lower_char]:
                    new_variant = variant[:i] + sub + variant[i+1:]
                    new_variants.add(new_variant)
            variants.update(new_variants)
    return variants

def generar_variantes(base_words: List[str]) -> Set[str]:
    """Crea variantes de cada palabra en minúsculas, mayúsculas, capitalizadas y con sustituciones."""
    variantes = set()
    for word in base_words:
        variantes.add(word.lower())
        variantes.add(word.upper())
        variantes.add(word.capitalize())
        # Aplica las sustituciones sobre la versión en minúsculas
        subs_variants = apply_substitutions(word.lower())
        variantes.update(subs_variants)
    return variantes

def generar_combinaciones(variantes: Set[str]) -> Set[str]:
    """Genera combinaciones de 2 y 3 elementos, y añade sufijos numéricos (0 a 99)."""
    contraseñas = set(variantes)
    
    # Combinaciones de dos elementos
    for a, b in itertools.product(variantes, repeat=2):
        if a != b:
            contraseñas.add(a + b)
            contraseñas.add(a + "_" + b)
            contraseñas.add(a + "@" + b)
    
    # Combinaciones de tres elementos (se pueden limitar para evitar explosión combinatoria)
    for combo in itertools.product(variantes, repeat=3):
        password = "".join(combo)
        contraseñas.add(password)
        contraseñas.add("_".join(combo))
    
    # Añadir sufijos numéricos (0 a 99)
    numeros = [str(i) for i in range(100)]
    contraseñas_num = set()
    for pwd in contraseñas:
        for num in numeros:
            contraseñas_num.add(pwd + num)
    contraseñas.update(contraseñas_num)
    return contraseñas

def cumple_politica(pwd: str, min_length: int, require_upper: bool,
                    require_lower: bool, require_digit: bool,
                    require_special: bool) -> bool:
    """Valida que la contraseña cumpla con la política establecida."""
    if len(pwd) < min_length:
        return False
    if require_upper and not any(c.isupper() for c in pwd):
        return False
    if require_lower and not any(c.islower() for c in pwd):
        return False
    if require_digit and not any(c.isdigit() for c in pwd):
        return False
    if require_special and not any(c in "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?`~" for c in pwd):
        return False
    return True

def filtrar_por_politica(contraseñas: Set[str], min_length: int, require_upper: bool,
                          require_lower: bool, require_digit: bool,
                          require_special: bool) -> Set[str]:
    """Filtra el conjunto de contraseñas para que cumplan la política definida."""
    return {pwd for pwd in contraseñas if cumple_politica(pwd, min_length, require_upper, require_lower, require_digit, require_special)}

def guardar_diccionario(contraseñas: Set[str], filename: str = "dictionary.txt"):
    """Guarda el diccionario generado en un archivo de texto."""
    with open(filename, "w", encoding="utf-8") as f:
        for pwd in sorted(contraseñas):
            f.write(pwd + "\n")
    print(f"Diccionario generado con {len(contraseñas)} contraseñas y guardado en '{filename}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Generador de diccionarios de contraseñas basado en perfiles, con variaciones, patrones y reglas basadas en políticas."
    )
    parser.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo para ingresar datos")
    parser.add_argument("--min-length", type=int, default=8, help="Longitud mínima de la contraseña (default: 8)")
    parser.add_argument("--require-upper", action="store_true", help="Requerir al menos una letra mayúscula")
    parser.add_argument("--require-lower", action="store_true", help="Requerir al menos una letra minúscula")
    parser.add_argument("--require-digit", action="store_true", help="Requerir al menos un dígito")
    parser.add_argument("--require-special", action="store_true", help="Requerir al menos un carácter especial")
    parser.add_argument("--output", type=str, default="dictionary.txt", help="Nombre del archivo de salida")
    
    args = parser.parse_args()
    
    if args.interactive:
        datos = obtener_datos_interactivo()
    else:
        # Datos de ejemplo en caso de no usar el modo interactivo
        datos = {
            "nombre": "Juan",
            "apellido": "Perez",
            "fecha_nac": "01/01/1990",
            "apodo": "JP",
            "mascota": "Max",
            "familiares": ["Ana", "Luis"],
            "hobbies": ["futbol", "correr"]
        }
        print("Usando datos de ejemplo:", datos)
    
    base_words = generar_lista_palabras(datos)
    variantes = generar_variantes(base_words)
    contraseñas = generar_combinaciones(variantes)
    
    # Filtra según las políticas definidas
    contraseñas_filtradas = filtrar_por_politica(
        contraseñas,
        args.min_length,
        args.require_upper,
        args.require_lower,
        args.require_digit,
        args.require_special
    )
    
    guardar_diccionario(contraseñas_filtradas, args.output)

if __name__ == "__main__":
    main()
