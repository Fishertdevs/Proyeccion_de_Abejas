import numpy as np
import pandas as pd
from scipy.integrate import odeint

def calculate_biodiversity_impact(bee_percentage, ecosystem_resilience):
    """
    Calculate the impact on biodiversity based on bee population percentage
    and ecosystem resilience.
    
    Parameters:
    -----------
    bee_percentage : float
        Percentage of bee population (0-100)
    ecosystem_resilience : float
        Ecosystem resilience factor (0-1)
        
    Returns:
    --------
    float
        Biodiversity index (0-100)
    """
    # Base model: biodiversity declines non-linearly with bee population
    # The decline is mitigated by ecosystem resilience
    
    # Calculate normalized bee population (0-1)
    bee_norm = bee_percentage / 100
    
    # Parameters for sigmoid function
    k = 5  # Steepness
    mid_point = 0.5  # Inflection point
    
    # Apply sigmoid function to model non-linear relationship
    # Higher resilience pushes the curve to the left, making the system more robust
    adjusted_bee = bee_norm + (ecosystem_resilience * 0.3)
    
    # Sigmoid function to model how biodiversity responds to bee population
    biodiversity_factor = 1 / (1 + np.exp(-k * (adjusted_bee - mid_point)))
    
    # Scale to 0-100
    biodiversity_index = biodiversity_factor * 100
    
    # Biodiversity can't be higher than 100%
    return min(biodiversity_index, 100)

def calculate_crop_production(bee_percentage):
    """
    Calculate the impact on crop production based on bee population percentage.
    
    Parameters:
    -----------
    bee_percentage : float
        Percentage of bee population (0-100)
        
    Returns:
    --------
    float
        Crop production index (0-100)
    """
    # Bee-dependent crops vs non-bee-dependent crops
    bee_dependent_percentage = 0.35  # 35% of crops are bee-dependent
    
    # For bee-dependent crops, we model a non-linear relationship
    # Below 20% bee population, crop yields collapse rapidly
    
    # Normalize bee population (0-1)
    bee_norm = bee_percentage / 100
    
    # For bee-dependent crops
    if bee_norm >= 0.8:
        # Near optimal conditions
        bee_crop_factor = 1.0
    elif bee_norm >= 0.5:
        # Some reduction, but still manageable
        bee_crop_factor = 0.8 + ((bee_norm - 0.5) / 0.3) * 0.2
    elif bee_norm >= 0.2:
        # Significant reduction
        bee_crop_factor = 0.4 + ((bee_norm - 0.2) / 0.3) * 0.4
    else:
        # Critical collapse
        bee_crop_factor = bee_norm / 0.2 * 0.4
    
    # Calculate weighted average for all crops
    crop_production_factor = (bee_dependent_percentage * bee_crop_factor) + \
                             ((1 - bee_dependent_percentage) * 1.0)
    
    # Scale to percentage
    return crop_production_factor * 100

def create_ecosystem_simulation(bee_percentage, years, ecosystem_resilience):
    """
    Simulate ecosystem changes over time based on bee population.
    
    Parameters:
    -----------
    bee_percentage : float
        Percentage of bee population (0-100)
    years : int
        Number of years to simulate
    ecosystem_resilience : float
        Ecosystem resilience factor (0-1)
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with simulation results
    """
    # Initialize time points (in years)
    t = np.linspace(0, years, years * 12)  # Monthly intervals
    
    # Normalize bee population
    bee_norm = bee_percentage / 100
    
    # Initial conditions
    # [biodiversity, crop_production, wild_plants, bee_population]
    initial_state = [1.0, 1.0, 1.0, bee_norm]
    
    # Define the system of differential equations
    def ecosystem_model(y, t, resilience):
        biodiversity, crop_production, wild_plants, bee_pop = y
        
        # Parameters
        alpha = 0.05  # Rate of biodiversity decline due to bee loss
        beta = 0.08   # Rate of crop production decline due to bee loss
        gamma = 0.03  # Rate of wild plant decline due to bee loss
        delta = 0.1   # Feedback rate from biodiversity to bees
        
        # Differential equations
        dbio_dt = -alpha * (1 - bee_pop) * biodiversity + (resilience * 0.02 * (1 - biodiversity))
        dcrop_dt = -beta * (1 - bee_pop) * crop_production
        dwild_dt = -gamma * (1 - bee_pop) * wild_plants
        dbee_dt = 0  # Bee population is kept constant in this model
        
        return [dbio_dt, dcrop_dt, dwild_dt, dbee_dt]
    
    # Solve ODE system
    solution = odeint(ecosystem_model, initial_state, t, args=(ecosystem_resilience,))
    
    # Extract solutions
    biodiversity = solution[:, 0]
    crop_production = solution[:, 1]
    wild_plants = solution[:, 2]
    bee_population = solution[:, 3]
    
    # Create DataFrame
    df = pd.DataFrame({
        'time': t,
        'biodiversity': biodiversity * 100,  # Scale to percentage
        'crop_production': crop_production * 100,
        'wild_plants': wild_plants * 100,
        'bee_population': bee_population * 100
    })
    
    return df
