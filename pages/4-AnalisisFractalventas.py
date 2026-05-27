import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Análisis Fractal de Ventas", layout="wide", page_icon=":material/monitoring:")
st.subheader("Análisis Neosimbólico y Fractal aplicado a Ventas")

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        try:
            df = pd.read_excel(nombre_archivo)
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            return df.dropna(subset=['fecha', 'venta'])
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            return None
    else:
        st.warning(f"No se encontró el archivo '{nombre_archivo}'.")
        return None

def calcular_hurst(serie, max_lag=20):
    if len(serie) < max_lag + 1:
        return np.nan
    lags = range(2, max_lag)
    tau = [np.std(np.subtract(serie.values[lag:], serie.values[:-lag])) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0]    

def calcular_rsi(serie, period=14):
    delta = serie.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def detectar_fase(serie):
    if len(serie) < 50:
        return "Datos insuficientes (Mínimo 50 días)", "N/A"
    
    rsi_serie = calcular_rsi(serie)
    sma_serie = serie.rolling(window=50).mean()
    
    rsi = rsi_serie.iloc[-1]
    sma = sma_serie.iloc[-1]
    venta_actual = serie.iloc[-1]
    
    if pd.isna(rsi) or pd.isna(sma):
        return "Calculando estabilidad...", "N/A"
    
    if rsi < 35: 
        return "Acumulación (Ventas estancadas, posible inicio de ciclo)", "Reversible (Soporte Comercial)"
    elif rsi >= 35 and rsi < 55 and venta_actual > sma: 
        return "Expansión (Tendencia de Crecimiento Sostenido)", "Irreversible (Momento Fuerte)"
    elif rsi >= 55 and rsi < 75: 
        return "Distribución (Pico de Ventas, posible saturación)", "Reversible (Resistencia Comercial)"
    else:
        return "Contracción (Pérdida de inercia de ventas)", "Irreversible (Caída Estructural)"

# --- BARRA LATERAL: SELECCIÓN ---
st.sidebar.subheader(":material/filter_alt: Filtros Comerciales")

# Cargar el dataset (Asegúrate de que el nombre coincida con tu archivo local)
archivo_db = "data/ventas-db.xlsx" 
df_raw = cargar_datos(archivo_db)

