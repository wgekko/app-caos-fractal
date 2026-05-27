import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Análisis Neosimbólico y Fractal", layout="wide", page_icon=":material/developer_mode_tv:")
st.title("Análisis Neosimbólico y Fractal (Teoría del Caos)")

# Carga de archivos desde la carpeta local 'data'
def cargar_xlsx(nombre_archivo):
    path = os.path.join("data", nombre_archivo)
    if os.path.exists(path):
        try:
            return pd.read_excel(path)
        except Exception as e:
            st.error(f":material/error: Error al leer el archivo {nombre_archivo}: {e}")
            return None
    else:
        st.warning(f":material/warning: No se encontró el archivo '{nombre_archivo}' en la carpeta 'data/'.")
        return None
    
def calcular_hurst(serie, max_lag=20):
    """Calcula el Exponente de Hurst para evaluar la memoria fractal del mercado."""
    if len(serie) < max_lag + 1:
        return np.nan
    lags = range(2, max_lag)
    # Calculamos la desviación estándar de las diferencias para cada lag
    tau = [np.std(np.subtract(serie.values[lag:], serie.values[:-lag])) for lag in lags]
    # Ajuste lineal en escala log-log para encontrar la pendiente (Hurst)
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0]    

def calcular_rsi(df, col, period=14):
    delta = df[col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- CÁLCULO DE FASE (EL SPIN DE MOVILIDADES) ---
def detectar_fase(df, col):
    if len(df) < 50:
        return "Datos insuficientes (Mínimo 50 registros)", "N/A"
    
    rsi_serie = calcular_rsi(df, col)
    sma_serie = df[col].rolling(window=50).mean()
    
    rsi = rsi_serie.iloc[-1]
    sma = sma_serie.iloc[-1]
    precio = df[col].iloc[-1]
    
    if pd.isna(rsi) or pd.isna(sma):
        return "Calculando estabilidad...", "N/A"
    
    if rsi < 35: 
        return "M (Menesteroso / Acumulación - Inicio desde Cero)", "Inverso al reloj (Reversible)"
    elif rsi >= 35 and rsi < 55 and precio > sma: 
        return "G (Guerrero / Tendencia de Recuperación)", "Sentido del reloj (Irreversible)"
    elif rsi >= 55 and rsi < 75: 
        return "I (Intelectual / Máximo y Distribución)", "Inverso al reloj (Reversible)"
    else:
        return "L (Logrero / Pérdida de Tendencia Alcista)", "Sentido del reloj (Irreversible)"

# --- BARRA LATERAL: SELECCIÓN DE ACTIVOS ---
st.sidebar.subheader(":material/settings: Configuración del Análisis")

archivos_disponibles = {
    "Dólar (Dolar.xlsx)": "Dolar.xlsx",
    "IPC var% (ipc-var.xlsx)": "ipc-var.xlsx"
}

archivo_visual = st.sidebar.selectbox("**:material/select_check_box: Selecciona el Análisis / Archivo a desplegar:**", list(archivos_disponibles.keys()))
archivo_real = archivos_disponibles[archivo_visual]

df = cargar_xlsx(archivo_real)

if df is not None:
    st.sidebar.success(f"Datos de '{archivo_real}' vinculados.")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    all_cols = df.columns.tolist()
    
    st.sidebar.subheader("Mapeo Dinámico de Columnas")
    idx_fecha = 0
    for i, col in enumerate(all_cols):
        if 'fecha' in col.lower() or 'date' in col.lower():
            idx_fecha = i
            break
            
    date_col = st.sidebar.selectbox("**Columna de Fechas**", all_cols, index=idx_fecha, key=f"date_{archivo_real}")
    price_col = st.sidebar.selectbox("**Columna de Precio/Índice**", numeric_cols, key=f"price_{archivo_real}")
    vol_col = st.sidebar.selectbox("**Columna de Volumen (Opcional)**", ["Ninguno"] + numeric_cols, key=f"vol_{archivo_real}")

    if date_col in df.columns and price_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, price_col]).sort_values(by=date_col).reset_index(drop=True)
        
        st.subheader(f"Dashboard Activo: {archivo_visual}")
        
        # --- MÓDULO DE FASE (SPIN) ---
        with st.expander(":material/developer_mode_tv: Módulo de Fase (Spin): Análisis de Arquetipos", expanded=True):
            fase, tipo = detectar_fase(df, price_col)
            c1, c2 = st.columns(2)
            c1.metric("Fase Símbolo Detectada", fase)
            c2.metric("Giro Estructural", tipo)
            st.info(f"""
            **Análisis de Spin Aplicado:**
            - El comportamiento del activo en la variable **'{price_col}'** corresponds a la esquina **{fase}**.
            - **Dinámica del Caos:** {tipo}. Las transformaciones marcadas como *irreversibles* indican puntos de no retorno en la tendencia psicológica colectiva, mientras que las *reversibles* representan zonas de oscilación controlada (soportes y resistencias fractales).
            """)

        # --- MÓDULO 1: LOS 4 FUTUROS ---
        st.header("1. Los 4 Futuros (Esperanza Matemática)")
        if len(df) >= 11:
            ultimos_11 = df.tail(11).copy()
            ultimos_11['Variacion'] = ultimos_11[price_col].pct_change().abs()
            variabilidad = ultimos_11['Variacion'].mean()
            precio_actual = df.iloc[-1][price_col]
            
            f1_baja = precio_actual * (1 - variabilidad)
            f2_baja_doble = precio_actual * (1 - 2 * variabilidad)
            f3_alza = precio_actual * (1 + variabilidad)
            f4_alza_doble = precio_actual * (1 + 2 * variabilidad)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("1ª Baja (Var)", f"{f1_baja:,.2f}")
            col2.metric("2ª Baja (Doble)", f"{f2_baja_doble:,.2f}")
            col3.metric("1ª Alza (Var)", f"{f3_alza:,.2f}")
            col4.metric("2ª Alza (Doble)", f"{f4_alza_doble:,.2f}")
        else:
            st.warning("Se requieren al menos 11 filas.")

        st.markdown("---")
        
        # --- MÓDULO 2: PROBABILIDAD FRACTAL (0.636) ---
        st.header("2. Probabilidad Fractal (0.636) y Máquina de Catástrofes")
        max_window = min(len(df), 200)
        if max_window > 10:
            window = st.slider("Ventana retrospectiva", 10, max_window, min(50, max_window), key=f"win_{archivo_real}")
            df_window = df.tail(window)
            p_max = df_window[price_col].max()
            p_min = df_window[price_col].min()
            rango_tendencia = p_max - p_min
            nivel_retroceso_fractal = p_max - (rango_tendencia * 0.636)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_window[date_col], y=df_window[price_col], mode='lines', name=price_col, line=dict(color='#00CC96')))
            fig.add_hline(y=nivel_retroceso_fractal, line_dash="dot", line_color="red")
            fig.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig, width='stretch')

        st.markdown("---")

        # --- MÓDULO 3: RED FLAGS (CAOS 33°) - TOTALMENTE POTENCIADO ---
        st.header("3. Red Flags y Atractor Estructural del Caos")
        
        if len(df) > 20:
            delta = df[price_col].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            
            max_fuerza = max(gain.max(), loss.max()) if max(gain.max(), loss.max()) > 0 else 1
            grados_dinero = (gain / max_fuerza) * 180
            grados_papel = (loss / max_fuerza) * 180
            
            # NUEVO CÁLCULO: Eficiencia Fractal de Kaufman
            window_er = 14
            desplazamiento_neto = df[price_col].diff(window_er).abs()
            ruido_acumulado = df[price_col].diff().abs().rolling(window=window_er).sum()
            eficiencia_fractal = (desplazamiento_neto / ruido_acumulado).fillna(0.5)
            
            ult_dinero = grados_dinero.iloc[-1]
            ult_papel = grados_papel.iloc[-1]
            ult_eficiencia = eficiencia_fractal.iloc[-1]
            
            # Despliegue de métricas principales
            c_red1, c_red2, c_red3 = st.columns(3)
            c_red1.metric("Grados de Dinero (Compradores)", f"{ult_dinero:.1f}°")
            c_red2.metric("Grados de Papel (Vendedores)", f"{ult_papel:.1f}°")
            
            # Interpretación del nuevo cálculo de eficiencia
            if ult_eficiencia < 0.18:
                c_red3.metric("Eficiencia Estructural", f"{ult_eficiencia:.2%}", delta="RUIDO CRÍTICO / CAOS", delta_color="inverse")
            else:
                c_red3.metric("Eficiencia Estructural", f"{ult_eficiencia:.2%}", delta="Estructura Estable", delta_color="normal")

            # Alertas Dinámicas combinadas
            if ult_dinero > 33 and ult_papel > 33:
                st.error(f":material/flag: **RED FLAG DETECTADA (Caos Angular):** Dinero ({ult_dinero:.1f}°) y Papel ({ult_papel:.1f}°) superan los 33°. El sistema colapsa en ruido estadístico.")
            elif ult_eficiencia < 0.15:
                st.warning(f":material/warning: **RED FLAG DE COMPRESIÓN Fractal:** La eficiencia estructural es críticamente baja ({ult_eficiencia:.2%}). Se está gestando una catástrofe de precios por acumulación de energía caótica.")
            else:
                st.success(":material/check_box: **ORDEN DINÁMICO:** Los vectores de fuerza y eficiencia permanecen bajo parámetros predictivos.")

            # --- GRÁFICO DE CUADRANTES (ATRACTOR DEL CAOS) ---
            st.subheader(":material/map:  Mapa de Fases Angular: Atractor Dinero vs. Papel")
            
            df_trayectoria = pd.DataFrame({
                'Dinero': grados_dinero,
                'Papel': grados_papel,
                'Fecha': df[date_col].dt.strftime('%Y-%m-%d')
            }).tail(40).dropna()
            
            fig_quad = go.Figure()
            
            fig_quad.add_trace(go.Scatter(
                x=df_trayectoria['Dinero'], 
                y=df_trayectoria['Papel'],
                mode='lines+markers',
                name='Historial de Energía (Últimos 40p)',
                line=dict(color='rgba(0, 204, 150, 0.6)', width=2, shape='spline'),
                marker=dict(size=6, color='rgba(255, 255, 255, 0.5)'),
                text=df_trayectoria['Fecha'],
                hoverinfo='text+x+y'
            ))
            
            fig_quad.add_trace(go.Scatter(
                x=[ult_dinero], y=[ult_papel],
                mode='markers',
                name='ESTADO ACTUAL',
                marker=dict(color='#FF4B4B', size=14, symbol='diamond', line=dict(color='white', width=2))
            ))
            
            fig_quad.add_vline(x=33, line_dash="dash", line_color="rgba(255, 75, 75, 0.5)", line_width=1.5)
            fig_quad.add_hline(y=33, line_dash="dash", line_color="rgba(255, 75, 75, 0.5)", line_width=1.5)
            
            fig_quad.update_layout(
                template="plotly_dark",
                xaxis=dict(title="Fuerza del Dinero (Grados X)", range=[0, max(60, ult_dinero + 10)]),
                yaxis=dict(title="Fuerza del Papel (Grados Y)", range=[0, max(60, ult_papel + 10)]),
                height=450,
                annotations=[
                    dict(x=10, y=10, text="<b>Apatía / Compresión</b>", showarrow=False, font=dict(color="gray", size=16)),
                    dict(x=45, y=10, text="<b>Estructura Alcista</b>", showarrow=False, font=dict(color="#00CC96", size=16)),
                    dict(x=10, y=45, text="<b>Estructura Bajista</b>", showarrow=False, font=dict(color="#636EFA", size=16)),
                    dict(x=45, y=45, text="<b>ZONA RED FLAG (CAOS)</b>", showarrow=False, font=dict(color="#FF4B4B", size=16))
                ]
            )
            st.plotly_chart(fig_quad, width='stretch')
        else:
            st.warning(":material/warning: Historial cronológico insuficiente para mapear Red Flags.")

        st.markdown("---")

        # --- NUEVO MÓDULO 4: RECONSTRUCCIÓN DEL ESPACIO DE FASES (ATRACTOR OCULTO) ---
        # st.header("4. Atractor en el Espacio de Fases (Caos Determinista)")
        # st.markdown("""
        # En los sistemas caóticos, el ruido aparente esconde una geometría ordenada de largo plazo. 
        # Graficando la variable en el tiempo $t$ contra su valor en un retraso temporal $t - \\tau$, podemos visualizar el **Atractor Extraño** del activo.
        # """)
        
        # col_param1, col_param2 = st.columns(2)
        # with col_param1:
        #     tau = col_param2.slider("Retraso Temporal (Lag $\\tau$)", 1, 12, 1, key=f"lag_phase_{archivo_real}")
        #     puntos_atractor = col_param1.slider("Cantidad de puntos históricos a mapear", 30, len(df), min(120, len(df)), key=f"pts_phase_{archivo_real}")
        
        # df_phase = df.tail(puntos_atractor).copy()
        # df_phase['Lagged_Price'] = df_phase[price_col].shift(tau)
        # df_phase = df_phase.dropna()
        
        # fig_phase = go.Figure()
        # # Línea temporal que une los estados del sistema
        # fig_phase.add_trace(go.Scatter(
        #     x=df_phase['Lagged_Price'],
        #     y=df_phase[price_col],
        #     mode='lines+markers',
        #     name='Órbita Dinámica',
        #     line=dict(color='#636EFA', width=1.5),
        #     marker=dict(size=5, color='#00CC96', opacity=0.7),
        #     text=df_phase[date_col].dt.strftime('%Y-%m-%d'),
        #     hoverinfo='text+x+y'
        # ))
        # # Destacar el punto actual del sistema
        # fig_phase.add_trace(go.Scatter(
        #     x=[df_phase['Lagged_Price'].iloc[-1]],
        #     y=[df_phase[price_col].iloc[-1]],
        #     mode='markers',
        #     name='Estado Actual (Presente)',
        #     marker=dict(color='#FF4B4B', size=12, symbol='circle')
        # ))
        
        # fig_phase.update_layout(
        #     template="plotly_dark",
        #     xaxis=dict(title=f"Valor Retrasado: X(t - {tau})"),
        #     yaxis=dict(title="Valor Actual: X(t)"),
        #     height=500,
        #     title=f"Espacio de Fases Reconstruido para {price_col}"
        # )
        # st.plotly_chart(fig_phase, width='stretch')
        
        # st.info("""
        # 💡 **¿Cómo interpretar este Atractor?**
        # - **Estructura en Diagonal Limpia:** Indica una inercia muy alta (común en el IPC por arrastre inflacionario o en el Dólar en tendencias fuertes).
        # - **Espirales o Bucles:** Revelan ciclos ocultos y oscilaciones dinámicas recurrentes (cambios de régimen).
        # - **Nube amorfa de puntos:** Representa ruido puramente aleatorio y falta de causalidad temporal.
        # """)
