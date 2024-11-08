import requests

def obtener_variables_desde_servidor():
    """Función para obtener las variables procesadas desde el servidor Flask."""
    try:
        # Hacer una solicitud GET al servidor para obtener las variables
        respuesta = requests.get('http://127.0.0.1:5000/variables')
        if respuesta.status_code == 200:
            # Convertir la respuesta JSON en un diccionario
            variables = respuesta.json()
            imprimir_variables(variables)
        else:
            print(f"Error al obtener las variables. Código de estado: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")

def imprimir_variables(variables):
    """Función para imprimir las variables obtenidas."""
    print(f"VariableTema: {variables['VariableTema']}")
    print(f"VariableAnimal: {variables['VariableAnimal']}")
    print(f"VariableFondo: {variables['VariableFondo']}")
    print(f"VariableDescripcionFondo: {variables['VariableDescripcionFondo']}")
    print(f"VariableDescripcionAnimal: {variables['VariableDescripcionAnimal']}")

if __name__ == "__main__":
    obtener_variables_desde_servidor()


