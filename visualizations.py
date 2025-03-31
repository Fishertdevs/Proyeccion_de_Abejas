import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from models import calculate_crop_production, calculate_biodiversity_impact

def plot_bee_crop_relationship_3d(current_bee_percentage, years=10):
    """
    Create a 3D interactive visualization showing the relationship between
    bee population, time, and crop production.
    
    Parameters:
    -----------
    current_bee_percentage : float
        Current bee population percentage to highlight
    years : int
        Number of years to simulate
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive 3D plot
    """
    # Generate bee population range
    bee_range = np.linspace(0, 100, 40)
    
    # Generate time range
    time_range = np.linspace(0, years, 20)
    
    # Create meshgrid
    bee_grid, time_grid = np.meshgrid(bee_range, time_range)
    
    # Initialize crop production grid
    crop_grid = np.zeros_like(bee_grid)
    
    # Calculate crop production for each point with time decay
    for i in range(bee_grid.shape[0]):
        for j in range(bee_grid.shape[1]):
            bee_val = bee_grid[i, j]
            time_val = time_grid[i, j]
            
            # Base crop production based on current bee population
            base_crop = calculate_crop_production(bee_val)
            
            # Apply time effect - long-term decline if bee population is low
            time_factor = 1.0
            if bee_val < 50:
                # Calculate decline over time
                time_factor = max(0.5, 1.0 - (time_val / years) * (0.1 * (50 - bee_val) / 50))
            
            crop_grid[i, j] = base_crop * time_factor
    
    # Create 3D surface plot
    fig = go.Figure()
    
    # Add surface
    fig.add_trace(go.Surface(
        x=bee_grid,
        y=time_grid,
        z=crop_grid,
        colorscale='viridis',
        colorbar=dict(
            title=dict(
                text="Producción de Cultivos (%)",
                side="right"
            )
        ),
        lighting=dict(
            ambient=0.7,
            diffuse=0.8,
            roughness=0.5,
            specular=0.6,
            fresnel=0.8
        ),
        contours={
            "z": {"show": True, "start": 20, "end": 100, "size": 10, "color":"white"}
        }
    ))
    
    # Add marker for current position
    fig.add_trace(go.Scatter3d(
        x=[current_bee_percentage], 
        y=[0], 
        z=[calculate_crop_production(current_bee_percentage)],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
            symbol='circle'
        ),
        name='Punto Actual'
    ))
    
    # Update layout
    fig.update_layout(
        title='Proyección 3D: Relación entre Población de Abejas, Tiempo y Producción Agrícola',
        scene=dict(
            xaxis_title='Población de Abejas (%)',
            yaxis_title='Años',
            zaxis_title='Producción Agrícola (%)',
            xaxis=dict(gridcolor="white", gridwidth=2),
            yaxis=dict(gridcolor="white", gridwidth=2),
            zaxis=dict(gridcolor="white", gridwidth=2),
            bgcolor='#1E1E1E'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='#2D2D2D',
        font=dict(color='white'),
        autosize=True,
        height=600
    )
    
    # Add animation effect
    frames = []
    for year in np.linspace(0, years, 10):
        frame = go.Frame(
            data=[
                go.Scatter3d(
                    x=[current_bee_percentage], 
                    y=[year], 
                    z=[calculate_crop_production(current_bee_percentage) * 
                       (1.0 if current_bee_percentage >= 50 else 
                        max(0.5, 1.0 - (year / years) * (0.1 * (50 - current_bee_percentage) / 50)))],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='red',
                        symbol='circle'
                    )
                )
            ],
            name=f'Year {year:.1f}'
        )
        frames.append(frame)
    
    fig.frames = frames
    
    # Add animation buttons
    def frame_args(duration):
        return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }
    
    sliders = [
        {
            "active": 0,
            "steps": [
                {
                    "args": [[f.name], frame_args(300)],
                    "label": f"{year:.1f}",
                    "method": "animate",
                }
                for year, f in zip(np.linspace(0, years, 10), frames)
            ],
            "x": 0.1,
            "y": 0,
            "len": 0.9,
        }
    ]
    
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, frame_args(300)],
                        "label": "▶ Iniciar",
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "⏹ Pausar",
                        "method": "animate",
                    },
                ],
                "type": "buttons",
                "direction": "left",
                "x": 0.1,
                "y": 0,
            }
        ],
        sliders=sliders
    )
    
    return fig

