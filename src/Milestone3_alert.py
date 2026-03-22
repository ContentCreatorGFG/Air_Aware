# AIRAWARE SMART - MILESTONE 3
# AQI Category + Alert + Pie Chart

import pandas as pd
import matplotlib.pyplot as plt

print("Starting AQI Alert System...\n")

# 1. LOAD PREDICTED DATA
df = pd.read_csv("all_cities_aqi.csv")

#  You can change city here if needed
city_name = "Mumbai"
df = df[df["City"] == city_name]

print(f"Showing results for: {city_name}\n")

# 2. CATEGORY FUNCTION
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# Apply category
df["Category"] = df["Predicted_AQI"].apply(classify_aqi)

# 3. ALERT FUNCTION
def generate_alert(aqi):
    if aqi > 300:
        return "Emergency - Stay indoors"
    elif aqi > 200:
        return "High pollution - Avoid outside"
    elif aqi > 150:
        return "Wear mask"
    else:
        return "Air quality is acceptable"

# Apply alert
df["Alert"] = df["Predicted_AQI"].apply(generate_alert)

# 4. SHOW FINAL DATA
print("Final AQI Report:\n")
print(df[["Date", "Predicted_AQI", "Category", "Alert"]])

# 5. PIE CHART (MAIN VISUAL)
category_counts = df["Category"].value_counts()

plt.figure()

plt.pie(
    category_counts,
    labels=category_counts.index,
    autopct='%1.1f%%',
    startangle=90
)

plt.title(f"AQI Distribution - {city_name}")
plt.show()

print("\n Milestone 3 completed successfully!")