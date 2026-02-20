import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Emociómetro – Día de la EF en la Calle",
    layout="wide"
)

st.title("🏃‍♂️ Emociómetro del Día de la Educación Física en la Calle")

st.markdown("""
Bienvenido/a.

1. Vota tu emoción.
2. Te redirigirá automáticamente al marcador general.
3. Si no funciona, pulsa el botón de **Ver marcador general**.

¡Gracias por participar!  
""")

# Cargar el archivo HTML local
with open("emocionometro.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=800, scrolling=True)