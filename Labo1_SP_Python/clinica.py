# MIT License
#
# Copyright (c) 2024 [UTN FRA](https://fra.utn.edu.ar/) All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import datetime
import paciente
import turno

class Clinica:
    def __init__(self, razon_social):
        self.razon_social = razon_social
        self.lista_pacientes = []
        self.lista_turnos = []
        self.especialidades = {}
        self.obras_sociales_validas = {}
        self.recaudacion = 0.0
        self.hay_pacientes_sin_atencion = False
    
    def cargar_configuracion(self, archivo_config):
        with open(archivo_config, 'r') as file:
            config = json.load(file)
            self.especialidades = config.get('especialidades', {})
            self.obras_sociales_validas = config.get('obras_sociales', {})
    
    def registrar_paciente(self, nombre, apellido, dni, edad, obra_social):
        for paciente in self.lista_pacientes:
            if paciente.dni == dni:
                raise ValueError("Ya existe un paciente con el mismo DNI.")
        
        nuevo_paciente = paciente(nombre, apellido, dni, edad, obra_social)
        self.lista_pacientes.append(nuevo_paciente)
        self.hay_pacientes_sin_atencion = True
    
    def asignar_turno(self, id_paciente, especialidad):
        paciente_encontrado = None
        for paciente in self.lista_pacientes:
            if paciente.id == id_paciente:
                paciente_encontrado = paciente
                break
        
        if not paciente_encontrado:
            raise ValueError("El paciente no existe en el sistema.")
        
        if especialidad not in self.especialidades:
            raise ValueError("Especialidad no válida.")
        
        nuevo_turno = turno(id_paciente, especialidad, paciente_encontrado.obra_social, paciente_encontrado.edad)
        self.lista_turnos.append(nuevo_turno)
        return nuevo_turno

    def atender_pacientes(self):
        turnos_activos = [turno for turno in self.lista_turnos if turno.estado == "Activo"]
        turnos_a_atender = turnos_activos[:2]  # Selecciona los primeros 2 turnos activos
        
        for turno in turnos_a_atender:
            turno.estado = "Finalizado"
        
        if not turnos_a_atender:
            print("No hay pacientes en espera.")
    
    def cobrar_atenciones(self):
        turnos_finalizados = [turno for turno in self.lista_turnos if turno.estado == "Finalizado"]
        
        for turno in turnos_finalizados:
            turno.estado = "Pagado"
            self.recaudacion += turno.monto_a_pagar
        
        if not turnos_finalizados:
            print("No hay pacientes finalizados para cobrar.")
    
    def cerrar_caja(self):
        turnos_activos_o_finalizados = [turno for turno in self.lista_turnos if turno.estado in ["Activo", "Finalizado"]]
        
        if not turnos_activos_o_finalizados:
            print(f"Total recaudado: ${self.recaudacion:.2f}")
            self.guardar_datos()
        else:
            print("Aún hay pacientes por atender.")
    
    def guardar_datos(self):
        pacientes_data = [paciente.__dict__ for paciente in self.lista_pacientes]
        turnos_data = [turno.__dict__ for turno in self.lista_turnos]
        
        with open('pacientes.json', 'w') as file:
            json.dump(pacientes_data, file, indent=4)
        
        with open('turnos.json', 'w') as file:
            json.dump(turnos_data, file, indent=4)
    
    def mostrar_pacientes_en_espera(self):
        pacientes_espera = [turno for turno in self.lista_turnos if turno.estado == "Activo"]
        for turno in pacientes_espera:
            print(turno)