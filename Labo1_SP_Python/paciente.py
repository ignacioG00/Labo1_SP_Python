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

from datetime import datetime

class Paciente:
    _id_counter = 1
    
    def __init__(self, nombre, apellido, dni, edad, obra_social):
        self.id = Paciente._id_counter
        Paciente._id_counter += 1
        
        self.nombre = self.validar_nombre_apellido(nombre)
        self.apellido = self.validar_nombre_apellido(apellido)
        self.dni = dni
        self.edad = self.validar_edad(edad)
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.obra_social = self.validar_obra_social(obra_social, edad)

    def validar_nombre_apellido(self, valor):
        if not valor.isalpha() or len(valor) > 30:
            raise ValueError("El nombre y apellido deben contener solo caracteres alfabéticos y no exceder los 30 caracteres.")
        return valor
    
    def validar_edad(self, edad):
        if not isinstance(edad, int) or not (18 <= edad <= 90):
            raise ValueError("La edad debe ser un valor numérico entero entre 18 y 90.")
        return edad

    def validar_obra_social(self, obra_social, edad):
        obras_sociales_validas = ['Swiss Medical', 'Apres', 'PAMI', 'Particular']
        if edad >= 60:
            if obra_social != 'PAMI':
                raise ValueError("Si el paciente tiene 60 años o más, la única opción disponible es PAMI.")
        else:
            if obra_social == 'PAMI':
                raise ValueError("Si el paciente tiene menos de 60 años, no puede seleccionar PAMI.")
            if obra_social not in obras_sociales_validas:
                raise ValueError(f"Obra social no válida. Debe ser una de las siguientes: {', '.join(obras_sociales_validas)}.")
        return obra_social

    def __repr__(self):
        return (f"Paciente(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', "
                f"dni='{self.dni}', edad={self.edad}, fecha_registro='{self.fecha_registro}', "
                f"obra_social='{self.obra_social}')")