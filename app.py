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

# 2. CSS Maestro (Mantiene el diseño de la preview pero hace que los botones funcionen)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Espectacular */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at 5% 5%, rgba(0, 174, 239, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 95% 20%, rgba(236, 0, 140, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 15% 90%, rgba(141, 198, 63, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 85% 85%, rgba(249, 212, 35, 0.1) 0%, transparent 30%) !important;
        background-attachment: fixed !important;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {padding-top: 2rem !important;}

    /* Estilo de las Tarjetas (Visual) */
    .emotion-card {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 2.5rem;
        padding: 3rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 1;
    }

    /* Botón Invisible de Streamlit (Funcional) */
    div.stButton > button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 220px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10 !important;
        cursor: pointer !important;
        border-radius: 2.5rem !important;
    }

    /* Efecto Hover en la tarjeta cuando el botón tiene el foco */
    div.stButton:hover + .emotion-card, 
    .emotion-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        border-color: rgba(0,0,0,0.05);
    }

    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(3rem, 8vw, 5rem);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        line-height: 0.85;
        color: #2D2D2D;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        color: #ec008c;
        font-size: 1.1rem;
        opacity: 0.8;
    }

    .results-container {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 3rem;
        padding: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
    }
</style>

<!-- Cargar Iconos Lucide -->
<script src="https://unpkg.com/lucide@latest"></script>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        lucide.createIcons();
    });
</script>
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
        st.markdown('<div style="width:120px;height:120px;background:#eee;border-radius:30px;"></div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.5rem; font-weight:700; margin:0;">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown("<br>", unsafe_allow_html=True)
_, c_nav1, c_nav2 = st.columns([6, 1.2, 1.2])
with c_nav1:
    if st.button("📊 RESULTADOS", key="nav_res"): st.session_state.page = 'resultados'
with c_nav2:
    if st.button("🗳️ VOTAR", key="nav_vot"): st.session_state.page = 'votar'

# 6. VISTA: VOTACIÓN
if st.session_state.page == 'votar':
    st.markdown('<h2 style="font-weight:900; font-size:2.5rem; margin-bottom:2.5rem; letter-spacing:-0.04em; color:#2D2D2D;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    emociones = [
        {"id": "happy", "label": "Feliz", "icon": "😊", "color": "#FCD34D", "bg": "bg-amber-50", "text": "text-amber-600"},
        {"id": "excited", "label": "Entusiasmado", "icon": "⚡", "color": "#60A5FA", "bg": "bg-blue-50", "text": "text-blue-600"},
        {"id": "proud", "label": "Orgulloso", "icon": "🏆", "color": "#34D399", "bg": "bg-emerald-50", "text": "text-emerald-600"},
        {"id": "motivated", "label": "Motivado", "icon": "💪", "color": "#A78BFA", "bg": "bg-violet-50", "text": "text-violet-600"},
        {"id": "loved", "label": "Agradecido", "icon": "❤️", "color": "#F472B6", "bg": "bg-pink-50", "text": "text-pink-600"},
        {"id": "tired", "label": "Cansado", "icon": "🔥", "color": "#F87171", "bg": "bg-red-50", "text": "text-red-600"},
        {"id": "bored", "label": "Aburrido", "icon": "😐", "color": "#94A3B8", "bg": "bg-slate-50", "text": "text-slate-600"},
        {"id": "sad", "label": "Triste", "icon": "😢", "color": "#64748B", "bg": "bg-indigo-50", "text": "text-indigo-600"},
    ]

    cols = st.columns(4)
    for i, emo in enumerate(emociones):
        with cols[i % 4]:
            # El botón de Streamlit es el que detecta el click (es invisible)
            if st.button(emo['label'], key=f"v_{emo['id']}"):
                add_vote(emo['id'])
                st.balloons()
                st.session_state.page = 'resultados'
                st.rerun()
            
            # La tarjeta visual (lo que el usuario ve)
            st.markdown(f"""
                <div class="emotion-card" style="margin-top: -220px; margin-bottom: 180px;">
                    <div style="font-size: 4rem; margin-bottom: 0.5rem;">{emo['icon']}</div>
                    <div style="font-weight: 900; text-transform: uppercase; font-size: 1.2rem; color: {emo['color']};">{emo['label']}</div>
                </div>
            """, unsafe_allow_html=True)

# 7. VISTA: RESULTADOS
else:
    conn = init_db()
    df = pd.read_sql_query("SELECT emocion, COUNT(*) as conteo FROM votos GROUP BY emocion", conn)
    total = df['conteo'].sum() if not df.empty else 0
    
    st.markdown(f"""
        <div class="results-container">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3rem;">
                <h2 style="font-weight:900; font-size:3.5rem; margin:0; letter-spacing:-0.05em; color:#2D2D2D;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:0.7rem 2rem; border-radius:1.5rem; font-weight:900; font-size:1.8rem;">
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
                    <div style="font-weight:900; font-size:1.1rem; width:160px; text-transform:uppercase; letter-spacing:0.05em;">{row['emocion']}</div>
                    <div style="flex:1; background:rgba(0,0,0,0.05); height:14px; border-radius:10px; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #ec008c, #00aeef); width:{pct}%; height:100%;"></div>
                    </div>
                    <div style="font-weight:900; width:60px; font-size:1.2rem;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:1.5rem; padding:4rem;'>Aún no hay votos. ¡Sé el primero!</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Administración
st.markdown("<br><br>", unsafe_allow_html=True)
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
    <span style="color:#ec008c">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
