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

# 2. CSS MAESTRO: Elegancia de Preview en Streamlit
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo con Blobs Animados */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at 5% 5%, rgba(0, 174, 239, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 95% 20%, rgba(236, 0, 140, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 15% 90%, rgba(141, 198, 63, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 85% 85%, rgba(249, 212, 35, 0.08) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    .block-container {padding: 3rem 6rem !important;}

    /* Títulos y Lema */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(3rem, 7vw, 5rem);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        line-height: 0.85;
        color: #1A1A1A;
        margin: 0;
    }

    .event-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4A4A4A;
        margin-top: 0.5rem;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        color: #2D2D2D;
        font-size: 1.6rem; /* LEMA MÁS GRANDE */
        font-weight: 500;
        margin-top: 1rem;
        line-height: 1.4;
    }

    /* --- BOTONES DE NAVEGACIÓN (Elegantes) --- */
    .nav-zone [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 100px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        color: #1A1A1A !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .nav-zone [data-testid="stButton"] button:hover {
        background: #1A1A1A !important;
        color: white !important;
        transform: translateY(-2px);
    }

    /* --- TARJETAS DE EMOCIÓN (Botones Reales Estilizados) --- */
    .emotion-zone [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 3rem !important;
        height: 260px !important; /* ALTURA FIJA PARA UNIFORMIDAD */
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02) !important;
        padding: 2rem !important;
    }

    .emotion-zone [data-testid="stButton"] button:hover {
        transform: translateY(-12px) !important;
        background: white !important;
        box-shadow: 0 30px 60px rgba(0,0,0,0.08) !important;
        border-color: rgba(0,0,0,0.05) !important;
    }

    /* Iconos (Emojis) GIGANTES y Texto */
    .emotion-zone [data-testid="stButton"] button p {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.02em !important;
        color: #1A1A1A !important;
        line-height: 1.1 !important;
        white-space: pre-line !important;
    }

    /* Truco para el tamaño del Emoji */
    .emotion-zone [data-testid="stButton"] button p::first-line {
        font-size: 5rem !important; /* ICONOS GIGANTES */
    }
    
    .emotion-zone [data-testid="stButton"] button p {
        font-size: 1.2rem !important;
    }

    /* Resultados */
    .results-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(25px);
        border-radius: 4rem;
        padding: 4rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.06);
    }

    /* Fix Expander */
    .stExpander {
        border: none !important;
        background: rgba(0,0,0,0.02) !important;
        border-radius: 1.5rem !important;
        margin-top: 4rem !important;
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
        st.markdown('<div style="width:140px;height:140px;background:#eee;border-radius:40px;"></div>', unsafe_allow_html=True)

with col_text:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="event-name">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown('<div class="nav-zone">', unsafe_allow_html=True)
_, c_nav1, c_nav2 = st.columns([6, 1.5, 1.5])
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
    st.markdown('<h2 style="font-weight:900; font-size:3rem; margin: 3rem 0; letter-spacing:-0.05em; color:#1A1A1A;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="emotion-zone">', unsafe_allow_html=True)
    emociones = [
        {"id": "feliz", "label": "Feliz", "icon": "😊", "color": "#FBBF24"},
        {"id": "entusiasmado", "label": "Entusiasmado", "icon": "⚡", "color": "#F59E0B"},
        {"id": "orgulloso", "label": "Orgulloso", "icon": "🏆", "color": "#3B82F6"},
        {"id": "motivado", "label": "Motivado", "icon": "💪", "color": "#10B981"},
        {"id": "agradecido", "label": "Agradecido", "icon": "❤️", "color": "#EF4444"},
        {"id": "cansado", "label": "Cansado", "icon": "🔥", "color": "#F97316"},
        {"id": "aburrido", "label": "Aburrido", "icon": "😐", "color": "#64748B"},
        {"id": "triste", "label": "Triste", "icon": "😢", "color": "#6366F1"},
    ]

    cols = st.columns(4)
    for i, emo in enumerate(emociones):
        with cols[i % 4]:
            # Usamos salto de línea para separar emoji de texto
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
    
    # Colores elegantes y variados para los resultados
    color_map = {
        "feliz": "#FCD34D", "entusiasmado": "#FBBF24", "orgulloso": "#60A5FA",
        "motivado": "#34D399", "agradecido": "#F87171", "cansado": "#FB923C",
        "aburrido": "#94A3B8", "triste": "#818CF8"
    }

    st.markdown(f"""
        <div class="results-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4rem;">
                <h2 style="font-weight:900; font-size:4rem; margin:0; letter-spacing:-0.05em; color:#1A1A1A;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:1rem 3rem; border-radius:2rem; font-weight:900; font-size:2.2rem;">
                    TOTAL: {total}
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.bar_chart(df.set_index('emocion')['conteo'], color="#1A1A1A")
        
        # Referencia para labels bonitos
        emociones_ref = {e['id']: e['label'] for e in [
            {"id": "feliz", "label": "Feliz"}, {"id": "entusiasmado", "label": "Entusiasmado"},
            {"id": "orgulloso", "label": "Orgulloso"}, {"id": "motivado", "label": "Motivado"},
            {"id": "agradecido", "label": "Agradecido"}, {"id": "cansado", "label": "Cansado"},
            {"id": "aburrido", "label": "Aburrido"}, {"id": "triste", "label": "Triste"}
        ]}

        for _, row in df.iterrows():
            eid = row['emocion']
            label = emociones_ref.get(eid, eid).upper()
            color = color_map.get(eid, "#1A1A1A")
            pct = int((row['conteo'] / total) * 100)
            
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:2rem; margin-bottom:1.5rem; background:rgba(255,255,255,0.4); padding:1.5rem 2.5rem; border-radius:2.5rem; border: 1px solid rgba(0,0,0,0.05);">
                    <div style="font-weight:900; font-size:1.2rem; width:220px; letter-spacing:0.05em; color:#1A1A1A;">{label}</div>
                    <div style="flex:1; background:rgba(0,0,0,0.06); height:20px; border-radius:12px; overflow:hidden;">
                        <div style="background:{color}; width:{pct}%; height:100%; border-radius:12px;"></div>
                    </div>
                    <div style="font-weight:900; width:90px; font-size:1.6rem; color:#1A1A1A; text-align:right;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:2rem; padding:8rem;'>Aún no hay votos. ¡Sé el primero!</p>", unsafe_allow_html=True)
    
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
<div style="text-align:center; padding:8rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:8rem; font-size:1rem; font-weight:800; text-transform:uppercase; letter-spacing:0.3em; opacity:0.4; color:#1A1A1A;">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión <br>
    <span style="color:#4A4A4A; font-size:0.9rem;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
