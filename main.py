import streamlit as st
import base64
from pathlib import Path
import os
import streamlit.components.v1 as components
import urllib.parse

# --- Configuración página ---
st.set_page_config(
    page_title="Dashboard Análisis Inflacion", 
    layout="wide", 
    page_icon=":material/network_intel_node:", 
    initial_sidebar_state="collapsed"
)

# --- Estilos Globales (Ocultar elementos de Streamlit) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stAppViewContainer"] { margin-left: 0px; }
    </style>
""", unsafe_allow_html=True)

# --- CARGA DE CSS PARA BOTONES HOLOGRAMA ---
try:
    boton_css_raw = Path("static/boton.css").read_text(encoding="utf-8")
    hologram_css = f"<style>{boton_css_raw}</style>"
except:
    hologram_css = """
    <style>
    div[data-testid="stButton"] > button {
        width: 100% !important; 
        position: relative;
        padding: 1.2rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #fff !important;
        background: rgba(0, 255, 255, 0.1) !important;
        border: 2px solid rgba(0, 255, 255, 0.5) !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px) !important;
        text-transform: uppercase;
        transition: all 0.4s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: rgba(0, 255, 255, 0.2) !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5) !important;
        border-color: rgba(0, 255, 255, 0.8) !important;
    }
    </style>
    """

# --- LÓGICA DE CARGA DE ESTÁTICOS ---
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

def load_static_files():
    try:
        html_content = (STATIC_DIR / "digitalApocalypse.html").read_text(encoding="utf-8")
        css_content = (STATIC_DIR / "digitalApocalypse.css").read_text(encoding="utf-8")
        js_content = (STATIC_DIR / "digitalApocalypse.js").read_text(encoding="utf-8")
        
        # Combinamos usando f-strings seguros para HTML/CSS/JS
        full_html = f"""
        <style>{css_content}</style>
        {html_content}
        <script>{js_content}</script>
        """
        return full_html
    except Exception as e:
        st.error(f"Error al cargar archivos estáticos: {e}")
        return None

dashboard_html = load_static_files()


# --- ESTRUCTURA VISUAL Y REDUCCIÓN DE ANCHO ---
# Proporción [2, 6, 2] = 20% izq | 60% centro | 20% der.
col_izq, col_central, col_der = st.columns([2, 6, 2])

with col_central:
    st.header("Dashboard Teoria del Caos y Fractales (dólar/IPC)", anchor=False, text_alignment="center")

    st.markdown("""
        <style>
        .stAlert > div {
            text-align: center;
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Todo indentado bajo 'with col_central:'
    if dashboard_html:
        data_url = f"data:text/html;charset=utf-8,{urllib.parse.quote(dashboard_html)}"
        
        # CORRECCIÓN: iframe renderizado con components de Streamlit
        st.iframe(
            src=data_url,
            height=1000
        )
        
        # Inyectamos el CSS para los botones de abajo
        st.markdown(hologram_css, unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("Opciones de modelos", anchor=False, text_alignment="center")
            
            b1, b2 = st.columns(2)
            with b1:
                # CORRECCIÓN: use_container_width=True en lugar de width='stretch'
                if st.button(":material/threat_intelligence: Caos/Fractal", key="acceso", use_container_width=True): 
                    st.switch_page("pages/1-AnalisisNeosimbolicoFractal.py")
            with b2:
                if st.button(":material/threat_intelligence: Caos/Fractal plus", key="acceso1", use_container_width=True): 
                    st.switch_page("pages/2-AnalisisNeosimbolicoFractalAzdo.py")
            
            b3, b4 = st.columns(2)
            with b3:
                if st.button(":material/threat_intelligence: Estadístico Clásico", key="acceso2", use_container_width=True): 
                    st.switch_page("pages/3-AnalisisEstadisticoIPC-Dolar.py")
            with b4:
                if st.button(":material/threat_intelligence: Caos/Fractal Ventas", key="acceso3", use_container_width=True): 
                    st.switch_page("pages/4-AnalisisFractalventas.py")

    st.markdown("---")