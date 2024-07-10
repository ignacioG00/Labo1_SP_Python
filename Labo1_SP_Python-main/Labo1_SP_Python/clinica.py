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
import os
from paciente import Paciente
from turno import Turno
from validaciones import Validaciones

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
        try:
            with open(archivo_config, 'r') as file:
                config = json.load(file)
                self.especialidades = config.get('especialidades', {})
                self.obras_sociales_validas = config.get('obras_sociales', {})
        except FileNotFoundError:
            print(f"El archivo {archivo_config} no se encontró.")
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo {archivo_config}.")

    def guardar_datos(self, archivo_pacientes, archivo_turnos):
        with open(archivo_pacientes, 'w') as file:
            json.dump([p.__dict__ for p in self.lista_pacientes], file, indent=4)
        with open(archivo_turnos, 'w') as file:
            json.dump([t.__dict__ for t in self.lista_turnos], file, indent=4)

    def agregar_paciente(self, paciente):
        if not Validaciones.validar_nombre_apellido(paciente.nombre, paciente.apellido):
            print("Error: Nombre o apellido no válidos. Deben contener solo caracteres alfabéticos y no exceder los 30 caracteres.")
            return
        
        if not Validaciones.validar_edad(paciente.edad):
            print("Error: Edad no válida. Debe ser un valor numérico entero entre 18 y 90.")
            return
        
        if not Validaciones.validar_obra_social(paciente.obra_social, paciente.edad):
            print("Error: Obra social no válida.")
            return
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
        return paciente.obra_social if paciente else ""

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
            for turno in pacientes_en_espera:
                paciente = self.obtener_paciente_por_id(turno.id_paciente)
                print(f"Turno ID: {turno.id}, Paciente: {paciente.nombre} {paciente.apellido}, Obra Social: {paciente.obra_social}, Especialidad: {turno.especialidad}, Monto a Pagar: {turno.monto_a_pagar}, Estado: {turno.estado}")
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

    def cerrar_caja(self, archivo_pacientes, archivo_turnos):
        turnos_pendientes = [t for t in self.lista_turnos if t.estado in ["Activo", "Finalizado"]]
        if len(turnos_pendientes) > 0:
            print("Aún hay pacientes por atender o turnos por cobrar.")
        else:
            print(f"Total recaudado: {self.recaudacion}")
            self.guardar_datos(archivo_pacientes, archivo_turnos)
            print("Datos guardados y caja cerrada.")

    def mostrar_informe(self):
        ingresos_por_obra_social = {obra: 0 for obra in self.obras_sociales_validas.keys()}
        for t in self.lista_turnos:
            if t.estado == "Pagado":
                paciente = next(p for p in self.lista_pacientes if p.id == t.id_paciente)
                ingresos_por_obra_social[paciente.obra_social] += t.monto_a_pagar
        
        menos_ingresos = min(ingresos_por_obra_social, key=ingresos_por_obra_social.get)
        print(f"La obra social con menos ingresos es: {menos_ingresos} con un total de {ingresos_por_obra_social[menos_ingresos]}")