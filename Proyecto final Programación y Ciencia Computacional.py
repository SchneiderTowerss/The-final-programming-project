#Proyecto de Santiago FLórez Roldán y Schneider Alejandro Torres Ortega
#Simulación para dirigir vuelos hacia el EOH/JMC
import random
from datetime import datetime, timedelta
import time


AEROLINEAS = {
    'Sarpa': {'prefijo_comercial': 'HK', 'aviones': ['Embraer 145', 'Embraer 120 Brasilia', 'Jetstream 32']},
    'Satena': {'prefijo_comercial': 'HK', 'prefijo_militar': 'FAC', 'aviones': ['Embraer 145', 'ATR-42', 'ATR-72', 'DHC Twin Otter']},
    'Clic': {'prefijo_comercial': 'HK', 'aviones': ['ATR-42']},
    'Avianca': {'prefijo_comercial': 'N', 'sufijo': 'AV', 'aviones': ['Airbus A318', 'Airbus A319', 'Airbus A320', 'Airbus A321', 'Boeing 787', 'Airbus A330']},
    'LATAM': {'prefijo_comercial': 'CC', 'aviones': ['Airbus A320', 'Boeing 767']},
    'JetSmart': {'prefijo_comercial': 'CC', 'aviones': ['Airbus A320']},
    'Wingo': {'prefijo_comercial': 'HP', 'aviones': ['Boeing 737']}
}

RAMAS_MILITARES = {
    'Fuerza Aérea Colombiana': {'prefijo': 'FAC'},
    'Ejército Colombiano': {'prefijo': 'EJC'},
    'Policía Nacional': {'prefijo': 'PNC'}
}

AEROPUERTOS = {
    'JMC': {
        'nombre': 'Aeropuerto José María Córdova',
        'ubicación': 'Rionegro',
        'horario_apertura': (0, 24),  
        'internacional': True,
        'max_pasajeros': None,  
        'prob_mal_tiempo': 0.07 
    },
    'EOH': {
        'nombre': 'Aeropuerto Olaya Herrera',
        'ubicación': 'Medellín',
        'horario_apertura': (6, 18),  
        'internacional': False,
        'max_pasajeros': 50,
        'prob_mal_tiempo': 0.15  
    }
}

class CondicionesClimaticas:
    def __init__(self):
        self.condiciones = {
            'JMC': 'Despejado',
            'EOH': 'Despejado'
        }
    
    def actualizar_clima(self):
        for codigo_aeropuerto in self.condiciones:
            if random.random() < AEROPUERTOS[codigo_aeropuerto]['prob_mal_tiempo']:
                mal_tiempo = ['Niebla', 'Lluvia', 'Tormenta', 'Baja Visibilidad']
                self.condiciones[codigo_aeropuerto] = random.choice(mal_tiempo)
            else:
                self.condiciones[codigo_aeropuerto] = 'Despejado'
    
    def obtener_clima(self, codigo_aeropuerto):
        return self.condiciones.get(codigo_aeropuerto, 'Desconocido')
    
    def es_mal_tiempo(self, codigo_aeropuerto):
        return self.condiciones.get(codigo_aeropuerto, 'Despejado') != 'Despejado'

