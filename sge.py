"""
Sistema de Gestión de Estudiantes (SGE) básico
==============================================
Programa de consola (solo texto) con un menú para:
    1. Agregar estudiantes
    2. Mostrar la lista completa
    3. Buscar un estudiante por ID
    4. Salir

Necesita Python 3.10 o mayor porque uso `match`, que es el "switch" de Python.
Para correrlo:  python sge.py
"""

# ---------------------------------------------------------------------------
# CONSTANTES
# ---------------------------------------------------------------------------
# Número máximo de estudiantes. Puse un tope para que la lista no crezca sin
# límite y para poder probar qué pasa cuando la lista ya está llena.
MAX_ESTUDIANTES = 20

ID_MINIMO = 1
ID_MAXIMO = 999999
EDAD_MINIMA = 5
EDAD_MAXIMA = 99
LONGITUD_MAXIMA_NOMBRE = 25
LONGITUD_MAXIMA_CARRERA = 30


# ---------------------------------------------------------------------------
# FUNCIONES DE ENTRADA (con validación)
# ---------------------------------------------------------------------------
def leer_entero(mensaje, minimo, maximo):
    """Pide un número entero entre minimo y maximo y vuelve a preguntar hasta que sea válido.

    Uso try/except porque si el usuario escribe letras, int() da error (ValueError)
    y el programa se cerraría. Así solo muestro un aviso y pregunto otra vez.
    """
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("  [!] Entrada inválida: escribe un número entero.")
            continue

        if valor < minimo or valor > maximo:
            print(f"  [!] El valor debe estar entre {minimo} y {maximo}.")
            continue

        return valor


def leer_texto(mensaje, longitud_maxima, solo_letras):
    """Pide un texto que no esté vacío y que no pase de `longitud_maxima` caracteres.

    Si `solo_letras` es True, no acepta números ni símbolos (un nombre no los lleva).
    Sí acepto espacios, punto, guion y apóstrofo (por ejemplo "O'Brien").
    """
    while True:
        texto = input(mensaje).strip()

        if texto == "":
            print("  [!] Este campo no puede quedar vacío.")
            continue

        if len(texto) > longitud_maxima:
            print(f"  [!] Máximo {longitud_maxima} caracteres.")
            continue

        if solo_letras and not all(c.isalpha() or c in " .-'" for c in texto):
            print("  [!] Usa solo letras (se permiten espacios, punto, guion y apóstrofo).")
            continue

        return texto


# ---------------------------------------------------------------------------
# FUNCIONES DE SALIDA
# ---------------------------------------------------------------------------
def mostrar_menu(total_estudiantes):
    """Imprime el menú y cuántos estudiantes hay registrados."""
    print()
    print("=" * 46)
    print("   SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE)")
    print("=" * 46)
    print(f"   Estudiantes registrados: {total_estudiantes}/{MAX_ESTUDIANTES}")
    print("-" * 46)
    print("   1. Agregar estudiante")
    print("   2. Mostrar todos los estudiantes")
    print("   3. Buscar estudiante por ID")
    print("   4. Salir")
    print("=" * 46)


def mostrar_encabezado_tabla():
    """Imprime los títulos de las columnas de la tabla."""
    print(f"{'ID':<8}{'NOMBRE':<27}{'EDAD':<6}CARRERA")
    print("-" * 71)


def mostrar_estudiante(estudiante):
    """Imprime los datos de UN estudiante en una fila.

    La hice como función aparte para usarla en "Mostrar todos" y en "Buscar por ID"
    y no escribir el mismo código dos veces.
    """
    print(
        f"{estudiante['id']:<8}"
        f"{estudiante['nombre']:<27}"
        f"{estudiante['edad']:<6}"
        f"{estudiante['carrera']}"
    )


# ---------------------------------------------------------------------------
# FUNCIONES DE LÓGICA
# ---------------------------------------------------------------------------
def buscar_indice_por_id(estudiantes, id_buscado):
    """Revisa la lista uno por uno y devuelve la posición del estudiante con ese ID.

    Si no lo encuentra devuelve -1 (no existe ninguna posición -1, así que no se confunde).
    La uso al agregar (para no repetir IDs) y al buscar.
    """
    for indice in range(len(estudiantes)):
        if estudiantes[indice]["id"] == id_buscado:
            return indice
    return -1


