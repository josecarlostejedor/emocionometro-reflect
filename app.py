import streamlit as st
import pandas as pd
import sqlite3
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Emocionómetro EF",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS NUCLEAR: Forzando el diseño sobre Streamlit
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Espectacular */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(0, 174, 239, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 90% 10%, rgba(236, 0, 140, 0.05) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {padding: 3rem 6rem !important;}

    /* Títulos y LEMA GIGANTE */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.06em !important;
        color: #1A1A1A !important;
        margin: 0 !important;
    }

    .slogan-box {
        font-family: 'Libre Baskerville', serif !important;
        font-style: italic !important;
        color: #1A1A1A !important;
        font-size: 2.8rem !important; /* LEMA MUCHO MÁS GRANDE */
        font-weight: 400 !important;
        margin: 2.5rem 0 5rem 0 !important;
        line-height: 1.1 !important;
        opacity: 0.95;
    }

    /* --- NAVEGACIÓN --- */
    .nav-zone [data-testid="stButton"] button {
        background: white !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        border-radius: 15px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        color: #1A1A1A !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }

    /* --- TARJETAS DE EMOCIÓN (ESTILO BENTO GRID) --- */
    /* Forzamos que todos los botones de la zona de emociones sean iguales */
    #emotion-zone [data-testid="stButton"] {
        width: 100% !important;
    }

    #emotion-zone [data-testid="stButton"] button {
        border: none !important;
        border-radius: 3rem !important;
        height: 320px !important; /* Altura fija y grande */
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        padding: 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03) !important;
    }

    #emotion-zone [data-testid="stButton"] button:hover {
        transform: translateY(-15px) scale(1.02) !important;
        box-shadow: 0 30px 60px rgba(0,0,0,0.1) !important;
    }

    /* Texto e iconos dentro de la tarjeta */
    #emotion-zone [data-testid="stButton"] button div[data-testid="stMarkdownContainer"] p {
        font-family: 'Libre Baskerville', serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-size: 1.5rem !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ICONOS GIGANTES (Forzados) */
    #emotion-zone [data-testid="stButton"] button p::first-line {
        font-size: 7rem !important; /* ICONOS REALMENTE GRANDES */
        line-height: 1.4 !important;
    }

    /* COLORES DE LAS TARJETAS (Asignación por orden) */
    #emotion-zone div[data-testid="column"]:nth-child(1) button { background: #FFFBEB !important; color: #D97706 !important; }
    #emotion-zone div[data-testid="column"]:nth-child(2) button { background: #EFF6FF !important; color: #2563EB !important; }
    #emotion-zone div[data-testid="column"]:nth-child(3) button { background: #F0FDF4 !important; color: #16A34A !important; }
    #emotion-zone div[data-testid="column"]:nth-child(4) button { background: #F5F3FF !important; color: #7C3AED !important; }
    
    /* Segunda fila (Streamlit las numera globalmente en el grid) */
    #emotion-zone div[data-testid="column"]:nth-child(5) button { background: #FDF2F8 !important; color: #DB2777 !important; }
    #emotion-zone div[data-testid="column"]:nth-child(6) button { background: #FEF2F2 !important; color: #DC2626 !important; }
    #emotion-zone div[data-testid="column"]:nth-child(7) button { background: #F8FAFC !important; color: #475569 !important; }
    #emotion-zone div[data-testid="column"]:nth-child(8) button { background: #EEF2FF !important; color: #4F46E5 !important; }

    /* Resultados Card */
    .results-card {
        background: white;
        border-radius: 4rem;
        padding: 5rem;
        box-shadow: 0 40px 100px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. Base de Datos
def init_db():
    db_path = os.path.join(os.getcwd(), 'emocionometro.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS votos (emocion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    return conn

def add_vote(emo):
    conn = init_db()
    c = conn.cursor()
    c.execute('INSERT INTO votos (emocion) VALUES (?)', (emo,))
    conn.commit()
    conn.close()

def reset_db():
    conn = init_db()
    c = conn.cursor()
    c.execute('DELETE FROM votos')
    conn.commit()
    conn.close()

# 4. Cabecera
col_logo, col_text = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown('<div style="width:180px;height:180px;background:#eee;border-radius:50px;"></div>', unsafe_allow_html=True)

with col_text:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:2.2rem; font-weight:700; color:#4A4A4A; margin:0;">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<div class="slogan-box">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</div>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown('<div class="nav-zone">', unsafe_allow_html=True)
_, c_nav1, c_nav2 = st.columns([6, 1.8, 1.8])
with c_nav1:
    if st.button("📊 RESULTADOS", key="nav_res"): 
        st.session_state.page = 'resultados'
        st.rerun()
with c_nav2:
    if st.button("🗳️ VOTAR", key="nav_vot"): 
        st.session_state.page = 'votar'
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 6. VISTA: VOTACIÓN
if st.session_state.page == 'votar':
    st.markdown('<h2 style="font-weight:900; font-size:3.5rem; margin: 3rem 0; letter-spacing:-0.06em; color:#1A1A1A;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    # Contenedor ID para el CSS Nuclear
    st.markdown('<div id="emotion-zone">', unsafe_allow_html=True)
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
            # El salto de línea \n es vital para que el CSS separe icono de texto
            if st.button(f"{emo['icon']}\n{emo['label']}", key=f"v_{emo['id']}"):
                add_vote(emo['id'])
                st.balloons()
                st.session_state.page = 'resultados'
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 7. VISTA: RESULTADOS
else:
    conn = init_db()
    df = pd.read_sql_query("SELECT emocion, COUNT(*) as conteo FROM votos GROUP BY emocion", conn)
    total = df['conteo'].sum() if not df.empty else 0
    
    st.markdown(f"""
        <div class="results-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5rem;">
                <h2 style="font-weight:900; font-size:4.5rem; margin:0; letter-spacing:-0.07em; color:#1A1A1A;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:1.2rem 4rem; border-radius:2.5rem; font-weight:900; font-size:2.8rem;">
                    TOTAL: {total}
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.bar_chart(df.set_index('emocion')['conteo'], color="#1A1A1A")
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:2.5rem; padding:10rem;'>Aún no hay votos.</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Administración
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🛠️ CONFIGURACIÓN"):
    pwd = st.text_input("Contraseña", type="password")
    if pwd == "1234":
        if st.button("⚠️ REINICIAR"):
            reset_db()
            st.rerun()

# 9. Footer
st.markdown(f"""
<div style="text-align:center; padding:10rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:10rem; font-size:1.1rem; font-weight:800; text-transform:uppercase; letter-spacing:0.4em; opacity:0.4; color:#1A1A1A;">
    © 2026 Día de la Educación Física en la Calle <br>
    <span style="color:#4A4A4A; font-size:1rem;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
