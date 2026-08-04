import streamlit as st
import numpy as np
import pandas as pd
import json

# Configuración de la página
st.set_page_config(
    page_title="SAT - Quebrada La Honda (Interactivo)",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1A365D;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4A5568;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F7FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-header">🌊 Sistema de Alerta Temprana (SAT) Interactivo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Cuenca Quebrada La Honda — Modelo de Evaluación Multicriterio en Tiempo Real</div>', unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/color/96/000000/water-basin.png", width=80)
st.sidebar.title("🎛️ Panel de Control del SAT")
st.sidebar.markdown("Ajuste los parámetros biofísicos e hidroclimáticos para simular el **Índice Global de Riesgo (IGR)**.")

# Sliders para las variables del Cerebro Multicriterio
p_val = st.sidebar.slider("🌧️ Precipitación Diaria (mm/día)", min_value=0.0, max_value=25.0, value=6.5, step=0.1)
c_val = st.sidebar.slider("🌲 Cobertura Arbórea (%)", min_value=0.0, max_value=100.0, value=8.5, step=0.5)
d_val = st.sidebar.selectbox("📉 Nivel de Degradación del Suelo", ["Baja / Estable", "Moderada (Terrazas)", "Alta (Cárcavas activas)"], index=2)
a_val = st.sidebar.slider("🏔️ Cota de Altitud Principal (m s. n. m.)", min_value=1000, max_value=2800, value=2100, step=50)
t_val = st.sidebar.slider("🌡️ Anomalía Térmica (°C)", min_value=-1.0, max_value=4.0, value=2.1, step=0.1)

# Normalización de variables a escala 0 - 10
# 1. Precipitación (P) -> >6.0 mm es crítico (10)
p_norm = min(10.0, (p_val / 6.0) * 8.0)

# 2. Cobertura Arbórea (C) -> Menor cobertura = Mayor riesgo
c_norm = max(0.0, (100.0 - c_val) / 10.0)

# 3. Degradación de Suelos (D)
d_map = {"Baja / Estable": 2.0, "Moderada (Terrazas)": 6.0, "Alta (Cárcavas activas)": 10.0}
d_norm = d_map[d_val]

# 4. Altitud (A) -> >2000 m es crítico (10)
a_norm = min(10.0, (a_val / 2000.0) * 8.5)

# 5. Anomalía Térmica (T) -> >2.0 °C es crítico (10)
t_norm = min(10.0, max(0.0, (t_val / 2.0) * 8.0))

# Pesos Ponderados
W_p, W_d, W_c, W_a, W_t = 0.30, 0.25, 0.20, 0.15, 0.10

# Cálculo del IGR (Índice Global de Riesgo)
igr = (W_p * p_norm) + (W_d * d_norm) + (W_c * c_norm) + (W_a * a_norm) + (W_t * t_norm)
igr = round(min(10.0, igr), 2)

# Determinación del nivel de alerta
if igr <= 2.5:
    nivel = "NORMAL"
    color_code = "#38A169"
    alert_type = "success"
    recomendacion = "Condiciones estables en la cuenca. Mantener monitoreo rutinario."
elif igr <= 5.0:
    nivel = "ATENCIÓN"
    color_code = "#D69E2E"
    alert_type = "info"
    recomendacion = "Precipitación o degradación moderada. Emitir boletín preventivo a la CAR y Municipio."
elif igr <= 7.5:
    nivel = "ALERTA"
    color_code = "#DD6B20"
    alert_type = "warning"
    recomendacion = "Alta probabilidad de escorrentía acelerada. Alistamiento de Comités Locales de Emergencia."
else:
    nivel = "EMERGENCIA"
    color_code = "#E53E3E"
    alert_type = "error"
    recomendacion = "🚨 RIESGO INMINENTE DE DESLIZAMIENTO / CRECIENTE SÚBITA. Activar sirenas y evacuar zonas críticas."

# Métricas Principales en Pantalla
col1, col2, col3, col4 = st.columns(4)
col1.metric("Índice Global de Riesgo (IGR)", f"{igr} / 10.0")
col2.metric("Nivel de Alerta", nivel)
col3.metric("Lluvia Registrada", f"{p_val} mm/día")
col4.metric("Estado del Suelo", d_val.split()[0])

st.markdown("---")

# Banner de Estado del SAT
if alert_type == "success":
    st.success(f"🟢 **ESTADO DEL SAT: {nivel}** (IGR: {igr}) — {recomendacion}")
elif alert_type == "info":
    st.info(f"🟡 **ESTADO DEL SAT: {nivel}** (IGR: {igr}) — {recomendacion}")
elif alert_type == "warning":
    st.warning(f"🟠 **ESTADO DEL SAT: {nivel}** (IGR: {igr}) — {recomendacion}")
else:
    st.error(f"🔴 **ESTADO DEL SAT: {nivel}** (IGR: {igr}) — {recomendacion}")

# Sección de Ponderación e Desglose
st.subheader("📊 Desglose de Contribución por Variable al IGR")

chart_data = pd.DataFrame({
    "Variable": ["Precipitación (30%)", "Degradación Suelos (25%)", "Cobertura Arbórea (20%)", "Altitud (15%)", "Anomalía Térmica (10%)"],
    "Puntaje Normalizado (0-10)": [p_norm, d_norm, c_norm, a_norm, t_norm],
    "Puntos Aportados al IGR": [round(p_norm*W_p, 2), round(d_norm*W_d, 2), round(c_norm*W_c, 2), round(a_norm*W_a, 2), round(t_norm*W_t, 2)]
})

col_chart, col_table = st.columns([3, 2])

with col_chart:
    st.bar_chart(chart_data.set_index("Variable")["Puntos Aportados al IGR"])

with col_table:
    st.dataframe(chart_data, hide_index=True)

# Sección de Simulación Espacial (Mapa Conceptual de Riesgo)
st.subheader("🗺️ Representación Espacial del Riesgo — Quebrada La Honda")

# Generar puntos simulados dentro de la cuenca
np.random.seed(42)
lats = 4.65 + np.random.normal(0, 0.008, 100)
lons = -74.38 + np.random.normal(0, 0.008, 100)
weights = np.random.uniform(igr*0.8, min(10.0, igr*1.2), 100)

map_df = pd.DataFrame({
    'lat': lats,
    'lon': lons,
    'riesgo': weights
})

st.map(map_df, latitude='lat', longitude='lon', size=20, zoom=13)

st.caption("📍 *Puntos de monitoreo simulados a lo largo del cauce principal de la Quebrada La Honda y laderas con cárcavas.*")

st.markdown("---")
st.markdown("##### 📌 Instrucciones para ejecutar en su computador:")
st.code("pip install streamlit pandas numpy\nstreamlit run app_sat_quebrada_honda.py", language="bash")
