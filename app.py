import streamlit as st
import pandas as pd
import sqlite3
import os
import time

# 1. Configuración de la página
st.set_page_config(
    page_title="Emocionómetro EF",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inyección de CSS Avanzado para calcar la Preview
st.markdown("""
<style>
    /* Importar Fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Dinámico con Blobs (Igual que la Preview) */
    .stApp {
        background-color: #FAFAFA !important;
        background-image: 
            radial-gradient(circle at -10% -10%, rgba(0, 174, 239, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 110% 20%, rgba(236, 0, 140, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 20% 110%, rgba(141, 198, 63, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 90%, rgba(249, 212, 35, 0.15) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }

    /* Reset de fuentes */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif !important;
        color: #1A1A1A !important;
    }

    /* Cabecera Elegante */
    .header-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 3rem;
    }

    .main-title {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.05em !important;
        line-height: 0.9 !important;
        margin: 0 !important;
        color: #2D2D2D !important;
    }

    .event-name {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #2D2D2D !important;
        margin-top: 0.5rem !important;
    }

    .slogan {
        font-family: 'Libre Baskerville', serif !important;
        font-style: italic !important;
        color: #ec008c !important;
        font-size: 1rem !important;
        opacity: 0.8;
    }

    /* Botones de Emoción (Glassmorphism) */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 2.5rem !important;
        padding: 3rem 1rem !important;
        height: 220px !important;
        width: 100% !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03) !important;
    }

    div.stButton > button:hover {
        transform: translateY(-10px) !important;
        background: rgba(255, 255, 255, 0.8) !important;
        border-color: rgba(0,0,0,0.1) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08) !important;
    }

    /* Iconos y Texto dentro de botones */
    .emo-label {
        display: block;
        font-size: 1.25rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-top: 1rem;
        letter-spacing: -0.02em;
    }

    .emo-icon {
        font-size: 3rem;
        display: block;
    }

    /* Contenedor de Resultados */
    .results-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 3rem;
        padding: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 4rem 2rem;
        border-top: 1px solid rgba(0,0,0,0.05);
        margin-top: 5rem;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.5;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# 3. Base de Datos Compartida
def init_db():
    # Usamos una ruta absoluta para asegurar persistencia en Streamlit Cloud
    db_path = os.path.join(os.getcwd(), 'votos_ef.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS votos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, emocion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()

def add_vote(emocion):
    c = conn.cursor()
    c.execute("INSERT INTO votos (emocion) VALUES (?)", (emocion,))
    conn.commit()

def get_results():
    return pd.read_sql_query("SELECT emocion, COUNT(*) as conteo FROM votos GROUP BY emocion", conn)

def reset_db():
    c = conn.cursor()
    c.execute("DELETE FROM votos")
    conn.commit()

# 4. Cabecera con Logo
col_l, col_r = st.columns([1, 4])
with col_l:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown('<div style="width:120px;height:120px;background:#eee;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:10px;text-align:center">Sube logo.png a GitHub</div>', unsafe_allow_html=True)

with col_r:
    st.markdown(f"""
        <div style="margin-top: 10px;">
            <h1 class="main-title">Emocionómetro</h1>
            <p class="event-name">Día de la Educación Física en la Calle</p>
            <p class="slogan">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>
        </div>
    """, unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
with c3:
    if st.button("📊 RESULTADOS", key="btn_res"): st.session_state.page = 'resultados'
with c4:
    if st.button("🗳️ VOTAR", key="btn_vot"): st.session_state.page = 'votar'

# 6. VISTA: VOTACIÓN
if st.session_state.page == 'votar':
    st.markdown('<h2 style="font-weight:800; font-size:2.5rem; margin-bottom:2rem; letter-spacing:-0.03em;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
    emociones = [
        {"id": "feliz", "label": "Feliz", "icon": "😊", "color": "#FCD34D"},
        {"id": "entusiasmado", "label": "Entusiasmado", "icon": "⚡", "color": "#60A5FA"},
        {"id": "orgulloso", "label": "Orgulloso", "icon": "🏆", "color": "#34D399"},
        {"id": "motivado", "label": "Motivado", "icon": "💪", "color": "#A78BFA"},
        {"id": "agradecido", "label": "Agradecido", "icon": "❤️", "color": "#F472B6"},
        {"id": "cansado", "label": "Cansado", "icon": "🔥", "color": "#F87171"},
        {"id": "aburrido", "label": "Aburrido", "icon": "😐", "color": "#94A3B8"},
        {"id": "triste", "label": "Triste", "icon": "😢", "color": "#64748B"},
    ]

    cols = st.columns(4)
    for i, emo in enumerate(emociones):
        with cols[i % 4]:
            # Usamos HTML dentro del botón para el estilo
            label_html = f'<span class="emo-icon">{emo["icon"]}</span><span class="emo-label" style="color:{emo["color"]}">{emo["label"]}</span>'
            if st.button(emo["label"], key=f"vote_{emo['id']}", help=f"Votar {emo['label']}"):
                add_vote(emo['id'])
                st.balloons()
                st.session_state.page = 'resultados'
                st.rerun()
            # Inyectamos el label visual sobre el botón de Streamlit
            st.markdown(f"""
                <div style="margin-top:-185px; text-align:center; pointer-events:none; margin-bottom:120px;">
                    {label_html}
                </div>
            """, unsafe_allow_html=True)

# 7. VISTA: RESULTADOS
else:
    df = get_results()
    total = df['conteo'].sum() if not df.empty else 0
    
    st.markdown(f"""
        <div class="results-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
                <h2 style="font-weight:800; font-size:3rem; margin:0; letter-spacing:-0.03em;">Marcador General</h2>
                <div style="background:black; color:white; padding:0.5rem 1.5rem; border-radius:1rem; font-weight:900; font-size:1.5rem;">
                    TOTAL: {total}
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Gráfico
        st.bar_chart(df.set_index('emocion')['conteo'], color="#ec008c")
        
        # Lista con porcentajes
        for _, row in df.iterrows():
            pct = int((row['conteo'] / total) * 100)
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem; background:rgba(0,0,0,0.03); padding:1rem; border-radius:1.5rem;">
                    <div style="font-weight:900; font-size:1.2rem; width:150px; text-transform:uppercase;">{row['emocion']}</div>
                    <div style="flex:1; background:rgba(0,0,0,0.05); height:12px; border-radius:10px; overflow:hidden;">
                        <div style="background:#ec008c; width:{pct}%; height:100%;"></div>
                    </div>
                    <div style="font-weight:900; width:50px;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; opacity:0.5;'>Aún no hay votos. ¡Sé el primero!</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Administración
with st.expander("🛠️ ADMIN"):
    pwd = st.text_input("Contraseña", type="password")
    if pwd == "1234":
        if st.button("REINICIAR TODO"):
            reset_db()
            st.rerun()

# 9. Footer
st.markdown("""
<div class="footer">
    © 2026 Día de la Educación Física en la Calle • Construido con Pasión. <br>
    <span style="color:#ec008c">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
