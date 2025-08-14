import pandas as pd
import numpy as np
import random   

# Define parameters for each class
conditions = {
    "High": {
        "soil_moisture": (65, 80),    # Optimal moisture
        "humidity": (60, 75),         # Ideal RH
        "temp": (20, 28),             # Prime growing temp
        "light": (800, 1200),         # Full sunlight
        "months": [4, 5, 6, 9, 10]   # Peak seasons
    },
    "Medium": {
        "soil_moisture": (50, 65),    # Slightly dry
        "humidity": (50, 60),         # Moderate RH
        "temp": (25, 32),             # Tolerable range
        "light": (600, 800),          # Partial shade
        "months": [3, 7, 11]          # Shoulder months
    },
    "Low": {
        "soil_moisture": (20, 50),    # Explicitly dry (previously overlapped with Medium)
        "humidity": (30, 50),         # Low RH
        "temp": (32, 38),             # Heat stress
        "light": (200, 600),          # Low light (300-600 was overlapping with Medium)
        "months": [1, 2, 12]          # Off-season
    },
    "Unsustainable": {
        "soil_moisture": (0, 30),     # Critical drought (no overlap with Low)
        "humidity": (10, 70),         # Extreme aridity
        "temp": [(0, 10), (38, 50)],  # Frost OR extreme heat
        "light": [(0, 500), (1500, 2000)], # Pitch dark OR scorching
        "months": [8]                 # Stress peak month
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
                'Soil Moisture': generate_value(params['soil_moisture']),
                'Humidity': generate_value(params['humidity']),
                'Temperature': generate_value(params['temp']),
                'Light Intensity': generate_value(params['light']),
                'Month': int(np.random.choice(params['months'])),
                'Status': status
            }
        data.append(row)

df = pd.DataFrame(data)
df.to_csv("crop_yield_data.csv", index=False)