def plot_bee_crop_relationship(current_bee_percentage):
    """
    Create an interactive plot showing the relationship between
    bee population and crop production.
    
    Parameters:
    -----------
    current_bee_percentage : float
        Current bee population percentage to highlight
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot
    """
    # Generate data points
    bee_percentages = np.arange(0, 101, 1)
    crop_productions = [calculate_crop_production(p) for p in bee_percentages]
    
    # Create figure
    fig = go.Figure()
    
    # Add line
    fig.add_trace(go.Scatter(
        x=bee_percentages,
        y=crop_productions,
        mode='lines',
        name='Producción de cultivos',
        line=dict(color='#4CAF50', width=3)
    ))
    
    # Add point for current value
    current_crop = calculate_crop_production(current_bee_percentage)
    fig.add_trace(go.Scatter(
        x=[current_bee_percentage],
        y=[current_crop],
        mode='markers',
        name='Nivel actual',
        marker=dict(color='red', size=12, symbol='circle')
    ))
    
    # Add threshold lines and areas
    fig.add_shape(
        type="line",
        x0=20, y0=0, x1=20, y1=100,
        line=dict(color="red", width=2, dash="dash"),
        name="Umbral crítico"
    )
    
    # Add annotations for threshold explanation
    fig.add_annotation(
        x=15, y=35,
        text="Zona crítica",
        showarrow=False,
        font=dict(color="red"),
        align="center"
    )
    
    # Add title and axis labels
    fig.update_layout(
        title="Relación entre Población de Abejas y Producción Agrícola",
        xaxis_title="Población de Abejas (%)",
        yaxis_title="Producción Agrícola (%)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        shapes=[
            # Add rectangle for critical zone
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=0,
                y0=0,
                x1=20,
                y1=100,
                fillcolor="rgba(255, 0, 0, 0.1)",
                line_width=0,
                layer="below"
            ),
            # Add rectangle for warning zone
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=20,
                y0=0,
                x1=50,
                y1=100,
                fillcolor="rgba(255, 165, 0, 0.1)",
                line_width=0,
                layer="below"
            )
        ]
    )
    
    # Update axes
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 105])
    
    return fig

