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

import itertools
import json
import os
from paciente import Paciente
from turno import Turno
from validaciones import Validaciones

class Clinica:
    def __init__(self, razon_social):
        self.razon_social = razon_social
        self.lista_pacientes = {}
        self.lista_turnos = {}
        self.especialidades = {}
        self.obras_sociales_validas = {}
        self.recaudacion = 0.0
        self.hay_pacientes_sin_atencion = False
    
    def cargar_configuracion(self, archivo_config):
        try:
            with open(archivo_config, 'r') as file:
                config = json.load(file)
                self.especialidades = config.get('especialidades', [])
                self.obras_sociales_validas = config.get('obras_sociales', [])
                # Cargar lista de pacientes
            pacientes_data = config.get('lista_pacientes', [])
            self.lista_pacientes = []
            max_id = 0  # Variable para almacenar el máximo ID encontrado
            
            for paciente_data in pacientes_data:
                paciente = Paciente(paciente_data.get('nombre'),
                                    paciente_data.get('apellido'),
                                    paciente_data.get('dni'),
                                    paciente_data.get('edad'),
                                    paciente_data.get('obra_social'))
                self.lista_pacientes.append(paciente)
                if paciente.id > max_id:
                    max_id = paciente.id  # Actualizar máximo ID encontrado
            
            # Actualizar el contador de ID en la clase Paciente
            Paciente.id_counter = itertools.count(max_id + 1)
            
            # Cargar lista de turnos
            turnos_data = config.get('lista_turnos', [])
            self.lista_turnos = []
            for turno_data in turnos_data:
                turno = Turno(turno_data.get('id_paciente'),
                              turno_data.get('especialidad'),
                              turno_data.get('monto_a_pagar'),
                              turno_data.get('estado'))
                self.lista_turnos.append(turno)
                
        except FileNotFoundError:
            print(f"El archivo {archivo_config} no se encontró.")
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo {archivo_config}.")

    def guardar_datos(self, archivo_config):
        datos = {
            "lista_pacientes": [p.__dict__ for p in self.lista_pacientes],
            "lista_turnos": [t.__dict__ for t in self.lista_turnos],
            "especialidades": self.especialidades,
            "obras_sociales": self.obras_sociales_validas
        }
        with open(archivo_config, 'w') as file:
            json.dump(datos, file, indent=4)

    def agregar_paciente(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        while not Validaciones.validar_nombre_apellido(nombre, apellido):
            nombre = input("Error: Nombre o apellido no válidos. Deben contener solo caracteres alfabéticos y no exceder los 30 caracteres.")
            apellido = input("Error: Nombre o apellido no válidos. Deben contener solo caracteres alfabéticos y no exceder los 30 caracteres.")
            pass
        dni = input("DNI: ")
        edad = input("Edad: ")
        while not Validaciones.validar_edad(edad):
            edad = input("Edad: ")
            pass
        obra_social = input("Obra social:(Swiss Medical, Apres, PAMI, Particular)")
            
        while not Validaciones.validar_obra_social(obra_social, edad):
            obra_social = input("Error: Obra social no válida.")
            pass
        paciente = Paciente(nombre.strip(), apellido.strip(), dni.strip(), edad, obra_social.strip())    
        for p in self.lista_pacientes:
            if p.dni == paciente.dni:
                print("Error: Ya existe un paciente con ese DNI.")
                return
        self.lista_pacientes.append(paciente)
        print(f"Paciente {paciente.nombre} {paciente.apellido} agregado con éxito.")

    def agregar_turno(self, turno):
        if any(p.id == turno.id_paciente for p in self.lista_pacientes):
            self.lista_turnos.append(turno)
            print(f"Turno para paciente con ID {turno.id_paciente} agregado con éxito.")
        else:
            print("Error: No existe un paciente con ese ID.")

    def obtener_obra_social_paciente(self, id_paciente):
        paciente = next((p for p in self.lista_pacientes if p.id == id_paciente), None)
        return paciente.obra_social.lower() if paciente else ""

    def ordenar_turnos(self, criterio):
        if criterio == "Obra Social ASC":
            self.lista_turnos.sort(key=lambda t: self.obtener_obra_social_paciente(t.id_paciente))
        elif criterio == "Monto DESC":
            self.lista_turnos.sort(key=lambda x: x.monto_a_pagar, reverse=True)
    
    def obtener_paciente_por_id(self, id_paciente):
        return next((p for p in self.lista_pacientes if p.id == id_paciente), None)

    def mostrar_pacientes_en_espera(self):
        pacientes_en_espera = [t for t in self.lista_turnos if t.estado == "Activo"]
        if pacientes_en_espera:
            print("\n=== Pacientes en Espera ===\n")
            print("\n╔══════╦══════════════════════╦══════════════════════╦══════════════════════╦═══════════════════════╦══════════════════════╗")
            print("║ ID   ║ Paciente             ║ Obra Social          ║ Especialidad         ║ Monto a Pagar         ║ Estado               ║")
            print("╠══════╬══════════════════════╬══════════════════════╬══════════════════════╬═══════════════════════╬══════════════════════╣")
            for turno in pacientes_en_espera:
                paciente = self.obtener_paciente_por_id(turno.id_paciente)
                print(f"║ {turno.id:<4} ║ {paciente.nombre:<20} ║ {paciente.obra_social:<20} ║ {turno.especialidad:<20} ║ ${turno.monto_a_pagar:<20.2f} ║ {turno.estado:<20} ║")
            print("╚══════╩══════════════════════╩══════════════════════╩══════════════════════╩═══════════════════════╩══════════════════════╝")

        else:
            print("No hay pacientes en espera.")

    def atender_pacientes(self):
        pacientes_en_espera = [t for t in self.lista_turnos if t.estado == "Activo"]
        if len(pacientes_en_espera) == 0:
            print("No hay pacientes en espera.")
        else:
            to_atender = pacientes_en_espera[:2]
            for t in to_atender:
                t.estado = "Finalizado"
                print(f"Paciente con turno ID: {t.id} ha sido atendido.")

    def cobrar_atenciones(self):
        turnos_finalizados = [t for t in self.lista_turnos if t.estado == "Finalizado"]
        if len(turnos_finalizados) == 0:
            print("No hay turnos para cobrar.")
        else:
            for t in turnos_finalizados:
                t.estado = "Pagado"
                self.recaudacion += t.monto_a_pagar
                print(f"Se ha cobrado el turno ID: {t.id} por un monto de {t.monto_a_pagar}")

    def cerrar_caja(self, archivo_config):
        turnos_pendientes = [t for t in self.lista_turnos if t.estado in ["Activo", "Finalizado"]]
        if len(turnos_pendientes) > 0:
            print("Aún hay pacientes por atender o turnos por cobrar.")
        else:
            print(f"Total recaudado: {self.recaudacion}")
            self.guardar_datos(archivo_config)
            print("Datos guardados y caja cerrada.")

    def mostrar_informe(self):
    # Filtramos los turnos pagados
        turnos_pagados = filter(lambda t: t.estado == "Pagado", self.lista_turnos)

    # Extraemos el monto a pagar y la obra social de cada turno pagado
        ingresos_por_obra_social = {}
        for turno in turnos_pagados:
            paciente = self.obtener_paciente_por_id(turno.id_paciente)
            obra_social = paciente.obra_social.lower()
            monto_a_pagar = turno.monto_a_pagar
            if obra_social in ingresos_por_obra_social:
                ingresos_por_obra_social[obra_social] += monto_a_pagar
            else:
                ingresos_por_obra_social[obra_social] = monto_a_pagar
    
    # Imprimimos el monto de cada ingreso por obra social
        if ingresos_por_obra_social:
            print("\n=== Informe de Ingresos por Obra Social ===\n")
        for obra_social, monto in ingresos_por_obra_social.items():
            print(f"Obra Social: {obra_social.capitalize()}")
            print(f"Monto Total: ${monto:.2f}\n")
    
    # Encontramos la obra social con menos ingresos
        if ingresos_por_obra_social:
            obra_social_menos_ingresos = min(ingresos_por_obra_social, key=ingresos_por_obra_social.get)
            print(f"La obra social con menos ingresos es: {obra_social_menos_ingresos.capitalize()} con un total de ${ingresos_por_obra_social[obra_social_menos_ingresos]:.2f}")
        else:
            print("No hay ingresos registrados.")