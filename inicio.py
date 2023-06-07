import os
import csv
import matplotlib.pyplot as plt
import streamlit as st
from apriory import app_apriori

def calcular_imc(peso, altura_cm):
    peso = float(peso)
    altura_m = float(altura_cm) / 100
    imc = peso / (altura_m ** 2)
    return imc

def definir_objetivo(imc, altura_cm):
    altura_m = altura_cm / 100
    if imc < 18.5:
        return "Ganar peso", (18.5 - imc) * altura_m ** 2
    elif imc <= 24.9:
        return "Mantener peso", 0
    elif imc <= 29.9:
        return "Perder peso", (imc - 24.9) * altura_m ** 2
    else:
        return "Perder peso (Obesidad)", (imc - 24.9) * altura_m ** 2

def guardar_datos(nombre, apellidoP, edad, peso, altura_cm, imc, genero):
    archivo_csv = "datos_personas.csv"
    objetivo_registrado = None

    if imc > 24.9:
        objetivo_registrado = 3  # IMC alto
    elif imc < 18.5:
        objetivo_registrado = 1  # IMC bajo
    else:
        objetivo_registrado = 2  # IMC normal

    os.environ["OBJETIVO_REGISTRADO"] = str(objetivo_registrado)

    datos = [nombre, apellidoP, edad, peso, altura_cm, imc, genero, objetivo_registrado]

    with open(archivo_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(datos)

def app_inicio():
    st.markdown("""
    <style>
    .reportview-container {
        flex-direction: column;
        background-color: #4B8BBE;
        color: #ffffff;
        padding: 10px;
    }
    h1 {
        color: #FFD43B;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Nutria AI - Página de inicio")

    nombre = st.text_input("Nombre", max_chars=20, key="nombre_input")
    apellidoP = st.text_input("Apellido Paterno", max_chars=20, key="apellido_input")
    edad = st.number_input("Edad", min_value=0, key="edad_input")
    peso = st.number_input("Peso (kg)", min_value=0.0, key="peso_input")
    altura_cm = st.number_input("Altura (cm)", min_value=0.0, key="altura_input")

    genero = st.selectbox("Género", ("Hombre", "Mujer"))

    datos_completos = nombre and apellidoP and edad and peso and altura_cm

    guardar_button = st.button("Guardar")

    if guardar_button and datos_completos:
        imc = calcular_imc(peso, altura_cm)
        imc_ideal_min = 18.5
        imc_ideal_max = 24.9

        st.markdown(f"## Tu IMC es: {imc:.2f}")

        if imc > imc_ideal_max:
            objetivo, kilos = definir_objetivo(imc, altura_cm)
            st.warning(f"Tu IMC es alto. Debes bajar {kilos:.2f} kg para llegar al IMC ideal.")
        elif imc < imc_ideal_min:
            objetivo, kilos = definir_objetivo(imc, altura_cm)
            st.warning(f"Tu IMC es bajo. Debes subir {abs(kilos):.2f} kg para llegar al IMC ideal.")
        else:
            objetivo, kilos = definir_objetivo(imc, altura_cm)
            st.success("Tu IMC está dentro del rango ideal.")

        st.markdown(f"## Tu objetivo nutricional es: {objetivo}")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(["Tu IMC"], [imc], label="Tu IMC")
        ax.bar(["IMC ideal"], [imc_ideal_max], label="IMC ideal")
        ax.set_ylabel("IMC")
        ax.set_title("Comparación de IMC")
        ax.legend()
        st.pyplot(fig)

        guardar_datos(nombre, apellidoP, edad, peso, altura_cm, imc, genero)
    elif guardar_button:
        st.warning("Por favor, introduce todos los datos.")

if __name__ == "__main__":
    app_inicio()
