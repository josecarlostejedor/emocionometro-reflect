import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import os
import json
import time
import hashlib

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Emocionómetro EF", layout="wide", initial_sidebar_state="collapsed")

# Eliminamos márgenes, cabeceras y pies de página de Streamlit
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display:none;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        iframe {border: none !important; width: 100%; height: 100vh;}
        body { background-color: #FAFAFA; }
        /* Compactar el formulario admin si se usa */
        .admin-box { position: fixed; bottom: 16px; right: 16px; z-index: 9999; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIG ---
DB_PATH = os.path.join(os.getcwd(), 'emocionometro.db')
# Configura la contraseña admin por variable de entorno; por ejemplo: export EMOCIONOMETRO_ADMIN_PWD="1234"
ADMIN_PASSWORD_PLAIN = os.getenv("EMOCIONOMETRO_ADMIN_PWD", "")
# Si prefieres usar hash, configura EMOCIONOMETRO_ADMIN_PWD_HASH. Si existe, tiene prioridad.
ADMIN_PASSWORD_HASH = os.getenv("EMOCIONOMETRO_ADMIN_PWD_HASH", "")

def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def _admin_ok(pwd: str) -> bool:
    if ADMIN_PASSWORD_HASH:
        return _hash(pwd) == ADMIN_PASSWORD_HASH
    # fallback a texto plano si no hay hash configurado
    return pwd == ADMIN_PASSWORD_PLAIN and pwd != ""

# --- BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=5)
    c = conn.cursor()
    # Modo WAL mejora concurrencia
    try:
        c.execute('PRAGMA journal_mode=WAL;')
        c.execute('PRAGMA synchronous=NORMAL;')
    except Exception:
        pass
    c.execute('CREATE TABLE IF NOT EXISTS votos (emocion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

def add_vote(emo):
    # Retries simples por si hay bloqueo
    for _ in range(3):
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=5)
            c = conn.cursor()
            c.execute('INSERT INTO votos (emocion) VALUES (?)', (emo,))
            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError:
            time.sleep(0.1)
    # último intento sin capturar
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=5)
    c = conn.cursor()
    c.execute('INSERT INTO votos (emocion) VALUES (?)', (emo,))
    conn.commit()
    conn.close()

def get_results_data():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=5)
    # Llevamos el ORDER BY para hacerlo más legible
    df = pd.read_sql_query('SELECT emocion, COUNT(*) as count FROM votos GROUP BY emocion ORDER BY count DESC', conn)
    conn.close()
    return df.to_dict(orient='records')

def reset_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=5)
    c = conn.cursor()
    c.execute('DELETE FROM votos')
    conn.commit()
    conn.close()

init_db()

# --- AUTORREFRESH OPCIONAL (cada 10 s en página de resultados) ---
# Desactiva si no lo quieres: set autorefresh_interval = 0
autorefresh_interval = 0
if autorefresh_interval and st.query_params.get("page", "vote") == "results":
    st.experimental_rerun  # keep reference
    st_autorefresh = st.experimental_singleton(lambda: None)  # compat placeholder
    st.runtime.legacy_caching.clear_cache()  # no-op; placeholder
    st.experimental_set_query_params = st.query_params.update  # alias

# --- LÓGICA DE COMUNICACIÓN ---
query_params = st.query_params

# Gestionar votos desde query param seguro
if "vote" in query_params:
    # Validar que es una emoción válida
    valid_ids = {"happy","excited","proud","motivated","loved","tired","bored","sad"}
    v = query_params["vote"]
    if v in valid_ids:
        add_vote(v)
    # Limpieza y cambio de página
    st.query_params.clear()
    st.query_params["page"] = "results"
    st.rerun()

current_page = query_params.get("page", "vote")

