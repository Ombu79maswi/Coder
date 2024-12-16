import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import re 

# API de OpenAI
openai.api_key = "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" 

# Función para generar respuestas del modelo y limpiar el texto
def generar_respuesta(prompt, max_tokens=150, temperature=0.7):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en gestión de propiedades y consorcios. Genera mensajes claros, formales y breves."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    # Obtener y limpiar la respuesta generada
    respuesta = response['choices'][0]['message']['content'].strip()
    respuesta = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', respuesta)  # Espacio entre número y letra
    respuesta = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', respuesta)  # Espacio entre letra y número
    respuesta = re.sub(r'\s+', ' ', respuesta).strip()  # Elimina espacios redundantes
    return respuesta

# Configuración de Streamlit
st.title("Gestión de Propiedades con AI")
st.header("Cargar Datos de Inquilinos")

# Crear o cargar DataFrame en Streamlit
if "data_inquilinos" not in st.session_state:
    st.session_state["data_inquilinos"] = pd.DataFrame(columns=[
        "Nombre", "Dirección", "Monto Pendiente ($)", "Días Pendientes", "Interés (%)", "Alquiler ($)", "Expensas ($)"
    ])

# Formulario para agregar datos de inquilinos
with st.form("form_inquilinos"):
    nombre = st.text_input("Nombre del Inquilino")
    direccion = st.text_input("Dirección")
    monto_pendiente = st.number_input("Monto Pendiente ($)", min_value=0.0, step=0.01)
    dias_pendientes = st.number_input("Días Pendientes", min_value=0, step=1)
    interes = st.number_input("Interés (%)", min_value=0.0, step=0.1)
    alquiler = st.number_input("Alquiler ($)", min_value=0.0, step=0.01)
    expensas = st.number_input("Expensas ($)", min_value=0.0, step=0.01)
    agregar = st.form_submit_button("Agregar")

if agregar and nombre and direccion:
    nuevo_inquilino = pd.DataFrame({
        "Nombre": [nombre],
        "Dirección": [direccion],
        "Monto Pendiente ($)": [monto_pendiente],
        "Días Pendientes": [dias_pendientes],
        "Interés (%)": [interes],
        "Alquiler ($)": [alquiler],
        "Expensas ($)": [expensas]
    })
    st.session_state["data_inquilinos"] = pd.concat([st.session_state["data_inquilinos"], nuevo_inquilino], ignore_index=True)
    st.success("Inquilino agregado correctamente.")

# Mostrar tabla actualizada
st.subheader("Datos de Inquilinos")
st.table(st.session_state["data_inquilinos"])

# Generar recordatorios usando OpenAI
st.header("Generar Recordatorios")
if not st.session_state["data_inquilinos"].empty:
    for index, row in st.session_state["data_inquilinos"].iterrows():
        prompt = (
            f"El inquilino \"{row['Nombre']}\" tiene un pago pendiente de ${row['Monto Pendiente ($)']:.2f}. "
            f"El pago está atrasado {row['Días Pendientes']} días y acumula un interés del {row['Interés (%)']:.2f}%. "
            f"Genera un mensaje breve y formal recordándole el total a pagar."
        )
        respuesta = generar_respuesta(prompt)
        st.markdown(f"**Recordatorio para {row['Nombre']}**: {respuesta}")
else:
    st.warning("No hay inquilinos cargados para generar recordatorios.")

# Generar gráficos
st.header("Gráficos Comparativos")
if not st.session_state["data_inquilinos"].empty:
    # Gráfico de Montos Pendientes por Inquilino
    st.subheader("Montos Pendientes por Inquilino")
    fig, ax = plt.subplots()
    ax.bar(
        st.session_state["data_inquilinos"]["Nombre"],
        st.session_state["data_inquilinos"]["Monto Pendiente ($)"],
        color="skyblue"
    )
    ax.set_title("Montos Pendientes por Inquilino")
    ax.set_xlabel("Inquilinos")
    ax.set_ylabel("Monto Pendiente ($)")
    st.pyplot(fig)

    # Gráfico Comparativo de Alquiler y Expensas
    st.subheader("Comparativo Alquiler vs Expensas")
    fig, ax = plt.subplots()
    ancho_barras = 0.4
    index = range(len(st.session_state["data_inquilinos"]))
    ax.bar(index, st.session_state["data_inquilinos"]["Alquiler ($)"], ancho_barras, label="Alquiler ($)", color="blue")
    ax.bar(
        [i + ancho_barras for i in index],
        st.session_state["data_inquilinos"]["Expensas ($)"],
        ancho_barras,
        label="Expensas ($)",
        color="orange"
    )
    ax.set_title("Comparativo Alquiler vs Expensas")
    ax.set_xlabel("Inquilinos")
    ax.set_ylabel("Monto ($)")
    ax.set_xticks([i + ancho_barras / 2 for i in index])
    ax.set_xticklabels(st.session_state["data_inquilinos"]["Nombre"], rotation=45)
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("No hay datos para generar gráficos.")