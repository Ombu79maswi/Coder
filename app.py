import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configuración de la API de OpenAI
openai.api_key = ""  # Ingresa tu clave aquí

# Función para generar respuestas del modelo
def generar_respuesta(prompt, max_tokens=150, temperature=0.7):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en gestión de propiedades y consorcios."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response['choices'][0]['message']['content'].strip()

# Configurar Streamlit
st.title("Gestión de Propiedades con AI")
st.sidebar.header("Opciones de interacción")

# Sección 1: Generar recordatorios para inquilinos
st.header("Generar Recordatorios")
inquilino = st.text_input("Nombre del Inquilino")
direccion = st.text_input("Dirección")
monto_pendiente = st.number_input("Monto pendiente ($)", min_value=0.0, step=0.01)
dias_pendientes = st.number_input("Días de atraso", min_value=0)
interes = st.number_input("Porcentaje de interés (%)", min_value=0.0, step=0.1)

if st.button("Generar Recordatorio"):
    prompt = (
        f"El inquilino en {direccion} tiene un pago pendiente de ${monto_pendiente} desde hace {dias_pendientes} días. "
        f"Calcula el interés acumulado al {interes}% y genera un mensaje breve para recordarle el total a pagar."
    )
    respuesta = generar_respuesta(prompt)
    st.success(f"Respuesta del modelo: {respuesta}")

# Sección 2: Cálculo y visualización de expensas
st.header("Distribución de Expensas")
expensas_totales = st.number_input("Monto total de expensas ($)", min_value=0.0, step=0.01)
unidades = st.text_area("Detalles de unidades (ej: A:50, B:30, C:20)")

if st.button("Calcular Expensas"):
    # Procesar unidades y proporciones
    unidades_dict = {u.split(":")[0]: float(u.split(":")[1]) for u in unidades.split(",")}
    total_m2 = sum(unidades_dict.values())
    expensas_data = {
        "Unidad": list(unidades_dict.keys()),
        "Expensas ($)": [expensas_totales * (m2 / total_m2) for m2 in unidades_dict.values()]
    }
    df_expensas = pd.DataFrame(expensas_data)

    # Mostrar tabla y gráfico
    st.table(df_expensas)
    st.bar_chart(df_expensas.set_index("Unidad"))

# Sección 3: Estado financiero
st.header("Estado Financiero")
data = {
    "Unidad": ['A', 'B', 'C'],
    "Pagos Pendientes ($)": [500, 200, 300],
    "Expensas Mensuales ($)": [800, 600, 400]
}
df = pd.DataFrame(data)
st.subheader("Tabla de Estado Financiero")
st.table(df)

st.subheader("Gráfico de Estado Financiero")
st.bar_chart(df.set_index("Unidad"))
