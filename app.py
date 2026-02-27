import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import os

# --- CONFIGURACIÓN BÁSICA ---
st.set_page_config(page_title="Emocionómetro EF", layout="wide", initial_sidebar_state="collapsed")

# Ocultar elementos de Streamlit
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}
iframe {border: none !important;}
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ---
DB_PATH = os.path.join(os.getcwd(), "emocionometro.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS votos (emocion TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

def add_vote(e):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO votos (emocion) VALUES (?)", (e,))
    conn.commit()
    conn.close()

def get_results():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT emocion, COUNT(*) AS count FROM votos GROUP BY emocion", conn)
    conn.close()
    return df.to_dict(orient="records")

def reset_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM votos")
    conn.commit()
    conn.close()

init_db()

# --- LÓGICA DE QUERY PARAMS ---
qp = st.query_params

# Registrar voto
if "vote" in qp:
    add_vote(qp["vote"])
    st.query_params.clear()
    st.query_params["page"] = "results"
    st.rerun()

# Reset admin
if "reset" in qp:
    reset_db()
    st.query_params.clear()
    st.query_params["page"] = "results"
    st.rerun()

current_page = qp.get("page", "vote")

# --- RENDER HTML ---
def render_ui():

    results = get_results()
    total_votos = sum(r["count"] for r in results)

    emociones = [
        {"id": "happy", "label": "Feliz", "icon": "smile", "bg": "bg-amber-50", "text": "text-amber-600"},
        {"id": "excited", "label": "Entusiasmado", "icon": "zap", "bg": "bg-blue-50", "text": "text-blue-600"},
        {"id": "proud", "label": "Orgulloso", "icon": "trophy", "bg": "bg-emerald-50", "text": "text-emerald-600"},
        {"id": "motivated", "label": "Motivado", "icon": "dumbbell", "bg": "bg-violet-50", "text": "text-violet-600"},
        {"id": "loved", "label": "Agradecido", "icon": "heart", "bg": "bg-pink-50", "text": "text-pink-600"},
        {"id": "tired", "label": "Cansado", "icon": "flame", "bg": "bg-red-50", "text": "text-red-600"},
        {"id": "bored", "label": "Aburrido", "icon": "meh", "bg": "bg-slate-50", "text": "text-slate-600"},
        {"id": "sad", "label": "Triste", "icon": "frown", "bg": "bg-indigo-50", "text": "text-indigo-600"},
    ]

    resmap = {r["emocion"]: r["count"] for r in results}

    html = f"""
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>

        <style>
            body {{ font-family: 'Inter', sans-serif; background: #FAFAFA; }}
            .card-btn:hover {{ transform: translateY(-8px); }}
        </style>
    </head>

    <body>

    <div class="p-6 max-w-6xl mx-auto">

        <header class="flex justify-between items-center mb-10 pb-6 border-b border-gray-300">
            <h1 class="text-5xl font-black">Emocionómetro</h1>
            <div class="flex gap-4">
                <button onclick="go('vote')" class="px-4 py-2 border rounded-full">Votar</button>
                <button onclick="go('results')" class="px-4 py-2 border rounded-full">Resultados</button>
                <button onclick="resetDB()" class="px-3 py-2 border rounded-full text-red-500">Reset</button>
            </div>
        </header>

        <!-- Página votar -->
        <div id="vote" style="display:{'block' if current_page=='vote' else 'none'};">
            <h2 class="text-3xl font-bold mb-6">¿Cómo te sientes hoy?</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6">

                {''.join([f'''
                    <div onclick="vote('{e['id']}')" class="p-8 rounded-3xl card-btn {e['bg']} text-center cursor-pointer">
                        <i data-lucide="{e['icon']}" class="w-12 h-12 mb-4 {e['text']}"></i>
                        <p class="font-bold">{e['label']}</p>
                    </div>
                ''' for e in emociones])}

            </div>
        </div>

        <!-- Página resultados -->
        <div id="results" style="display:{'block' if current_page=='results' else 'none'};">
            <h2 class="text-3xl font-bold mb-6">Resultados</h2>
            <p class="font-bold text-xl mb-6">Total votos: {total_votos}</p>

            {''.join([f'''
                <div class="mb-4">
                    <div class="flex justify-between font-bold">
                        <span>{e["label"]}</span>
                        <span>{resmap.get(e["id"],0)}</span>
                    </div>

                    <div class="w-full bg-gray-200 h-3 rounded-full">
                        <div class="bg-pink-500 h-full rounded-full" style="width:{ (resmap.get(e['id'],0)/total_votos*100) if total_votos>0 else 0 }%"></div>
                    </div>
                </div>
            ''' for e in emociones])}
        </div>

    </div>

    <script>
        lucide.createIcons();

        function go(p) {{
            const u = new URL(window.location.href);
            u.searchParams.set("page", p);
            window.location.href = u;
        }}

        function vote(id) {{
            const u = new URL(window.location.href);
            u.searchParams.set("vote", id);
            window.location.href = u;
        }}

        function resetDB() {{
            if (confirm("¿Seguro que quieres borrar todos los votos?")) {{
                const u = new URL(window.location.href);
                u.searchParams.set("reset", "true");
                window.location.href = u;
            }}
        }}
    </script>

    </body>
    </html>
    """

    components.html(html, height=1000, scrolling=False)

# Renderiza
render_ui()
