import simpy
import random

# Define constants
NUM_CARS = 10
GAS_STATION_CAPACITY = 1
GAS_STATION_WAIT_MEAN = 5
TRACK_CAPACITY = 1


# Function to simulate a car
def car(env, car_id, gas_station, track):
    arrival_time = env.now
    print(f'Carro {car_id} llega a {arrival_time}')
    with gas_station.request() as req:
        yield req
        start_refuel_time = env.now
        print(f'Car {car_id} inicia a llenar su tanque {start_refuel_time}')
        fueling_time = 20
        yield env.timeout(fueling_time)  # Fueling time
        end_refuel_time = env.now
        print(f'Car {car_id} termino de llenar {end_refuel_time}')
        refuel_wait_time = start_refuel_time - arrival_time
        print(f'Car {car_id} espera {refuel_wait_time} para llenar.')

    print(f'Car {car_id} entra a la pista {env.now}')
    with track.request() as req:
        yield req
        print(f'Car {car_id} entra a la pista {env.now}')
        yield env.timeout(random.randint(1, 5))  # Time to complete laps
        print(f'Car {car_id} sale de la pista {env.now}')


# Function to print the status of the gas station queue
def print_queue_status(env, gas_station):
    count  = 0
    while count < 10 and len(gas_station.queue) > 0:
        print(f'Gas station queue at time {env.now}: {len(gas_station.queue)} cars waiting')
        count +=1
        yield env.timeout(1)  # Print status every minute


# Function to generate cars
def generate_cars(env, gas_station, track):
    for i in range(NUM_CARS):
        car_id = f'Car-{i+1}'
        env.process(car(env, car_id, gas_station, track))
        yield env.timeout(random.randint(1, 5))  # Time between car arrivals


# Setup and start the simulation
env = simpy.Environment()
gas_station = simpy.Resource(env, capacity=GAS_STATION_CAPACITY)
track = simpy.Resource(env, capacity=TRACK_CAPACITY)
env.process(generate_cars(env, gas_station, track))
env.process(print_queue_status(env, gas_station))
env.run()