class Avion:
    def __init__(self, matricula_comercial, matricula_militar, aerolinea, tipo_avion, cantidad_pasajeros, nivel_emergencia=0):
        self._matricula_comercial = matricula_comercial
        self._matricula_militar = matricula_militar
        self._aerolinea = aerolinea
        self._tipo_avion = tipo_avion
        self._cantidad_pasajeros = cantidad_pasajeros
        self._nivel_emergencia = nivel_emergencia
        self._aeropuerto_asignado = None
    
    # Getters
    @property
    def matricula_comercial(self):
        return self._matricula_comercial
    
    @property
    def matricula_militar(self):
        return self._matricula_militar
    
    @property
    def aerolinea(self):
        return self._aerolinea
    
    @property
    def tipo_avion(self):
        return self._tipo_avion
    
    @property
    def cantidad_pasajeros(self):
        return self._cantidad_pasajeros
    
    @property
    def nivel_emergencia(self):
        return self._nivel_emergencia
    
    @property
    def aeropuerto_asignado(self):
        return self._aeropuerto_asignado
    
    # Setters
    @nivel_emergencia.setter
    def nivel_emergencia(self, valor):
        if 0 <= valor <= 3:
            self._nivel_emergencia = valor
        else:
            raise ValueError("El nivel de emergencia debe estar entre 0 y 3")
    
    @aeropuerto_asignado.setter
    def aeropuerto_asignado(self, valor):
        self._aeropuerto_asignado = valor
    
    def es_militar(self):
        return self._matricula_militar is not None and self._matricula_comercial is None
    
    def es_comercial(self):
        return self._matricula_comercial is not None and self._matricula_militar is None
    
    def es_satena(self):
        return self._aerolinea == 'Satena' and self._matricula_comercial is not None and self._matricula_militar is not None
    
    def matricula_mostrar(self):
        if self.es_militar():
            return self._matricula_militar
        elif self.es_comercial() or self._aerolinea == 'Sarpa':
            return self._matricula_comercial
        elif self.es_satena():
            return f"{self._matricula_comercial} / {self._matricula_militar}"
        return "Desconocida"
    
    def __str__(self):
        matricula = self.matricula_mostrar()
        return f"{matricula} - {self._aerolinea} ({self._tipo_avion}) - Pasajeros: {self._cantidad_pasajeros} - Emergencia: {self._nivel_emergencia}"

class AvionComercial(Avion):
    def __init__(self, matricula_comercial, aerolinea, tipo_avion, cantidad_pasajeros, nivel_emergencia=0):
        super().__init__(matricula_comercial, None, aerolinea, tipo_avion, cantidad_pasajeros, nivel_emergencia)
    
    def puede_aterrizar_eoh(self, hora_actual):
        hora_apertura, hora_cierre = AEROPUERTOS['EOH']['horario_apertura']
        hora_actual = hora_actual.hour
        
       
        if not (hora_apertura <= hora_actual < hora_cierre):
            return False
        
      
        if self.cantidad_pasajeros > AEROPUERTOS['EOH']['max_pasajeros'] and self.aerolinea not in ['Satena', 'Sarpa']:
            return False
        
       
        if self.aerolinea in ['Avianca', 'LATAM', 'JetSmart', 'Wingo', 'Clic']:
            return True
        
        return True

class AvionMilitar(Avion):
    def __init__(self, matricula_militar, rama, tipo_avion, nivel_emergencia=0):
        super().__init__(None, matricula_militar, rama, tipo_avion, 0, nivel_emergencia)
        self._rama = rama
    
    @property
    def rama(self):
        return self._rama
    
    def puede_aterrizar_eoh(self, hora_actual):
        return True

class Aeropuerto:
    def __init__(self, codigo):
        self._codigo = codigo
        self._aviones_asignados = []
        self._clima = 'Despejado'
        self._capacidad = 35 if codigo == 'JMC' else 30  
    
    # Getters
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def aviones_asignados(self):
        return self._aviones_asignados
    
    @property
    def clima(self):
        return self._clima
    
    @property
    def capacidad(self):
        return self._capacidad
    
    # Setters
    @clima.setter
    def clima(self, valor):
        self._clima = valor
    
    def asignar_avion(self, avion):
        self._aviones_asignados.append(avion)
        avion.aeropuerto_asignado = self._codigo
    
    def esta_abierto(self, hora_actual):
        hora_apertura, hora_cierre = AEROPUERTOS[self._codigo]['horario_apertura']
        hora_actual = hora_actual.hour
        return hora_apertura <= hora_actual < hora_cierre
    
    def acepta_internacionales(self):
        return AEROPUERTOS[self._codigo]['internacional']
    
    def obtener_limite_pasajeros(self):
        return AEROPUERTOS[self._codigo]['max_pasajeros']
    
    def __str__(self):
        return f"{AEROPUERTOS[self._codigo]['nombre']} ({self._codigo}) - Clima: {self._clima} - Vuelos asignados: {len(self._aviones_asignados)}"

