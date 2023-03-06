import requests
import pandas as pd
from scipy.fft import fft
import matplotlib.pyplot as plt

token = 'f9cc0ba317d94318075c597df818c413def16b7046acb73099f59b728fa2ab7e'
start_date = '2018-09-02T00:00:00'
end_date = '2018-10-06T23:59:59'
variable_id = '1293'
url = 'https://api.esios.ree.es/indicators/1293'


# Define los encabezados de la solicitud
headers = {
    "Accept": "Accept: application/json; application/vnd.esios-api-v2+json",
    "Content-Type": "application/json",
    "x-api-key": "f9cc0ba317d94318075c597df818c413def16b7046acb73099f59b728fa2ab7e"
}

# Realiza la solicitud GET y obtiene la respuesta
response = requests.get(url, headers=headers, params={"start_date": start_date, "end_date": end_date})

# Si la respuesta HTTP fue exitosa (código 200), obtiene el contenido de la respuesta
if response.status_code == 200:
    data = response.json()
    # Hacer algo con los datos obtenidos, como imprimirlos en la consola
    print(data)
else:
    # Si la respuesta HTTP no fue exitosa, mostrar el código de estado
    print(f"Error: {response.status_code}")