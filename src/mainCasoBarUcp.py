from typing import Callable
import simpy
from simpy import Environment, Resource
#import random
import csv
import os
from typing import TypeVar, Any

WriterType = TypeVar('WriterType', bound=csv.writer) # truco para obtener el tipo writer de la libreria de csv

# Parámetros de la simulación
LLEGADA = (1.0, 3.0)  # Tasa de llegada de clientes (entre 1 y 3 minutos)
TIEMPO_SERVICIO_CAJA = (0.3, 0.7)  # Tiempo de servicio en caja (minutos)
TIEMPO_SERVICIO_BARRA = (2, 4.5)  # Tiempo de servicio en barra (minutos)

NUM_CAJEROS = 1  # Número de cajeros
NUM_BARRAS = 1  # Número de barras



RandomGeneratorFunction = Callable[[float, float], float]


# Function to get the next available filename
def get_next_filename(base_name: str):
    # If the base file doesn't exist, return it
    if not os.path.exists(base_name):
        return base_name
    
    # Split the filename and extension
    name, ext = os.path.splitext(base_name)
    counter = 1
    
    # Keep trying new filenames until we find one that doesn't exist
    while True:
        new_name = f"{name}_{counter}{ext}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

# Función para simular la llegada de clientes
def cliente(env: Environment, nombre: str, quiosco: dict[str, Resource], writer: WriterType, random_func: RandomGeneratorFunction):
    llegada = env.now
    print(f'{nombre} llega al quiosco en {llegada:.2f} minutos.')
    tiempo_entrega_barra= 0
    
    with quiosco['caja'].request() as request:
        yield request
        tiempo_servicio_caja = random_func(*TIEMPO_SERVICIO_CAJA)
        yield env.timeout(tiempo_servicio_caja)
        tiempo_atencion_caja = env.now
        print(f'{nombre} es atendido en caja en {tiempo_atencion_caja:.2f} minutos.')

    # si el tiempo de atencion de caja se pasa del 80% del maximo del tiempo ir a la barra
    if tiempo_servicio_caja > ( 0.8 * TIEMPO_SERVICIO_CAJA[1]):
        with quiosco['barra'].request() as request:
            yield request
            tiempo_servicio_barra = random_func(*TIEMPO_SERVICIO_BARRA)
            yield env.timeout(tiempo_servicio_barra)
            tiempo_entrega_barra = env.now
            print(f'{nombre} recibe su pedido en barra en {tiempo_entrega_barra:.2f} minutos.')

    # Guardar datos en el CSV
    writer.writerow([nombre, llegada, tiempo_atencion_caja, tiempo_entrega_barra])

# Función para simular la llegada de clientes
def llegada_clientes(env: Environment, quiosco: dict[str, Resource], writer: WriterType, random_func: RandomGeneratorFunction):
    cliente_id = 1
    while True:
        yield env.timeout(random_func(*LLEGADA))
        env.process(cliente(env, f'Cliente {cliente_id}', quiosco, writer, random_func))
        cliente_id += 1

# Función principal de la simulación
def simular_quiosco(random_func: RandomGeneratorFunction, nombreArchivoCsv= "resultados_quiosco"):
    """
    Ejecuta la simulación del quiosco.
    
    Args:
        random_func: Función que genera números aleatorios. Por defecto usa random.expovariate.
                    Para tiempos de servicio debe aceptar dos parámetros (min, max) y devolver un número entre ellos.
                    Para llegadas debe aceptar un parámetro lambda y devolver un tiempo exponencial.
    """
    env = simpy.Environment()
    quiosco = {
        'caja': simpy.Resource(env, capacity=NUM_CAJEROS),
        'barra': simpy.Resource(env, capacity=NUM_BARRAS)
    }
    
    # Get the next available filename
    filename = get_next_filename(f'{nombreArchivoCsv}.csv')
    
    # Crear y abrir el archivo CSV para escritura
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escribir encabezados en el CSV
        writer.writerow(['Cliente', 'Llegada (min)', 'Atencion en Caja (min)', 'Entrega en Barra (min)'])
        
        env.process(llegada_clientes(env, quiosco, writer, random_func))
        
        # Ejecutar la simulación durante un tiempo determinado (por ejemplo, 120 minutos)
        env.run(until=120)

indiceValorLlegada= 0
indiceValorCaja= 0
IndiceValorBarra= 0

# Para usar una función personalizada:
with open("valoresGenerados.txt") as archivo:
  valoresArchivo= archivo.read().replace("[]", "").split(', ') 
indiceArchivo= 0 # saber cual es el siguiente valor a tomar

def obtenerSiguienteValorDeArchivo():
    """
    los valores del archivo tienen que estar normalizados,
    sino no funcionara correctamente
    devuelve: un valor flotante de 0 a 1
    """
    global indiceArchivo
    if indiceArchivo > len(valoresArchivo) - 1:
      print("Se usaron todos los valores del archivo") # para que el usuario sepa si tendria que agregar mas valores al archivo
      indiceArchivo= 0
    valorObtenido= float(valoresArchivo[indiceArchivo])
    indiceArchivo+= 1
    return valorObtenido
  

def obtenerValorAleatorio(min: float, max: float):
    diferencia= max - min # se saca la diferencia entre el maximo y el minimo
    valorDeAdicion= diferencia * obtenerSiguienteValorDeArchivo()
    valorFinal= min + valorDeAdicion
    return valorFinal

    
simular_quiosco(obtenerValorAleatorio)
