"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 5
NPED = 7
TIME_CARS_NORTH = 0.5  # a new car enters each 0.5s
TIME_CARS_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) # normal 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.patata = Value('i', 0)
        self.nped=Value('i',0)
        self.ncarN=Value('i',0)
        self.ncarS=Value('i',0)
        self.ForCarsS= Condition(self.mutex)
        self.ForCarsN= Condition(self.mutex) 
        self.ForPed= Condition (self.mutex)
        #waiting
        self.waiting1=Value('i',0) #numero de coches-norte esperando
        self.waiting2=Value('i',0) #numero de coches-sur esperando
        self.waiting3=Value('i',0) #numero de peatones esperando
        self.NoWaiting=Condition(self.mutex)
        
    #necesitamos tres condiciones y tres funciones booleanas
    def no_cars_north_or_ped(self):
        return self.ncarN.value==0 and self.nped.value==0
    
    def no_cars_south_or_ped(self):
        return self.ncarS.value==0 and self.nped.value==0
    
    def no_cars(self):
        return self.ncarN.value==0 and self.ncarS.value==0

    def atLeast51(self):
        return self.waiting2.value + self.waiting3.value <= 5
    
    def atLeast52(self):
        return self.waiting1.value + self.waiting3.value <= 5
    
    def atLeast53(self):
        return self.waiting2.value + self.waiting1.value <= 5
    
    #tenemos un problema si todos los waiting son del mismo tipo, direccion 
    #lo solucionamos con tres variables waiting para diferenciar tipos

    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        if direction==NORTH:
            self.waiting1.value +=1
            self.NoWaiting.wait_for(self.atLeast51)
            self.ForCarsN.wait_for(self.no_cars_south_or_ped)
            self.ncarN.value+=1
            self.waiting1.value -=1
            self.NoWaiting.notify_all()
        else:
            self.waiting2.value +=1
            self.NoWaiting.wait_for(self.atLeast52)
            self.ForCarsS.wait_for(self.no_cars_north_or_ped)
            self.ncarS.value+=1
            self.waiting2.value-=1
            self.NoWaiting.notify_all()

        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        self.patata.value += 1
        if direction==NORTH:
            self.ncarN.value-=1
            self.ForCarsS.notify_all()
        else: 
            self.ncarS.value-=1
            self.ForCarsN.notify_all()
        self.ForPed.notify_all()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.waiting3.value+=1
        self.NoWaiting.wait_for(self.atLeast53)
        self.ForPed.wait_for(self.no_cars)
        self.nped.value+=1
        self.waiting3.value-=1
        self.NoWaiting.notify_all()
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.nped.value-=1
        self.ForCarsN.notify_all()
        self.ForCarsS.notify_all()
        self.mutex.release()

    def __repr__(self) -> str:
        return f'Monitor: {self.patata.value} Terminado: {self.patata.value==2*(NPED+2*NCARS)}'

def delay_car_north() -> None:
    time.sleep(abs(random.normalvariate(TIME_IN_BRIDGE_CARS[0],TIME_IN_BRIDGE_CARS[1])))
    
def delay_pedestrian() -> None:
    time.sleep(abs(random.normalvariate(TIME_IN_BRIDGE_PEDESTRIAN[0],TIME_IN_BRIDGE_PEDESTRIAN[1])))
    

def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"\n car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    delay_car_north()
    
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")



def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/time_cars))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars_north = Process(target=gen_cars, args=(NORTH, TIME_CARS_NORTH, monitor))
    gcars_south = Process(target=gen_cars, args=(SOUTH, TIME_CARS_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_north.start()
    gcars_south.start()
    gped.start()
    gcars_north.join()
    gcars_south.join()
    gped.join()
    #han acabado todos si monitor.patata.value== 2+(NPED+2*NCARS)

if __name__ == '__main__':
    main()