def plot_biodiversity_impact_3d(bee_percentage, ecosystem_resilience):
    """
    Create a 3D interactive plot showing biodiversity impact based on
    bee population percentage and ecosystem resilience.
    
    Parameters:
    -----------
    bee_percentage : float
        Bee population percentage
    ecosystem_resilience : float
        Ecosystem resilience factor
        
    Returns:
    --------
    plotly.graph_objects.Figure
        3D interactive plot
    """
    # Generate a grid of x-y points
    bee_range = np.linspace(10, 100, 30)
    resilience_range = np.linspace(0.2, 1.0, 30)
    bee_grid, resilience_grid = np.meshgrid(bee_range, resilience_range)
    
    # Calculate biodiversity for each point on the grid
    biodiversity_values = np.zeros_like(bee_grid)
    for i in range(bee_grid.shape[0]):
        for j in range(bee_grid.shape[1]):
            biodiversity_values[i, j] = calculate_biodiversity_impact(
                bee_grid[i, j], resilience_grid[i, j]
            )
    
    # Create the 3D surface plot
    fig = go.Figure(data=[
        go.Surface(
            x=bee_grid, 
            y=resilience_grid, 
            z=biodiversity_values,
            colorscale='viridis',
            colorbar=dict(
                title=dict(
                    text="Biodiversidad (%)",
                    side="right"
                )
            )
        )
    ])
    
    # Highlight the current point
    fig.add_trace(
        go.Scatter3d(
            x=[bee_percentage],
            y=[ecosystem_resilience],
            z=[calculate_biodiversity_impact(bee_percentage, ecosystem_resilience)],
            mode='markers',
            marker=dict(
                size=8,
                color='red',
            ),
            name='Punto Actual'
        )
    )
    
    # Update layout
    fig.update_layout(
        title='Modelo 3D de Impacto en Biodiversidad',
        scene=dict(
            xaxis_title='Población de Abejas (%)',
            yaxis_title='Resiliencia del Ecosistema',
            zaxis_title='Biodiversidad (%)',
            xaxis=dict(gridcolor="white", gridwidth=2),
            yaxis=dict(gridcolor="white", gridwidth=2),
            zaxis=dict(gridcolor="white", gridwidth=2),
            bgcolor='#1E1E1E'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='#2D2D2D',
        font=dict(color='white'),
        autosize=True,
        height=500
    )
    
    return fig

def plot_biodiversity_impact(bee_percentage, ecosystem_resilience):
    """
    Create an interactive plot showing the impact on different ecosystems
    based on bee population percentage.
    
    Parameters:
    -----------
    bee_percentage : float
        Bee population percentage
    ecosystem_resilience : float
        Ecosystem resilience factor
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot
    """
    # Define ecosystem types with different resilience modifiers
    ecosystems = [
        "Bosque templado", 
        "Pradera", 
        "Bosque tropical",
        "Zona agrícola",
        "Humedal",
        "Ecosistema urbano"
    ]
    
    # Different resilience modifiers for each ecosystem
    resilience_modifiers = [1.2, 0.9, 1.1, 0.7, 1.3, 0.5]
    
    # Calculate biodiversity impact for each ecosystem
    biodiversity_impacts = []
    for modifier in resilience_modifiers:
        # Adjust resilience based on ecosystem type, but keep within 0-1 range
        adjusted_resilience = min(1.0, max(0.0, ecosystem_resilience * modifier))
        impact = calculate_biodiversity_impact(bee_percentage, adjusted_resilience)
        biodiversity_impacts.append(impact)
    
    # Create color scale based on impact values
    colors = []
    for impact in biodiversity_impacts:
        if impact >= 80:
            colors.append('#4CAF50')  # Green
        elif impact >= 60:
            colors.append('#8BC34A')  # Light green
        elif impact >= 40:
            colors.append('#FFEB3B')  # Yellow
        elif impact >= 20:
            colors.append('#FF9800')  # Orange
        else:
            colors.append('#F44336')  # Red
    
    # Create figure
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=ecosystems,
        y=biodiversity_impacts,
        marker_color=colors,
        text=[f"{impact:.1f}%" for impact in biodiversity_impacts],
        textposition='auto'
    ))
    
    # Add reference line for current average
    avg_impact = sum(biodiversity_impacts) / len(biodiversity_impacts)
    fig.add_shape(
        type="line",
        x0=-0.5, y0=avg_impact, x1=len(ecosystems)-0.5, y1=avg_impact,
        line=dict(color="black", width=2, dash="dash"),
    )
    
    # Add annotation for average
    fig.add_annotation(
        x=len(ecosystems)-1,
        y=avg_impact + 3,
        text=f"Promedio: {avg_impact:.1f}%",
        showarrow=False,
        font=dict(color="black"),
    )
    
    # Update layout
    fig.update_layout(
        title=f"Impacto en la Biodiversidad por Tipo de Ecosistema",
        xaxis_title="Tipo de Ecosistema",
        yaxis_title="Biodiversidad Remanente (%)",
        template="plotly_white",
        yaxis=dict(range=[0, 105])
    )
    
    return fig

