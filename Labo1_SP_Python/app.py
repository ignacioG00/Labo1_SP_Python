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

from library_utn import UTN_messenger
from clinica import Clinica
from paciente import Paciente
from turno import Turno
from validaciones import Validaciones


def main_app():
    """
    Aplicacion principal del Segundo Parcial de Laboratorio 1
    """
    clinica = Clinica("Clínica Ejemplo")
    clinica.cargar_configuracion("configs.json")
    
    while True:
        print("╔════════════════════════════════╗")
        print("║         Menú de opciones:      ║")
        print("╠════════════════════════════════╣")
        print("║ 1. Alta paciente               ║")
        print("║ 2. Alta turno                  ║")
        print("║ 3. Ordenar turnos              ║")
        print("║ 4. Mostrar pacientes en espera ║")
        print("║ 5. Atender pacientes           ║")
        print("║ 6. Cobrar atenciones           ║")
        print("║ 7. Cerrar caja                 ║")
        print("║ 8. Mostrar informe             ║")
        print("║ 9. Salir                       ║")
        print("╚════════════════════════════════╝")
        
        selected_option = Validaciones.ingresar_numero()
            
        match selected_option:
            case 1: # Alta paciente
                clinica.agregar_paciente()
                pass
            case 2: # Alta turno
                id_paciente = int(input("ID del paciente : "))
                especialidad = input("Especialidad(medico clinico, odontologia, psicologia, traumatologia): ")

                if Validaciones.validar_especialidad(especialidad, clinica.especialidades):
                    paciente = next((p for p in clinica.lista_pacientes if p.id == id_paciente), None)
                    if paciente:
                        monto_a_pagar = Validaciones.calcular_monto_a_pagar(paciente.edad, paciente.obra_social)
                        turno = Turno(id_paciente, especialidad, monto_a_pagar, "Activo")
                        clinica.agregar_turno(turno)
                    else:
                        print("Paciente no encontrado.")
                else:
                    print("Especialidad no válida.")
                pass
            case 3: # Ordenar turnos
                print("Ordenar por ( 1.Obra Social ASC / 2.Monto DESC): ")
                criterio = Validaciones.ingresar_numero()
                while criterio!= 1 and criterio != 2 :
                    print("Numero invalido, ingrese una opcion valida.")
                    criterio = Validaciones.ingresar_numero()
                clinica.ordenar_turnos(criterio)
                pass
            case 4: # Mostrar pacientes en espera
                clinica.mostrar_pacientes_en_espera()
                pass
            case 5: # Atender pacientes
                clinica.atender_pacientes()
                pass
            case 6: # Cobrar atenciones
                clinica.cobrar_atenciones()
                pass
            case 7: # Cerrar caja
                clinica.cerrar_caja("configs.json")
                pass
            case 8: # Mostrar informe
                clinica.mostrar_informe()
                pass
            case 9: # Salir
                print("Saliendo del programa.")
                break
            case _:
                print('Opción inválida. Por favor, seleccione una opción válida.', 'Error')
                pass
            