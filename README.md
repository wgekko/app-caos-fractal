# Dashboard Analítico Avanzado: Dinámica No Lineal, Teoría del Caos y Econometría

Bienvenido al ecosistema interactivo de análisis predictivo y estructural. Esta aplicación, construida sobre **Streamlit**, representa un puente entre la econometría clásica y la física de los sistemas complejos. 

El objetivo principal de esta plataforma es modelar, diagnosticar y proyectar el comportamiento de variables macroeconómicas críticas (como la relación histórica entre el Dólar y el Índice de Precios al Consumidor - IPC) y variables microeconómicas (volumen de ventas), superando las limitaciones de los modelos lineales tradicionales mediante la integración de la **Teoría del Caos** y la **Geometría Fractal**.

# Fundamentos Teóricos del Ecosistema

Los mercados financieros y la economía no siempre se comportan como sistemas estables y lineales; a menudo presentan turbulencias, ruido y comportamientos caóticos. Este dashboard implementa métricas avanzadas para desentrañar esa complejidad:

* **Geometría Fractal y Dimensión Fractal:** Permite medir la "rugosidad" o complejidad de una serie temporal. A diferencia de la geometría euclidiana, los fractales nos ayudan a entender cómo los patrones del mercado se repiten a diferentes escalas de tiempo (autosimilitud).
* **Memoria del Mercado (Exponente de Hurst):** Un indicador crítico para determinar si una serie de tiempo es un paseo aleatorio puro (ruido blanco), si tiene persistencia (tendencia a continuar en la misma dirección) o si es antipersistente (tendencia a la reversión a la media).
* **Dinámica Simbólica (Neosimbólica):** Transforma series temporales continuas y ruidosas en secuencias discretas de símbolos. Esto permite filtrar el ruido del mercado y analizar la "gramática" subyacente de los movimientos de precios o inflación, evaluando el grado de entropía y desorden del sistema.

# Arquitectura y Módulos de la Aplicación

La plataforma está diseñada con una arquitectura modular. Cuenta con una página de inicio inmersiva (con estética ciberpunk/holográfica mediante inyección de HTML/CSS/JS) que actúa como centro de mando, ramificándose en cuatro motores de análisis independientes:

# Módulo 1: Análisis Neosimbólico y Fractal Base
Este módulo introduce el análisis de series temporales desde una perspectiva no lineal. 
* **Función:** Procesa los datos históricos transformándolos mediante mapeo simbólico.
* **Indicadores:** Calcula métricas de entropía para medir el nivel de estrés del mercado. 
* **Salida visual:** Incorpora un semáforo de estabilidad estructural que diagnostica si el sistema se encuentra en un estado de equilibrio, en alerta temprana de volatilidad, o en pleno caos estructural.

# Módulo 2: Análisis Neosimbólico y Fractal Plus (Avanzado)
Una evolución del Modelo 1, diseñado para usuarios que requieren mayor granularidad en la evaluación de riesgos.
* **Función:** Profundiza en la reconstrucción del espacio de fases de los datos.
* **Indicadores:** Amplía los parámetros de sensibilidad del modelo fractal.
* **Salida visual:** Ofrece tableros de diagnóstico enriquecidos y gráficos de atractores que permiten visualizar visualmente hacia dónde "tira" la tendencia subyacente de la inflación o el tipo de cambio.

# Módulo 3: Análisis Estadístico Clásico (Dólar vs IPC)
Actúa como el "grupo de control" del sistema, aplicando econometría tradicional para contrastar con los modelos no lineales.
* **Función:** Evalúa la relación directa y el rezago entre la emisión/inflación (IPC) y la cotización de la divisa.
* **Indicadores:** Correlación de Pearson, Regresión Lineal Simple y Múltiple, R-Cuadrado y pruebas de significancia (P-Value).
* **Salida visual:** Gráficos de dispersión, líneas de tendencia y análisis de residuos, ideales para reportes ejecutivos tradicionales.

# Módulo 4: Análisis Fractal Aplicado a Ventas
Traslada el poder de la dinámica no lineal desde la macroeconomía hacia la microeconomía y la gestión empresarial.
* **Función:** Analiza el flujo histórico de ventas e inventarios de una compañía.
* **Indicadores:** Utiliza perfiles fractales para determinar si las ventas tienen ciclos predecibles ocultos o si están gobernadas por el azar.
* **Salida visual:** Proyecciones de demanda ajustadas por volatilidad, permitiendo optimizar el stock y reducir costos operativos frente a escenarios inciertos.

---

# Requisitos Técnicos y Entorno de Ejecución

El proyecto está desarrollado enteramente en Python y requiere las siguientes librerías core (ver `requirements.txt` para versiones exactas):

* **Streamlit:** Framework principal para la interfaz de usuario interactiva y el enrutamiento multipágina.
* **Pandas & NumPy:** Motores de cálculo matricial, limpieza y manipulación de DataFrames.
* **SciPy & Scikit-Learn:** Librerías para el procesamiento de señales, cálculo de entropía y modelado estadístico/regresiones.
* **Plotly:** Renderizado de gráficos interactivos de alta calidad.
* **Openpyxl:** Motor necesario para la ingesta de las bases de datos en formato Excel (`.xlsx`).

---

# Guía de Instalación Rápida

Sigue estos pasos para desplegar el ecosistema en tu entorno local:

1. **Clonar el repositorio:**

   git clone [https://github.com/wgekko/app-caos-fractal.git]

video demo



https://github.com/user-attachments/assets/33845385-2169-43f8-bdcd-8dfe2a2f2e57





   
   