def agregar_estudiante(estudiantes, total_estudiantes):
    """Pide los datos de un estudiante nuevo y lo guarda en la lista.

    Devuelve el contador `total_estudiantes` ya actualizado.
    """
    print("\n--- AGREGAR ESTUDIANTE ---")

    # Primero reviso que la lista no esté llena.
    if total_estudiantes >= MAX_ESTUDIANTES:
        print(f"  [!] Capacidad máxima alcanzada ({MAX_ESTUDIANTES}). No se puede agregar más.")
        return total_estudiantes

    # El ID no se puede repetir: pregunto de nuevo mientras ya exista.
    while True:
        id_nuevo = leer_entero(f"ID ({ID_MINIMO}-{ID_MAXIMO}): ", ID_MINIMO, ID_MAXIMO)
        if buscar_indice_por_id(estudiantes, id_nuevo) == -1:
            break
        print(f"  [!] Ya existe un estudiante con el ID {id_nuevo}. Intenta con otro.")

    nombre = leer_texto("Nombre completo: ", LONGITUD_MAXIMA_NOMBRE, solo_letras=True)
    edad = leer_entero(f"Edad ({EDAD_MINIMA}-{EDAD_MAXIMA}): ", EDAD_MINIMA, EDAD_MAXIMA)
    carrera = leer_texto("Carrera: ", LONGITUD_MAXIMA_CARRERA, solo_letras=False)

    estudiantes.append({"id": id_nuevo, "nombre": nombre, "edad": edad, "carrera": carrera})
    total_estudiantes = total_estudiantes + 1

    print(f"  [OK] Estudiante '{nombre}' agregado correctamente.")
    return total_estudiantes


def mostrar_todos(estudiantes, total_estudiantes):
    """Muestra la tabla con todos los estudiantes."""
    print("\n--- LISTA DE ESTUDIANTES ---")

    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return

    mostrar_encabezado_tabla()
    for estudiante in estudiantes:
        mostrar_estudiante(estudiante)
    print(f"\nTotal: {total_estudiantes} estudiante(s).")


def buscar_por_id(estudiantes, total_estudiantes):
    """Pide un ID y muestra ese estudiante, o avisa que no existe."""
    print("\n--- BUSCAR ESTUDIANTE POR ID ---")

    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return

    id_buscado = leer_entero(f"ID a buscar ({ID_MINIMO}-{ID_MAXIMO}): ", ID_MINIMO, ID_MAXIMO)
    indice = buscar_indice_por_id(estudiantes, id_buscado)

    if indice == -1:
        print(f"  [X] No se encontró ningún estudiante con el ID {id_buscado}.")
    else:
        print("  [OK] Estudiante encontrado:\n")
        mostrar_encabezado_tabla()
        mostrar_estudiante(estudiantes[indice])


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    estudiantes = []          # aquí guardo a los estudiantes (cada uno es un diccionario)
    total_estudiantes = 0     # variable de conteo: cuántos estudiantes hay
    bandera_salir = False     # bandera: cuando cambia a True se termina el ciclo

    try:
        # Ciclo while: el menú se repite hasta que el usuario elija salir.
        while not bandera_salir:
            mostrar_menu(total_estudiantes)
            opcion = leer_entero("Seleccione una opción (1-4): ", 1, 4)

            # match (switch): según la opción llamo a la función que corresponde.
            match opcion:
                case 1:
                    total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
                case 2:
                    mostrar_todos(estudiantes, total_estudiantes)
                case 3:
                    buscar_por_id(estudiantes, total_estudiantes)
                case 4:
                    bandera_salir = True
                    print("\nGracias por usar el SGE. ¡Hasta pronto!")
                case _:
                    # leer_entero ya solo deja pasar 1 a 4; este caso es por seguridad.
                    print("  [!] Opción no reconocida.")

    except (EOFError, KeyboardInterrupt):
        # Si el usuario presiona Ctrl+C, cierro el programa sin mostrar un error feo.
        print("\n\nEntrada interrumpida. Cerrando el SGE...")


if __name__ == "__main__":
    main()
