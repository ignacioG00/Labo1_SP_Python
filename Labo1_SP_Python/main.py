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

from clinica import Clinica

def alta_paciente(clinica):
    nombre = input("Ingrese el nombre del paciente: ")
    apellido = input("Ingrese el apellido del paciente: ")
    dni = input("Ingrese el DNI del paciente: ")
    edad = int(input("Ingrese la edad del paciente: "))
    obra_social = input("Ingrese la obra social del paciente: ")
    
    try:
        clinica.registrar_paciente(nombre, apellido, dni, edad, obra_social)
        print("Paciente registrado exitosamente.")
    except ValueError as e:
        print(e)

def alta_turno(clinica):
    id_paciente = int(input("Ingrese el ID del paciente: "))
    especialidad = input("Ingrese la especialidad para el turno: ")
    
    try:
        turno = clinica.asignar_turno(id_paciente, especialidad)
        print(f"Turno asignado exitosamente: {turno}")
    except ValueError as e:
        print(e)

def ordenar_turnos(clinica):
    print("Opciones de ordenamiento: ")
    print("a. Obra Social ASC")
    print("b. Monto DESC")
    opcion = input("Seleccione una opción de ordenamiento: ")
    
    if opcion == 'a':
        clinica.lista_turnos.sort(key=lambda t: t.obra_social)
    elif opcion == 'b':
        clinica.lista_turnos.sort(key=lambda t: t.monto_a_pagar, reverse=True)
    else:
        print("Opción no válida.")
        return
    
    print("Turnos ordenados exitosamente.")
    for turno in clinica.lista_turnos:
        print(turno)

def mostrar_pacientes_en_espera(clinica):
    clinica.mostrar_pacientes_en_espera()

def atender_pacientes(clinica):
    clinica.atender_pacientes()

def cobrar_atenciones(clinica):
    clinica.cobrar_atenciones()

def cerrar_caja(clinica):
    clinica.cerrar_caja()

def mostrar_informe(clinica):
    ingresos_por_obra_social = {}
    
    for turno in clinica.lista_turnos:
        if turno.estado == "Pagado":
            ingresos_por_obra_social[turno.obra_social] = ingresos_por_obra_social.get(turno.obra_social, 0) + turno.monto_a_pagar
    
    obra_social_menor_ingreso = min(ingresos_por_obra_social, key=ingresos_por_obra_social.get)
    print(f"Obra social con menos ingresos: {obra_social_menor_ingreso}, Monto: {ingresos_por_obra_social[obra_social_menor_ingreso]:.2f}")

def main():
    clinica = Clinica("UTN-Medical Center")
    clinica.cargar_configuracion('configs.json')
    
    while True:
        print("\nMenú de opciones:")
        print("1. Alta paciente")
        print("2. Alta turno")
        print("3. Ordenar turnos")
        print("4. Mostrar pacientes en espera")
        print("5. Atender pacientes")
        print("6. Cobrar atenciones")
        print("7. Cerrar caja")
        print("8. Mostrar informe")
        print("9. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            alta_paciente(clinica)
        elif opcion == '2':
            alta_turno(clinica)
        elif opcion == '3':
            ordenar_turnos(clinica)
        elif opcion == '4':
            mostrar_pacientes_en_espera(clinica)
        elif opcion == '5':
            atender_pacientes(clinica)
        elif opcion == '6':
            cobrar_atenciones(clinica)
        elif opcion == '7':
            cerrar_caja(clinica)
        elif opcion == '8':
            mostrar_informe(clinica)
        elif opcion == '9':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main()