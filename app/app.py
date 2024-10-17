import requests
from flask import Flask, render_template, jsonify, request
import pandas as pd
from urllib.parse import urlencode
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en km
    R = 6371.0  
    # Convertir grados a radianes
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return R * c  # Distancia en kilómetros

@app.route('/water', methods=['GET'])
def get_water_data():
    # Captura todos los parámetros de consulta en un diccionario
    params = request.args.to_dict()
    ide = request.args.get('id', type=str)

    # Construye la URL base
    base_url = f"https://g3e0772c2cebad1-yi93oz1p4mw80tdf.adb.eu-madrid-1.oraclecloudapps.com/ords/admin/agua/?limit=3000&q={{\"ID\":\"{ide}\"}}"

    # Si hay parámetros adicionales, conviértelos a una cadena de consulta
    if params:
        query_string = urlencode(params)  # Convierte el diccionario a una cadena de consulta
        full_url = f"{base_url}&{query_string}"  # Concatena la URL base con la cadena de consulta
    else:
        full_url = base_url  # Si no hay parámetros, solo usa la base_url

    # Realiza la petición a la URL
    try:
        response = requests.get(full_url)  # Realiza la solicitud HTTP
        response.raise_for_status()  # Lanza una excepción si el código de estado HTTP indica un error
        data = response.json()  # Obtiene los datos en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")
        return jsonify({"error": "Error al hacer la solicitud HTTP"}), 500

    # Verificar si se recibieron elementos
    if 'items' not in data or not data['items']:
        return jsonify({"error": "No se encontraron datos para el ID proporcionado."}), 404

    # Convertir los datos en un DataFrame
    df = pd.DataFrame(data['items'])

    # Asegúrate de que la columna 'fecha' esté en formato de fecha
    try:
        df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%y %H:%M')
    except Exception as e:
        print(f"Error al convertir la columna de fecha: {e}")
        return jsonify({"error": "Error al procesar las fechas."}), 500

    # Extraer el año de la fecha
    df['año'] = df['fecha'].dt.year

    # Calcular estadísticas
    resultados = {}

    # Iterar sobre los años únicos
    for ano in df['año'].unique():
        datos_ano = df[df['año'] == ano]
        
        # Asegurarse de que haya datos para el año
        if not datos_ano.empty:
            media_agua = datos_ano['agua_actual'].mean()
            max_agua = datos_ano['agua_actual'].max()
            min_agua = datos_ano['agua_actual'].min()
            
            # Almacenar los resultados con el año como clave
            resultados["2024"] = {  # Convertir la clave del año a string
                'media': media_agua.item() if isinstance(media_agua, (np.integer, np.floating)) else media_agua,
                'maximo': max_agua.item() if isinstance(max_agua, (np.integer, np.floating)) else max_agua,
                'minimo': min_agua.item() if isinstance(min_agua, (np.integer, np.floating)) else min_agua
            }
        else:
            # Si no hay datos para ese año, almacenar None
            resultados["2024"] = {
                'media': None,
                'maximo': None,
                'minimo': None
            }
    
    return jsonify(resultados)



@app.route('/data', methods=['GET'])
def get_data():
    # Captura todos los parámetros de consulta en un diccionario
    params = request.args.to_dict()

    # Muestra los parámetros recibidos
    print("Parámetros recibidos:", params)
    

    # Construye la URL base
    base_url = "https://g3e0772c2cebad1-yi93oz1p4mw80tdf.adb.eu-madrid-1.oraclecloudapps.com/ords/admin/embalses/?limit=300"
    
    # Si hay parámetros, conviértelos a una cadena de consulta
    if params:
        query_string = urlencode(params)  # Convierte el diccionario a una cadena de consulta
        full_url = base_url  # Concatena la URL base con la cadena de consulta
    else:
        full_url = base_url  # Si no hay parámetros, solo usa la base_url
    
    # Realiza la petición a la URL
    try:
        response = requests.get(full_url)  # Realiza la solicitud HTTP
        response.raise_for_status()  # Lanza una excepción si el código de estado HTTP indica un error
        data = response.json()  # Obtiene los datos en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud HTTP: {e}")
        return jsonify({"error": "Error al hacer la solicitud HTTP"}), 500
    
    # Imprimir el JSON recibido para inspección
    print("Datos recibidos:", data)

    # Accede a la lista bajo la clave "items"
    items = data.get('items', [])

    # Verificar si 'items' es una lista
    if not isinstance(items, list):
        return jsonify({"error": "Los datos no son una lista."}), 400

    # Intentar crear el DataFrame
    try:
        df = pd.DataFrame(items)  # Crear el DataFrame directamente desde 'items'
        df['distancia'] = 0.0
        print(df['distancia'].head())  # Ver los primeros registros

        # Asegurarse de que las columnas 'x' y 'y' sean numéricas (float)
        df['x'] = pd.to_numeric(df['x'], errors='coerce')
        df['y'] = pd.to_numeric(df['y'], errors='coerce')

        # Eliminar filas con valores NaN en las coordenadas

    except ValueError as e:
        print(f"Error al crear DataFrame: {e}")
        return jsonify({"error": str(e)}), 400

    # Parámetros opcionales de latitud, longitud y radio
    lat = request.args.get('lat', type=float)  # Obtener la latitud desde la URL
    lon = request.args.get('lon', type=float)  # Obtener la longitud desde la URL
    radio = request.args.get('distance', type=float)  # Radio en kilómetros (por defecto 100 km)
    print(radio)

    # Si se proporcionan latitud y longitud, filtrar los resultados
    if lat is not None and lon is not None:
        try:
            # Calcular la distancia de cada embalse con respecto a las coordenadas proporcionadas
            df['distancia'] = haversine(lat, lon, df['x'], df['y'])

            # Filtrar los embalses que estén dentro del radio especificado
            df_filtrado = df[df['distancia'] <= radio]
        except Exception as e:
            print(f"Error al filtrar por distancia: {e}")
            return jsonify({"error": "Error al filtrar por distancia"}), 500
    else:
        df_filtrado = df  # Si no se proporcionan lat/lon, devolver todos los datos

    # Convertir el DataFrame filtrado a JSON y devolverlo
    print(df_filtrado)
    return df_filtrado.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
