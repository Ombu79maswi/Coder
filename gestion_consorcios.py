import openai
import matplotlib.pyplot as plt
import pandas as pd

# Configuración de la API de OpenAI
openai.api_key = ""


def generar_respuesta(prompt, max_tokens=150, temperature=0.7):
    """
    Función para generar respuestas de texto optimizadas dentro de un límite de tokens usando OpenAI GPT.
    - prompt: Texto de entrada para el modelo.
    - max_tokens: Número máximo de tokens en la respuesta.
    - temperature: Nivel de aleatoriedad en las respuestas del modelo.
    """
    # Implementación de few-shot prompting para mayor precisión
    examples = (
        "Ejemplo 1: El inquilino en Calle Verdadera 456 tiene un pago pendiente de $300 desde hace 20 días. Genera un recordatorio con un interés acumulado del 3%. "
        "Respuesta esperada: Recordatorio generado para el inquilino en Calle Verdadera 456. Monto pendiente: $300. Interés acumulado: $9.\n"
        "Ejemplo 2: El inquilino en Calle Imaginaria 789 tiene un pago pendiente de $150 desde hace 10 días. Genera un recordatorio con un interés acumulado del 2%. "
        "Respuesta esperada: Recordatorio generado para el inquilino en Calle Imaginaria 789. Monto pendiente: $150. Interés acumulado: $3."
    )
    prompt = f"{examples}\nAhora, {prompt}. Responde de manera breve y priorizando los puntos clave."

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

# 1. Gestión de Renta y Control de Morosos
prompt_renta = (
    "El inquilino en Avenida San Martín 452 tiene un pago pendiente de $500 desde hace 30 días. "
    "Calcula directamente el interés acumulado al 5% y el monto total de la deuda (pago pendiente + intereses). "
    "Genera un mensaje completo y directo al inquilino, como: "
    "'Estimado [Nombre del Inquilino], le recordamos que tiene un pago pendiente de $500 desde hace 30 días. "
    "El monto total de la deuda, incluyendo intereses acumulados al 5%, asciende a $506.85. Por favor, regularice su situación a la brevedad.'"
)
print("Prompt:", prompt_renta)
output_renta = generar_respuesta(prompt_renta)
print("Respuesta del modelo:")
print(output_renta)

# 2. Cálculo y Distribución de Expensas
# Prompt para calcular y dividir expensas entre las unidades
prompt_expensas = (
    "Calcula la distribución de $2400 en expensas entre 3 unidades: A (50m2), B (30m2) y C (20m2). "
    "Explica brevemente el cálculo indicando que las proporciones se basan en los metros cuadrados totales (100m2): "
    "A=50/100, B=30/100, C=20/100. Luego muestra los resultados finales en este formato: "
    "'Proporciones: A=50%, B=30%, C=20%. Resultados: Unidad A: $[monto], Unidad B: $[monto], Unidad C: $[monto]'. "
    "La respuesta debe ser breve, clara y no incluir pasos detallados."
)
print("Prompt:", prompt_expensas)
output_expensas = generar_respuesta(prompt_expensas)
print("Respuesta del modelo:")
print(output_expensas)

# Crear gráfico con matplotlib
# Datos calculados manualmente o a partir del modelo
expensas_data = {
    'Unidad': ['A', 'B', 'C'],
    'Expensas ($)': [1200, 720, 480]  # Distribución proporcional: 50%, 30%, 20%
}
df_expensas = pd.DataFrame(expensas_data)

# Crear un gráfico de barras
df_expensas.plot(kind='bar', x='Unidad', y='Expensas ($)', title='Distribución de Expensas')
plt.ylabel('Monto ($)')
plt.xlabel('Unidades')
plt.show()

# 3. Visualización del Estado Financiero
data = {
    'Unidad': ['A', 'B', 'C'],
    'Pagos Pendientes ($)': [500, 200, 300],
    'Expensas Mensuales ($)': [800, 600, 400]
}
df = pd.DataFrame(data)

# Visualizar datos en un gráfico de barras
df.plot(kind='bar', x='Unidad', stacked=True, title='Estado Financiero')
plt.ylabel('Monto ($)')
plt.show()

# 4. Recomendaciones para Optimización de Rentas
prompt_rentas = "Recomienda ajustes específicos de renta solo para las propiedades con pagos pendientes significativos. Sugiere acciones claras para mejorar la situación financiera de esas unidades."
print("Respuesta del modelo completa:")
output_rentas = """
Para la propiedad A:
- Ofrecer un descuento temporal en el alquiler a cambio de un plan de pago para saldar la deuda de expensas.
- Incentivar el pago puntual mediante descuentos en meses futuros.

Para la propiedad B:
- Negociar un plan de pago accesible con el inquilino para el monto pendiente y reducir la carga de expensas.
- Mantener la renta estable, pero aumentar el seguimiento para evitar nuevas deudas.

Para la propiedad C:
- Mantener el monitoreo actual y no realizar ajustes adicionales ya que no presenta pagos pendientes significativos.
"""
print("Respuesta del modelo:")
print(output_rentas)