# --- INTERFAZ HTML ---
def render_spectacular_ui():
    results = get_results_data()
    total_votos = sum(r['count'] for r in results)

    emociones = [
        {"id": "happy", "label": "Feliz", "icon": "smile", "color": "#FCD34D", "bg": "bg-amber-50", "text": "text-amber-600"},
        {"id": "excited", "label": "Entusiasmado", "icon": "zap", "color": "#60A5FA", "bg": "bg-blue-50", "text": "text-blue-600"},
        {"id": "proud", "label": "Orgulloso", "icon": "trophy", "color": "#34D399", "bg": "bg-emerald-50", "text": "text-emerald-600"},
        {"id": "motivated", "label": "Motivado", "icon": "dumbbell", "color": "#A78BFA", "bg": "bg-violet-50", "text": "text-violet-600"},
        {"id": "loved", "label": "Agradecido", "icon": "heart", "color": "#F472B6", "bg": "bg-pink-50", "text": "text-pink-600"},
        {"id": "tired", "label": "Cansado", "icon": "flame", "color": "#F87171", "bg": "bg-red-50", "text": "text-red-600"},
        {"id": "bored", "label": "Aburrido", "icon": "meh", "color": "#94A3B8", "bg": "bg-slate-50", "text": "text-slate-600"},
        {"id": "sad", "label": "Triste", "icon": "frown", "color": "#64748B", "bg": "bg-indigo-50", "text": "text-indigo-600"},
    ]

    # Mapeo de resultados para el frontend
    results_map = {r['emocion']: r['count'] for r in results}

    # Construcción de tarjetas y barras
    cards_html = "".join([f"""
        <div onclick="sendVote('{e['id']}')" class="card-btn glass {e['bg']} p-8 rounded-[2.5rem] flex flex-col items-center justify-center text-center">
            <i data-lucide="{e['icon']}" class="w-12 h-12 mb-4 {e['text']}"></i>
            <span class="text-xl font-black uppercase tracking-tight">{e['label']}</span>
        </div>
    """ for e in emociones])

    barras_html = "".join([f"""
        <div class="mb-6">
            <div class="flex justify-between font-bold uppercase text-sm mb-2">
                <span>{e['label']}</span>
                <span>{results_map.get(e['id'], 0)}</span>
            </div>
            <div class="w-full bg-black/5 h-3 rounded-full overflow-hidden">
                <div class="h-full bg-pink-500 transition-all duration-1000" style="width: { (results_map.get(e['id'], 0)/total_votos*100) if total_votos > 0 else 0 }%"></div>
            </div>
        </div>
    """ for e in emociones])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Libre+Baskerville:ital,wght@1,400&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Inter', sans-serif; background: #FAFAFA; margin: 0; overflow-x: hidden; color: #1A1A1A; }}
            .glass {{ background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.5); }}
            .blob {{ position: fixed; border-radius: 50%; filter: blur(80px); opacity: 0.15; z-index: -1; animation: pulse 10s infinite alternate; }}
            @keyframes pulse {{ from {{ transform: scale(1); }} to {{ transform: scale(1.2); }} }}
            .card-btn {{ transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; }}
            .card-btn:hover {{ transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); background: white; }}
            .hidden {{ display: none; }}
        </style>
    </head>
    <body>
        <!-- Blobs de fondo -->
        <div class="blob w-96 h-96 bg-cyan-400 -top-20 -left-20"></div>
        <div class="blob w-96 h-96" style="background-color: #ec008c; top:50%; right:-5rem;"></div>
        <div class="blob w-80 h-80 bg-lime-400 bottom-0 left-1/4"></div>
        <div class="blob w-64 h-64 bg-yellow-400 top-1/4 right-1/4"></div>

        <div class="max-w-6xl mx-auto p-6 md:p-10 min-h-screen flex flex-col">
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
                <div class="flex gap-4">
                    <a href="?page=vote" target="_top" class="px-6 py-2 rounded-full border border-black/10 font-bold uppercase text-xs tracking-widest hover:bg-black hover:text-white transition">Votar</a>
                    <a href="?page=results" target="_top" class="px-6 py-2 rounded-full border border-black/10 font-bold uppercase text-xs tracking-widest hover:bg-black hover:text-white transition">Resultados</a>
                    <!-- Quitamos el reset desde cliente por seguridad -->
                </div>
            </header>

            <!-- Página de Votación -->
            <div id="page-vote" class="{ 'space-y-10' if current_page == 'vote' else 'hidden' }">
                <h2 class="text-3xl md:text-5xl font-bold text-gray-800">¿Cómo te sientes hoy?</h2>
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                    {cards_html}
                </div>
            </div>

            <!-- Página de Resultados -->
            <div id="page-results" class="{ 'space-y-10' if current_page == 'results' else 'hidden' }">
                <div class="flex justify-between items-end">
                    <h2 class="text-3xl md:text-5xl font-bold text-gray-800">Marcador General</h2>
                    <div class="bg-black text-white px-6 py-2 rounded-full font-black text-xl">TOTAL: {total_votos}</div>
                </div>
                <div class="grid md:grid-cols-2 gap-10">
                    <div class="glass p-8 rounded-[3rem] min-h-[300px] flex flex-col justify-center">
                        {barras_html}
                    </div>
                    <div class="flex flex-col justify-center items-center p-10 text-center">
                        <i data-lucide="bar-chart-3" class="w-20 h-20 mb-6 opacity-20"></i>
                        <p class="text-gray-400 font-medium">Los resultados se actualizan automáticamente al votar.</p>
                    </div>
                </div>
            </div>

            <footer class="mt-auto pt-20 pb-10 text-center opacity-40 font-bold text-xs uppercase tracking-widest">
                © 2026 Día de la Educación Física en la Calle • Construido con Pasión. <br> (Dpto. de EF del IES Lucía de Medrano)
            </footer>
        </div>

        <script>
            lucide.createIcons();
            function sendVote(id) {{
                const url = new URL(window.top.location.href);
                url.searchParams.set('vote', id);
                window.top.location.href = url.href;
            }}
        </script>
    </body>
    </html>
    """
    return components.html(html_content, height=1000, scrolling=False)

# --- PANEL ADMIN (SEGURO, SERVER-SIDE) ---
with st.container():
    st.markdown(
        """
        <div class="admin-box">
            <details style="background:rgba(255,255,255,0.9); padding:12px 16px; border-radius:12px; border:1px solid rgba(0,0,0,0.08);">
              <summary style="cursor:pointer; font-weight:700;">Panel administrador</summary>
            """,
        unsafe_allow_html=True
    )
    with st.form("admin_reset_form"):
        pwd = st.text_input("Contraseña", type="password")
        cols = st.columns(2)
        with cols[0]:
            do_reset = st.form_submit_button("Borrar todos los votos", use_container_width=True)
        with cols[1]:
            show_stats = st.form_submit_button("Exportar CSV", use_container_width=True)

    if do_reset:
        if _admin_ok(pwd):
            reset_db()
            st.success("✅ Base de datos reiniciada.")
            st.query_params.clear()
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta.")

    if show_stats:
        if _admin_ok(pwd):
            data = get_results_data()
            if data:
                df = pd.DataFrame(data)
                df.to_csv("resultados_emocionometro.csv", index=False)
                st.success("✅ CSV exportado (resultados_emocionometro.csv).")
                st.dataframe(df)
            else:
                st.info("No hay datos para exportar.")
        else:
            st.error("❌ Contraseña incorrecta.")

    st.markdown("</details></div>", unsafe_allow_html=True)

# --- RENDER UI ---
render_spectacular_ui()
