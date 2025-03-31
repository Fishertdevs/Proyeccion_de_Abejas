import streamlit as st

def get_emoji(emoji_type):
    """
    Return an emoji based on the requested type.
    
    Parameters:
    -----------
    emoji_type : str
        Type of emoji to return
        
    Returns:
    --------
    str
        Emoji character
    """
    emoji_map = {
        'bee': '🐝',
        'flower': '🌸',
        'tree': '🌳',
        'farm': '🌾',
        'chart': '📊',
        'warning': '⚠️',
        'globe': '🌍',
        'food': '🍎',
        'honey': '🍯',
        'microscope': '🔬',
        'leaf': '🍃',
        'seedling': '🌱',
        'herb': '🌿'
    }
    
    return emoji_map.get(emoji_type, '✨')

def add_vertical_space(num_lines=1):
    """
    Add vertical space to the Streamlit app.
    
    Parameters:
    -----------
    num_lines : int
        Number of lines of vertical space to add
    """
    for _ in range(num_lines):
        st.markdown("<br>", unsafe_allow_html=True)

def format_number(number, precision=1):
    """
    Format a number with commas as thousands separators.
    
    Parameters:
    -----------
    number : float or int
        Number to format
    precision : int
        Number of decimal places
        
    Returns:
    --------
    str
        Formatted number
    """
    return f"{number:,.{precision}f}"

def get_biodiversity_impact_text(impact_percentage):
    """
    Get descriptive text about biodiversity impact based on percentage.
    
    Parameters:
    -----------
    impact_percentage : float
        Impact percentage
        
    Returns:
    --------
    str
        Descriptive text
    """
    if impact_percentage >= 90:
        return "Mínimo impacto en la biodiversidad. Los ecosistemas mantienen su funcionalidad."
    elif impact_percentage >= 75:
        return "Impacto leve. Algunas especies sensibles pueden verse afectadas."
    elif impact_percentage >= 60:
        return "Impacto moderado. Reducción notable en la diversidad de plantas con flores."
    elif impact_percentage >= 40:
        return "Impacto severo. Múltiples especies en riesgo de extinción local."
    else:
        return "Impacto crítico. Colapso potencial de ecosistemas y pérdida masiva de biodiversidad."

def get_crop_impact_text(impact_percentage):
    """
    Get descriptive text about crop production impact based on percentage.
    
    Parameters:
    -----------
    impact_percentage : float
        Impact percentage
        
    Returns:
    --------
    str
        Descriptive text
    """
    if impact_percentage >= 90:
        return "Producción agrícola óptima. Sin pérdidas significativas."
    elif impact_percentage >= 75:
        return "Ligera reducción en rendimientos de cultivos dependientes de polinizadores."
    elif impact_percentage >= 60:
        return "Reducción moderada. Algunos cultivos muestran déficit de polinización."
    elif impact_percentage >= 40:
        return "Reducción severa. Cultivos como almendras, manzanas y fresas en niveles críticos."
    else:
        return "Crisis agrícola. Escasez significativa de alimentos y aumento dramático de precios."

def get_quick_facts():
    """
    Return a list of quick facts about bees and pollination.
    
    Returns:
    --------
    list
        List of fact strings
    """
    facts = [
        "Las abejas polinizan aproximadamente 1/3 de todos los alimentos que consumimos.",
        "Una sola abeja puede visitar hasta 5,000 flores en un solo día.",
        "La polinización por abejas contribuye con más de 15 mil millones de dólares a la economía agrícola de EE.UU. anualmente.",
        "Existen más de 20,000 especies de abejas en todo el mundo, pero solo 7 especies producen miel.",
        "Las abejas han existido por más de 30 millones de años.",
        "Las abejas pueden reconocer rostros humanos.",
        "Las abejas pueden comunicarse mediante la 'danza de las abejas' para indicar la ubicación de fuentes de alimento.",
        "Para producir 1 libra de miel, las abejas deben visitar aproximadamente 2 millones de flores.",
        "Una colonia de abejas puede contener hasta 60,000 abejas durante la temporada alta.",
        "Las abejas son responsables de polinizar más del 80% de las plantas con flores del mundo."
    ]
    
    return facts
