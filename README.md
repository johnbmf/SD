### Instanciacion de una torre:
-En una terminal, instanciaremos una torre de control. Para ello abrir una terminal
en la carpeta "aeropuerto".  
-Ejecutar: python torre.py  
-En nombre del aeropuerto solo está disponible: Santiago, Antofagasta, Lima  
-Solo estan disponibles tales nombres para hacer un match con puertos pre establecidos de comunicación.  
-Ingresar cantidad de pistas de aterrizaje. Se recomienda un valor bajo (ej: 2) para posteriormente probar la cola de aviones.  
-Ingresar cantidad de pistas de despegue.  

### Instanciacion de un avion:
-Para la instalación de los modulos necesarios para la correcta ejecución, nos ubicamos en el directorio ../SD/aeropuerto/ una vez en ese directorio, se ejecuta el comando npm install.   
-En una terminal, instanciaremos un avion. Para ello abrir una terminal en la carpeta 
"aeropuerto".  
-Ejecutar: node avion.js  
-En nombre avion poner cualquier nombre (ej: STG4555)  
-En carga maxima, ingresar la carga maxima del avion.  
-En capacidad de combustible maxima, ingresar la cantidad maxima de combustible del avion.  
-IMPORTANTE: en torre inicial, si se quiere iniciar en Santiago se debe poner localhost:50051 .  
Si se quiere iniciar en Antofagasta se debe poner localhost:50061.
Si se quiere iniciar en Lima se debe poner localhost:50071.   
-Se pedirá aterrizaje en la torre inicial (sujeto a disponibilidad de pistas).  
-Una vez aterrizado, se despliegan opciones de cargar combustible, seleccionar carga actual y peticion para despegar.  
-Cuando se carga combustible este se llena al max (y se reduce a la mitad con cada viaje).  
-Cuando se quiere despegar, se debe indicar el nombre del destino (Santiago, Antofagasta o Lima).  

### Instanciacion de la pantalla
-En una terminal, instanciaremos una pantalla. Para ello abrir una terminal en la carpeta "aeropuerto".  
-Ejecutar: ruby pantalla.rb  
-La pantalla solo se instancia y no logra comunicacion con la torre de control.  

### Limitacion de pistas y encolamiento
-La torre de control limita las pistas encolando aviones que intenten usar las pistas
cuando otro avion ya está usándolas. Además se indica el avión predecesor como el avión
que está antes en la cola.

### Control del espacio aereo
-La torre de control indica a que altura esperar para un aterrizaje. Este valor
varía de avión en avión dependiendo cuantos aviones estén encolados esperando su
turno.

### Ayuda
En caso de tener algun tipo de problema o duda con la instalación de gRPC para los lenguajes utilizados puede consultar el siguiente link https://grpc.io/docs/quickstart/ 
�
