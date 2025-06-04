import glob
import json
from collections import Counter
from prng.mid_square import generate_sequence as von_neumann_generate
from prng.fibonacci import generate_sequence as fibonacci_generate
from prng.congruential_mixed import generate_sequence as mixed_generate
from prng.congruential_additive import generate_sequence as additive_generate
from prng.congruential_multiplicative import generate_sequence as multiplicative_generate
from prng.normaliser import normaliser
from prng.chi_square import chi_square_test, chi_square_test_uniform, chi_square_test_distribution
from prng.distributions import create_distribution
from prng.queue_models import create_queue_model

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

def generarDatosNormalizados(parametrosDeGeneracion: dict) -> list[float]:
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

def generarMuestraArtificial(datos: dict) -> list:
    """Generate artificial sample using the specified distribution."""
    # Generate normalized random numbers
    normalized = generarDatosNormalizados(datos["parametros_generador"])
    
    # Create distribution and generate values
    distribution = create_distribution(datos["metodo_distribucion"])
    return distribution.generate(normalized)

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

def analizar_cola(datos: dict) -> None:
    """Analyze queue model metrics"""
    if "modelo_cola" not in datos:
        return

    try:
        # Create queue model
        queue_model = create_queue_model(
            datos["modelo_cola"]["tipo"],
            datos["modelo_cola"]["parametros"]
        )
        
        # Get metrics
        metrics = queue_model.get_metrics()
        
        # Print results
        print("\n=== MÉTRICAS DEL MODELO DE COLA ===")
        print(f"Tipo de modelo: {datos['modelo_cola']['tipo']}")
        print(f"Tasa de llegada (λ): {datos['modelo_cola']['parametros']['lambda_rate']}")
        print(f"Tasa de servicio (μ): {datos['modelo_cola']['parametros']['mu_rate']}")
        if datos['modelo_cola']['tipo'] == 'MM1K':
            print(f"Capacidad máxima (K): {datos['modelo_cola']['parametros']['K']}")
        
        print("\nMétricas calculadas:")
        print(f"Intensidad de tráfico (ρ): {metrics['rho']:.4f}")
        print(f"Número promedio de clientes en el sistema (L): {metrics['L']:.4f}")
        print(f"Número promedio de clientes en la cola (Lq): {metrics['Lq']:.4f}")
        print(f"Tiempo promedio en el sistema (W): {metrics['W']:.4f}")
        print(f"Tiempo promedio en la cola (Wq): {metrics['Wq']:.4f}")
        print(f"Probabilidad de sistema vacío (P0): {metrics['P0']:.4f}")
        
        if datos['modelo_cola']['tipo'] == 'MM1K':
            print(f"Probabilidad de sistema lleno (PK): {metrics['PK']:.4f}")
            print(f"Tasa efectiva de llegada (λ_eff): {metrics['lambda_eff']:.4f}")
        
    except ValueError as e:
        print(f"\nError en el modelo de cola: {str(e)}")
    except Exception as e:
        print(f"\nError al analizar el modelo de cola: {str(e)}")

def main():
    # Historia 3: Cargar datos desde un JSON
    datos = elejirArchivo()
    if datos is None:
        return

    # Verificar que el archivo tenga la estructura correcta
    if "metodo_distribucion" not in datos:
        print("ERROR: El archivo JSON no contiene el método de distribución.")
        return
    if "parametros_generador" not in datos:
        print("ERROR: El archivo JSON no contiene los parámetros de generación.")
        return

    try:
        # Generar números normalizados
        numerosNormalizados = generarDatosNormalizados(datos["parametros_generador"])
        
        # Realizar prueba chi-cuadrado en los números normalizados
        chi_square_uniform, p_value_uniform, df_uniform = chi_square_test_uniform(numerosNormalizados)
        
        # Generar la muestra artificial usando el sistema de distribuciones
        distribution = create_distribution(datos["metodo_distribucion"])
        valoresArtificiales = distribution.generate(numerosNormalizados)
        
        # Obtener probabilidades teóricas
        theoretical_probs = distribution.get_theoretical_probabilities()
        
        # Realizar prueba chi-cuadrado en la distribución
        chi_square_dist, p_value_dist, df_dist = chi_square_test_distribution(
            valoresArtificiales, theoretical_probs)

        # Imprimir los valores normalizados
        print("\nValores normalizados generados:")
        print(numerosNormalizados)
        
        # Imprimir resultados de la prueba chi-cuadrado para uniformidad
        print("\nResultados de la prueba chi-cuadrado (uniformidad):")
        print(f"Valor chi-cuadrado: {chi_square_uniform:.4f}")
        print(f"Grados de libertad: {df_uniform}")
        print(f"p-valor: {p_value_uniform:.4f}")
        print(f"Interpretación: {'PASA' if p_value_uniform > 0.05 else 'NO PASA'} la prueba de aleatoriedad")
        
        # Imprimir resultados de la prueba chi-cuadrado para la distribución
        print("\nResultados de la prueba chi-cuadrado (distribución):")
        print(f"Valor chi-cuadrado: {chi_square_dist:.4f}")
        print(f"Grados de libertad: {df_dist}")
        print(f"p-valor: {p_value_dist:.4f}")
        print(f"Interpretación: {'PASA' if p_value_dist > 0.05 else 'NO PASA'} la prueba de ajuste a la distribución")

        # Imprimir los valores artificiales
        print("\nValores generados según la distribución:")
        print(valoresArtificiales)
        print(f"\nCantidad generada: {len(valoresArtificiales)}")
        
        # Contar y mostrar la frecuencia de cada elemento
        frecuencias = Counter(valoresArtificiales)
        print("\nFrecuencias observadas vs teóricas:")
        for elemento, cantidad in frecuencias.items():
            prob_teorica = theoretical_probs.get(elemento, 0)
            print(f"{elemento}: {cantidad} \t\t({cantidad/len(valoresArtificiales)*100:.1f}%) vs {prob_teorica*100:.1f}% teórico")

        # Analizar modelo de cola si está presente
        analizar_cola(datos)

    except Exception as e:
        print(f"Error al generar la muestra: {str(e)}")

if __name__ == "__main__":
    main()
