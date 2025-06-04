import glob
import json
from collections import Counter
from prng.mid_square import generate_sequence as von_neumann_generate
from prng.fibonacci import generate_sequence as fibonacci_generate
from prng.congruential_mixed import generate_sequence as mixed_generate
from prng.congruential_additive import generate_sequence as additive_generate
from prng.congruential_multiplicative import generate_sequence as multiplicative_generate
from prng.normaliser import normaliser
from prng.chi_square import chi_square_test

from prng.normaliser import normaliser

def cargar_datos_generacion(archivo_json):
    """Historia 3: Cargar datos de un archivo JSON."""
    with open(archivo_json, 'r') as archivo:
        datos = json.load(archivo)
    return datos

def pedir_parametros(parametros_requeridos):
    """Historia 2: Pedir parámetros para el generador elegido."""
    parametros = {}
    for param in parametros_requeridos:
        valor = input(f"Ingrese el valor para '{param}': ")
        parametros[param] = float(valor) if valor.replace('.', '', 1).isdigit() else valor
    return parametros

def generarDatosNormalizados(parametrosDeGeneracion: dict) -> list[float]: # TODO
  sequence = None  # Initialize sequence variable
  # Call appropriate PRNG method
  if parametrosDeGeneracion["nombre"] == "Von Neumann":
      sequence = von_neumann_generate(
          n=parametrosDeGeneracion['n'],
          d=parametrosDeGeneracion['d'],
          x1=parametrosDeGeneracion['x1']
      )
      # Normalize using 10^d
      normalized = normaliser(sequence, 10 ** parametrosDeGeneracion['d'])
  elif parametrosDeGeneracion["nombre"] == "Fibonacci":
      sequence = fibonacci_generate(
          n=parametrosDeGeneracion['n'],
          x0=parametrosDeGeneracion['x0'],
          x1=parametrosDeGeneracion['x1'],
          m=parametrosDeGeneracion['m']
      )
      normalized = normaliser(sequence, parametrosDeGeneracion['m'])
  elif parametrosDeGeneracion["nombre"] == "Mixed Congruential":
      sequence = mixed_generate(
          n=parametrosDeGeneracion['n'],
          x0=parametrosDeGeneracion['x0'],
          a=parametrosDeGeneracion['a'],
          c=parametrosDeGeneracion['c'],
          m=parametrosDeGeneracion['m']
      )
      normalized = normaliser(sequence, parametrosDeGeneracion['m'])
  elif parametrosDeGeneracion["nombre"] == "Additive Congruential":
      sequence = additive_generate(
          n=parametrosDeGeneracion['n'],
          x0=parametrosDeGeneracion['x0'],
          c=parametrosDeGeneracion['c'],
          m=parametrosDeGeneracion['m']
      )
      normalized = normaliser(sequence, parametrosDeGeneracion['m'])
  elif parametrosDeGeneracion["nombre"] == "Congruencial Multiplicativo":
      sequence = multiplicative_generate(
          n=parametrosDeGeneracion['n'],
          x0=parametrosDeGeneracion['x0'],
          a=parametrosDeGeneracion['a'],
          m=parametrosDeGeneracion['m']
      )
      normalized = normaliser(sequence, parametrosDeGeneracion['m'])
  
  if sequence is None:
      raise ValueError("No sequence was generated")

  return normalized

def elejirArchivo():
    # pedir al usuario que elija de los archivos que cumplen el patron muestra_artificial_*.json

    # Obtener lista de archivos que coinciden con el patrón
    archivos = glob.glob("muestra_artificial_*.json")
    
    if not archivos:
        print("No se encontraron archivos de muestra artificial.")
        return None
    
    # Mostrar opciones al usuario
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    # Pedir al usuario que elija
    while True:
        try:
            eleccion = int(input("\nElija un número de archivo: "))
            if 1 <= eleccion <= len(archivos):
                filename = archivos[eleccion - 1]
                print(f"\nArchivo seleccionado: {filename}")
                return cargar_datos_generacion(filename)
            else:
                print("Número de archivo inválido. Intente de nuevo.")
        except ValueError:
            print("Por favor ingrese un número válido.")

def main():
    # Historia 3: Cargar datos desde un JSON
    datos = elejirArchivo()
    if datos is None:
        return

    # Historia 4: Procesar la tabla de contingencia
    if "tabla_contingencia" not in datos:
        print("ERROR: El archivo JSON no contiene una tabla de contingencia.")
        return
    if "parametros_generador" not in datos:
        print("ERROR: El archivo JSON no contiene los parametros de generacion.")
        return

    tablaDeContingenciaRaw: dict[str, float]= datos["tabla_contingencia"]
    tablaDeContingencia: dict[str, float]= {}
    ultimoValorAgregado= 0
    for nombreValor, valor in tablaDeContingenciaRaw.items():
        # sumar el valor del ultimo agregado
        tablaDeContingencia[nombreValor] = valor + ultimoValorAgregado
        ultimoValorAgregado = tablaDeContingencia[nombreValor]

    if ultimoValorAgregado > 1:
        raise Exception(f'El porcentaje total dio mas del 100%({ultimoValorAgregado})')

    # Historia 2: Selección de generador
    datosDeGeneracionNormalizados = generarDatosNormalizados(datos['parametros_generador'])

    # Lista para almacenar los valores artificiales generados
    valoresArtificiales = []
    for numeroNormalizado in datosDeGeneracionNormalizados:
        for nombreVariableArtificial, valor in tablaDeContingencia.items():
            if numeroNormalizado <= valor:
                valoresArtificiales.append(nombreVariableArtificial)
                break  # Una vez encontrado el valor, pasamos al siguiente número

    # Imprimir los valores artificiales
    print(valoresArtificiales)

    print(f"cantidad generada: {len(valoresArtificiales)}")
    
    # Contar y mostrar la frecuencia de cada elemento
    frecuencias = Counter(valoresArtificiales)
    print("\nFrecuencia de cada elemento:")
    for elemento, cantidad in frecuencias.items():
        print(f"{elemento}: {cantidad}")



if __name__ == "__main__":
    main()
