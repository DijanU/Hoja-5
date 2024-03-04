import simpy
import numpy as np
import csv


class RAM:
    def __init__(self, env, init=200, capacity=200):
        self.env = env
        self.container = simpy.Container(env, init=init, capacity=capacity)

    def get(self, memoria):
        return self.container.get(memoria)

    def put(self, memoria):
        return self.container.put(memoria)

class CPU:
    def __init__(self, env, capacity=6):
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)

    def request(self):
        return self.resource.request()
    
class Process:
    def __init__(self, name, env, memory, instruction):
        self.env = env
        self.name = name
        self.memory = memory
        self.instruction = instruction
        self.start = None
        self.finish = None
        self.time = None

    def set_finish_time(self):
        if self.start is not None and self.finish is not None:
            self.time = self.finish - self.start

    def run(self, ram, cpu):
        # Verificar si hay suficiente memoria RAM
        if ram.container.level >= self.memory:
            # Verificar si la CPU está disponible
            with cpu.request() as req:
                yield req  # Esperar hasta que la CPU esté disponible
                print(f"Proceso {self.name}: Ejecutando en CPU")

                # Solicitar memoria RAM
                yield ram.get(self.memory)
                print(f"Proceso {self.name}: Asignadas {self.memory} unidades de memoria RAM. Memoria disponible: {ram.container.level}")
                if self.start is None:
                    self.start = self.env.now

                # Ejecutar instrucciones
                for i in range(self.instruction):
                    print(f"Proceso {self.name}: Ejecutando instrucción {i+1}")
                    yield self.env.timeout(1)  # Simular el tiempo de ejecución de una instrucción

                # Liberar memoria RAM
                yield ram.put(self.memory)
                print(f"Proceso {self.name}: Liberando {self.memory} unidades de memoria RAM")
                self.finish = self.env.now
                self.set_finish_time()
        else:
            print(f"Proceso {self.name}: No hay suficiente memoria RAM disponible")


def simular(env, ram, simsize, cpu):
    # creamos el numero de procesos que entra como paraemtro
    for i in range(simsize):
        name = f"process_{i}"
        memoria = np.random.randint(1, 10)
        instrucciones = np.random.randint(1, 10)
        newProcess = Process(name, env, memoria, instrucciones)
        lista_procesos.append(newProcess)
        env.process(newProcess.run(ram, cpu))
        yield env.timeout(1) # np.random.normal(1, 10, 1) espera 3 ticks para poner otro proceso

# Configuración de la simulación


sims = 200

lista_procesos = []
env = simpy.Environment()
cpu1 = CPU(env, capacity=10)  # Crear dos recursos de CPU
cpu2 = CPU(env, capacity=10)  # Crear el segundo recurso de CPU
RAM = RAM(env, init=200, capacity=200)  # Aumentar la capacidad de la RAM a 200
env.process(simular(env, RAM, sims, cpu1))
env.process(simular(env, RAM, sims, cpu2)) 
print("Llamada a simular")
env.run()


for proceso in lista_procesos:
    print("Cantidad de Procesos,Nombre,Hora de Inicio,Hora de Fin,Tiempo Total")
    print(f"{proceso.name},{proceso.start},{proceso.finish},{proceso.time}")


with open("procesadores_2_simulacion_"+str(sims)+"_procesos.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Cantidad de Procesos", "Nombre", "Hora de Inicio", "Hora de Fin", "Tiempo Total"])
    for proceso in lista_procesos:
        writer.writerow([len(lista_procesos), proceso.name, proceso.start, proceso.finish, proceso.time])

print("Los resultados se han guardado en el archivo 'simulacion_procesos.csv'.")