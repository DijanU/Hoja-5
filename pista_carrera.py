import simpy
import random

# Definición de constantes
NUM_CARS = 10
LOUNGE_SIZE = 3
GAS_STATION_WAIT_MEAN = 5


# Funcion para simular el carro
def car(env, car_id, laps, lounge, gas_station):
    print(f'{env.now}:El carro {car_id} llega a la cola del waiting room. Carros en espera {len(lounge.queue)}')
    with lounge.request() as req:
        yield req
        print(f'{env.now}: Car {car_id} entra a waiting room (lounge).')
        yield env.timeout(1)  # Tiempo de preparación del carro.
        print(f'{env.now}: Car {car_id} Está listo para entrar a la pista.')
        for lap in range(1, laps + 1):
            print(f'{env.now}: Car {car_id} vuelta: {lap}/{laps}')
            yield env.timeout(1)  # Time to complete lap
            if lap % 3 == 0:  # Time for gas after every 3 laps
                print(f'{env.now}: Car {car_id} Va a la estación de gasolina.')
                with gas_station.request() as gas_req:
                    yield gas_req
                    gas_wait_time = random.expovariate(1 / GAS_STATION_WAIT_MEAN)
                    yield env.timeout(gas_wait_time)
                    print(f'Car {car_id} finishes refueling at {env.now}')
        print(f'Car {car_id} exits the track at {env.now}')


# Function to generate cars
def generate_cars(env, lounge, gas_station):
    for i in range(NUM_CARS):
        laps = random.randint(4, 20)
        car_id = f'Car-{i+1}'
        env.process(car(env, car_id, laps, lounge, gas_station))
        yield env.timeout(2)  # Time between car arrivals


# Setup and start the simulation
env = simpy.Environment()
lounge = simpy.Resource(env, capacity=LOUNGE_SIZE)
gas_station = simpy.Resource(env, capacity=1)
env.process(generate_cars(env, lounge, gas_station))
env.run()