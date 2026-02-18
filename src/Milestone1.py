# AirAware - Milestone 1
# Basic Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create sample air quality data

data = {
    "City": ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"],
    "PM25": [180, 95, 70, 110, 60],
    "PM10": [250, 150, 120, 170, 100],
    "AQI": [300, 180, 150, 210, 130]
}

# Step 2: Converting into DataFrame
df = pd.DataFrame(data)

# Step 3: Display dataset
print("Air Quality Dataset:")
print(df)

# Step 4: Basic statistics
print("\nSummary Statistics:")
print(df.describe())

# Step 5: Plot Air Quality Index comparison
plt.figure()
plt.bar(df["City"], df["AQI"])
plt.title("AQI Comparison Across Cities")
plt.xlabel("City")
plt.ylabel("AQI")
plt.show()
