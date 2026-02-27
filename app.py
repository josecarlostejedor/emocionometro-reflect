import streamlit as st
import pandas as pd
import sqlite3
import os
import base64

# 1. Configuración de la página
st.set_page_config(
    page_title="Emocionómetro EF",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Maestro: Calca el diseño de la Preview sobre Streamlit
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Espectacular con Blobs Animados */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at 5% 5%, rgba(0, 174, 239, 0.15) 0%, transparent 30%),
            radial-gradient(circle at 95% 20%, rgba(236, 0, 140, 0.15) 0%, transparent 30%),
            radial-gradient(circle at 15% 90%, rgba(141, 198, 63, 0.15) 0%, transparent 30%),
            radial-gradient(circle at 85% 85%, rgba(249, 212, 35, 0.15) 0%, transparent 30%) !important;
        background-attachment: fixed !important;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {padding: 3rem 6rem !important;}

    /* Tipografía Global */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif !important;
        color: #1A1A1A !important;
    }

    /* Títulos Estilo Preview */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(3rem, 7vw, 5.5rem);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        line-height: 0.85;
        color: #2D2D2D;
        margin: 0;
    }

    .event-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2D2D2D;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        color: #ec008c;
        font-size: 1.15rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }

    /* CONTENEDOR DE TARJETA VISUAL */
    .visual-card {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 2.5rem;
        height: 240px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        z-index: 1;
    }

    .visual-card i, .visual-card span.icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }

    .visual-card span.label {
        font-weight: 900;
        text-transform: uppercase;
        font-size: 1.2rem;
        letter-spacing: -0.02em;
    }

    /* BOTÓN DE STREAMLIT ENCIMA DE LA TARJETA (INVISIBLE) */
    div.stButton > button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 240px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10 !important;
        cursor: pointer !important;
        border-radius: 2.5rem !important;
    }

    /* Efecto Hover */
    .card-wrapper:hover .visual-card {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
        border-color: rgba(0,0,0,0.1);
    }

    /* Resultados Card */
    .results-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 3.5rem;
        padding: 4rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.08);
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
        st.markdown('<div style="width:140px;height:140px;background:#eee;border-radius:40px;"></div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="event-name">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown("<br>", unsafe_allow_html=True)
_, c_nav1, c_nav2 = st.columns([6, 1.3, 1.3])
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
    st.markdown('<h2 style="font-weight:900; font-size:2.8rem; margin: 3rem 0; letter-spacing:-0.04em; color:#2D2D2D;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    emociones = [
        {"id": "happy", "label": "Feliz", "icon": "😊", "color": "#FCD34D", "bg": "bg-amber-50"},
        {"id": "excited", "label": "Entusiasmado", "icon": "⚡", "color": "#60A5FA", "bg": "bg-blue-50"},
        {"id": "proud", "label": "Orgulloso", "icon": "🏆", "color": "#34D399", "bg": "bg-emerald-50"},
        {"id": "motivated", "label": "Motivado", "icon": "💪", "color": "#A78BFA", "bg": "bg-violet-50"},
        {"id": "loved", "label": "Agradecido", "icon": "❤️", "color": "#F472B6", "bg": "bg-pink-50"},
        {"id": "tired", "label": "Cansado", "icon": "🔥", "color": "#F87171", "bg": "bg-red-50"},
        {"id": "bored", "label": "Aburrido", "icon": "😐", "color": "#94A3B8", "bg": "bg-slate-50"},
        {"id": "sad", "label": "Triste", "icon": "😢", "color": "#64748B", "bg": "bg-indigo-50"},
    ]

    cols = st.columns(4)
    for i, emo in enumerate(emociones):
        with cols[i % 4]:
            st.markdown(f'<div class="card-wrapper">', unsafe_allow_html=True)
            # 1. La tarjeta visual (lo que se ve)
            st.markdown(f"""
                <div class="visual-card {emo['bg']}">
                    <span class="icon">{emo['icon']}</span>
                    <span class="label" style="color: {emo['color']}">{emo['label']}</span>
                </div>
            """, unsafe_allow_html=True)
            # 2. El botón real (invisible pero encima de la tarjeta)
            if st.button(emo['label'], key=f"v_{emo['id']}"):
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
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4rem;">
                <h2 style="font-weight:900; font-size:3.8rem; margin:0; letter-spacing:-0.05em; color:#2D2D2D;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:0.8rem 2.5rem; border-radius:1.8rem; font-weight:900; font-size:2rem;">
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
                    <div style="flex:1; background:rgba(0,0,0,0.06); height:16px; border-radius:10px; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #ec008c, #00aeef); width:{pct}%; height:100%;"></div>
                    </div>
                    <div style="font-weight:900; width:70px; font-size:1.4rem; color:#2D2D2D; text-align:right;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:1.8rem; padding:6rem; color:#2D2D2D;'>Aún no hay votos. ¡Sé el primero!</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Administración
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🛠️ CONFIGURACIÓN"):
    pwd = st.text_input("Contraseña de administrador", type="password")
    if pwd == "1234":
        if st.button("⚠️ REINICIAR MARCADOR"):
            reset_db()
            st.rerun()

# 9. Footer
st.markdown(f"""
<div style="text-align:center; padding:6rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:6rem; font-size:0.9rem; font-weight:800; text-transform:uppercase; letter-spacing:0.25em; opacity:0.4; color:#2D2D2D;">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión <br>
    <span style="color:#ec008c; font-size:0.8rem; letter-spacing:0.1em;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
