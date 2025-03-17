# Generador de Diccionarios de Contraseñas

Este repositorio contiene dos herramientas en Python para la generación de diccionarios de contraseñas basadas en datos personales. Inspiradas en la herramienta CUPP, se han desarrollado dos versiones:

- **basic_wordlist**: Genera una lista básica de palabras a partir de la información ingresada.
- **advanced_wordlist**: Amplía la funcionalidad de la versión básica incorporando variaciones, patrones de sustitución, combinaciones de palabras y filtrado basado en políticas de contraseñas.

---

## Introducción

Estas herramientas están diseñadas para generar diccionarios de contraseñas a partir de datos personales del objetivo. El enfoque principal es facilitar la elaboración de listas de contraseñas potenciales durante pruebas de penetración o auditorías de seguridad, siempre bajo un uso ético y autorizado.

La **basic_wordlist** es ideal para generar un conjunto simple de palabras clave, mientras que la **advanced_wordlist** proporciona un mayor grado de personalización y sofisticación, generando numerosas variantes y combinaciones de contraseñas basadas en reglas y políticas definidas por el usuario.

---

## Estructura General

Ambos scripts siguen una estructura modular que incluye:

- **Entrada de Datos**: Se recopilan datos personales básicos (nombre, apellido, fecha de nacimiento, apodo, etc.) y listas adicionales (familiares, hobbies).
- **Generación de Lista Base**: Se extraen palabras relevantes a partir de los datos ingresados.
- **Generación de Variantes**: Se crean variaciones de las palabras (cambios de mayúsculas/minúsculas, capitalización) y se aplican patrones de sustitución comunes.
- **Generación de Combinaciones**: Se generan combinaciones entre palabras y se añade variabilidad con sufijos numéricos.
- **Filtrado (en la versión avanzada)**: Se aplica un filtro basado en políticas de contraseñas (longitud mínima, requerimiento de mayúsculas, dígitos y caracteres especiales).

---

## Script Basic_Wordlist

### Funcionamiento Basic

El script básico:
- Solicita al usuario (o utiliza datos de ejemplo) información personal.
- Genera una lista de palabras base que incluyen elementos como nombre, apellido, apodo, fecha de nacimiento (día, mes, año, año corto), familiares y hobbies.
- Opcionalmente, combina algunos campos simples (por ejemplo, concatenando nombre y apellido).

Este script es perfecto para usuarios que necesiten una generación rápida y sencilla de una lista de palabras para formar contraseñas.

### Uso Basic

Ejecuta el script en modo interactivo o con datos de ejemplo:

```bash
python basic_wordlist.py -i
```
---

## Script Advanced_Wordlist

### Características y Funcionalidades

La versión avanzada amplía la funcionalidad del script básico incorporando:

- **Variaciones de Texto:** Cada palabra se transforma en versiones en minúsculas, mayúsculas y con la primera letra en mayúscula.
- **Patrones de Sustitución:** Se aplican sustituciones comunes (por ejemplo, a → @ o 4, e → 3) para generar variantes adicionales.
- **Generación de Combinaciones:** Se crean combinaciones de dos y tres elementos, y se añaden sufijos numéricos (del 0 al 99) para incrementar la diversidad.
- **Políticas de Contraseñas:** Permite definir requisitos como longitud mínima, presencia de mayúsculas, minúsculas, dígitos y caracteres especiales, filtrando las contraseñas que no cumplen dichos criterios.
- **Configuración vía Línea de Comandos:** Con argparse, se pueden establecer opciones como el modo interactivo, las políticas de contraseña y el nombre del archivo de salida.

### Funcionamiento Advanced

- **Entrada de Datos**
  - Modo interactivo: Se solicita información personal y listas separadas por comas.
  - Modo no interactivo: Se usan datos de ejemplo.
- **Generación de Lista Base**
  - Se compilan palabras relevantes de los datos ingresados, incluyendo combinaciones simples como nombre+apellido.
- **Generación de Variantes**
  - Cada palabra se convierte a diferentes formatos (minúsculas, mayúsculas, capitalizadas).
  - Se aplican patrones de sustitución para aumentar la variabilidad.
- **Generación de Combinaciones**
  - Se generan combinaciones de dos y tres elementos, con diversas uniones (por ejemplo, concatenación directa, con guiones bajos o arrobas).
  - Se añaden sufijos numéricos a cada contraseña generada.
- **Filtrado Basado en Políticas**
  - Se verifica que cada contraseña cumpla con los requisitos definidos (por ejemplo, longitud mínima y complejidad).
  - Solo se guardan aquellas contraseñas que cumplen la política.
- **Guardado del Diccionario**
  - El resultado se guarda en un archivo de texto (por defecto, dictionary.txt).

### Uso Advanced

Ejecuta el script avanzado con opciones de configuración:

```bash
python advanced_wordlist.py -i --min-length 10 --require-upper --require-digit --require-special --output my_dictionary.txt
```

- `-i` o `--interactive`: Activa el modo interactivo.
- `--min-length`: Establece la longitud mínima de las contraseñas.
- `--require-upper`, `--require-digit`, `--require-special`: Especifica los requisitos de complejidad.
- `--output`: Define el nombre del archivo donde se guardará el diccionario.


---

## Requisitos

- Python 3
- Las bibliotecas utilizadas son estándar: itertools, argparse, re y typing.

---

## Advertencia

### Nota Importante:

Estas herramientas deben usarse exclusivamente para fines educativos y pruebas de seguridad autorizadas. El uso no autorizado puede ser ilegal y está sujeto a consecuencias legales.

