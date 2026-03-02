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

# 2. CSS DE MÁXIMA PRIORIDAD (Nuclear)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700;900&display=swap');

    /* Fondo Limpio */
    .stApp { background-color: #FAFAFA !important; }

    /* Ocultar basura de Streamlit */
    header, footer, .stDeployButton {display:none !important;}
    .block-container {padding: 3rem 6rem !important;}

    /* TÍTULO GIGANTE */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 6rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: -0.05em !important;
        color: #1A1A1A !important;
        margin: 0 !important;
        line-height: 0.9 !important;
    }

    /* LEMA MAJESTUOSO (Mucho más grande y elegante) */
    .slogan-text {
        font-family: 'Libre Baskerville', serif !important;
        font-size: 3.5rem !important; 
        font-weight: 700 !important;
        line-height: 1.1 !important;
        color: #1A1A1A !important;
        margin: 2rem 0 5rem 0 !important;
        font-style: italic;
        border-left: 12px solid #ec008c;
        padding-left: 2.5rem;
    }

    /* --- TARJETAS DE EMOCIÓN (ESTILO BENTO GRID) --- */
    /* Forzamos que los botones de Streamlit se conviertan en tarjetas GIGANTES */
    div[data-testid="stButton"] button {
        height: 350px !important; /* Altura fija y grande */
        width: 100% !important;
        border-radius: 50px !important;
        border: none !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.04) !important;
        padding: 0 !important;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-20px) scale(1.02) !important;
        box-shadow: 0 40px 80px rgba(0,0,0,0.12) !important;
    }

    /* Texto e ICONOS GIGANTES dentro del botón */
    div[data-testid="stButton"] button p {
        font-family: 'Libre Baskerville', serif !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        font-size: 1.8rem !important;
        margin: 0 !important;
        line-height: 1 !important;
        text-align: center !important;
    }

    /* Forzar tamaño del emoji (primera línea del botón) */
    div[data-testid="stButton"] button p::first-line {
        font-size: 9rem !important; /* ICONOS REALMENTE GIGANTES */
        line-height: 1.5 !important;
    }

    /* ASIGNACIÓN DE COLORES PASTEL (Por posición de columna) */
    /* Fila 1 */
    div[data-testid="column"]:nth-of-type(1) button { background-color: #FFFBEB !important; color: #D97706 !important; }
    div[data-testid="column"]:nth-of-type(2) button { background-color: #EFF6FF !important; color: #2563EB !important; }
    div[data-testid="column"]:nth-of-type(3) button { background-color: #F0FDF4 !important; color: #16A34A !important; }
    div[data-testid="column"]:nth-of-type(4) button { background-color: #F5F3FF !important; color: #7C3AED !important; }
    /* Fila 2 */
    div[data-testid="column"]:nth-of-type(5) button { background-color: #FDF2F8 !important; color: #DB2777 !important; }
    div[data-testid="column"]:nth-of-type(6) button { background-color: #FEF2F2 !important; color: #DC2626 !important; }
    div[data-testid="column"]:nth-of-type(7) button { background-color: #F8FAFC !important; color: #475569 !important; }
    div[data-testid="column"]:nth-of-type(8) button { background-color: #EEF2FF !important; color: #4F46E5 !important; }

    /* Navegación Elegante (Pills) */
    .nav-zone div[data-testid="stButton"] button {
        height: auto !important;
        border-radius: 100px !important;
        border: 2px solid #1A1A1A !important;
        background: white !important;
        color: #1A1A1A !important;
        font-weight: 800 !important;
        padding: 0.8rem 3rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
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
        st.image("logo.png", width=220)
    else:
        st.markdown('<div style="width:220px;height:220px;background:#eee;border-radius:50px;"></div>', unsafe_allow_html=True)

with col_text:
    st.markdown('<h1 class="main-title">Emocionómetro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:2.2rem; font-weight:700; color:#4A4A4A; margin:0;">Día de la Educación Física en la Calle</p>', unsafe_allow_html=True)
    st.markdown('<div class="slogan-text">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</div>', unsafe_allow_html=True)

# 5. Navegación
if 'page' not in st.session_state:
    st.session_state.page = 'votar'

st.markdown('<div class="nav-zone">', unsafe_allow_html=True)
_, c_nav1, c_nav2 = st.columns([6, 2, 2])
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
    st.markdown('<h2 style="font-weight:900; font-size:4rem; margin: 4rem 0 3rem 0; letter-spacing:-0.06em; color:#1A1A1A;">¿Cómo te sientes hoy?</h2>', unsafe_allow_html=True)
    
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

# 7. VISTA: RESULTADOS
else:
    conn = init_db()
    df = pd.read_sql_query("SELECT emocion, COUNT(*) as conteo FROM votos GROUP BY emocion", conn)
    total = df['conteo'].sum() if not df.empty else 0
    
    st.markdown(f"""
        <div style="background:white; border-radius:4rem; padding:5rem; box-shadow:0 40px 100px rgba(0,0,0,0.08); border:1px solid rgba(0,0,0,0.05);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5rem;">
                <h2 style="font-weight:900; font-size:5rem; margin:0; letter-spacing:-0.07em; color:#1A1A1A;">Marcador General</h2>
                <div style="background:#1A1A1A; color:white; padding:1.5rem 4rem; border-radius:3rem; font-weight:900; font-size:3rem;">
                    TOTAL: {total}
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.bar_chart(df.set_index('emocion')['conteo'], color="#1A1A1A")
    else:
        st.markdown("<p style='text-align:center; opacity:0.4; font-size:3rem; padding:12rem;'>Aún no hay votos.</p>", unsafe_allow_html=True)
    
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
<div style="text-align:center; padding:12rem 2rem; border-top:1px solid rgba(0,0,0,0.05); margin-top:12rem; font-size:1.2rem; font-weight:800; text-transform:uppercase; letter-spacing:0.5em; opacity:0.4; color:#1A1A1A;">
    © 2026 Día de la Educación Física en la Calle <br>
    <span style="color:#4A4A4A; font-size:1.1rem;">(Dpto. de EF del IES Lucía de Medrano)</span>
</div>
""", unsafe_allow_html=True)
