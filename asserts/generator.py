import pandas as pd
import numpy as np

# Define parameters for each class
conditions = {
    "High": {"soil_moisture": (65, 75), "humidity": (60, 75), "temp": (20, 25), "light": (800, 950), "months": [5, 6, 7]},
    "Medium": {"soil_moisture": (55, 65), "humidity": (50, 60), "temp": (25, 29), "light": (950, 1100), "months": [5, 6, 7]},
    "Low": {"soil_moisture": (45, 55), "humidity": (40, 50), "temp": (27, 31), "light": (700, 850), "months": [5, 6, 7]},
    "Unsustainable": {"soil_moisture": (20, 45), "humidity": (30, 50), "temp": (30, 36), "light": (1100, 1500), "months": [7, 8, 9]}
}

# Generate data
data = []
for status, params in conditions.items():
    for _ in range(750):
        row = {
            "soil_moisture": int(np.random.uniform(*params["soil_moisture"])),
            "humidity": np.random.uniform(*params["humidity"]),
            "temperature": np.random.uniform(*params["temp"]),
            "light_intensity": np.random.uniform(*params["light"]),
            "month": np.random.choice(params["months"]),
            "status": status
        }
        data.append(row)

df = pd.DataFrame(data)
df.to_csv("crop_yield_data.csv", index=False)