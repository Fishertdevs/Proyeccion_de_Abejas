def get_risk_regions():
    """
    Returns a list of regions with pollinator risk data in Colombia.
    
    This is a data source for the map visualization that shows regions
    at risk due to pollinator decline in Colombia.
    """
    # Data about Colombian regions and their risk levels
    # This is a simplified dataset for visualization purposes
    regions = [
        {
            "name": "Zona Cafetera",
            "lat": 5.0122,
            "lon": -75.4151,
            "risk": "Alto",
            "crops": "Café, plátano, aguacate",
            "dependency": 85,
            "description": "Alta dependencia de polinizadores para producción de café de calidad"
        },
        {
            "name": "Valle del Cauca",
            "lat": 3.4516,
            "lon": -76.5320,
            "risk": "Alto",
            "crops": "Caña de azúcar, frutas, cacao",
            "dependency": 75,
            "description": "Importante zona agrícola con cultivos de alto valor dependientes de polinizadores"
        },
        {
            "name": "Antioquia",
            "lat": 6.2476,
            "lon": -75.5658,
            "risk": "Alto",
            "crops": "Café, frutas, aguacate, cacao",
            "dependency": 80,
            "description": "Gran diversidad de cultivos con fuerte dependencia de polinizadores"
        },
        {
            "name": "Santander",
            "lat": 7.1254,
            "lon": -73.1198,
            "risk": "Alto",
            "crops": "Cacao, frutas, café",
            "dependency": 78,
            "description": "Cultivos de cacao altamente dependientes de polinizadores especializados"
        },
        {
            "name": "Boyacá",
            "lat": 5.5395,
            "lon": -73.3621,
            "risk": "Medio",
            "crops": "Papa, frutas, hortalizas",
            "dependency": 60,
            "description": "Mezcla de cultivos con variada dependencia de polinizadores"
        },
        {
            "name": "Cundinamarca",
            "lat": 4.6486,
            "lon": -74.0821,
            "risk": "Medio",
            "crops": "Flores, frutas, hortalizas",
            "dependency": 65,
            "description": "Importante producción de flores para exportación con alta dependencia"
        },
        {
            "name": "Huila",
            "lat": 2.4448,
            "lon": -75.7492,
            "risk": "Medio",
            "crops": "Café, frutas, arroz",
            "dependency": 70,
            "description": "Zona cafetera con dependencia significativa de polinizadores"
        },
        {
            "name": "Cauca",
            "lat": 2.4448,
            "lon": -76.6147,
            "risk": "Alto",
            "crops": "Café, caña, frutas",
            "dependency": 75,
            "description": "Ecosistemas diversos con cultivos altamente dependientes"
        },
        {
            "name": "Tolima",
            "lat": 4.0925,
            "lon": -75.1545,
            "risk": "Medio",
            "crops": "Arroz, café, frutas",
            "dependency": 65,
            "description": "Combinación de cultivos con dependencia variable de polinizadores"
        },
        {
            "name": "Nariño",
            "lat": 1.2136,
            "lon": -77.2811,
            "risk": "Medio",
            "crops": "Papa, café, hortalizas",
            "dependency": 55,
            "description": "Diversidad de cultivos en diferentes pisos térmicos"
        },
        {
            "name": "Córdoba",
            "lat": 8.7536,
            "lon": -75.8836,
            "risk": "Bajo",
            "crops": "Maíz, arroz, ganado",
            "dependency": 35,
            "description": "Predominio de cultivos con menor dependencia de polinizadores"
        },
        {
            "name": "Magdalena",
            "lat": 11.2404,
            "lon": -74.1990,
            "risk": "Medio",
            "crops": "Banano, palma, frutas",
            "dependency": 60,
            "description": "Cultivos de exportación con dependencia moderada"
        },
        {
            "name": "Amazonia",
            "lat": -0.7893,
            "lon": -71.8996,
            "risk": "Alto",
            "crops": "Frutales amazónicos, cacao, caucho",
            "dependency": 90,
            "description": "Alta biodiversidad con fuerte dependencia de polinizadores nativos"
        },
        {
            "name": "Guajira",
            "lat": 11.5444,
            "lon": -72.9072,
            "risk": "Bajo",
            "crops": "Arroz, yuca, ovino-caprino",
            "dependency": 30,
            "description": "Condiciones áridas con cultivos de menor dependencia"
        },
        {
            "name": "Meta",
            "lat": 4.1420,
            "lon": -73.6256,
            "risk": "Medio",
            "crops": "Palma, arroz, frutales",
            "dependency": 50,
            "description": "Cultivos extensivos con dependencia moderada"
        }
    ]
    
    return regions