def plot_timeseries_forecast(ecosystem_data):
    """
    Create a time series forecast plot based on ecosystem simulation data.
    
    Parameters:
    -----------
    ecosystem_data : pd.DataFrame
        Data frame with simulation results
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot
    """
    # Create figure
    fig = go.Figure()
    
    # Add lines for each variable
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['biodiversity'],
        mode='lines',
        name='Biodiversidad',
        line=dict(color='#4CAF50', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['crop_production'],
        mode='lines',
        name='Producción agrícola',
        line=dict(color='#FFC107', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['wild_plants'],
        mode='lines',
        name='Plantas silvestres',
        line=dict(color='#2196F3', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=ecosystem_data['time'],
        y=ecosystem_data['bee_population'],
        mode='lines',
        name='Población de abejas',
        line=dict(color='#FF9800', width=3, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title="Proyección a Futuro del Ecosistema",
        xaxis_title="Años",
        yaxis_title="Porcentaje del nivel óptimo (%)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add annotations for important thresholds
    # Find if biodiversity crosses below 50%
    if any(ecosystem_data['biodiversity'] < 50):
        # Get first time it crosses below 50%
        crossing_time = ecosystem_data.loc[ecosystem_data['biodiversity'] < 50, 'time'].iloc[0]
        
        fig.add_shape(
            type="line",
            x0=crossing_time, y0=0, x1=crossing_time, y1=100,
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.add_annotation(
            x=crossing_time,
            y=20,
            text="Punto crítico de biodiversidad",
            showarrow=True,
            arrowhead=1,
        )
    
    return fig

def create_risk_map(bee_percentage):
    """
    Create an interactive map showing regions at risk due to pollinator loss in Colombia.
    
    Parameters:
    -----------
    bee_percentage : float
        Current bee population percentage
        
    Returns:
    --------
    folium.Map
        Interactive map
    """
    # Create a base map centered on Colombia
    m = folium.Map(location=[4.5709, -74.2973], zoom_start=6, tiles='CartoDB positron')
    
    # Import regions data from data module
    from data.regions import get_risk_regions
    colombia_regions = get_risk_regions()
    
    # Adjust risk based on current bee population
    # Lower bee population = higher risk
    risk_multiplier = max(0.1, (100 - bee_percentage) / 100 * 2)
    
    # Add markers for each region
    for region in colombia_regions:
        name = region["name"]
        lat = region["lat"]
        lon = region["lon"]
        risk_level = region["risk"]
        crops = region["crops"]
        dependency = region["dependency"]
        description = region["description"]
        
        # Determine color based on risk level
        if risk_level == "Alto":
            color = 'red'
        elif risk_level == "Medio":
            color = 'orange'
        else:
            color = 'green'
            
        # Create tooltip and popup content
        tooltip = f"{name} - Riesgo: {risk_level}"
        popup_content = f"""
        <div style="width: 250px">
            <h4>{name}</h4>
            <p><strong>Nivel de riesgo:</strong> {risk_level}</p>
            <p><strong>Cultivos principales:</strong> {crops}</p>
            <p><strong>Dependencia de polinizadores:</strong> {dependency}%</p>
            <p><strong>Descripción:</strong> {description}</p>
        </div>
        """
        
        # Add marker with popup
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon='leaf', prefix='fa')
        ).add_to(m)
        
        # Add circle with radius proportional to risk
        adjusted_risk = min(1.0, (dependency/100) * risk_multiplier)
        folium.Circle(
            radius=adjusted_risk * 30000,  # Scale for visibility
            location=[lat, lon],
            color=color,
            fill=True,
            fill_opacity=0.2,
            opacity=0.6,
            weight=1
        ).add_to(m)
    
    # Add a Choropleth map layer for Colombia departments (simplified)
    folium.GeoJson(
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-78.0, 1.0], [-78.0, 11.0], 
                            [-71.0, 11.0], [-67.0, 4.0],
                            [-67.0, -4.0], [-78.0, 1.0]
                        ]]
                    }
                }
            ]
        },
        style_function=lambda x: {'fillColor': 'transparent', 'color': '#333333', 'weight': 1}
    ).add_to(m)
    
    # Add legend as HTML
    legend_html = '''
    <div style="position: fixed; 
        bottom: 50px; left: 10px; width: 180px; height: 120px; 
        border:2px solid grey; z-index:9999; background-color:white;
        padding: 10px;
        font-size: 14px;
        ">
        <p><strong>Nivel de Riesgo</strong></p>
        <p style="margin:0; color: red;">■ Alto: Alta dependencia</p>
        <p style="margin:0; color: orange;">■ Medio: Dependencia moderada</p>
        <p style="margin:0; color: green;">■ Bajo: Menor dependencia</p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
        top: 10px; left: 50px; width: 300px;
        z-index:9999; background-color:white;
        padding: 10px;
        font-size: 16px;
        opacity: 0.9;
        border-radius: 5px;
        ">
        <p><strong>Zonas de Riesgo por Pérdida de Polinizadores en Colombia</strong></p>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(title_html))
    
    return m
