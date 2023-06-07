import streamlit as st
from inicio import app_inicio
from apriory import app_apriori
from metricas import app_metricas
from clustering import app_clustering 
from arboles import app_arboles
from bosques import app_bosques
from recomendacion import app_recomendacion

def main():
    st.set_page_config(page_title="Aplicación de Nutrición", page_icon="🥦", layout="wide")

    # Menú de navegación
    menu = ["Inicio", "Apriori", "Métricas", "Clustering", "arboles", "bosques", "recomendacion" ]
    opcion = st.sidebar.selectbox("Selecciona una aplicación", menu)

    # Mostrar la aplicación correspondiente según la opción seleccionada
    if opcion == "Inicio":
        app_inicio()
    elif opcion == "Apriori":
        app_apriori()
    elif opcion == "Métricas":
        app_metricas()
    elif opcion == "Clustering":
        app_clustering()
    elif opcion == "arboles":
         app_arboles()
    elif opcion == "bosques":
         app_bosques()
    elif opcion == "recomendacion":
         app_recomendacion()

if __name__ == "__main__":
    main()

