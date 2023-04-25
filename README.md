# Practica2_Puente

SKEL.PY
El archivo skel.py tiene la versión básica y correcta del problema
Contiene un monitor con las variables
-nped= numero de peatones que se encuentran cruzando el puente
-Analogamente ncarN= numero de coches norte y ncarS= numero de coches sur
Además tiene tres variables condicion
-ForCarsS, que es para coches sur: que va asociada a la funcion booleana no_cars_north_or_ped

Tenemos cuatro funciones wants_leave_car, leaves_car, wants_enter_pedestrian y leaves_pedestrian que son las cuatro secciones criticas que tenemos (el lock mutex va a asociado a ellas)

SKEL_REALISTA.PY
El archivo skel_realista.py tiene la versión realista que incorpora waitings
Como no es muy realista que si hay 50 coches esperando desde el norte que pasen todos seguidos, añadimos unas variables waiting (numero de peatones esperando, y analogamente para los coches) y una variable condicion NoWaiting que cuenta cuantos hay esperando en funcion de las variables waiting

El archivo Demostración.pdf incluye las demostraciones del invariante, ausencia de inanición, ausencia de bloqueo(deadlock) y problemas de justicia
Además explica las diferencia entre la versión básica(skel.py) y la realista (skel_realista.py)
