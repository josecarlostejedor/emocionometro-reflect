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

# 2. CSS DE ALTA PRECISIÓN (Garantiza uniformidad y tamaño)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Espectacular */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(0, 174, 239, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 10%, rgba(236, 0, 140, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 50% 90%, rgba(141, 198, 63, 0.08) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }

    /* Limpieza de Interfaz */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {padding: 3rem 6rem !important;}

    /* CABECERA Y LEMA GIGANTE */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 5rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.06em !important;
        line-height: 0.8 !important;
        color: #1A1A1A !important;
    }

    .slogan-container {
        font-family: 'Libre Baskerville', serif !important;
        font-style: italic !important;
        color: #1A1A1A !important;
        font-size: 2.5rem !important; /* LEMA MUCHO MÁS GRANDE */
        font-weight: 600 !important;
        margin: 2.5rem 0 !important;
        line-height: 1.2 !important;
        border-left: 10px solid #ec008c;
        padding-left: 2.5rem;
        max-width: 1100px;
    }

    /* --- BOTONES DE NAVEGACIÓN (Pills Elegantes) --- */
    .nav-container [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #1A1A1A !important;
        border-radius: 100px !important;
        padding: 0.8rem 3rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        color: #1A1A1A !important;
        width: 100% !important;
    }

    /* --- TARJETAS DE EMOCIÓN (FORZANDO UNIFORMIDAD) --- */
    /* Target a todos los botones dentro de la zona de emociones */
    .emotion-grid [data-testid="stButton"] {
        width: 100% !important;
    }

    .emotion-grid [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
        border-radius: 4rem !important;
        
        /* FORZAMOS EL MISMO TAMAÑO PARA TODOS */
        height: 320px !important; 
        width: 100% !important;
        min-width: 100% !important;
        
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.03) !important;
    }

    .emotion-grid [data-testid="stButton"] button:hover {
        transform: translateY(-15px) !important;
        background: white !important;
        box-shadow: 0 40px 70px rgba(0,0,0,0.1) !important;
        border-color: #ec008c !important;
    }

    /* ICONOS Y TEXTO (CENTRADOS Y GRANDES) */
    .emotion-grid [data-testid="stButton"] button div[data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        color: #1A1A1A !important;
        text-align: center !important;
        margin: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* TAMAÑO DEL ICONO (Emoji) */
    .emotion-grid [data-testid="stButton"] button p {
        font-size: 1.3rem !important; /* Tamaño del texto inferior */
        line-height: 1.2 !important;
    }

    /* Forzamos el tamaño del emoji usando el truco de la primera línea */
    .emotion-grid [data-testid="stButton"] button p::first-line {
        font-size: 7rem !important; /* ICONO GIGANTE */
        line-height: 1.4 !important;
    }

    /* Resultados Card */
    .results-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(30px);
        border-radius: 4rem;
        padding: 4rem;
        box-shadow: 0 50px 100px rgba(0, 0, 0, 0.08);
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
        st.markdown('<div style="width:160px;height:160px;background:#eee;border-radius:50px;"></div>', unsafe_allow_html=True)

with col_text:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:2rem; font-weight:700; margin:0; color:#4A4A4A;">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<div class="slogan-container">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</div>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown('<div class="nav-container">', unsafe_allow_html=True)
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
    st.markdown('<h2 style="font-weight:900; font-size:3.5rem; margin: 4rem 0 3rem 0; letter-spacing:-0.06em; color:#1A1A1A;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="emotion-grid">', unsafe_allow_html=True)
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
    
    color_map = {
        "feliz": "#FCD34D", "entusiasmado": "#FBBF24", "orgulloso": "#60A5FA",
        "motivado": "#34D399", "agradecido": "#F87171", "cansado": "#FB923C",
        "aburrido": "#94A3B8", "triste": "#818CF8"
    }

    st.markdown(f"""
        <div class="results-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5rem;">
                <h2 style="font-weight:900; font-size:4.5rem; margin:0; letter-spacing:-0.06em; color:#1A1A1A;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:1.2rem 3.5rem; border-radius:2.5rem; font-weight:900; font-size:2.5rem;">
                    TOTAL: {total}
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.bar_chart(df.set_index('emocion')['conteo'], color="#1A1A1A")
        
        emociones_ref = {e['id']: e['label'] for e in emociones}

        for _, row in df.iterrows():
            eid = row['emocion']
            label = emociones_ref.get(eid, eid).upper()
            color = color_map.get(eid, "#1A1A1A")
            pct = int((row['conteo'] / total) * 100)
            
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:2.5rem; margin-bottom:2rem; background:rgba(255,255,255,0.5); padding:2rem 3rem; border-radius:3rem; border: 1px solid rgba(0,0,0,0.05);">
                    <div style="font-weight:900; font-size:1.4rem; width:240px; letter-spacing:0.05em; color:#1A1A1A;">{label}</div>
                    <div style="flex:1; background:rgba(0,0,0,0.06); height:24px; border-radius:15px; overflow:hidden;">
                        <div style="background:{color}; width:{pct}%; height:100%; border-radius:15px;"></div>
                    </div>
                    <div style="font-weight:900; width:100px; font-size:1.8rem; color:#1A1A1A; text-align:right;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:2.5rem; padding:10rem;'>Aún no hay votos. ¡Sé el primero!</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Administración
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🛠️ CONFIGURACIÓN"):
    pwd = st.text_input("Contraseña de administrador", type="password")
    if pwd == "1234":
        if st.button("⚠️ REINICIAR MARCADOR"):
            reset_db()
            st.rerun()

# 9. Footer
st.markdown(f"""
<div style="text-align:center; padding:10rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:10rem; font-size:1.1rem; font-weight:800; text-transform:uppercase; letter-spacing:0.4em; opacity:0.4; color:#1A1A1A;">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión <br>
    <span style="color:#4A4A4A; font-size:1rem;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
