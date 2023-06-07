def app_arboles():
    import streamlit as st
    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
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

    st.subheader('Configuración de los Árboles de Decisión')
    st.markdown("""
    - **max_depth**: La máxima profundidad del árbol. Este es un límite para controlar el sobreajuste. Un árbol muy profundo puede capturar demasiado ruido en los datos de entrenamiento.
    - **min_samples_split**: El número mínimo de muestras necesarias para dividir un nodo interno. Este es otro límite para controlar el sobreajuste. Un valor alto puede prevenir una división que solo identifique ruido.
    - **min_samples_leaf**: El número mínimo de muestras necesarias para ser una hoja. Este límite asegura que cada hoja (una predicción final) esté respaldada por un número suficiente de muestras.
    """)

    max_depth = st.slider("max_depth", 1, 100, 2, 1)
    min_samples_split = st.slider("min_samples_split", 2, 10, 2, 1)
    min_samples_leaf = st.slider("min_samples_leaf", 1, 10, 1, 1)

    # Crear el modelo de árbol de regresión y entrenarlo
    regression_model = DecisionTreeRegressor(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    regression_model.fit(X, y_reg)

    # Crear el modelo de árbol de clasificación y entrenarlo
    classification_model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
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

    # Imprimir la representación textual del árbol de regresión
    st.subheader("Árbol de Regresión")
    tree_text_reg = export_text(regression_model, feature_names=X.columns.tolist())
    st.code(tree_text_reg)

    # Imprimir la representación textual del árbol de clasificación
    st.subheader("Árbol de Clasificación")
    tree_text_cls = export_text(classification_model, feature_names=X.columns.tolist())
    st.code(tree_text_cls)
