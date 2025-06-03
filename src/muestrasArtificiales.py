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
  elif parametrosDeGeneracion["nombre"] == "Multiplicative Congruential":
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



def main():
    # Historia 3: Cargar datos desde un JSON
    datos = cargar_datos_generacion("muestraArtificial.json")

    # Historia 4: Procesar la tabla de contingencia
    if "tabla_contingencia" not in datos:
        print("ERROR: El archivo JSON no contiene una tabla de contingencia.")
        return
    if "parametros_generador" not in datos:
        print("ERROR: El archivo JSON no contiene los parametros de generacion.")
        return
    tablaDeContingencia: dict[str, float]= datos["tabla_contingencia"]
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
