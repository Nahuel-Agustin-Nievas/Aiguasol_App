import requests
import pandas as pd
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

token = 'f9cc0ba317d94318075c597df818c413def16b7046acb73099f59b728fa2ab7e'
start_date = '2018-09-02T00:00:00'
end_date = '2018-10-06T23:59:59'
variable_id = '1293'
url = 'https://api.esios.ree.es/indicators/1293'


# Define los encabezados de la solicitud
headers = {
    "Accept": "Accept: application/json; application/vnd.esios-api-v2+json",
    "Content-Type": "application/json",
    "x-api-key": token
}

# Realiza la solicitud GET y obtiene la respuesta
response = requests.get(url, headers=headers, params={"start_date": start_date, "end_date": end_date})

# Si la respuesta HTTP fue exitosa (código 200), obtiene el contenido de la respuesta
if response.status_code == 200:
    data = response.json()
    # Hacer algo con los datos obtenidos, como imprimirlos en la consola
    # print(data)
    # Extraemos los datos relevantes del JSON y los guardamos en una lista de diccionarios
    values = data['indicator']['values']
    data_list = []
    for value in values:
        data_dict = {}
        data_dict['datetime'] = value['datetime']
        data_dict['value'] = value['value']
        data_list.append(data_dict)
        # print(data_list)

    # Creamos el DataFrame a partir de la lista de diccionarios
    df = pd.DataFrame(data_list)

    # Convertimos la columna 'datetime' a un objeto datetime y la establecemos como índice del DataFrame
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')

    # Calculamos el valor promedio de la demanda eléctrica para cada hora en el período
    hourly_data = df.groupby(pd.Grouper(freq='H')).mean()
    hourly_data = hourly_data.dropna()

    # Realizamos la transformada de Fourier
    n = len(hourly_data)
    yf = fft(hourly_data['value'].to_numpy())
    xf = np.linspace(0.0, 1.0/(2.0*60*60), n//2)

    # Graficamos la demanda eléctrica en función del tiempo
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    axs[0].plot(hourly_data.index, hourly_data['value'])
    axs[0].set_xlabel('Tiempo')
    axs[0].set_ylabel('Demanda eléctrica')
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
    axs[0].tick_params(axis='x', rotation=45)

    # Graficamos la transformada de Fourier de la demanda eléctrica en función de la frecuencia
    max_demand = hourly_data['value'].max()
    axs[1].plot(xf, 2.0/n * np.abs(yf[0:n//2]))
    axs[1].set_xlabel('Frecuencia (Hz)')
    axs[1].set_ylabel('Demanda eléctrica')
    axs[1].set_xlim([0, 1.0/(2.0*60*60)])
    axs[1].set_ylim([0, max_demand])

    plt.tight_layout()
    plt.show()
else:
    # Si la respuesta HTTP no fue exitosa, mostrar el código de estado
    print(f"Error: {response.status_code}")





'''
Este código crea una figura con dos subgráficos utilizando la función subplots(). Luego, se grafica la demanda eléctrica en el primer subgráfico utilizando la función axs[0].plot(), y la transformada de Fourier de la demanda eléctrica en el segundo subgráfico utilizando la función axs[1].plot(). Por último, se utilizan las funciones axs[0].set_xlabel() y axs[0].set_ylabel() para establecer los títulos de los ejes en el primer subgráfico, y las funciones axs[1].set_xlabel() y axs[1].set_ylabel() para establecer los títulos de los ejes en el segundo subgráfico.

'''