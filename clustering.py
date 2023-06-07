import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

def hierarchical_clustering(data_std, num_clusters):
    model = AgglomerativeClustering(n_clusters=num_clusters)
    model.fit(data_std)
    labels = model.labels_
    return labels

def kmeans_clustering(data_std, num_clusters):
    model = KMeans(n_clusters=num_clusters)
    model.fit(data_std)
    labels = model.labels_
    return labels

def select_clustering_algorithm():
    clustering_algorithm = st.selectbox('Seleccione el algoritmo de clustering', ('Clustering Jerárquico', 'Clustering Particional'))
    return clustering_algorithm

@st.cache(allow_output_mutation=True)
def load_data():
    try:
        data = pd.read_csv('alimentos.csv')
    except FileNotFoundError:
        st.error("El archivo 'alimentos.csv' no se encuentra en el directorio actual.")
        return None
    except pd.errors.ParserError:
        st.error("El archivo 'alimentos.csv' no se pudo leer. Verifica su formato.")
        return None
    return data

def plot_cluster_graphs(data, data_std, clustering_algorithm):
    if clustering_algorithm == 'Clustering Particional':
        st.subheader("Gráfica por cluster")
        sns.pairplot(data, vars=['Calorías', 'Grasas', 'Proteínas', 'Carbohidratos'], hue='cluster', palette='Dark2')
        st.pyplot(plt.gcf())
        plt.clf()
    elif clustering_algorithm == 'Clustering Jerárquico':
        linked = linkage(data_std, 'single')
        plt.figure(figsize=(10, 7))
        dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=True)
        st.subheader("Dendrograma")
        st.pyplot(plt.gcf())
        plt.clf()

def plot_cluster_statistics(data, num_clusters):
    for i in range(num_clusters):
        col1, col2 = st.columns(2)
        with col1:
            st.header(f"Cluster {i+1}:")
            st.write(data[data['cluster'] == i]['Nombre_alimento'].values)
        with col2:
            st.header(f"Estadísticas del Cluster {i+1}:")
            st.write(data[data['cluster'] == i][['Calorías', 'Grasas', 'Proteínas', 'Carbohidratos']].describe())

def calculate_elbow_method(data_std, max_clusters):
    sse = []
    list_k = list(range(1, max_clusters+1))

    for k in list_k:
        km = KMeans(n_clusters=k)
        km.fit(data_std)
        sse.append(km.inertia_)

    plt.figure(figsize=(6, 6))
    plt.plot(list_k, sse, '-o')
    plt.xlabel('Número de clusters *k*')
    plt.ylabel('Suma de errores cuadrados')
    st.pyplot(plt.gcf())
    plt.clf()

def app_clustering():
    st.title('Clustering de Alimentos')

    data_load_state = st.text('Cargando datos...')
    data = load_data()
    if data is None:
        return
    data = data.copy()
    data_load_state.text('Datos cargados correctamente!')

    nutritional_data = data[['Calorías', 'Grasas', 'Proteínas', 'Carbohidratos']]
    standardized_data = StandardScaler().fit_transform(nutritional_data)

    max_clusters = st.slider('Máximo número de clusters para el método del codo', 2, 20)

    calculate_elbow_method(standardized_data, max_clusters)

    num_clusters = st.slider('Número de clusters', 2, 10)

    clustering_algorithm = select_clustering_algorithm()

    if clustering_algorithm == 'Clustering Jerárquico':
        cluster_labels = hierarchical_clustering(standardized_data, num_clusters)
    elif clustering_algorithm == 'Clustering Particional':
        cluster_labels = kmeans_clustering(standardized_data, num_clusters)

    data['cluster'] = cluster_labels

    st.subheader("Datos")
    st.write(data)

    plot_cluster_graphs(data, standardized_data, clustering_algorithm)

    plot_cluster_statistics(data, num_clusters)

app_clustering()
