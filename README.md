# Practica2_Puente
Un puente compartido por peatones y vehículos. La anchura del puente no permite el paso de vehículos en ambos sentidos.
Por motivos de seguridad los peatones y los vehículos no pueden compartir el puente. 
En el caso de los peatones, sí que que pueden pasar peatones en sentido contrario.

Escribe el invariante del monitor.
Demuestra que el puente es seguro (no hay coches y peatones a la vez en el puente,
no hay coches en sentidos opuestos)
Demuestra la ausencia de deadlocks
Demuestra la ausencia de inanición

El archivo skel.py tiene la versión básica y correcta del problema
El archivo skel_realista.py tiene la versión realista que incorpora waitings
El archivo Demostración.pdf incluye las demostraciones del invariante, ausencia de inanición, bloqueo
además explica las diferencia entre la versión básica y la realista
