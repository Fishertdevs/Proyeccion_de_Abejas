import pandas as pd
import numpy as np

def get_initial_data():
    """
    Generate initial data for the application.
    
    This function creates synthetic data for various metrics related to
    bee populations, agricultural production, and biodiversity.
    
    Returns:
    --------
    dict
        Dictionary containing various dataframes and values
    """
    # Define crop types and their dependence on pollinators
    crops_data = pd.DataFrame({
        'crop': [
            'Almendras', 'Manzanas', 'Fresas', 'Café', 'Cacao', 
            'Tomates', 'Calabazas', 'Melones', 'Kiwi', 'Cerezas',
            'Pepinos', 'Arándanos', 'Aguacates', 'Trigo', 'Maíz',
            'Arroz', 'Patatas', 'Caña de azúcar'
        ],
        'pollinator_dependence': [
            0.90, 0.85, 0.80, 0.75, 0.70,
            0.65, 0.95, 0.85, 0.90, 0.80,
            0.65, 0.90, 0.40, 0.05, 0.10,
            0.00, 0.10, 0.00
        ],
        'global_production_value': [
            8.5, 9.2, 7.5, 9.8, 8.9,
            10.0, 4.2, 5.8, 3.2, 6.7,
            5.1, 4.8, 7.2, 9.5, 9.8,
            10.0, 8.7, 9.2
        ]
    })
    
    # Historical bee population data (percentage of optimal)
    years = np.arange(1990, 2023)
    historical_bee_pop = 100 - (0.8 * (years - 1990))
    # Ensure no negative values
    historical_bee_pop = np.maximum(historical_bee_pop, 10)
    
    historical_data = pd.DataFrame({
        'year': years,
        'bee_population_percentage': historical_bee_pop
    })
    
    # Ecosystem types and their characteristics
    ecosystems_data = pd.DataFrame({
        'ecosystem': [
            'Bosque templado', 'Pradera', 'Bosque tropical',
            'Zona agrícola', 'Humedal', 'Ecosistema urbano'
        ],
        'plant_species_count': [
            1200, 800, 2500,
            300, 900, 150
        ],
        'pollinator_dependent_percentage': [
            0.65, 0.80, 0.75,
            0.60, 0.70, 0.50
        ],
        'resilience_factor': [
            0.7, 0.6, 0.8,
            0.4, 0.75, 0.3
        ]
    })
    
    # Departments in Colombia and their agricultural dependency on pollinators
    colombia_data = pd.DataFrame({
        'department': [
            'Antioquia', 'Valle del Cauca', 'Cundinamarca', 'Santander', 'Boyacá',
            'Huila', 'Tolima', 'Nariño', 'Cauca', 'Caldas',
            'Magdalena', 'Cesar', 'Meta', 'Risaralda', 'Quindío'
        ],
        'pollinator_dependent_crops_value': [
            85, 75, 80, 70, 65,
            85, 75, 75, 80, 90,
            70, 60, 60, 80, 75
        ],
        'bee_decline_rate': [
            2.8, 2.5, 3.0, 2.2, 1.8,
            2.6, 2.5, 2.0, 2.7, 3.1,
            2.4, 2.2, 2.1, 2.9, 2.7
        ],
        'main_crops': [
            'Café, Aguacate, Flores', 'Caña, Frutas, Café', 'Flores, Fresas, Hortalizas', 
            'Cacao, Cítricos, Plátano', 'Frutas, Papa, Cereales',
            'Café, Frutas exóticas', 'Arroz, Café, Frutas', 'Café, Papa, Frutas andinas',
            'Café, Caña panelera', 'Café, Plátano, Cítricos',
            'Banano, Palma, Cítricos', 'Palma, Algodón, Arroz', 'Palma, Cítricos, Piña',
            'Café, Plátano, Aguacate', 'Café, Cítricos, Plátano'
        ]
    })
    
    return {
        'crops': crops_data,
        'historical': historical_data,
        'ecosystems': ecosystems_data,
        'colombia': colombia_data
    }
