import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def cargar_datos(nombre_archivo):
    datos = pd.read_csv(nombre_archivo)
    columnas_ingredientes = [col for col in datos.columns if col.startswith("ingrediente")]
    datos_ingredientes = datos[columnas_ingredientes]
    return datos_ingredientes

def encontrar_reglas_asociacion(datos, confianza, soporte, elevacion):
    transacciones = datos.apply(lambda row: row.dropna().tolist(), axis=1).tolist()
    te = TransactionEncoder()
    te_transacciones = te.fit(transacciones).transform(transacciones)
    df_transacciones = pd.DataFrame(te_transacciones, columns=te.columns_)
    frecuentes = apriori(df_transacciones, min_support=soporte, use_colnames=True)
    reglas = association_rules(frecuentes, metric="confidence", min_threshold=confianza)
    reglas_filtradas = reglas[reglas['lift'] > elevacion]
    reglas_filtradas["interpretacion"] = reglas_filtradas.apply(lambda row: f"Si se tiene {', '.join(list(row['antecedents']))}, entonces es probable ({row['confidence']*100:.2f}% de confianza) que también se tenga {', '.join(list(row['consequents']))}. Esta regla tiene una fuerza de asociación de {row['lift']:.2f}.", axis=1)

    return reglas_filtradas

def graficar_frecuencia(datos):
    datos_filtrados = datos.apply(lambda x: x[x != ""], axis=1)
    ingredientes_frecuencia = datos_filtrados.unstack().value_counts()
    ingredientes_frecuencia = ingredientes_frecuencia[ingredientes_frecuencia > 1]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=ingredientes_frecuencia.values, y=ingredientes_frecuencia.index)
    plt.xlabel("Frecuencia")
    plt.ylabel("Ingrediente")
    plt.title("Frecuencia de los Ingredientes")
    st.pyplot(fig)

def app_apriori():
    st.title("Nutria AI - Apriori")
    valor_objetivo = int(os.environ.get("OBJETIVO_REGISTRADO", 0))

    if valor_objetivo == 1:
        nombre_archivo = "recetas_bajas.csv"
    elif valor_objetivo == 2:
        nombre_archivo = "receta_normal.csv"
    elif valor_objetivo == 3:
        nombre_archivo = "receta_altas.csv"
    else:
        nombre_archivo = ""

    if nombre_archivo:
        datos = cargar_datos(nombre_archivo)
        st.info(f"Leyendo archivo: {nombre_archivo}")
    else:
        st.warning("Por favor, ingrese el nombre del archivo CSV correspondiente al objetivo registrado.")

    confianza = st.slider("Confianza", min_value=0.0, max_value=1.0, step=0.1, value=0.5)
    soporte = st.slider("Soporte", min_value=0.0, max_value=1.0, step=0.1, value=0.1)
    elevacion = st.slider("Elevación", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

    if st.button("Generar Interpretación y Gráfica de Frecuencias"):
        if datos is not None:
            reglas = encontrar_reglas_asociacion(datos, confianza, soporte, elevacion)

            if reglas.empty:
                st.write("No se encontraron reglas de asociación.")
            else:
                st.write("Reglas de asociación encontradas:")
                st.dataframe(reglas)

                st.write("Interpretación de las reglas de asociación:")
                st.table(reglas["interpretacion"])

        graficar_frecuencia(datos)

if __name__ == "__main__":
    app_apriori()
