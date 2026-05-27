import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

# ==========================================================
# CONFIGURACION GENERAL
# ==========================================================

st.set_page_config(
    page_title="Dashboard Dólar + IPC",
    page_icon=":material/analytics:",
    layout="wide"
)

# ==========================================================
# ESTILOS CSS
# ==========================================================

st.markdown("""
<style>
body {
    background-color: #0d1117;
}
.main {
    background-color: #0d1117;
    color: white;
}
h1, h2, h3 {
    color: #00d4ff;
}
.stMetric {
    background-color: #161b22;
    padding: 15px;
    border-radius: 12px;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# COLORES GRAFICOS
# ==========================================================

PLOT_BG = "#0d1117"
PAPER_BG = "#0d1117"
FONT_COLOR = "white"
GRID_COLOR = "rgba(255,255,255,0.1)"

# ==========================================================
# FUNCION ESTILO GRAFICOS
# ==========================================================

def aplicar_estilo(fig):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(
            color=FONT_COLOR,
            size=14
        ),
        title_font=dict(
            size=22
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig

# ==========================================================
# TITULO
# ==========================================================
st.markdown("---")
st.header(":material/analytics: Económico Profesional")
st.markdown("""
<div style='font-size:20px;'>
Análisis avanzado de: 
    - Dólar
    - IPC
    - Correlaciones
    - Tendencias
    - Variaciones
    - Regresión lineal
    - Estadística descriptiva
</div>
""", unsafe_allow_html=True)

# st.markdown(""" Análisis avanzado de: 
# - Dólar
# - IPC
# - Correlaciones
# - Tendencias
# - Variaciones
# - Regresión lineal
# - Estadística descriptiva
# """)

# ==========================================================
# RUTAS ARCHIVOS
# ==========================================================
RUTA_IPC = "data/dolar-ipc.xlsx"
# ==========================================================
# FUNCION CARGA DATOS
# ==========================================================
@st.cache_data
def cargar_datos():
    df_ipc = pd.read_excel(RUTA_IPC)
    # ======================================================
    # LIMPIEZA COLUMNAS
    # ======================================================
    df_ipc.columns = [c.strip() for c in df_ipc.columns]
    # ======================================================
    # BUSCAR FECHA
    # ======================================================
    fecha_ipc = None
    for c in df_ipc.columns:
        if "fecha" in c.lower():
            fecha_ipc = c
    # ======================================================
    # CONVERTIR FECHA
    # ======================================================
    if fecha_ipc:
        df_ipc[fecha_ipc] = pd.to_datetime(
            df_ipc[fecha_ipc],
            errors="coerce"
        )
    # ======================================================
    # COLUMNAS NUMERICAS
    # ======================================================
    cols_num_ipc = [
        c for c in df_ipc.columns
        if c != fecha_ipc
    ]
    # ======================================================
    # LIMPIEZA NUMERICA
    # ======================================================
    for c in cols_num_ipc:
        df_ipc[c] = (
            df_ipc[c]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df_ipc[c] = pd.to_numeric(
            df_ipc[c],
            errors="coerce"
        )
    return df_ipc, fecha_ipc, cols_num_ipc
# ==========================================================
# CARGA
# ==========================================================
df_ipc, fecha_ipc, cols_num_ipc = cargar_datos()
# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.subheader(":material/settings: Configuración")
dataset = st.sidebar.selectbox(
    "Seleccione Dataset",
    ["IPC"]
)
# ==========================================================
# SELECCION DATASET
# ==========================================================
if dataset == "IPC":
    df = df_ipc
    fecha = fecha_ipc
    cols_num = cols_num_ipc
# ==========================================================
# VARIABLE PRINCIPAL
# ==========================================================
variable = st.sidebar.selectbox(
    "Seleccione Variable",
    cols_num_ipc
)
# ==========================================================
# METRICAS
# ==========================================================
st.subheader(":material/bid_landscape: Resumen Estadístico")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Promedio",
        round(df[variable].mean(), 2)
    )
with col2:
    st.metric(
        "Máximo",
        round(df[variable].max(), 2)
    )
with col3:
    st.metric(
        "Mínimo",
        round(df[variable].min(), 2)
    )
with col4:
    st.metric(
        "Desviación",
        round(df[variable].std(), 2)
    )

st.markdown("---")    
# ==========================================================
# TEXTO EXPLICATIVO
# ==========================================================
# st.markdown(f"""
# ###  Interpretación Automática
# La variable seleccionada **{variable}** presenta:

# - Promedio: **{round(df[variable].mean(),2)}**
# - Máximo: **{round(df[variable].max(),2)}**
# - Mínimo: **{round(df[variable].min(),2)}**

# La desviación estándar indica el nivel de volatilidad.

# """)
st.markdown(f"""
<div style='font-size:24px;'>
<h2> Interpretación Automática</h2>
La variable seleccionada <b>{variable}</b> presenta:
<ul>
<li>Promedio: <b>{round(df[variable].mean(),2)}</b></li>
<li>Máximo: <b>{round(df[variable].max(),2)}</b></li>
<li>Mínimo: <b>{round(df[variable].min(),2)}</b></li>
</ul>
La desviación estándar indica el nivel de volatilidad.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
# ==========================================================
# EVOLUCION TEMPORAL
# ==========================================================

st.subheader(":material/moving: Evolución Temporal")

# limpieza para evitar gráficos vacíos
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=[variable])

if fecha is not None:
    fig = px.line(
        df,
        x=fecha,
        y=variable,
        title=f"Evolución temporal de {variable}",
        template="plotly_dark"
    )
    fig = aplicar_estilo(fig)

    st.plotly_chart(
        fig,
        width='stretch'
    )

st.markdown("---")
# ==========================================================
# HISTOGRAMA
# ==========================================================
st.subheader(":material/border_horizontal: Distribución")

fig_hist = px.histogram(
    df,
    x=variable,
    nbins=30,
    title=f"Distribución de {variable}",
    template="plotly_dark"
)

fig_hist = aplicar_estilo(fig_hist)

st.plotly_chart(
    fig_hist,
    width='stretch'
)
st.markdown("---")

# ==========================================================
# VARIACION PORCENTUAL
# ==========================================================

st.subheader(":material/difference: Variación Porcentual")

# cálculo
df["variacion_pct"] = df[variable].pct_change() * 100
# limpieza
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=["variacion_pct"])
# gráfico
fig_pct = px.line(
    df,
    x=fecha,
    y="variacion_pct",
    title="Variación porcentual",
    template="plotly_dark"
)
fig_pct = aplicar_estilo(fig_pct)
st.plotly_chart(
    fig_pct,
    width='stretch'
)
# st.markdown("""
# ### 🧠 Explicación

# La variación porcentual ayuda a detectar:

# - cambios bruscos
# - volatilidad
# - crisis económicas
# - estabilidad de mercado
# """)

st.markdown("""
<div style='font-size:22px;'>
<h3>Explicación</h3>
La variación porcentual ayuda a detectar:
            
- cambios bruscos  
- volatilidad  
- crisis económicas  
- estabilidad de mercado  
</div>
""", unsafe_allow_html=True)

st.markdown("---")
# ==========================================================
# MATRIZ CORRELACION
# ==========================================================

st.subheader(":material/qr_code_scanner: Matriz de Correlación")

corr = df[cols_num].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlación entre variables",
    template="plotly_dark"
)
fig_corr = aplicar_estilo(fig_corr)

st.plotly_chart(
    fig_corr,
    width='stretch'
)
st.markdown("---")
# ==========================================================
# EXPLICACION
# ==========================================================

# st.markdown("""
# ### Interpretación

# - Cercano a 1 ⇒ correlación positiva
# - Cercano a -1 ⇒ correlación negativa
# - Cercano a 0 ⇒ poca relación
# """)

st.markdown("""
<div style='font-size:28px;'>

<h3>Interpretación</h3>

<ul>
<li>Cercano a 1 ⇒ correlación positiva</li>
<li>Cercano a -1 ⇒ correlación negativa</li>
<li>Cercano a 0 ⇒ poca relación</li>
</ul>

</div>
""", unsafe_allow_html=True)
st.markdown("---")
# ==========================================================
# REGRESION
# ==========================================================

st.header("🤖 Modelo Predictivo")

x_var = st.selectbox(
    "Variable X",
    cols_num,
    index=0
)

y_var = st.selectbox(
    "Variable Y",
    cols_num,
    index=min(1, len(cols_num)-1)
)

data_model = df[[x_var, y_var]].dropna()

X = data_model[[x_var]]
Y = data_model[y_var]

modelo = LinearRegression()
modelo.fit(X, Y)

pred = modelo.predict(X)

coef = modelo.coef_[0]
inter = modelo.intercept_
score = modelo.score(X, Y)

st.markdown("---")
# ==========================================================
# GRAFICO REGRESION
# ==========================================================

fig_reg = go.Figure()

fig_reg.add_trace(
    go.Scatter(
        x=X[x_var],
        y=Y,
        mode='markers',
        name='Datos'
    )
)

fig_reg.add_trace(
    go.Scatter(
        x=X[x_var],
        y=pred,
        mode='lines',
        name='Regresión'
    )
)

fig_reg.update_layout(
    title=f"Regresión {x_var} vs {y_var}",
    template="plotly_dark"
)

fig_reg = aplicar_estilo(fig_reg)

st.plotly_chart(
    fig_reg,
    width='stretch'
)

st.markdown("---")
# ==========================================================
# RESULTADOS MODELO
# ==========================================================
# st.markdown(f"""
# ### Resultado del Modelo

# - Coeficiente: **{round(coef,4)}**
# - Intercepto: **{round(inter,4)}**
# - Precisión R²: **{round(score,4)}**

# Interpretación:

# - R² alto ⇒ buena capacidad predictiva
# - R² bajo ⇒ relación débil
# """)
st.markdown(f"""
<div style='font-size:22px;'>

<h3>Resultado del Modelo</h3>

<ul>
<li>Coeficiente: <b>{round(coef,4)}</b></li>
<li>Intercepto: <b>{round(inter,4)}</b></li>
<li>Precisión R²: <b>{round(score,4)}</b></li>
</ul>

<p><b>Interpretación:</b></p>

<ul>
<li>R² alto ⇒ buena capacidad predictiva</li>
<li>R² bajo ⇒ relación débil</li>
</ul>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# PEARSON
# ==========================================================

corr_pearson, pvalue = pearsonr(
    data_model[x_var],
    data_model[y_var]
)

st.subheader(" Correlación de Pearson")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Correlación",
        round(corr_pearson, 4)
    )

with c2:
    st.metric(
        "P-Value",
        round(pvalue, 8)
    )


# ==========================================================
# EXPLICACION PEARSON
# ==========================================================
# st.markdown(f"""
# ### 🧠 Interpretación Estadística

# La correlación obtenida es:

# **{round(corr_pearson,4)}**

# - > 0.7 ⇒ fuerte positiva
# - < -0.7 ⇒ fuerte negativa
# - ~ 0 ⇒ débil
# """)

st.markdown(f"""
<div style='font-size:22px;'>

<h3>Interpretación Estadística</h3>

<p>La correlación obtenida es:</p>

<p><b>{round(corr_pearson,4)}</b></p>

<ul>
<li>&gt; 0.7 ⇒ fuerte positiva</li>
<li>&lt; -0.7 ⇒ fuerte negativa</li>
<li>~ 0 ⇒ débil</li>
</ul>

</div>
""", unsafe_allow_html=True)

st.markdown("---")
# ==========================================================
# TABLA
# ==========================================================

with st.expander("Dataset"):
    st.subheader("Dataset")

    st.dataframe(
        df.head(100),
        width='stretch'
    )
    # ==========================================================
    # EXPORTACION
    # ==========================================================

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        ":material/arrow_circle_down: Descargar CSV",
        csv,
        "dataset_procesado.csv",
        "text/csv"
    )


st.markdown("---")