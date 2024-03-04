import simpy
import numpy as np

MAX_GAS = 10

class Car:
    def __init__(self, name, env, track, gas, laps):
        self.env = env
        self.name = name
        self.track = track
        if gas > MAX_GAS:
            self.gas = 10
        else:
            self.gas = gas
        self.laps = laps
        self.inicio = -1
        self.fin = -2
        print(f"{env.now}:Carro {name} gas: {self.gas}, laps: {self.laps}")

    def rest(self):
        print(env.now, "Va descanasar.", self.name)
        yield env.timeout(1)
        print(env.now, "Ya mucho.", self.name)

    def run(self):
        self.inicio = env.now
        print(f"{env.now} Carro {self.name} creado.")
        while (self.laps > 0):
            with self.track.request() as req:
                yield req # espera hasta que puede usar la pista
                print(f"{env.now} Carro {self.name} a entrado a la pista.")
                descanso = 1
                while self.gas > 0 and self.laps > 0:
                    # Mientras pueda seguir dando vueltas
                    self.gas -= 1 # gasta gas
                    self.laps -= 1 # tiene menos vueltas para dar
                    yield env.timeout(1) # Da una vuelta
                    if descanso == 3:
                        yield env.process(self.rest())
                    else:
                        descanso += 1
                    print("Aqui deberia descansa.")
                    print(f"{env.now} Carro {self.name} se quedo sin gasolna.")
            if self.gas == 0:
                print(f"{env.now} Carro {self.name} va poner gasolina")
                # le toma un tiempo aleatorio poner gasolina.
                yield env.timeout(
                    np.random.randint(5, 20))
                self.gas = MAX_GAS
                print(f"{env.now} Carro {self.name} termina de poner gasolina laps: {self.laps}")
            yield self.env.process(self.rest())
        self.fin = env.now


def simular(env, track):
    # creamos 10 carros
    for i in range(5):
        name = f"carro_{i}"
        newCar = Car(name, env, track,
                     np.random.randint(1, 5),
                     np.random.randint(5, 20))
        lista_carros.append(newCar)
        env.process(newCar.run())
        yield env.timeout(3) # np.random.normal(1, 10, 1) espera 3 ticks para poner otro carro


lista_carros = []
env = simpy.Environment()
track = simpy.Resource(env, capacity=1)  # Define the race track as a shared resource
print("Llamada a simular")
env.process(simular(env, track))

env.run()

for c in lista_carros:
    print(f"{c.inicio} -- {c.fin}")
