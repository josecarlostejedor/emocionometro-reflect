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
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.05em;
        line-height: 1;
        color: #2D2D2D;
        margin-bottom: 0.5rem;
        white-space: nowrap !important;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif;
        font-style: italic;
        color: #4A4A4A;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* --- ESTILO BASE PARA BOTONES (EMOCIONES) --- */
    [data-testid="stButton"] button {
        background: white !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 24px !important;
        height: 180px !important; /* Altura fija para igualdad absoluta */
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        padding: 2rem !important;
    }

    [data-testid="stButton"] button:hover {
        transform: translateY(-5px) !important;
        border-color: #2D2D2D !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.08) !important;
    }

    /* Estilo del texto en los botones */
    [data-testid="stButton"] button p {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #1A1A1A !important;
        line-height: 1 !important;
        white-space: pre-line !important;
        text-align: center !important;
        font-size: 0.9rem !important;
    }

    /* Emoji gigante (primera línea del botón) */
    [data-testid="stButton"] button p::first-line {
        font-size: 3.5rem !important;
        line-height: 1.5 !important;
    }

    /* --- NAVEGACIÓN (SOBREESCRIBIR ESTILO BASE) --- */
    .nav-container [data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.5) !important;
        height: auto !important;
        border-radius: 100px !important;
        padding: 0.5rem 2rem !important;
        flex-direction: row !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }

    .nav-container [data-testid="stButton"] button:hover {
        background: #2D2D2D !important;
        color: white !important;
        border-color: #2D2D2D !important;
    }

    /* --- CONFIGURACIÓN (SOBREESCRIBIR ESTILO BASE) --- */
    .stExpander [data-testid="stButton"] button {
        height: auto !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem 1rem !important;
        flex-direction: row !important;
    }

    /* --- FIX PARA EL EXPANDER --- */
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
        background: rgba(255, 255, 255, 0.75);
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
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
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
    st.markdown('<h2 style="font-weight:900; font-size:2.5rem; margin-bottom:2.5rem; letter-spacing:-0.04em; color:#2D2D2D;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
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

    # Usamos un grid de 2 columnas con espaciado controlado
    cols = st.columns(2, gap="large")
    for i, emo in enumerate(emociones):
        with cols[i % 2]:
            # El salto de línea es clave para el truco del CSS ::first-line
            if st.button(f"{emo['icon']}\n{emo['label']}", key=f"v_{emo['id']}", use_container_width=True):
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
        "feliz": "#FFD93D",
        "entusiasmado": "#FF8400",
        "orgulloso": "#4D96FF",
        "motivado": "#6BCB77",
        "agradecido": "#FF6B6B",
        "cansado": "#FF4C29",
        "aburrido": "#94A3B8",
        "triste": "#5F9DF7"
    }

    # Construir el HTML de resultados
    results_html = f"""<div class="results-card">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2.5rem; flex-wrap: wrap; gap: 1rem;">
<h2 style="font-weight:900; font-size:1.8rem; margin:0; letter-spacing:-0.05em; color:#2D2D2D; text-transform:uppercase;">Marcador General</h2>
<div style="background:#1A1A1A; color:white; padding:0.5rem 1.2rem; border-radius:1rem; font-weight:900; font-size:1.2rem;">
TOTAL: {total}
</div>
</div>
"""
    
    if not df.empty:
        emociones_ref = {
            "feliz": "Feliz", "entusiasmado": "Entusiasmado", "orgulloso": "Orgulloso",
            "motivado": "Motivado", "agradecido": "Agradecido", "cansado": "Cansado",
            "aburrido": "Aburrido", "triste": "Triste"
        }

        # Ordenar por conteo descendente para que sea más dinámico
        df_sorted = df.sort_values(by='conteo', ascending=False)

        for _, row in df_sorted.iterrows():
            emo_id = row['emocion']
            label = emociones_ref.get(emo_id, emo_id)
            color = color_map.get(emo_id, "#2D2D2D")
            pct = int((row['conteo'] / total) * 100) if total > 0 else 0
            
            results_html += f"""<div style="margin-bottom:1.5rem;">
<div style="display:flex; justify-content:space-between; margin-bottom:0.5rem; font-weight:800; font-size:0.85rem; text-transform:uppercase; color:#4A4A4A;">
<span>{label}</span>
<span>{pct}% ({row['conteo']})</span>
</div>
<div style="background:rgba(0,0,0,0.05); height:14px; border-radius:20px; overflow:hidden; border:1px solid rgba(0,0,0,0.02);">
<div style="background:{color}; width:{pct}%; height:100%; border-radius:20px; transition: width 1s ease-in-out;"></div>
</div>
</div>
"""
    else:
        results_html += "<p style='text-align:center; opacity:0.4; font-size:1.2rem; padding:3rem; color:#2D2D2D;'>Aún no hay votos. ¡Sé el primero!</p>"
    
    results_html += "</div>"
    st.markdown(results_html, unsafe_allow_html=True)

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
<div style="text-align:center; padding:5rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:5rem; font-size:0.85rem; font-weight:800; text-transform:uppercase; letter-spacing:0.2em; opacity:0.4; color:#2D2D2D;">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión <br>
    <span style="color:#4A4A4A; font-size:0.75rem;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
