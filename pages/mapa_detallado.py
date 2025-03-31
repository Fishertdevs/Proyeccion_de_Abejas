import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
from data.regions import get_risk_regions

st.set_page_config(
    page_title="Mapa Detallado - Impacto de Abejas en Colombia",
    page_icon="🐝",
    layout="wide"
)

# Estilo para mantener consistencia con la página principal
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A7C59;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A7C59;
    }
    .description {
        font-size: 1rem;
        line-height: 1.5;
    }
    .highlight {
        background-color: #4A7C59;
        color: white;
        padding: 0.2rem;
        border-radius: 0.2rem;
    }
    .card {
        background-color: #2D2D2D;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        border: 1px solid #3a3a3a;
    }
    .map-container {
        border: 1px solid #4A7C59;
        border-radius: 0.5rem;
        padding: 5px;
        margin-bottom: 1rem;
    }
    /* Ajustes para el contraste de texto */
    h1, h2, h3, h4, h5, h6, p, li, span {
        color: #F0F0F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>Mapa Detallado de Riesgo en Colombia</h1>", unsafe_allow_html=True)

# Contenido principal
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Análisis de Vulnerabilidad por Región</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Este mapa detallado muestra las regiones de Colombia más vulnerables a la disminución de poblaciones de abejas y otros polinizadores. 
Puede explorar diferentes visualizaciones y filtrar por tipo de riesgo o dependencia de polinizadores.
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Controles
control_col1, control_col2, control_col3 = st.columns(3)
with control_col1:
    map_type = st.selectbox(
        "Tipo de visualización",
        ["Marcadores", "Mapa de calor", "Clusters"],
        index=0
    )

with control_col2:
    risk_filter = st.multiselect(
        "Filtrar por nivel de riesgo",
        ["Alto", "Medio", "Bajo"],
        default=["Alto", "Medio", "Bajo"]
    )

with control_col3:
    dependency_threshold = st.slider(
        "Dependencia mínima de polinizadores (%)",
        min_value=0,
        max_value=100,
        value=30,
        step=5
    )

# Crear el mapa
st.markdown("<div class='map-container'>", unsafe_allow_html=True)

# Obtener datos de regiones
regions = get_risk_regions()

# Filtrar datos según selecciones
filtered_regions = [
    region for region in regions
    if region["risk"] in risk_filter and region["dependency"] >= dependency_threshold
]

# Crear mapa base
m = folium.Map(location=[4.5709, -74.2973], zoom_start=6, tiles='CartoDB dark_matter')

# Agregar visualización según selección
if map_type == "Marcadores":
    for region in filtered_regions:
        # Determinar color basado en riesgo
        if region["risk"] == "Alto":
            color = 'red'
        elif region["risk"] == "Medio":
            color = 'orange'
        else:
            color = 'green'
            
        # Crear popup con información
        popup_content = f"""
        <div style="width: 250px">
            <h4>{region['name']}</h4>
            <p><strong>Nivel de riesgo:</strong> {region['risk']}</p>
            <p><strong>Cultivos principales:</strong> {region['crops']}</p>
            <p><strong>Dependencia de polinizadores:</strong> {region['dependency']}%</p>
            <p><strong>Descripción:</strong> {region['description']}</p>
        </div>
        """
        tooltip = f"{region['name']} - Riesgo: {region['risk']}"
        
        # Añadir marcador
        folium.Marker(
            location=[region['lat'], region['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon='leaf', prefix='fa')
        ).add_to(m)
        
        # Círculo con tamaño proporcional al nivel de dependencia
        folium.Circle(
            radius=region['dependency'] * 500,
            location=[region['lat'], region['lon']],
            color=color,
            fill=True,
            fill_opacity=0.2,
            opacity=0.6,
            weight=1
        ).add_to(m)

elif map_type == "Mapa de calor":
    # Datos para el mapa de calor
    heat_data = [[region['lat'], region['lon'], region['dependency']] for region in filtered_regions]
    
    # Añadir mapa de calor
    HeatMap(
        heat_data,
        radius=15,
        min_opacity=0.4,
        gradient={
            0.4: 'blue',
            0.6: 'lime',
            0.8: 'yellow',
            1.0: 'red'
        },
        blur=10
    ).add_to(m)

elif map_type == "Clusters":
    # Crear clúster de marcadores
    marker_cluster = MarkerCluster().add_to(m)
    
    for region in filtered_regions:
        # Determinar color basado en riesgo
        if region["risk"] == "Alto":
            color = 'red'
        elif region["risk"] == "Medio":
            color = 'orange'
        else:
            color = 'green'
            
        # Crear popup con información
        popup_content = f"""
        <div style="width: 250px">
            <h4>{region['name']}</h4>
            <p><strong>Nivel de riesgo:</strong> {region['risk']}</p>
            <p><strong>Cultivos principales:</strong> {region['crops']}</p>
            <p><strong>Dependencia de polinizadores:</strong> {region['dependency']}%</p>
        </div>
        """
        
        # Añadir marcador al clúster
        folium.Marker(
            location=[region['lat'], region['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=region['name'],
            icon=folium.Icon(color=color, icon='leaf', prefix='fa')
        ).add_to(marker_cluster)

# Mostrar el mapa
st_folium(m, width=1200, height=600)
st.markdown("</div>", unsafe_allow_html=True)

# Análisis adicional
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Análisis Regional</h2>", unsafe_allow_html=True)

# Crear dataframe para análisis
region_df = pd.DataFrame([
    {
        'Región': region['name'],
        'Riesgo': region['risk'],
        'Dependencia (%)': region['dependency'],
        'Cultivos': region['crops']
    }
    for region in regions
])

# Mostrar estadísticas
analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    st.subheader("Regiones por nivel de riesgo")
    risk_counts = region_df['Riesgo'].value_counts()
    st.bar_chart(risk_counts)

with analysis_col2:
    st.subheader("Dependencia promedio por riesgo")
    avg_dependency = region_df.groupby('Riesgo')['Dependencia (%)'].mean().sort_values(ascending=False)
    st.bar_chart(avg_dependency)

# Tabla de datos
st.subheader("Datos detallados por región")
st.dataframe(region_df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Conclusiones y recomendaciones
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Conclusiones y Recomendaciones</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
El análisis del mapa de riesgo muestra que las regiones con mayor vulnerabilidad a la disminución de poblaciones
de abejas se concentran en zonas agrícolas con alta dependencia de polinizadores, principalmente:
</p>

<ul>
    <li><strong>Zona Cafetera (Eje Cafetero):</strong> Alta dependencia para la producción de café de calidad</li>
    <li><strong>Santander:</strong> Cultivos de cacao altamente dependientes de polinizadores especializados</li>
    <li><strong>Antioquia:</strong> Diversidad de cultivos con fuerte dependencia de polinizadores</li>
</ul>

<p class='description'>
Se recomienda implementar estrategias de conservación focalizadas en estas regiones, incluyendo:
</p>

<ol>
    <li>Establecimiento de corredores biológicos entre áreas naturales y zonas agrícolas</li>
    <li>Promoción de prácticas agrícolas amigables con polinizadores</li>
    <li>Programas de monitoreo continuos para evaluar la salud de las poblaciones de abejas</li>
    <li>Sensibilización a agricultores sobre la importancia económica de los polinizadores</li>
</ol>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 20px; padding: 10px; font-size: 0.8rem; border-top: 1px solid #4A7C59; color: #bbb;">
Desarrollado para la conservación de abejas en Colombia | 2025
</div>
""", unsafe_allow_html=True)