# --- NUEVO MÓDULO 4: RECONSTRUCCIÓN DEL ESPACIO DE FASES (ATRACTOR OCULTO) ---
        st.header("4. Atractor en el Espacio de Fases (Caos Determinista)")
        st.markdown("""
        En los sistemas caóticos, el ruido aparente esconde una geometría ordenada de largo plazo. 
        Graficando la variable en el tiempo $t$ contra su valor en un retraso temporal $t - \\tau$, podemos visualizar el **Atractor Extraño** del activo.
        """)
        
        col_param1, col_param2 = st.columns(2)
        with col_param1:
            puntos_atractor = col_param1.slider("Cantidad de puntos históricos a mapear", 30, len(df), min(120, len(df)), key=f"pts_phase_{archivo_real}")
        with col_param2:
            tau = col_param2.slider("Retraso Temporal (Lag $\\tau$)", 1, 12, 1, key=f"lag_phase_{archivo_real}")
        
        df_phase = df.tail(puntos_atractor).copy()
        df_phase['Lagged_Price'] = df_phase[price_col].shift(tau)
        df_phase = df_phase.dropna()
        
        # VALIDACIÓN: Evita que el sistema colapse si el dataframe se queda vacío
        if df_phase.empty or len(df_phase) < 2:
            st.warning(":material/warning: **Datos insuficientes para el Atractor:** El retraso (Lag) seleccionado es demasiado grande para la cantidad de puntos históricos. Por favor, disminuye el Lag o aumenta los puntos a mapear.")
        else:
            fig_phase = go.Figure()
            # Línea temporal que une los estados del sistema
            fig_phase.add_trace(go.Scatter(
                x=df_phase['Lagged_Price'],
                y=df_phase[price_col],
                mode='lines+markers',
                name='Órbita Dinámica',
                line=dict(color='#636EFA', width=1.5),
                marker=dict(size=5, color='#00CC96', opacity=0.7),
                text=df_phase[date_col].dt.strftime('%Y-%m-%d'),
                hoverinfo='text+x+y'
            ))
            # Destacar el punto actual del sistema (Ahora protegido)
            fig_phase.add_trace(go.Scatter(
                x=[df_phase['Lagged_Price'].iloc[-1]],
                y=[df_phase[price_col].iloc[-1]],
                mode='markers',
                name='Estado Actual (Presente)',
                marker=dict(color='#FF4B4B', size=12, symbol='circle')
            ))
            
            fig_phase.update_layout(
                template="plotly_dark",
                xaxis=dict(title=f"Valor Retrasado: X(t - {tau})"),
                yaxis=dict(title="Valor Actual: X(t)"),
                height=500,
                title=f"Espacio de Fases Reconstruido para {price_col}"
            )
            st.plotly_chart(fig_phase, width='stretch')
            
            st.info("""
            💡 **¿Cómo interpretar este Atractor?**
            - **Estructura en Diagonal Limpia:** Indica una inercia muy alta (común en el IPC por arrastre inflacionario o en el Dólar en tendencias fuertes).
            - **Espirales o Bucles:** Revelan ciclos ocultos y oscilaciones dinámicas recurrentes (cambios de régimen).
            - **Nube amorfa de puntos:** Representa ruido puramente aleatorio y falta de causalidad temporal.
            """)


        st.markdown("---")

        # --- MÓDULO 5: SÍNTESIS GLOBAL Y MEMORIA FRACTAL (ACTUALIZADO) ---
        st.header("5. Veredicto del Sistema: Semáforo de Riesgo Global")
        
        hurst_val = calcular_hurst(df[price_col])
        dim_fractal = 2 - hurst_val if not np.isnan(hurst_val) else np.nan
        
        nivel_riesgo = 0
        razones_riesgo = []
        
        if 'nivel_retroceso_fractal' in locals() and df.iloc[-1][price_col] < nivel_retroceso_fractal:
            nivel_riesgo += 2
            razones_riesgo.append("Ruptura del umbral fractal del 0.636.")
            
        if 'ult_dinero' in locals() and 'ult_papel' in locals():
            if ult_dinero > 33 and ult_papel > 33:
                nivel_riesgo += 2
                razones_riesgo.append("Colisión de fuerzas (>33°). Entropía de mercado.")
                
        if 'ult_eficiencia' in locals() and ult_eficiencia < 0.18:
            nivel_riesgo += 1
            razones_riesgo.append("Baja eficiencia estructural (Mucha compresión/ruido).")
            
        if not np.isnan(hurst_val):
            if hurst_val < 0.45:
                nivel_riesgo += 1
                razones_riesgo.append(f"### Antipersistencia (H={hurst_val:.2f}).")
                estado_hurst = "### Antipersistente (Reversión violenta)"
            elif hurst_val > 0.65:
                estado_hurst = "### Persistente (Tendencia Robusta)"
            else:
                estado_hurst = "### Paseo Aleatorio (Ruido Estándar)"
        else:
            estado_hurst = "### Datos insuficientes para Hurst"

        st.write("### Estado Estructural del Activo")
        col_res1, col_res2 = st.columns([1, 2])
        
        with col_res1:
            if nivel_riesgo == 0:
                st.success("### 🟢 **SISTEMA ESTABLE**")
                st.write("### El activo opera bajo geometrías predecibles.")
            elif nivel_riesgo <= 2:
                st.warning("### 🟡 **ALERTA TEMPRANA**")
                st.write("### Se detectan anomalías en la estructura del precio.")
            else:
                st.error("### 🔴 **CAOS ESTRUCTURAL**")
                st.write("### Riesgo inminente. Pérdida de memoria del mercado.")
                
        with col_res2:
            st.info(f"### Análisis de Memoria (Exponente de Hurst): {estado_hurst} (H ≈ {hurst_val:.2f})")
            if not np.isnan(dim_fractal):
                st.metric("Dimensión Fractal Calculada (D)", f"{dim_fractal:.2f}", 
                          help="Mide la complejidad geométrica de la serie temporal. Valores más altos implican mayor impredecibilidad.")
            
            if razones_riesgo:
                st.write("### Desencadenantes de Riesgo Detectados: ")
                for razon in razones_riesgo:
                    st.write(f"### - :material/flag_circle: {razon}")
            else:
                st.write("### Observaciones: No se registran vulneraciones matemáticas en los marcos de tiempo analizados.")

st.markdown("---")