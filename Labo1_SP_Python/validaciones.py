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

class Validaciones:
    @staticmethod
    def validar_nombre_apellido(nombre, apellido):
        if not nombre.isalpha() or not apellido.isalpha():
            return False
        if len(nombre) > 30 or len(apellido) > 30:
            return False
        return True

    @staticmethod
    def validar_edad(edad):
        try:
            edad = int(edad)
            if isinstance(edad, int) and 18 <= edad <= 90:
                return True
            else:
                print("La edad debe estar entre 18 y 90.")
                return False
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
            return False

    @staticmethod
    def validar_obra_social(obra_social, edad):
        obras_sociales_validas = ["swiss medical", "apres", "pami", "particular"]
        if obra_social.lower() not in obras_sociales_validas:
            return False
        if int(edad) >= 60 and obra_social != "pami":
            return False
        if int(edad) < 60 and obra_social == "pami":
            return False
        return True

    @staticmethod
    def validar_especialidad(especialidad):
        especialidades_validas = ["medico clinico", "odontologia", "psicologia", "traumatologia"]
        return especialidad in especialidades_validas

    @staticmethod
    def calcular_monto_a_pagar(edad, obra_social):
        precio_base = 4000
        
        descuentos = {
            "swiss medical": 0.40,
            "apres": 0.25,
            "pami": 0.60,
            "particular": -0.05
        }
        adicionales = {
            "swiss medical": (-0.10 if 18 <= int(edad) <= 60 else 0),
            "apres": (-0.03 if 26 <= int(edad) <= 59 else 0),
            "pami": (-0.03 if int(edad) >= 80 else 0),
            "particular": (+0.15 if 40 <= int(edad) <= 60 else 0)
        }
        obra_social = obra_social.lower()
        descuento_base = descuentos.get(obra_social, 0)
        adicional = adicionales.get(obra_social, 0)
        
        print(f"Edad: {edad}, Obra Social: {obra_social}")
        print(f"Descuento Base: {descuento_base}, Adicional: {adicional}")
        
        monto = int(precio_base) * (1 - descuento_base) * (1 + adicional)
        print(f"Monto Calculado: {monto}")
        return round(monto, 2)
    
    @staticmethod
    def ingresar_numero():
        while True:
            try:
                numero = int(input("Ingrese la opcion: "))
                return numero  # Retorna la edad si se ingresó correctamente como un entero
            except ValueError:
                print('Opción inválida. Por favor, seleccione una opción válida.', 'Error')