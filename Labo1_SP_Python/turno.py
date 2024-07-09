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

class Turno:
    _id_counter = 1
    _especialidades_validas = ['Odontología', 'Médico Clínico', 'Psicología', 'Traumatología']
    _precio_base = 4000

    def __init__(self, id_paciente, especialidad, obra_social_paciente, edad_paciente):
        self.id = Turno._id_counter
        Turno._id_counter += 1
        
        self.id_paciente = id_paciente
        self.especialidad = self.validar_especialidad(especialidad)
        self.monto_a_pagar = self.calcular_monto(obra_social_paciente, edad_paciente)
        self.estado = "Activo"

    def validar_especialidad(self, especialidad):
        if especialidad not in Turno._especialidades_validas:
            raise ValueError(f"Especialidad no válida. Debe ser una de las siguientes: {', '.join(Turno._especialidades_validas)}.")
        return especialidad

    def calcular_monto(self, obra_social, edad):
        monto = Turno._precio_base
        if obra_social == "Swiss Medical":
            monto *= 0.60
            if 18 <= edad < 60:
                monto *= 0.90
        elif obra_social == "Apres":
            monto *= 0.75
            if 26 <= edad < 59:
                monto *= 0.97
        elif obra_social == "PAMI":
            monto *= 0.40
            if edad >= 80:
                monto *= 0.97
        elif obra_social == "Particular":
            monto *= 1.05
            if 40 <= edad < 60:
                monto *= 1.15
        return round(monto, 2)

    def __repr__(self):
        return (f"Turno(id={self.id}, id_paciente={self.id_paciente}, especialidad='{self.especialidad}', "
                f"monto_a_pagar={self.monto_a_pagar}, estado='{self.estado}')")