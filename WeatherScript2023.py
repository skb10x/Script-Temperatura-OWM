import requests
import time

def obtener_datos_climaticos(api_key, ciudad, pais):
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': f'{ciudad},{pais}',
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Verificar si la respuesta contiene datos válidos
        if 'main' not in data or 'temp' not in data['main']:
            print('Datos de temperatura no disponibles en la respuesta')
            return None, None, None

        # Obtener los datos
        temperatura_actual = data['main']['temp']
        sensacion_termica = data['main'].get('feels_like')
        humedad = data['main'].get('humidity')

        return temperatura_actual, sensacion_termica, humedad
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a la API: {e}")
        return None, None, None
    except Exception as e:
        print(f"Error desconocido: {e}")
        return None, None, None

def redondear_temperatura_personalizado(temperatura):
    parte_entera = int(temperatura)
    parte_decimal = int((temperatura - parte_entera) * 10)

    # Formatear la cadena según los casos mencionados
    if parte_decimal != 0:
        return f"{parte_entera}.{parte_decimal}"
    else:
        return f"{parte_entera}.{parte_decimal}"

def actualizar_archivo_clima(temperatura, sensacion_termica, humedad, archivo_temperatura, archivo_sensacion_termica, archivo_humedad):
    temperatura_redondeada = redondear_temperatura_personalizado(temperatura)
    
    with open(archivo_temperatura, 'w', encoding='utf-8') as file:
        file.write(f" {temperatura_redondeada}° ")

    if sensacion_termica is not None:
        with open(archivo_sensacion_termica, 'w', encoding='utf-8') as file:
            file.write(f" ST {sensacion_termica:.1f}° ")

    if humedad is not None:
        with open(archivo_humedad, 'w', encoding='utf-8') as file:
            file.write(f" H: {humedad}% ")

if __name__ == "__main__":
    api_key_owm = '1ca4a975eab32b7fc7b332a64a744d1c'
    ciudad = 'Buenos Aires F.D.'
    pais = 'AR'
    archivo_temperatura = 'temperatura_bsas.txt'
    archivo_sensacion_termica = 'sensacion_termica_bsas.txt'
    archivo_humedad = 'humedad_bsas.txt'

    while True:
        temperatura_actual, sensacion_termica, humedad = obtener_datos_climaticos(api_key_owm, ciudad, pais)

        if temperatura_actual is not None:
            actualizar_archivo_clima(temperatura_actual, sensacion_termica, humedad, archivo_temperatura, archivo_sensacion_termica, archivo_humedad)
            print(f"Temperatura: {redondear_temperatura_personalizado(temperatura_actual)}°   ST {sensacion_termica:.1f}°  H: {humedad}% ")

        # Espera 5 minutos antes de la próxima actualización
        time.sleep(300)
