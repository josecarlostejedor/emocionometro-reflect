import streamlit as st
import pandas as pd
import sqlite3
import time
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Emocionómetro EF",
    page_icon="🏃‍♂️",
    layout="wide"
)

# 2. Estilos CSS para mantener la estética "Elegante y Visual"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    .stApp {
        background-color: #FDFCFB;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 174, 239, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(236, 0, 140, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(141, 198, 63, 0.08) 0%, transparent 40%);
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -3px;
        color: #2D2D2D;
        font-size: 4.5rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .event-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #5A5A40;
        margin-bottom: 0.2rem;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        color: #ec008c;
        font-size: 1.1rem;
        opacity: 0.8;
        margin-bottom: 2rem;
    }

    /* Estilo de los botones de emoción */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0,0,0,0.1) !important;
        border-radius: 2rem !important;
        padding: 2rem 1rem !important;
        height: 180px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #1A1A1A !important;
    }

    div.stButton > button:hover {
        transform: translateY(-5px) !important;
        background-color: white !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1) !important;
        border-color: #ec008c !important;
    }

    .footer {
        text-align: center;
        padding: 3rem;
        border-top: 1px solid rgba(0,0,0,0.05);
        margin-top: 4rem;
        font-size: 0.85rem;
        font-weight: bold;
        opacity: 0.6;
    }
</style>
""", unsafe_allow_html=True)

# 3. Gestión de Base de Datos (SQLite)
def init_db():
    conn = sqlite3.connect('votos_ef.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS votos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, emocion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_vote(emocion):
    conn = sqlite3.connect('votos_ef.db')
    c = conn.cursor()
    c.execute("INSERT INTO votos (emocion) VALUES (?)", (emocion,))
    conn.commit()
    conn.close()

def get_results():
    conn = sqlite3.connect('votos_ef.db')
    df = pd.read_sql_query("SELECT emocion, COUNT(*) as conteo FROM votos GROUP BY emocion", conn)
    conn.close()
    return df

init_db()

# 4. Cabecera con Logo y Título
col_logo, col_text = st.columns([1, 4])

with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    else:
        st.info("Sube 'logo.png' a GitHub")

with col_text:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="event-name">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>', unsafe_allow_html=True)

# 5. Lógica de Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

col_n1, col_n2, col_n3 = st.columns([6, 1, 1])
with col_n2:
    if st.button("📊 Resultados"): st.session_state.page = 'resultados'
with col_n3:
    if st.button("🗳️ Votar"): st.session_state.page = 'votar'

# 6. VISTA: VOTACIÓN
if st.session_state.page == 'votar':
    st.markdown("### ¿Cómo te sientes después de la actividad?")
    
    emociones = [
        {"id": "feliz", "label": "Feliz", "icon": "😊"},
        {"id": "entusiasmado", "label": "Entusiasmado", "icon": "⚡"},
        {"id": "orgulloso", "label": "Orgulloso", "icon": "🏆"},
        {"id": "motivado", "label": "Motivado", "icon": "💪"},
        {"id": "agradecido", "label": "Agradecido", "icon": "❤️"},
        {"id": "cansado", "label": "Cansado", "icon": "🔥"},
        {"id": "aburrido", "label": "Aburrido", "icon": "😐"},
        {"id": "triste", "label": "Triste", "icon": "😢"},
    ]

    cols = st.columns(4)
    for i, emo in enumerate(emociones):
        with cols[i % 4]:
            if st.button(f"{emo['icon']}\n\n{emo['label']}", key=emo['id']):
                add_vote(emo['id'])
                st.balloons()
                st.session_state.page = 'resultados'
                st.rerun()

# 7. VISTA: RESULTADOS
else:
    df = get_results()
    total = df['conteo'].sum() if not df.empty else 0
    st.markdown(f"### Marcador en Tiempo Real (Total: {total} votos)")
    
    if not df.empty:
        # Gráfico atractivo
        st.bar_chart(df.set_index('emocion')['conteo'])
        
        # Lista detallada
        for _, row in df.iterrows():
            st.write(f"**{row['emocion'].capitalize()}**: {row['conteo']} votos")
    else:
        st.write("Esperando el primer voto...")

# 8. Pie de página
st.markdown("""
<div class="footer">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión. (Dpto. de EF del IES Lucía de Medrano)
</div>
""", unsafe_allow_html=True)