if df_raw is not None:
    # Filtros Dinámicos
    paises = ["Todos"] + sorted(df_raw['pais'].dropna().unique().tolist())
    categories = ["Todas"] + sorted(df_raw['categoria'].dropna().unique().tolist())
    
    pais_sel = st.sidebar.selectbox("**Selecciona un País:**", paises)
    cat_sel = st.sidebar.selectbox("**Selecciona una Categoría:**", categories)
    
    # Aplicar filtros
    df_filtered = df_raw.copy()
    if pais_sel != "Todos":
        df_filtered = df_filtered[df_filtered['pais'] == pais_sel]
    if cat_sel != "Todas":
        df_filtered = df_filtered[df_filtered['categoria'] == cat_sel]
        
    # AGRUPACIÓN: Clave para convertir transacciones en Serie Temporal
    df_agg = df_filtered.groupby('fecha')['venta'].sum().reset_index().sort_values('fecha')
    
    if len(df_agg) < 20:
        st.warning(f"No hay suficientes días con ventas para el cruce: {pais_sel} - {cat_sel}. (Mínimo 20 días requeridos).")
    else:
        st.success(f"Analizando {len(df_agg)} días de ventas.")
        st.subheader(f"Dashboard Estructural: {pais_sel} | {cat_sel}")
        
        serie_ventas = df_agg['venta']
        
        # --- MÓDULO DE FASE (SPIN) ---
        with st.expander(":material/all_inclusive: Módulo de Fase Comercial", expanded=True):
            fase, tipo = detectar_fase(serie_ventas)
            c1, c2 = st.columns(2)
            c1.metric("Fase Estructural Actual", fase)
            c2.metric("Naturaleza del Ciclo", tipo)
            st.info("Este módulo evalúa si el ritmo de ventas actual es un pico transitorio (reversible) o una nueva base de facturación consolidada (irreversible).")

        # --- MÓDULO 1: EXPECTATIVA MATEMÁTICA ---
        st.header("1. Rango de Volatilidad Esperada (Próximo Día)")
        ultimos_11 = df_agg.tail(11).copy()
        ultimos_11['Variacion'] = ultimos_11['venta'].pct_change().abs()
        variabilidad = ultimos_11['Variacion'].mean()
        venta_actual = serie_ventas.iloc[-1]
        
        f1_baja = venta_actual * (1 - variabilidad)
        f3_alza = venta_actual * (1 + variabilidad)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Caída Esperada (-1σ)", f"${f1_baja:,.2f}")
        col2.metric("Venta Diaria Actual", f"${venta_actual:,.2f}")
        col3.metric("Alza Esperada (+1σ)", f"${f3_alza:,.2f}")

        st.markdown("---")
        
        # --- MÓDULO 2: ATRACTOR DEL CAOS ---
        st.header("2. Red Flags y Eficiencia Fractal (Ruido Comercial)")
        
        delta = serie_ventas.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        max_fuerza = max(gain.max(), loss.max()) if max(gain.max(), loss.max()) > 0 else 1
        grados_crecimiento = (gain / max_fuerza) * 180
        grados_caida = (loss / max_fuerza) * 180
        
        # Eficiencia de Kaufman aplicada a ventas
        desplazamiento_neto = serie_ventas.diff(14).abs()
        ruido_acumulado = serie_ventas.diff().abs().rolling(window=14).sum()
        eficiencia_fractal = (desplazamiento_neto / ruido_acumulado).fillna(0.5)
        
        ult_crecimiento = grados_crecimiento.iloc[-1]
        ult_caida = grados_caida.iloc[-1]
        ult_eficiencia = eficiencia_fractal.iloc[-1]
        
        c_red1, c_red2, c_red3 = st.columns(3)
        c_red1.metric("Vector Crecimiento", f"{ult_crecimiento:.1f}°")
        c_red2.metric("Vector Caída", f"{ult_caida:.1f}°")
        
        if ult_eficiencia < 0.18:
            c_red3.metric("Eficiencia de Ventas", f"{ult_eficiencia:.2%}", delta="RUIDO CRÍTICO / CAOS", delta_color="inverse")
        else:
            c_red3.metric("Eficiencia de Ventas", f"{ult_eficiencia:.2%}", delta="Tendencia Limpia", delta_color="normal")

        if ult_crecimiento > 33 and ult_caida > 33:
            st.error("### :material/flag_circle:  RED FLAG (Caos Angular): Alta variabilidad extrema diaria. El canal de ventas está altamente inestable.")
        elif ult_eficiencia < 0.15:
            st.warning("### :material/warning:  ALERTA DE COMPRESIÓN: Las ventas suben y bajan sin dirección. Se avecina una ruptura brusca (alza o baja).")
        else:
            st.success("### :material/bookmark_check:  ORDEN DINÁMICO: Las ventas mantienen una inercia predecible.")

        # --- NUEVO GRÁFICO DE CUADRANTES INTEGRADO CON SEGUIMIENTO ---
        st.subheader(":material/map: Mapa de Fases Angular: Atractor de Ventas (Crecimiento vs. Caída)")
        
        # Vinculamos las variables de tu módulo de ventas con la estructura del mapa fractal
        grados_dinero = grados_crecimiento
        grados_papel = grados_caida
        ult_dinero = ult_crecimiento
        ult_papel = ult_caida
        
        # Armamos la trayectoria histórica de los últimos 40 periodos usando las fechas agrupadas
        df_trayectoria = pd.DataFrame({
            'Dinero': grados_dinero,
            'Papel': grados_papel,
            'Fecha': df_agg['fecha'].dt.strftime('%Y-%m-%d')
        }).tail(40).dropna().reset_index(drop=True)
        
        fig_quad = go.Figure()
        
        # Añadir rectángulos de fondo (Zonas del atractor)
        max_r = 60  # Rango máximo visual sugerido
        fig_quad.add_shape(type="rect", x0=0, y0=0, x1=33, y1=33, fillcolor="rgba(128,128,128,0.1)", line=dict(width=0))
        fig_quad.add_shape(type="rect", x0=33, y0=0, x1=max_r, y1=33, fillcolor="rgba(0,204,150,0.1)", line=dict(width=0))
        fig_quad.add_shape(type="rect", x0=0, y0=33, x1=33, y1=max_r, fillcolor="rgba(99,110,250,0.1)", line=dict(width=0))
        fig_quad.add_shape(type="rect", x0=33, y0=33, x1=max_r, y1=max_r, fillcolor="rgba(255,75,75,0.1)", line=dict(width=0))
        
        # Dibujar trayectoria temporal con degradado en los marcadores
        num_points = len(df_trayectoria)
        colors = [f'rgba(200, 200, 200, {0.2 + (i/num_points)*0.5})' for i in range(num_points)]
        
        fig_quad.add_trace(go.Scatter(
            x=df_trayectoria['Dinero'], 
            y=df_trayectoria['Papel'],
            mode='lines+markers',
            name='Trayectoria Temporal',
            line=dict(color='rgba(255, 255, 255, 0.3)', width=2),
            marker=dict(size=8, color=colors, line=dict(width=1, color='white')),
            text=df_trayectoria['Fecha'],
            hoverinfo='text+x+y'
        ))
        
        # Resaltar el estado del día de hoy (Último registro)
        fig_quad.add_trace(go.Scatter(
            x=[ult_dinero], y=[ult_papel],
            mode='markers',
            name='ESTADO ACTUAL',
            marker=dict(color='#FF4B4B', size=16, symbol='diamond', line=dict(color='white', width=2))
        ))
        
        # Líneas divisorias críticas (Umbral del Caos a 33°)
        fig_quad.add_vline(x=33, line_dash="dash", line_color="white", line_width=1)
        fig_quad.add_hline(y=33, line_dash="dash", line_color="white", line_width=1)
        
        # Configuraciones de diseño y etiquetas de los cuadrantes adaptadas a Ventas
        fig_quad.update_layout(
            template="plotly_dark",
            xaxis=dict(title="Fuerza del Vector Crecimiento (X)", range=[0, max_r], showgrid=False),
            yaxis=dict(title="Fuerza del Vector Caída (Y)", range=[0, max_r], showgrid=False),
            height=500,
            showlegend=False,
            annotations=[
                dict(x=16.5, y=16.5, text="<b>APATÍA / COMPRESIÓN</b>", showarrow=False, font=dict(color="gray", size=16)),
                dict(x=47, y=16.5, text="<b>ESTRUCTURA ALCISTA</b>", showarrow=False, font=dict(color="#00CC96", size=16)),
                dict(x=16.5, y=47, text="<b>ESTRUCTURA BAJISTA</b>", showarrow=False, font=dict(color="#636EFA", size=16)),
                dict(x=47, y=47, text="<b>ZONA RED FLAG (CAOS)</b>", showarrow=False, font=dict(color="#FF4B4B", size=16, weight='bold'))
            ]
        )
        st.plotly_chart(fig_quad, width='stretch')

        st.markdown("---")
        
        # --- MÓDULO 3: MEMORIA FRACTAL ---
        st.header("3. Semáforo de Predictibilidad (Exponente de Hurst)")
        hurst_val = calcular_hurst(serie_ventas)
        
        if not np.isnan(hurst_val):
            if hurst_val < 0.45:
                estado_hurst = ":material/dangerous: Antipersistente (Reversiones violentas, difícil proyectar stock)"
                color = "🔴"
            elif hurst_val > 0.65:
                estado_hurst = ":materail/thumb_up: Persistente (Tendencia robusta, ideal para proyecciones)"
                color = "🟢"
            else:
                estado_hurst = ":material/warning: Paseo Aleatorio (Ventas aleatorias normales)"
                color = "🟡"
                
            st.write(f"### {color} Comportamiento: {estado_hurst} (H ≈ {hurst_val:.2f})")
            st.info("### Si H > 0.65, un día de ventas altas predice otro día de ventas altas. Si H < 0.45, a un día muy bueno le sigue un día muy malo estadísticamente.")
        else:
            st.write("Datos insuficientes para calcular la memoria fractal.")
            
        # Grafico simple de ventas
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_agg['fecha'], y=df_agg['venta'], mode='lines', name='Ventas Diarias', line=dict(color='#00CC96')))
        fig.update_layout(template="plotly_dark", height=300, title="Evolución Histórica de Ventas Agrupadas")
        st.plotly_chart(fig, width='stretch')

st.markdown("---")