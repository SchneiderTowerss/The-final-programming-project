La idea es que use la librería random para generar las aeronaves y los eventos meteorológicos y hacer una simulación.
Las aeronaves deben ser de tipo:
1. comercial (matricula HK-XXXX, N-XXXXAV para avianca, CC-XXXX, HP-XXXX, se pueden usar números random o CC-XXX para aeronaves LATAM, con XXX random usando letras como caractéres en mayúsculas, sin la ñ)
2. Militar (Matrícula FAC-XXXX, EJC-XXXX, o PNC-XXXX, con cuatro dígitos aleatorios)

El aeropuerto Jose María Córdova, de Rionegro, está abierto 24/7, recibe vuelos internacionales.
El aeropuerto Enrique Olaya Herrera, de Medellín, está abierto de 6:00 am a 6:00 pm, no recibe vuelos internacionales ni vuelos de aviones de más de 50 pasajeros (excepto vuelos militares, incluyendo la aerolínea Satena)

Las aerolíneas a utilizar son.

Sarpa (operado por satena, puede usar embraer 145, usa embraer 120 brasilia y jetstream 32 para entrar a Medellín sin problema, matrícula HK)
Satena (Matrícula HK y FAC, operan como aeronaves comerciales, pero si se pasa el horario del olaya, pueden utilizar su matrícula FAC para entrar, usan embraer 145, atr-42, atr 72, DHC twin otter, todos pueden entrar al olaya herrera a pesar de sus capacidades.)
Clic (matrícula HK, comercial, opera con atr 42 en el olaya herrera)
Avianca (Opera en rionegro, matrícula N-XXXXAV, usa airbus a318, a319. a320. a321, b787 y para carga utiliza a330)
LATAM (Opera en rionegro, matrícula CC-XXX con letras, usa airbus a320 y 767 de carga)
JetSmart (opera en rionegro, matrícula CC-XXX con letras, usa airbus a320)
Wingo (Opera en rionegro, matrícula HP-XXXX con números aleatorios, usa B737)

Mediante código para ver los aeropuertos e iteraciones por cada media hora durante un día, necesito que simules aeronaves que entran en emergencia (con 0.5% de probabilidad por día) mal clima meteorológico (15% de probabilidad en Medellín, 7% de probabilidad en Rionegro) 

Y que el código redirija las aeronaves al aeropuerto más oportuno.
Al aeropuerto de rionegro tiene aproximadamente 35 vuelos por hora al día (aterrizaje y despegue) y el olaya herrera aproximadamente 15 vuelos por hora.
la proporción de aeronaves entre militares y comerciales es de 4% militares y 96% comerciales. (sin contar a satena)

El código está hecho teniendo en cuenta la programación orientada a objetos, utilizando herencia para la clase Avion, y generar aeronaves comerciales y militares.

Para el número de iteraciones, también se utilizó un ciclo for al final, donde cada iteración cuenta media hora.
