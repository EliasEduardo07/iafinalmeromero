import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import pdist, squareform

@st.cache_data
def load_data():
    """
    Esta función carga los datos del archivo 'alimentos.csv'.
    Devuelve un error si el archivo no se encuentra o no puede ser leído.
    """
    try:
        data = pd.read_csv('alimentos.csv')
    except FileNotFoundError:
        st.error("El archivo 'alimentos.csv' no se encuentra en el directorio actual. Asegúrate de tener el archivo en la misma carpeta que este script.")
        return None
    except pd.errors.ParserError:
        st.error("El archivo 'alimentos.csv' no se pudo leer. Verifica que esté en formato CSV.")
        return None
    return data

def compute_distance_matrix(data, metric, p=None):
    """
    Esta función calcula la matriz de distancias basada en una métrica seleccionada por el usuario.
    La métrica puede ser euclidiana, chebyshev o minkowski.
    """
    if metric == 'minkowski':
        distance_matrix = pdist(data.values, metric=metric, p=p)
    else:
        distance_matrix = pdist(data.values, metric=metric)
    distance_matrix = squareform(distance_matrix)
    return pd.DataFrame(distance_matrix, index=data.index, columns=data.index)

def average_distance(distance_matrix):
    """
    Esta función calcula la distancia promedio entre todos los pares de objetos.
    """
    np.fill_diagonal(distance_matrix.values, np.nan)  # Excluir la diagonal (distancia de un elemento a sí mismo)
    return np.nanmean(distance_matrix.values)  # Calcular la media ignorando NaN

def app_recomendacion():
    st.title('Cálculo de Distancias entre Alimentos')

    data = load_data()
    if data is None:
        return

    # Selecciona solo las columnas numéricas para el análisis
    nutritional_data = data.select_dtypes(include=['number'])

    # Escala los datos para que todas las características tengan la misma importancia
    standardized_data = StandardScaler().fit_transform(nutritional_data)

    st.write("Por favor, selecciona una métrica de distancia para calcular las distancias entre los diferentes alimentos.")
    # Permite al usuario seleccionar la métrica de distancia
    metric = st.selectbox('Seleccione la métrica de distancia', ('euclidean', 'chebyshev', 'minkowski'))

    p = None
    if metric == 'minkowski':
        st.write("La métrica de Minkowski es una generalización de otras métricas. Necesita un parámetro 'p'. Cuando 'p' es 1, se convierte en la métrica de Manhattan. Cuando 'p' es 2, se convierte en la métrica euclidiana.")
        p = st.slider('Seleccione el valor de p para la distancia Minkowski', 1, 10)

    distance_matrix = compute_distance_matrix(pd.DataFrame(standardized_data, columns=nutritional_data.columns, index=nutritional_data.index), metric, p)

    st.write("Aquí está la matriz de distancias entre los diferentes alimentos, calculada utilizando la métrica seleccionada:")
    st.dataframe(distance_matrix.style.format("{:.2f}"))

    avg_dist = average_distance(distance_matrix)
    st.write(f"La distancia promedio entre todos los pares de alimentos es: {avg_dist:.2f}")

app_recomendacion()
