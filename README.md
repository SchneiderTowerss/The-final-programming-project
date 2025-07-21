# Simulador de Asignación de Vuelos — JMC y EOH
 Autores: Santiago Flórez Roldán — Schneider Alejandro Torres Ortega

# Descripción
 Este proyecto simula la asignación de vuelos hacia el Aeropuerto José María Córdova (JMC) y el Aeropuerto Olaya Herrera (EOH), considerando:
- Tipo de avión (comercial o militar)
- Condiciones climáticas aleatorias
- Emergencias simuladas
- Horarios y restricciones de operación de cada aeropuerto

El código aplica programación orientada a objetos para modelar el comportamiento de las aeronaves y la gestión aeroportuaria.

# ¿Qué hace el programa?
- Genera aviones comerciales y militares con matrículas según el operador
- Simula eventos meteorológicos como niebla, lluvia y tormenta
- Gestiona emergencias con baja probabilidad
- Asigna los vuelos al aeropuerto más adecuado según las condiciones
- Controla el tráfico aéreo cada 30 minutos de simulación

# Lógica de la Simulación
- JMC (Rionegro): abierto 24/7, acepta vuelos internacionales, capacidad 35 vuelos
- EOH (Medellín): abierto de 6:00 a 18:00, vuelos nacionales o militares, máximo 15 vuelos
- Emergencias y clima afectan la asignación de los vuelos en tiempo real

# Estructura del Código
- CondicionesClimaticas: gestiona el estado del clima por aeropuerto
- Avion (base), AvionComercial, AvionMilitar: definen características y comportamiento de las aeronaves
- Aeropuerto: administra los vuelos asignados y el estado operativo
- DespachadorVuelos: centraliza la simulación, crea aviones, gestiona clima y toma decisiones

# La simulación muestra:
- El clima de cada aeropuerto
- Los vuelos generados y su asignación
- Estado final de los aeropuertos después de cada intervalo

//Proyecto desarrollado como práctica final de Programación Orientada a Objetos
