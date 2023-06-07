def app_bosques():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.tree import export_text

    # Leer datos del archivo alimentos.csv
    data = pd.read_csv("alimentos.csv")

    # Seleccionar solo las columnas numéricas (excluyendo la columna "ID")
    numeric_columns = ["Calorías", "Grasas", "Proteínas", "Carbohidratos"]
    data_numeric = data[numeric_columns]

    # Dividir los datos en características (X) y la variable objetivo para ambos modelos
    X = data_numeric.drop("Calorías", axis=1)
    y_reg = data_numeric["Calorías"]
    y_cls = data["Grupo_alimento"]

    st.title("App de Análisis de Alimentos")

    st.subheader('Configuración de los Bosques Aleatorios')
    st.markdown("""
    - **n_estimators**: La cantidad de árboles en el bosque.
    - **max_depth**: La máxima profundidad de cada árbol. Controla la complejidad del modelo y evita el sobreajuste.
    - **min_samples_split**: El número mínimo de muestras requeridas para dividir un nodo interno.
    - **min_samples_leaf**: El número mínimo de muestras requeridas en cada hoja.
    """)

    n_estimators = st.slider("n_estimators", 1, 100, 10, 1)
    max_depth = st.slider("max_depth", 1, 100, 2, 1)
    min_samples_split = st.slider("min_samples_split", 2, 10, 2, 1)
    min_samples_leaf = st.slider("min_samples_leaf", 1, 10, 1, 1)

    # Crear el modelo de bosque aleatorio de regresión y entrenarlo
    regression_model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    regression_model.fit(X, y_reg)

    # Crear el modelo de bosque aleatorio de clasificación y entrenarlo
    classification_model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    classification_model.fit(X, y_cls)

    # Obtener los valores de entrada del usuario
    grasas = st.number_input("Grasas", value=0.0)
    proteinas = st.number_input("Proteínas", value=0.0)
    carbohidratos = st.number_input("Carbohidratos", value=0.0)

    # Botón para generar la predicción de regresión y clasificación
    if st.button("Generar Predicción"):
        # Realizar la predicción de regresión
        input_data = pd.DataFrame([[grasas, proteinas, carbohidratos]], columns=["Grasas", "Proteínas", "Carbohidratos"])
        prediction_regression = regression_model.predict(input_data)

        # Realizar la predicción de clasificación
        prediction_classification = classification_model.predict(input_data)

        # Mostrar los resultados de la predicción de regresión y clasificación
        st.subheader("Resultados de la Predicción")
        st.write("Calorías Predichas:", prediction_regression[0])
        st.write("Grupo de Alimento:", prediction_classification[0])

    # Mostrar la importancia de las características para ambos modelos
    st.subheader("Importancia de las Características para la Regresión")
    feature_importance_reg = pd.DataFrame(regression_model.feature_importances_, index=X.columns, columns=['Importancia']).sort_values('Importancia', ascending=False)
    st.write(feature_importance_reg)
    fig_reg = plt.figure()
    plt.bar(feature_importance_reg.index, feature_importance_reg['Importancia'])
    plt.xlabel('Características')
    plt.ylabel('Importancia')
    plt.title('Importancia de las Características - Regresión')
    st.pyplot(fig_reg)

    st.subheader("Importancia de las Características para la Clasificación")
    feature_importance_cls = pd.DataFrame(classification_model.feature_importances_, index=X.columns, columns=['Importancia']).sort_values('Importancia', ascending=False)
    st.write(feature_importance_cls)
    fig_cls = plt.figure()
    plt.bar(feature_importance_cls.index, feature_importance_cls['Importancia'])
    plt.xlabel('Características')
    plt.ylabel('Importancia')
    plt.title('Importancia de las Características - Clasificación')
    st.pyplot(fig_cls)
