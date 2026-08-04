
import streamlit as st
import geopandas as gpd
import rasterio
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd # Import pandas for data creation

st.set_page_config(layout="wide")
st.title('Dashboard de Análisis de Datos')

st.write('Este es el dashboard para visualizar los análisis de tu notebook.')

# --- Data Loading ---
# Define the path to the GeoTIFF file
geotiff_path = '/content/QUEBRADA LA HONDA.tif'

# Open the GeoTIFF file and read raster data
with rasterio.open(geotiff_path) as src:
    raster_data = src.read(1) # Read the first band
    raster_transform = src.transform
    raster_crs = src.crs
    raster_bounds = src.bounds

# Define the path to the extracted watershed data
extraction_dir = '/content/watershed_data'
shp_file_path = os.path.join(extraction_dir, 'watershed.shp')

# Load the shapefile into a GeoDataFrame
watershed_gdf = gpd.read_file(shp_file_path)

st.success('Datos GeoTIFF y Shapefile cargados exitosamente en el dashboard.')

# --- Implementar Lógica de Análisis y Visualizaciones ---
st.markdown('### Visualización Combinada de Datos Ráster y Vectoriales')

colormaps = ['gray', 'viridis', 'plasma', 'inferno', 'magma', 'cividis']
selected_cmap = st.selectbox('Selecciona un mapa de color para el ráster:', colormaps, key='raster_cmap_dashboard')

# Create a single figure and axes for combined visualization
fig_combined, ax_combined = plt.subplots(1, 1, figsize=(12, 10))

# Display the raster data
imshow_plot = ax_combined.imshow(raster_data, cmap=selected_cmap, extent=[raster_bounds.left, raster_bounds.right, raster_bounds.bottom, raster_bounds.top])
fig_combined.colorbar(imshow_plot, ax=ax_combined, label='Valor del Píxel')

# Overlay the vector data on the same plot
watershed_gdf.plot(ax=ax_combined, color='none', edgecolor='red', alpha=0.8, linewidth=2)

ax_combined.set_title('Visualización Combinada: QUEBRADA LA HONDA.tif y Cuenca')
ax_combined.set_xlabel('Longitud')
ax_combined.set_ylabel('Latitud')

st.pyplot(fig_combined)

# --- Análisis Estadístico del Ráster ---
st.markdown('### Análisis Estadístico del Ráster')

mean_val = np.mean(raster_data)
median_val = np.median(raster_data)
min_val = np.min(raster_data)
max_val = np.max(raster_data)
std_dev_val = np.std(raster_data)

st.write(f"**Valor Medio:** {mean_val:.2f}")
st.write(f"**Mediana:** {median_val:.2f}")
st.write(f"**Valor Mínimo:** {min_val:.2f}")
st.write(f"**Valor Máximo:** {max_val:.2f}")
st.write(f"**Desviación Estándar:** {std_dev_val:.2f}")

# --- Histograma de Valores Ráster ---
st.markdown('### Histograma de Valores Ráster')

fig_hist, ax_hist = plt.subplots(1, 1, figsize=(10, 6))
ax_hist.hist(raster_data.flatten(), bins=50, color='skyblue', edgecolor='black')
ax_hist.set_title('Distribución de Valores de Píxel en el Ráster')
ax_hist.set_xlabel('Valor del Píxel')
ax_hist.set_ylabel('Frecuencia')

st.pyplot(fig_hist)

# --- Gráfica de Barras de Datos de Ejemplo ---
st.markdown('### Gráfica de Barras de Datos de Ejemplo')

# Create some example data for the bar chart
bar_data = pd.DataFrame({
    'Categoría': ['A', 'B', 'C', 'D'],
    'Valor': [10, 20, 15, 25]
})

fig_bar, ax_bar = plt.subplots(1, 1, figsize=(8, 6))
ax_bar.bar(bar_data['Categoría'], bar_data['Valor'], color='lightgreen', edgecolor='black')
ax_bar.set_title('Valores por Categoría')
ax_bar.set_xlabel('Categoría')
ax_bar.set_ylabel('Valor')

st.pyplot(fig_bar)

print("Archivo 'app_dashboard.py' actualizado con visualización combinada, análisis estadístico, histograma y gráfica de barras.")

st.markdown('---')
st.markdown('## Análisis de Cuencas y Pendientes')
st.markdown('### Integración de análisis geoespaciales específicos')
st.write("""
Esta sección está dedicada a la integración de análisis geoespaciales avanzados 
relacionados con cuencas y pendientes. Los resultados y visualizaciones de estos 
análisis se incorporarán aquí en función de los fragmentos de código y las 
especificaciones proporcionadas por el usuario a partir del notebook 
'PROFE_NORMAN_JULIO_26.ipynb'. Se espera que los botones de control para estos 
análisis se añadan en una etapa posterior.
""")

print("Archivo 'app_dashboard.py' actualizado con la nueva sección para Análisis de Cuencas y Pendientes.")


st.markdown('### Controles de Visualización')

show_cuencas_analysis = st.button('Mostrar Análisis de Cuencas')
show_pendientes_analysis = st.button('Mostrar Análisis de Pendientes')

if show_cuencas_analysis:
    st.write('Aquí se mostrará el análisis de cuencas una vez integrado el código de PROFE_NORMAN_JULIO_26.ipynb.')

if show_pendientes_analysis:
    st.write('Aquí se mostrará el análisis de pendientes una vez integrado el código de PROFE_NORMAN_JULIO_26.ipynb.')

print("Archivo 'app_dashboard.py' actualizado con botones para análisis específicos.")

st.markdown('---')
st.markdown('## Análisis de Cuencas y Pendientes')
st.markdown('### Integración de análisis geoespaciales específicos')
st.write("""
Esta sección está dedicada a la integración de análisis geoespaciales avanzados 
relacionados con cuencas y pendientes. Los resultados y visualizaciones de estos 
análisis se incorporarán aquí en función de los fragmentos de código y las 
especificaciones proporcionadas por el usuario a partir del notebook 
'PROFE_NORMAN_JULIO_26.ipynb'. Se espera que los botones de control para estos 
análisis se añadan en una etapa posterior.
""")

print("Archivo 'app_dashboard.py' actualizado con la nueva sección para Análisis de Cuencas y Pendientes.")

st.markdown('### Controles de Visualización')

show_cuencas_analysis = st.button('Mostrar Análisis de Cuencas')
show_pendientes_analysis = st.button('Mostrar Análisis de Pendientes')

if show_cuencas_analysis:
    st.write('Aquí se mostrará el análisis de cuencas una vez integrado el código de PROFE_NORMAN_JULIO_26.ipynb.')

if show_pendientes_analysis:
    st.write('Aquí se mostrará el análisis de pendientes una vez integrado el código de PROFE_NORMAN_JULIO_26.ipynb.')

print("Archivo 'app_dashboard.py' actualizado con botones para análisis específicos.")
