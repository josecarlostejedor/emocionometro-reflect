import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import os
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Emocionómetro EF", layout="wide", initial_sidebar_state="collapsed")

# --- BASE DE DATOS ---
def init_db():
    db_path = os.path.join(os.getcwd(), 'emocionometro.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS votos (emocion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    return conn

conn = init_db()

def add_vote(emo):
    c = conn.cursor()
    c.execute('INSERT INTO votos (emocion) VALUES (?)', (emo,))
    conn.commit()

def get_results_json():
    df = pd.read_sql_query('SELECT emocion, COUNT(*) as count FROM votos GROUP BY emocion', conn)
    return df.to_json(orient='records')

def reset_db():
    c = conn.cursor()
    c.execute('DELETE FROM votos')
    conn.commit()

# --- LÓGICA DE ESTADO ---
if 'voted' not in st.session_state:
    st.session_state.voted = False

# --- COMPONENTE UI ESPECTACULAR (HTML/CSS/JS) ---
def render_spectacular_ui():
    results = get_results_json()
    
    # Definición de emociones para el JS
    emociones_js = [
        {"id": "happy", "label": "Feliz", "icon": "smile", "color": "#FCD34D", "bg": "bg-amber-50", "text": "text-amber-600"},
        {"id": "excited", "label": "Entusiasmado", "icon": "zap", "color": "#60A5FA", "bg": "bg-blue-50", "text": "text-blue-600"},
        {"id": "proud", "label": "Orgulloso", "icon": "trophy", "color": "#34D399", "bg": "bg-emerald-50", "text": "text-emerald-600"},
        {"id": "motivated", "label": "Motivado", "icon": "dumbbell", "color": "#A78BFA", "bg": "bg-violet-50", "text": "text-violet-600"},
        {"id": "loved", "label": "Agradecido", "icon": "heart", "color": "#F472B6", "bg": "bg-pink-50", "text": "text-pink-600"},
        {"id": "tired", "label": "Cansado", "icon": "flame", "color": "#F87171", "bg": "bg-red-50", "text": "text-red-600"},
        {"id": "bored", "label": "Aburrido", "icon": "meh", "color": "#94A3B8", "bg": "bg-slate-50", "text": "text-slate-600"},
        {"id": "sad", "label": "Triste", "icon": "frown", "color": "#64748B", "bg": "bg-indigo-50", "text": "text-indigo-600"},
    ]

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Libre+Baskerville:ital,wght@1,400&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Inter', sans-serif; background: #FAFAFA; margin: 0; overflow-x: hidden; }}
            .glass {{ background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.5); }}
            .blob {{ position: fixed; border-radius: 50%; filter: blur(80px); opacity: 0.15; z-index: -1; animation: pulse 10s infinite alternate; }}
            @keyframes pulse {{ from {{ transform: scale(1); }} to {{ transform: scale(1.2); }} }}
            .card-btn {{ transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; }}
            .card-btn:hover {{ transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); background: white; }}
        </style>
    </head>
    <body>
        <!-- Blobs de fondo -->
        <div class="blob w-96 h-96 bg-cyan-400 -top-20 -left-20"></div>
        <div class="blob w-96 h-96 bg-magenta-400 top-1/2 -right-20" style="background-color: #ec008c;"></div>
        <div class="blob w-80 h-80 bg-lime-400 bottom-0 left-1/4"></div>

        <div class="max-w-6xl mx-auto p-6 md:p-10">
            <!-- Header -->
            <header class="flex flex-col md:flex-row items-center justify-between gap-8 mb-12 pb-10 border-b border-black/5">
                <div class="flex flex-col md:flex-row items-center gap-6">
                    <img src="./logo.png" class="w-24 h-24 md:w-32 md:h-32 object-contain" onerror="this.src='https://placehold.co/200x200?text=LOGO'">
                    <div class="text-center md:text-left">
                        <h1 class="text-5xl md:text-7xl font-black uppercase tracking-tighter leading-none text-gray-800">Emocionómetro</h1>
                        <p class="text-xl font-bold text-gray-600 mt-2">Día de la Educación Física en la Calle</p>
                        <p class="italic text-pink-600 font-medium">"Moviendo cuerpos, conectando mentes. La calle es salud mental en movimiento"</p>
                    </div>
                </div>
            </header>

            <!-- Grid de Votación -->
            <div id="vote-grid" class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                { "".join([f'''
                <div onclick="vote('{e['id']}')" class="card-btn glass {e['bg']} p-8 rounded-[2.5rem] flex flex-col items-center justify-center text-center">
                    <i data-lucide="{e['icon']}" class="w-12 h-12 mb-4 {e['text']}"></i>
                    <span class="text-xl font-black uppercase tracking-tight">{e['label']}</span>
                </div>
                ''' for e in emociones_js]) }
            </div>
        </div>

        <script>
            lucide.createIcons();
            function vote(id) {{
                // Enviamos el ID de la emoción a Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: id
                }}, '*');
            }}
        </script>
    </body>
    </html>
    """
    return components.html(html_code, height=900, scrolling=False)

# --- RENDERIZADO ---

# Capturamos el voto desde el componente HTML
voto_detectado = render_spectacular_ui()

if voto_detectado:
    add_vote(voto_detectado)
    st.balloons()
    st.session_state.voted = True
    st.rerun()

# Panel de Resultados (se muestra debajo o en otra página)
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Marcador en Tiempo Real")
    df = pd.read_sql_query('SELECT emocion, COUNT(*) as conteo FROM votos GROUP BY emocion', conn)
    if not df.empty:
        st.bar_chart(df.set_index('emocion'), color="#ec008c")
    else:
        st.info("Esperando votos...")

with col2:
    with st.expander("🛠️ Admin"):
        pwd = st.text_input("Contraseña", type="password")
        if pwd == "1234":
            if st.button("REINICIAR TODO"):
                reset_db()
                st.rerun()

st.markdown(f"""
    <div style="text-align:center; padding:2rem; opacity:0.5; font-weight:bold;">
        © 2026 Día de la Educación Física en la Calle • (Dpto. de EF del IES Lucía de Medrano)
    </div>
""", unsafe_allow_html=True)