class DespachadorVuelos:
    def __init__(self):
        self._jmc = Aeropuerto('JMC')
        self._eoh = Aeropuerto('EOH')
        self._clima = CondicionesClimaticas()
        self._hora_simulacion = datetime(2025, 7, 21, 0, 0)  
    
    def generar_avion_aleatorio(self):
      
        if random.random() < 0.04:
            return self._generar_avion_militar()
        else:
            return self._generar_avion_comercial()
    
    def _generar_avion_militar(self):
        rama = random.choice(list(RAMAS_MILITARES.keys()))
        prefijo = RAMAS_MILITARES[rama]['prefijo']
        matricula = f"{prefijo}-{random.randint(1000, 9999)}"
        tipos_avion = ['C-130 Hercules', 'KC-767 Tanquero', 'CASA CN-235', 'Black Hawk', 'Super Tucano']
        tipo_avion = random.choice(tipos_avion)
        
       
        nivel_emergencia = 1 if random.random() < 0.005 else 0
        
        return AvionMilitar(matricula, rama, tipo_avion, nivel_emergencia)
    
    def _generar_avion_comercial(self):
        aerolinea = random.choice(list(AEROLINEAS.keys()))
        datos_aerolinea = AEROLINEAS[aerolinea]
        
      
        if aerolinea == 'Avianca':
            matricula_comercial = f"{datos_aerolinea['prefijo_comercial']}-{random.randint(1000, 9999)}{datos_aerolinea['sufijo']}"
        elif aerolinea in ['LATAM', 'JetSmart']:
            letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            matricula_comercial = f"{datos_aerolinea['prefijo_comercial']}-{''.join(random.choices(letras, k=3))}"
        elif aerolinea == 'Wingo':
            matricula_comercial = f"{datos_aerolinea['prefijo_comercial']}-{random.randint(1000, 9999)}"
        else:  
            matricula_comercial = f"{datos_aerolinea['prefijo_comercial']}-{random.randint(1000, 9999)}"
        
       
        matricula_militar = None
        if aerolinea == 'Satena' and 'prefijo_militar' in datos_aerolinea:
            matricula_militar = f"{datos_aerolinea['prefijo_militar']}-{random.randint(1000, 9999)}"
        
        tipo_avion = random.choice(datos_aerolinea['aviones'])
        
        
        if 'Embraer 120' in tipo_avion:
            pasajeros = random.randint(15, 30)
        elif 'DHC Twin Otter' in tipo_avion:
            pasajeros= random.randint(6, 20)
        elif 'Jetstream 32' in tipo_avion:
            pasajeros = random.randint(5, 17)
        elif 'Embraer 145' in tipo_avion:
            pasajeros = random.randint(30, 50)
        elif 'ATR-42' in tipo_avion:
            pasajeros = random.randint(40, 50)
        elif 'ATR-72' in tipo_avion:
            pasajeros = random.randint(50, 70)
        elif 'Airbus A318' in tipo_avion:
            pasajeros = random.randint(100, 120)
        elif 'Airbus A319' in tipo_avion:
            pasajeros = random.randint(120, 140)
        elif 'Airbus A320' in tipo_avion or 'Boeing 737' in tipo_avion:
            pasajeros = random.randint(140, 180)
        elif 'Airbus A321' in tipo_avion:
            pasajeros = random.randint(180, 220)
        elif 'Boeing 787' in tipo_avion:
            pasajeros = random.randint(240, 300)
        elif 'Airbus A330' in tipo_avion or 'Boeing 767' in tipo_avion:
         
            pasajeros = 0 if random.random() < 0.7 else random.randint(200, 250)
        else:
            pasajeros = random.randint(50, 100)
        
       
        nivel_emergencia = 1 if random.random() < 0.005 else 0
        
       
        if aerolinea == 'Satena' and matricula_militar is not None:
            return Avion(matricula_comercial, matricula_militar, aerolinea, tipo_avion, pasajeros, nivel_emergencia)
        else:
            return AvionComercial(matricula_comercial, aerolinea, tipo_avion, pasajeros, nivel_emergencia)
    
    def decidir_aeropuerto_aterrizaje(self, avion):
        
        if avion.nivel_emergencia > 0:
           
            if self._eoh.esta_abierto(self._hora_simulacion) and not self._clima.es_mal_tiempo('EOH'):
                return self._eoh
            else:
                return self._jmc
        
       
        if avion.es_militar():
         
            if not self._clima.es_mal_tiempo('EOH'):
                return self._eoh
            else:
                return self._jmc
        
     
        if isinstance(avion, AvionComercial) or (isinstance(avion, Avion) and avion.es_comercial()):
            
            if avion.puede_aterrizar_eoh(self._hora_simulacion) and not self._clima.es_mal_tiempo('EOH'):
                
                if len(self._eoh.aviones_asignados) < self._eoh.capacidad:
                    return self._eoh
        
        
        return self._jmc
    
    def ejecutar_simulacion(self, iteraciones=48):  
        print("Iniciando simulación de despachador de vuelos...\n")
        
        for i in range(iteraciones):
           
            self._clima.actualizar_clima()
            self._jmc.clima = self._clima.obtener_clima('JMC')
            self._eoh.clima = self._clima.obtener_clima('EOH')
            
            print(f"\nIteración {i+1}/{iteraciones}")
            print(f"Hora: {self._hora_simulacion.strftime('%Y-%m-%d %H:%M')}")
            print(f"JMC Clima: {self._jmc.clima}")
            print(f"EOH Clima: {self._eoh.clima}")
            print(f"EOH está {'ABIERTO' if self._eoh.esta_abierto(self._hora_simulacion) else 'CERRADO'}")
            
       
            vuelos_jmc = random.randint(10, 20)  
            vuelos_eoh = random.randint(5, 10)    
            total_vuelos = vuelos_jmc + vuelos_eoh
            
            print(f"\nGenerando {total_vuelos} vuelos para este intervalo...")
            
            for _ in range(total_vuelos):
                avion = self.generar_avion_aleatorio()
                aeropuerto = self.decidir_aeropuerto_aterrizaje(avion)
                aeropuerto.asignar_avion(avion)
                
                print(f"Asignado {avion} a {aeropuerto.codigo}")
            
      
            print(f"\nJMC Estado: {len(self._jmc.aviones_asignados)} vuelos")
            print(f"EOH Estado: {len(self._eoh.aviones_asignados)} vuelos")
            
           
            self._limpiar_vuelos_completados()
            
        
            self._hora_simulacion += timedelta(minutes=30)
            time.sleep(1)  
    
    def _limpiar_vuelos_completados(self):
        if len(self._jmc.aviones_asignados) > 0:
            cantidad_limpiar = random.randint(0, min(5, len(self._jmc.aviones_asignados)))
            for _ in range(cantidad_limpiar):
                self._jmc.aviones_asignados.pop(0)
        
        if len(self._eoh.aviones_asignados) > 0:
            cantidad_limpiar = random.randint(0, min(3, len(self._eoh.aviones_asignados)))
            for _ in range(cantidad_limpiar):
                self._eoh.aviones_asignados.pop(0)


if __name__ == "__main__":
    despachador = DespachadorVuelos()
    
    for num_iteraciones in [45]:  
        print(f"\n=== INICIANDO SIMULACIÓN CON {num_iteraciones} ITERACIONES ({(num_iteraciones/2)} horas) ===")
        despachador.ejecutar_simulacion(num_iteraciones)
        print("\n=== SIMULACIÓN COMPLETADA ===")
        time.sleep(2)  
