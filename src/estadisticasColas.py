def simular_m_m_1(tiempos_llegada, tiempos_servicio):
    n = len(tiempos_llegada)
    
    tiempo_inicio_servicio = []
    tiempo_fin_servicio = []
    tiempo_en_cola = []
    tiempo_en_sistema = []

    reloj_servidor = 0
    tiempo_ocupado = 0

    for i in range(n):
        llegada = tiempos_llegada[i]
        servicio = tiempos_servicio[i]

        # El cliente empieza cuando llega o cuando se libera el servidor, lo que ocurra después
        inicio = max(llegada, reloj_servidor)
        fin = inicio + servicio

        tiempo_inicio_servicio.append(inicio)
        tiempo_fin_servicio.append(fin)

        tiempo_en_cola.append(inicio - llegada)
        tiempo_en_sistema.append(fin - llegada)

        # Avanzamos el reloj del servidor
        reloj_servidor = fin
        tiempo_ocupado += servicio

    tiempo_simulado = tiempo_fin_servicio[-1]

    Wq = sum(tiempo_en_cola) / n
    W = sum(tiempo_en_sistema) / n
    Lq = Wq * n / tiempo_simulado
    L = W * n / tiempo_simulado
    rho = tiempo_ocupado / tiempo_simulado

    return {
        "Wq (Tiempo promedio en cola)": round(Wq, 2),
        "W  (Tiempo promedio en sistema)": round(W, 2),
        "Lq (Longitud promedio de cola)": round(Lq, 2),
        "L  (Nº promedio en el sistema)": round(L, 2),
        "ρ   (Utilización del servidor)": round(rho, 2),
    }

'''
# Ejemplo: tiempos ya generados artificialmente
tiempos_llegada = [0, 2.5, 5.8, 9.0, 13.0, 15.1]
tiempos_servicio = [4, 3.2, 5, 2.8, 3.1, 4.2]

resultados = simular_m_m_1(tiempos_llegada, tiempos_servicio)

for clave, valor in resultados.items():
    print(f"{clave}: {valor}")
'''