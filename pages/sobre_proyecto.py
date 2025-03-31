import streamlit as st

st.set_page_config(
    page_title="Sobre el Proyecto - Impacto de Abejas en Colombia",
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
    /* Ajustes para el contraste de texto */
    h1, h2, h3, h4, h5, h6, p, li, span {
        color: #F0F0F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>Sobre el Proyecto</h1>", unsafe_allow_html=True)

# Contenido principal
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Acerca de esta Aplicación</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Este proyecto tiene como objetivo modelar el impacto de la reducción de poblaciones de abejas en la biodiversidad y producción agrícola de Colombia.
La aplicación utiliza datos y modelos científicos para simular cómo diferentes niveles de poblaciones de abejas pueden afectar a distintos
ecosistemas y cultivos en Colombia.
</p>
""", unsafe_allow_html=True)

st.markdown("<h3>Objetivos del Proyecto</h3>", unsafe_allow_html=True)
st.markdown("""
<ul>
    <li>Crear conciencia sobre la importancia de las abejas y otros polinizadores para los ecosistemas de Colombia</li>
    <li>Proporcionar una herramienta educativa que muestre visualmente el impacto de la pérdida de polinizadores</li>
    <li>Ofrecer datos específicos para Colombia que puedan ser utilizados en la toma de decisiones</li>
    <li>Promover acciones de conservación de polinizadores a nivel individual y colectivo</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección de metodología
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Metodología</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
La aplicación utiliza una combinación de modelos matemáticos y datos de investigaciones científicas para simular el impacto 
de la disminución de poblaciones de abejas. Los modelos incluyen:
</p>

<ol>
    <li><strong>Modelo de impacto en biodiversidad:</strong> Basado en estudios sobre la dependencia de polinizadores en diferentes ecosistemas</li>
    <li><strong>Modelo de producción agrícola:</strong> Derivado de investigaciones sobre el efecto de la polinización en rendimientos de cultivos</li>
    <li><strong>Simulación de ecosistemas:</strong> Utilizando ecuaciones diferenciales que modelan las interacciones entre especies</li>
    <li><strong>Análisis de riesgo regional:</strong> Basado en datos específicos de cada región de Colombia</li>
</ol>

<p class='description'>
Los datos específicos de Colombia fueron recopilados de diversas fuentes, incluyendo estudios del Instituto Humboldt,
informes del Ministerio de Agricultura, y publicaciones científicas sobre biodiversidad y agricultura en Colombia.
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sección de créditos
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Créditos y Contribuciones</h2>", unsafe_allow_html=True)
st.markdown("""
<p class='description'>
Este proyecto fue desarrollado como un esfuerzo para crear conciencia sobre la importancia de las abejas y otros polinizadores en Colombia.
</p>

<h3>Fuentes de Datos</h3>
<ul>
    <li>Instituto Alexander von Humboldt - Datos de biodiversidad en Colombia</li>
    <li>Ministerio de Agricultura y Desarrollo Rural - Datos sobre producción agrícola</li>
    <li>IPBES (2016) - Informe sobre polinizadores, polinización y producción de alimentos</li>
    <li>FAO (2018) - Datos sobre dependencia de cultivos a polinizadores</li>
</ul>

<h3>Herramientas y Tecnologías</h3>
<ul>
    <li>Streamlit - Framework para desarrollo de la aplicación web</li>
    <li>Pandas/NumPy - Análisis y manipulación de datos</li>
    <li>Plotly/Folium - Visualizaciones interactivas</li>
    <li>SciPy - Modelos matemáticos y simulaciones</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 20px; padding: 10px; font-size: 0.8rem; border-top: 1px solid #4A7C59; color: #bbb;">
Desarrollado para la conservación de abejas en Colombia | 2025
</div>
""", unsafe_allow_html=True)