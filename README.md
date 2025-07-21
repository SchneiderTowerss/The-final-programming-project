Asigna los vuelos según las condiciones del momento

Muestra el estado de los aeropuertos cada media hora de simulación

Lógica de la Simulación
JMC (Rionegro): abierto 24/7 — acepta vuelos internacionales — capacidad: 35 vuelos

EOH (Medellín): abierto de 6:00 a 18:00 — solo nacionales y aviones pequeños — capacidad: 15 vuelos

Las emergencias y el mal tiempo influyen en la asignación de los vuelos

Estructura del Código
CondicionesClimaticas — Gestiona el clima

Avion — Clase base para los aviones

AvionComercial y AvionMilitar — Definen el comportamiento específico de cada tipo

Aeropuerto — Controla vuelos asignados y clima

DespachadorVuelos — Administra la simulación y la toma de decisiones

Ejecución
Solo corré el archivo Python para ver la simulación:

bash
Copy
Edit
python simulador.py
Cada simulación genera vuelos, actualiza el clima y muestra las decisiones que toma el despachador.
