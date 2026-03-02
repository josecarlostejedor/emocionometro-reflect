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

# 2. CSS Maestro: Específico y Elegante (Evita solapamientos)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Espectacular con Blobs Animados */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at 5% 5%, rgba(0, 174, 239, 0.1) 0%, transparent 35%),
            radial-gradient(circle at 95% 20%, rgba(236, 0, 140, 0.1) 0%, transparent 35%),
            radial-gradient(circle at 15% 90%, rgba(141, 198, 63, 0.1) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(249, 212, 35, 0.1) 0%, transparent 35%) !important;
        background-attachment: fixed !important;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Contenedor principal */
    .block-container {
        padding: 3rem 5rem !important;
        max-width: 1200px !important;
    }

    /* Tipografía */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(3rem, 8vw, 5.5rem);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        line-height: 0.85;
        color: #2D2D2D;
        margin-bottom: 0.5rem;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        color: #ec008c;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    /* --- ESTILO ESPECÍFICO PARA BOTONES DE EMOCIÓN --- */
    /* Usamos un ID de contenedor para no romper el resto de la app */
    #emotion-zone [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-radius: 2.5rem !important;
        height: 220px !important;
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02) !important;
        padding: 2rem !important;
        margin-bottom: 1rem !important;
    }

    #emotion-zone [data-testid="stButton"] button:hover {
        transform: translateY(-10px) !important;
        background: white !important;
        box-shadow: 0 25px 50px rgba(0,0,0,0.1) !important;
        border-color: rgba(0,0,0,0.1) !important;
    }

    #emotion-zone [data-testid="stButton"] button p {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        font-size: 1.2rem !important;
        letter-spacing: -0.02em !important;
        color: #1A1A1A !important;
        margin-top: 10px !important;
    }

    /* --- FIX PARA EL EXPANDER (CONFIGURACIÓN) --- */
    /* Aseguramos que el expander se vea normal y no herede estilos locos */
    .stExpander {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 1rem !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        margin-top: 4rem !important;
    }
    
    .stExpander [data-testid="stExpanderHeader"] {
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-size: 0.8rem !important;
    }

    /* Resultados Card */
    .results-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 3rem;
        padding: 3.5rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
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
col_l, col_r = st.columns([1, 4])
with col_l:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown('<div style="width:120px;height:120px;background:rgba(0,0,0,0.05);border-radius:30px;display:flex;align-items:center;justify-content:center;font-size:0.7rem;color:gray;">LOGO</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.5rem; font-weight:700; margin:0; opacity:0.8;">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown("<br>", unsafe_allow_html=True)
_, c_nav1, c_nav2 = st.columns([6, 1.5, 1.5])
with c_nav1:
    if st.button("📊 RESULTADOS", key="nav_res"): 
        st.session_state.page = 'resultados'
        st.rerun()
with c_nav2:
    if st.button("🗳️ VOTAR", key="nav_vot"): 
        st.session_state.page = 'votar'
        st.rerun()

# 6. VISTA: VOTACIÓN
if st.session_state.page == 'votar':
    st.markdown('<h2 style="font-weight:900; font-size:2.5rem; margin-bottom:2.5rem; letter-spacing:-0.04em; color:#2D2D2D;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    # ENCAPSULAMOS EN UN DIV PARA EL CSS ESPECÍFICO
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
            if st.button(f"{emo['icon']} {emo['label']}", key=f"v_{emo['id']}"):
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
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3rem;">
                <h2 style="font-weight:900; font-size:3.5rem; margin:0; letter-spacing:-0.05em; color:#2D2D2D;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:0.8rem 2.5rem; border-radius:1.5rem; font-weight:900; font-size:1.8rem;">
                    TOTAL: {total}
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.bar_chart(df.set_index('emocion')['conteo'], color="#ec008c")
        for _, row in df.iterrows():
            pct = int((row['conteo'] / total) * 100)
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1.5rem; margin-bottom:1.2rem; background:rgba(0,0,0,0.03); padding:1.2rem; border-radius:2rem; border: 1px solid rgba(0,0,0,0.05);">
                    <div style="font-weight:900; font-size:1.1rem; width:180px; text-transform:uppercase; letter-spacing:0.05em; color:#2D2D2D;">{row['emocion']}</div>
                    <div style="flex:1; background:rgba(0,0,0,0.05); height:14px; border-radius:10px; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #ec008c, #00aeef); width:{pct}%; height:100%;"></div>
                    </div>
                    <div style="font-weight:900; width:60px; font-size:1.2rem; color:#2D2D2D; text-align:right;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:1.5rem; padding:4rem; color:#2D2D2D;'>Aún no hay votos. ¡Sé el primero!</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Administración (Corregido para que no se pise)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🛠️ CONFIGURACIÓN"):
    pwd = st.text_input("Contraseña de administrador", type="password")
    if pwd == "1234":
        if st.button("⚠️ REINICIAR MARCADOR"):
            reset_db()
            st.rerun()

# 9. Footer
st.markdown(f"""
<div style="text-align:center; padding:5rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:5rem; font-size:0.85rem; font-weight:800; text-transform:uppercase; letter-spacing:0.2em; opacity:0.4; color:#2D2D2D;">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión <br>
    <span style="color:#ec008c; font-size:0.75rem;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
