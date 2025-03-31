import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from models import (
    calculate_biodiversity_impact, 
    calculate_crop_production, 
    create_ecosystem_simulation
)
from visualizations import (
    plot_bee_crop_relationship,
    plot_bee_crop_relationship_3d,
    plot_biodiversity_impact,
    plot_biodiversity_impact_3d,
    plot_timeseries_forecast,
    create_risk_map
)
from data_module import get_initial_data
from utils import get_emoji, add_vertical_space

# Page configuration
st.set_page_config(
    page_title="Simulador de Impacto de Abejas en Colombia",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para tema oscuro/verde
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
    .info-box {
        background-color: #1E1E1E;
        border-left: 4px solid #4A7C59;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        text-align: center;
        border: 1px solid #4A7C59;
    }
    
    /* Estilo para los botones y widgets */
    .stButton button {
        background-color: #4A7C59 !important;
        color: white !important;
        border: none !important;
    }
    
    .stSlider .stSlider-track {
        background-color: #4A7C59 !important;
    }
    
    /* Footer personalizado */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1E1E1E;
        padding: 10px;
        text-align: center;
        border-top: 1px solid #4A7C59;
        font-size: 0.8rem;
    }
    
    /* Estilos para el dashboard */
    .dashboard-header {
        background-color: #4A7C59;
        padding: 10px;
        border-radius: 5px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .dashboard-card {
        background-color: #2D2D2D;
        border: 1px solid #4A7C59;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* Ajustes para el contraste de texto */
    h1, h2, h3, h4, h5, h6, p, li, span {
        color: #F0F0F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Toggle para cambiar entre modo claro y oscuro (predeterminado: oscuro) - Futuro
theme_mode = "oscuro"  # No implementado todavía, pero preparado para una versión futura

# Header
st.markdown(f"<h1 class='main-header'>{get_emoji('bee')} Impacto de la Reducción de Abejas en Ecosistemas de Colombia</h1>", unsafe_allow_html=True)

# Introduction
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Sobre esta aplicación</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p class='description'>
    Esta aplicación modela el impacto crítico de la disminución de las poblaciones de abejas en la biodiversidad y la producción agrícola en Colombia. 
    A través de visualizaciones interactivas y modelos matemáticos, podrás explorar cómo los cambios en las poblaciones de polinizadores 
    afectan a los ecosistemas y a la producción de alimentos en las diferentes regiones del país.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
    <p>Las abejas y otros polinizadores son responsables de la reproducción de aproximadamente el 
    <span class='highlight'>80% de las especies de plantas con flores</span> y del 
    <span class='highlight'>35% de la producción agrícola mundial</span>, con un valor económico estimado de 
    <span class='highlight'>235-577 mil millones de dólares anuales</span>.
    </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main content in two columns
col1, col2 = st.columns([2, 3])

# Left column - Controls and information
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Controles de Simulación</h2>", unsafe_allow_html=True)
    
    # Slider for bee population adjustment
    bee_population_percentage = st.slider(
        "Porcentaje de población de abejas respecto al nivel óptimo",
        min_value=10,
        max_value=100,
        value=100,
        step=5,
        help="Ajusta el porcentaje de la población de abejas para ver el impacto"
    )
    
    # Additional parameters
    st.markdown("<h3>Parámetros adicionales</h3>", unsafe_allow_html=True)
    
    selected_region = st.selectbox(
        "Región de Colombia",
        options=["Todas las regiones", "Zona Cafetera", "Valle del Cauca", "Antioquia", "Santander", 
                "Boyacá", "Cundinamarca", "Huila", "Cauca", "Amazonia"],
        help="Selecciona una región específica para analizar"
    )
    
    years_to_simulate = st.slider(
        "Años a simular",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )
    
    ecosystem_resilience = st.select_slider(
        "Resiliencia del ecosistema",
        options=["Muy baja", "Baja", "Media", "Alta", "Muy alta"],
        value="Media",
        help="Capacidad del ecosistema para adaptarse a cambios en los polinizadores"
    )
    
    cultivation_type = st.radio(
        "Tipo de cultivo",
        options=["Todos", "Café", "Frutales", "Hortalizas", "Cereales"],
        horizontal=True,
        help="Tipo de cultivo para enfocar el análisis"
    )
    
    # Convert resilience to numerical value for calculations
    resilience_mapping = {
        "Muy baja": 0.2,
        "Baja": 0.4,
        "Media": 0.6,
        "Alta": 0.8,
        "Muy alta": 1.0
    }
    resilience_value = resilience_mapping[ecosystem_resilience]
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Importance of pollinators section
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Importancia de los Polinizadores</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p class='description'>
    Los polinizadores, especialmente las abejas, son fundamentales para:
    </p>
    <ul>
        <li><strong>Biodiversidad:</strong> La polinización permite la reproducción de numerosas especies vegetales, manteniendo la diversidad de ecosistemas.</li>
        <li><strong>Agricultura:</strong> Muchos cultivos dependen directamente de la polinización por insectos.</li>
        <li><strong>Economía:</strong> El valor económico de la polinización es enorme en términos de producción agrícola.</li>
        <li><strong>Equilibrio ecológico:</strong> Los polinizadores son parte de cadenas alimenticias complejas.</li>
    </ul>
    """, unsafe_allow_html=True)
    
    with st.expander("¿Por qué están disminuyendo las poblaciones de abejas?"):
        st.markdown("""
        <p class='description'>
        Las principales amenazas para las poblaciones de abejas incluyen:
        </p>
        <ul>
            <li><strong>Pesticidas y agroquímicos</strong>: Especialmente los neonicotinoides.</li>
            <li><strong>Pérdida de hábitat</strong>: Debido a la urbanización y agricultura intensiva.</li>
            <li><strong>Cambio climático</strong>: Altera los ciclos de floración y comportamiento de las abejas.</li>
            <li><strong>Parásitos y enfermedades</strong>: Como el ácaro Varroa y diversos patógenos.</li>
            <li><strong>Monocultivos</strong>: Reducen la diversidad de fuentes de alimentación.</li>
        </ul>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Right column - Visualizations
with col2:
    # Calculate impacts based on the slider and parameters
    biodiversity_impact = calculate_biodiversity_impact(bee_population_percentage, resilience_value)
    crop_production_impact = calculate_crop_production(bee_population_percentage)
    ecosystem_data = create_ecosystem_simulation(bee_population_percentage, years_to_simulate, resilience_value)
    
    # Metrics display
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Impacto Calculado</h2>", unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        # Adjust impact based on selected crop type
        crop_modifier = 1.0
        if cultivation_type == "Café":
            crop_modifier = 1.2  # Café tiene alta dependencia
        elif cultivation_type == "Frutales":
            crop_modifier = 1.15  # Frutales también alta dependencia
        elif cultivation_type == "Hortalizas":
            crop_modifier = 0.9  # Hortalizas dependencia variable
        elif cultivation_type == "Cereales":
            crop_modifier = 0.6  # Cereales menor dependencia
            
        adjusted_crop_impact = min(100, crop_production_impact * crop_modifier)
        
        st.metric(
            label="Producción Agrícola",
            value=f"{adjusted_crop_impact:.1f}%",
            delta=f"{adjusted_crop_impact - 100:.1f}%" if bee_population_percentage < 100 else None,
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        # Adjust biodiversity impact based on selected region
        region_modifier = 1.0
        region_name = "Colombia"
        
        if selected_region == "Zona Cafetera":
            region_modifier = 1.15
            region_name = "Eje Cafetero"
        elif selected_region == "Valle del Cauca":
            region_modifier = 1.1
            region_name = "Valle del Cauca"
        elif selected_region == "Antioquia":
            region_modifier = 1.2
            region_name = "Antioquia"
        elif selected_region == "Amazonia":
            region_modifier = 1.3
            region_name = "Amazonia"
        
        adjusted_biodiversity = biodiversity_impact * region_modifier
        adjusted_biodiversity = min(100, adjusted_biodiversity)
        
        st.metric(
            label=f"Biodiversidad en {region_name}",
            value=f"{adjusted_biodiversity:.1f}%",
            delta=f"{adjusted_biodiversity - 100:.1f}%" if bee_population_percentage < 100 else None,
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        # Adjust species at risk based on region
        base_species = 20000  # Especies estimadas en Colombia
        if selected_region != "Todas las regiones":
            if selected_region == "Amazonia":
                base_species = 8000
            elif selected_region in ["Antioquia", "Cauca"]:
                base_species = 5000
            else:
                base_species = 3000
                
        species_at_risk = int(max(0, 100 - bee_population_percentage) * 0.2 * base_species / 100)
        
        st.metric(
            label="Especies en Riesgo",
            value=f"{species_at_risk:,}",
            delta=f"+{species_at_risk}" if bee_population_percentage < 100 else "0",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Add economic impact metric
    st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
    metric_col4, metric_col5 = st.columns(2)
    
    with metric_col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        # Economic impact in millions of dollars
        economic_base = 2800  # Millones de dólares como base
        if selected_region != "Todas las regiones":
            if selected_region in ["Zona Cafetera", "Antioquia"]:
                economic_base = 950
            elif selected_region == "Valle del Cauca":
                economic_base = 850
            else:
                economic_base = 450
        
        economic_loss = economic_base * (max(0, 100 - bee_population_percentage) / 100)
        
        st.metric(
            label="Impacto Económico Estimado",
            value=f"${economic_loss:.1f}M USD",
            delta=f"-${economic_loss:.1f}M" if bee_population_percentage < 100 else "0",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with metric_col5:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        # Employment impact
        jobs_base = 800000  # Empleos base impactados
        if selected_region != "Todas las regiones":
            if selected_region in ["Zona Cafetera", "Antioquia"]:
                jobs_base = 250000
            elif selected_region == "Valle del Cauca":
                jobs_base = 200000
            else:
                jobs_base = 100000
                
        jobs_affected = int(jobs_base * (max(0, 100 - bee_population_percentage) / 100) * 0.7)
        
        st.metric(
            label="Empleos Potencialmente Afectados",
            value=f"{jobs_affected:,}",
            delta=f"-{jobs_affected:,}" if bee_population_percentage < 100 else "0",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Visualizations
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Relación Abejas - Producción Agrícola</h2>", unsafe_allow_html=True)
    
    # Selector para tipo de visualización (2D o 3D)
    crop_viz_type = st.radio(
        "Selecciona tipo de visualización",
        options=["Gráfico 2D", "Modelo 3D con Animación"],
        horizontal=True,
        key="crop_viz_type"
    )
    
    if crop_viz_type == "Gráfico 2D":
        # Create plot of bee-crop relationship
        fig_relationship = plot_bee_crop_relationship(bee_population_percentage)
        st.plotly_chart(fig_relationship, use_container_width=True)
        
        # Add explanation
        st.markdown("""
        <p class='description'>
        El gráfico muestra la relación no lineal entre la población de abejas y la producción agrícola. 
        Conforme la población de abejas disminuye, el impacto en la producción se acelera, 
        demostrando la vital importancia de estos polinizadores para nuestra seguridad alimentaria.
        </p>
        """, unsafe_allow_html=True)
    else:
        # Create 3D animated plot
        fig_relationship_3d = plot_bee_crop_relationship_3d(bee_population_percentage, years_to_simulate)
        st.plotly_chart(fig_relationship_3d, use_container_width=True)
        
        # Add explanation for 3D visualization
        st.markdown("""
        <p class='description'>
        Esta visualización 3D muestra la relación entre población de abejas, tiempo y producción agrícola. 
        La superficie representa cómo cambia la producción a lo largo del tiempo para diferentes niveles de población de abejas.
        El marcador rojo indica el punto actual de acuerdo a tus parámetros seleccionados.
        </p>
        
        <div style="background-color: #4A7C59; border-radius: 5px; padding: 10px; margin-top: 15px; text-align: center;">
        <p style="color: white !important; margin: 0; font-weight: bold;">📱 Controles de animación</p>
        <p style="color: white !important; margin: 0; font-size: 0.9rem;">Usa los botones de reproducción debajo del gráfico para ver cómo evoluciona el sistema en el tiempo.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Biodiversity impact visualizations with both 2D and 3D options
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Impacto en Biodiversidad: Visualización Interactiva</h2>", unsafe_allow_html=True)
    
    # Selector para tipo de visualización (2D o 3D)
    viz_type = st.radio(
        "Tipo de visualización",
        options=["Gráfico 2D por Ecosistema", "Modelo 3D Interactivo"],
        horizontal=True,
        key="biodiversity_viz_type"
    )
    
    if viz_type == "Gráfico 2D por Ecosistema":
        fig_biodiversity = plot_biodiversity_impact(bee_population_percentage, resilience_value)
        st.plotly_chart(fig_biodiversity, use_container_width=True)
        
        st.markdown("""
        <p class='description'>
        Diferentes ecosistemas son afectados de manera distinta por la disminución de polinizadores. 
        Algunos ecosistemas son naturalmente más resilientes, mientras que otros pueden colapsar rápidamente 
        ante la pérdida de especies clave como las abejas.
        </p>
        """, unsafe_allow_html=True)
    else:
        # Mostrar visualización 3D
        fig_biodiversity_3d = plot_biodiversity_impact_3d(bee_population_percentage, resilience_value)
        st.plotly_chart(fig_biodiversity_3d, use_container_width=True)
        
        st.markdown("""
        <p class='description'>
        Este modelo 3D muestra la relación entre la población de abejas, la resiliencia del ecosistema y el impacto 
        en la biodiversidad. Puedes rotar, hacer zoom y explorar el modelo para entender mejor cómo interactúan estas variables.
        
        <ul>
            <li>Eje X: Población de abejas (%)</li>
            <li>Eje Y: Resiliencia del ecosistema</li>
            <li>Eje Z: Biodiversidad (%)</li>
        </ul>
        
        El punto rojo muestra los valores actuales según tus parámetros seleccionados.
        </p>
        """, unsafe_allow_html=True)
        
        # Añadir animación explicativa
        st.markdown("""
        <div style="background-color: #4A7C59; border-radius: 5px; padding: 10px; margin-top: 15px; text-align: center;">
        <p style="color: white !important; margin: 0; font-weight: bold;">💡 Interactúa con el modelo 3D:</p>
        <p style="color: white !important; margin: 0; font-size: 0.9rem;">• Haz clic y arrastra para rotar • Usa la rueda del ratón para hacer zoom • Doble clic para restablecer la vista</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Time series forecast
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Proyección a Futuro</h2>", unsafe_allow_html=True)
    
    fig_forecast = plot_timeseries_forecast(ecosystem_data)
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    st.markdown("""
    <p class='description'>
    Esta proyección muestra el posible impacto a largo plazo de mantener la población de abejas en el nivel seleccionado.
    Los efectos se acumulan con el tiempo, pudiendo llevar a puntos de inflexión ecológicos después de varios años.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Optional interactive map
add_vertical_space(2)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Mapa de Riesgo: Zonas vulnerables por pérdida de polinizadores</h2>", unsafe_allow_html=True)

map_col1, map_col2 = st.columns([3, 2])

with map_col1:
    risk_map = create_risk_map(bee_population_percentage)
    st_folium(risk_map, width=700, height=500)

with map_col2:
    st.markdown("""
    <p class='description'>
    Este mapa muestra las regiones más vulnerables a la disminución de polinizadores, basado en:
    </p>
    <ul>
        <li>Dependencia agrícola de polinizadores</li>
        <li>Biodiversidad actual</li>
        <li>Uso de pesticidas</li>
        <li>Cambio climático proyectado</li>
    </ul>
    <p class='description'>
    Las zonas coloreadas en <span style="color: red; font-weight: bold;">rojo</span> son las más vulnerables,
    mientras que las áreas en <span style="color: green; font-weight: bold;">verde</span> tienen mayor resiliencia
    o menor dependencia de polinizadores.
    </p>
    """, unsafe_allow_html=True)
    
    st.warning("""
    **Nota:** Las regiones de alta biodiversidad y con importante producción agrícola dependiente de polinizadores
    son las más afectadas por la disminución de las poblaciones de abejas.
    """)
st.markdown("</div>", unsafe_allow_html=True)

# Recommendations section
add_vertical_space(2)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>¿Qué podemos hacer?</h2>", unsafe_allow_html=True)

recommendations_col1, recommendations_col2 = st.columns(2)

with recommendations_col1:
    st.markdown("""
    <h3>A nivel individual:</h3>
    <ul>
        <li>Plantar flores nativas atractivas para polinizadores</li>
        <li>Evitar el uso de pesticidas en jardines y huertos</li>
        <li>Crear hábitats para abejas en espacios urbanos</li>
        <li>Consumir miel de productores locales y sostenibles</li>
        <li>Educar a otros sobre la importancia de los polinizadores</li>
    </ul>
    """, unsafe_allow_html=True)

with recommendations_col2:
    st.markdown("""
    <h3>A nivel colectivo/político:</h3>
    <ul>
        <li>Prohibir pesticidas dañinos para polinizadores</li>
        <li>Incentivar prácticas agrícolas amigables con polinizadores</li>
        <li>Crear corredores ecológicos para especies polinizadoras</li>
        <li>Financiar investigación sobre salud de abejas y otros polinizadores</li>
        <li>Implementar programas de monitoreo de poblaciones de abejas</li>
    </ul>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer with references
add_vertical_space(2)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Referencias</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Esta aplicación se basa en datos y modelos de las siguientes fuentes:
</p>
<ul>
    <li>IPBES (2016). The assessment report of the Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services on pollinators, pollination and food production.</li>
    <li>Klein, A. M. et al. (2007). Importance of pollinators in changing landscapes for world crops. Proceedings of the Royal Society B, 274(1608), 303-313.</li>
    <li>Potts, S. G. et al. (2016). Safeguarding pollinators and their values to human well-being. Nature, 540(7632), 220-229.</li>
    <li>FAO (2018). Why Bees Matter: The importance of bees and other pollinators for food and agriculture.</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Crear dashboard de resumen
st.markdown("<div class='dashboard-header'>Dashboard Interactivo de Impacto</div>", unsafe_allow_html=True)

# Nueva sección para un panel de control
dashboard_container = st.container()
with dashboard_container:
    # Crear pestañas para el dashboard
    dashboard_tab1, dashboard_tab2, dashboard_tab3 = st.tabs(["Resumen", "Datos por Región", "Recomendaciones"])
    
    with dashboard_tab1:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Resumen de Impacto")
        
        # Resumen visual de impacto 
        impact_summary_cols = st.columns(3)
        with impact_summary_cols[0]:
            st.metric("Impacto Promedio en Cultivos", f"{crop_production_impact:.1f}%")
        with impact_summary_cols[1]:
            st.metric("Biodiversidad en Riesgo", f"{100-biodiversity_impact:.1f}%")
        with impact_summary_cols[2]:
            st.metric("Especies Afectadas", f"{species_at_risk:,}")
            
        # Añadir información de contexto
        st.markdown("""
        <p>El dashboard muestra el estado actual de las simulaciones basadas en los parámetros seleccionados.
        Puedes ajustar los controles a la izquierda para ver diferentes escenarios.</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with dashboard_tab2:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Datos por Región de Colombia")
        
        # Tabla de datos por región
        data = {
            'Región': ["Zona Cafetera", "Valle del Cauca", "Antioquia", "Santander", "Cundinamarca"],
            'Cultivos Dependientes': ["Café, Plátano, Aguacate", "Caña, Frutas", "Café, Aguacate", "Cacao, Frutas", "Flores, Fresas"],
            'Riesgo': ["Alto", "Alto", "Alto", "Medio", "Medio"],
            'Impacto Económico (M USD)': [950, 850, 900, 500, 600]
        }
        region_df = pd.DataFrame(data)
        st.dataframe(region_df, use_container_width=True)
        
        st.markdown("""
        <p>La tabla muestra las regiones más importantes para la polinización en Colombia y 
        los cultivos que dependen de polinizadores en cada una.</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with dashboard_tab3:
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.subheader("Acciones Recomendadas")
        
        # Acciones recomendadas basadas en los parámetros actuales
        if bee_population_percentage < 30:
            st.error("⚠️ Situación crítica - Se requieren medidas urgentes")
        elif bee_population_percentage < 70:
            st.warning("⚠️ Situación preocupante - Se requieren acciones de conservación")
        else:
            st.success("✅ Situación estable - Mantener políticas de conservación")
        
        st.markdown("""
        <p>En base a los parámetros actuales, se recomiendan las siguientes acciones:</p>
        <ul>
            <li>Establecer corredores biológicos entre zonas agrícolas</li>
            <li>Reducir el uso de pesticidas neonicotinoides</li>
            <li>Aumentar la diversidad de cultivos y plantas nativas</li>
            <li>Implementar programas de monitoreo de poblaciones de abejas</li>
            <li>Educar a agricultores sobre prácticas amigables con polinizadores</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Footer con créditos
st.markdown("""
<div class="footer">
Desarrollado con 🐝 para la conservación de polinizadores en Colombia | 2025
</div>
""", unsafe_allow_html=True)
