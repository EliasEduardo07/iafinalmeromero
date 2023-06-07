import streamlit as st
import googlemaps
import folium
from geopy.distance import geodesic
from streamlit_folium import folium_static

API_KEY = "AIzaSyCRoRdEBeMZUfx_kSjmB-Dgezk2jYWh7bQ"
gmaps = googlemaps.Client(key=API_KEY)

def direccion_a_coordenadas(direccion):
    geocode_result = gmaps.geocode(direccion)
    if geocode_result:
        return geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
    else:
        return None, None

def buscar_supermercados(latitud, longitud, radio):
    supermercados = gmaps.places_nearby(location=(latitud, longitud), radius=radio, type='supermarket')['results']
    return supermercados

def calcular_distancia_euclidiana(coordenadas1, coordenadas2):
    return geodesic(coordenadas1, coordenadas2).meters

def calcular_ruta(latitud_origen, longitud_origen, latitud_destino, longitud_destino, mode):
    directions_result = gmaps.directions(
        (latitud_origen, longitud_origen),
        (latitud_destino, longitud_destino),
        mode=mode,
        units="metric"
    )
    return directions_result

def obtener_distancia_ruta(ruta):
    distancia_total = 0
    for leg in ruta[0]['legs']:
        for step in leg['steps']:
            distancia_total += step['distance']['value']
    return distancia_total

def app_metricas():
    st.title("Métricas de distancia")

    ubicacion_usuario = st.text_input("Por favor ingresa tu ubicación (ejemplo: 'Ciudad de México'):")
    transportation_modes = ['driving', 'walking', 'bicycling', 'transit']
    transportation_modes_spanish = ['Conduciendo', 'Caminando', 'En bicicleta', 'En transporte público']
    selected_mode_spanish = st.selectbox('Modo de transporte:', transportation_modes_spanish)
    selected_mode = transportation_modes[transportation_modes_spanish.index(selected_mode_spanish)]

    if ubicacion_usuario:
        latitud_actual, longitud_actual = direccion_a_coordenadas(ubicacion_usuario)

        if latitud_actual and longitud_actual:
            st.write("Tu ubicación actual: {}, {}".format(latitud_actual, longitud_actual))
            radio_busqueda = st.number_input("Ingresa el radio de búsqueda en metros:", min_value=100)

            supermercados_cercanos = buscar_supermercados(latitud_actual, longitud_actual, radio_busqueda)
            supermercados_y_distancias = []

            for supermercado in supermercados_cercanos:
                nombre = supermercado['name']
                direccion = supermercado['vicinity']
                coordenadas_supermercado = supermercado['geometry']['location']
                latitud_supermercado = coordenadas_supermercado['lat']
                longitud_supermercado = coordenadas_supermercado['lng']

                ruta = calcular_ruta(latitud_actual, longitud_actual, latitud_supermercado, longitud_supermercado, selected_mode)
                distancia_ruta = obtener_distancia_ruta(ruta)

                distancia_euclidiana = calcular_distancia_euclidiana(
                    (latitud_actual, longitud_actual),
                    (latitud_supermercado, longitud_supermercado)
                )

                supermercados_y_distancias.append((
                    nombre, distancia_ruta, distancia_euclidiana, latitud_supermercado, longitud_supermercado
                ))

            supermercados_y_distancias.sort(key=lambda x: x[2])

            st.subheader("Distancias de supermercados cercanos:")
            opciones_supermercados = [nombre for nombre, _, _, _, _ in supermercados_y_distancias]
            supermercado_seleccionado = st.selectbox("Seleccione un supermercado:", opciones_supermercados)

            for nombre, distancia_ruta, distancia_euclidiana, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                if nombre == supermercado_seleccionado:
                    st.write("Nombre: ", nombre)
                    st.write("Distancia Ruta: ", distancia_ruta)
                    st.write("Distancia Euclidiana: ", distancia_euclidiana)
                    break

            mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
            folium.Marker([latitud_actual, longitud_actual], popup='Ubicación actual', icon=folium.Icon(color='blue')).add_to(mapa)
            for nombre, _, _, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                folium.Marker([latitud_supermercado, longitud_supermercado], popup=nombre, icon=folium.Icon(color='red')).add_to(mapa)
            folium_static(mapa)

            if st.button("Calcular ruta"):
                for nombre, _, _, latitud_supermercado, longitud_supermercado in supermercados_y_distancias:
                    if nombre == supermercado_seleccionado:
                        ruta = calcular_ruta(
                            latitud_actual, longitud_actual, latitud_supermercado, longitud_supermercado, selected_mode
                        )
                        break
                if ruta:
                    ruta_mapa = folium.Map(location=[latitud_actual, longitud_actual], zoom_start=13)
                    folium.PolyLine(
                        [(step['start_location']['lat'], step['start_location']['lng']) for step in ruta[0]['legs'][0]['steps']],
                        color="green", weight=2.5, opacity=1
                    ).add_to(ruta_mapa)
                    folium_static(ruta_mapa)
                else:
                    st.write("No se pudo calcular la ruta.")
        else:
            st.write("No se pudo obtener la ubicación a partir de la dirección ingresada. Por favor intente con otra dirección.")
    else:
        st.write("Por favor ingrese su ubicación para continuar.")

if __name__ == "__main__":
    app_metricas()
