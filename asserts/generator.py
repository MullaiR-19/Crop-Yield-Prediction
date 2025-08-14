import pandas as pd
import numpy as np
import random   

# Define parameters for each class
conditions = {
    "High": {
        "soil_moisture": (65, 80),    # Optimal for most crops (e.g., wheat, corn)
        "humidity": (60, 75),          # Ideal RH range
        "temp": (20, 28),              # Moderate temperatures (°C)
        "light": (800, 1200),          # Full sunlight (μmol/m²/s, PAR)
        "months": [4, 5, 6, 9, 10]    # Spring/fall growing seasons
    },
    "Medium": {
        "soil_moisture": (50, 65),     # Slightly dry but manageable
        "humidity": (50, 60),          # Suboptimal humidity
        "temp": (28, 32),              # Warm but tolerable
        "light": (600, 800),           # Partial shade/cloudy
        "months": [3, 7, 11]           # Shoulder seasons
    },
    "Low": {
        "soil_moisture": (35, 50),     # Dry soil (needs irrigation)
        "humidity": (40, 50),          # Low humidity
        "temp": (32, 38),             # Heat stress possible
        "light": (300, 600),           # Heavy shade/low light
        "months": [1, 2, 12]          # Winter months (dormant)
    },
    "Unsustainable": {
        "soil_moisture": (0, 35),
        "humidity": (10, 40),
        "temp": [(0, 15), (38, 50)],  # List of possible ranges
        "light": [(0, 300), (1201, 2000)],
        "months": [8]
    }
}

def generate_value(range_def):
    """Handles both single ranges (tuple) and discontinuous ranges (list of tuples)"""
    if isinstance(range_def, list):
        chosen_range = random.choice(range_def)
        return float(np.random.uniform(*chosen_range))
    else:
        return float(np.random.uniform(*range_def))

# Generate data
data = []
for status, params in conditions.items():
    for _ in range(3000):
        row = {
                'soil_moisture': generate_value(params['soil_moisture']),
                'humidity': generate_value(params['humidity']),
                'temperature': generate_value(params['temp']),
                'light_intensity': generate_value(params['light']),
                'month': int(np.random.choice(params['months'])),
                'status': status
            }
        data.append(row)

df = pd.DataFrame(data)
df.to_csv("crop_yield_data.csv", index=False)