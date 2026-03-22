# AIRAWARE SMART - MILESTONE 2
# AQI Prediction for Multiple Cities (Prophet)
import pandas as pd
from prophet import Prophet

print("Starting AQI Prediction for All Cities...\n")

# 1. LOAD DATA
data = pd.read_csv("../Data/city_day.csv")

# Get all unique cities
cities = data["City"].dropna().unique()

all_results = []

# 2. LOOP THROUGH EACH CITY
for city in cities:
    print(f"Processing: {city}")

    city_df = data[data["City"] == city][["Date", "AQI"]].dropna()

    # Skip small datasets
    if len(city_df) < 20:
        print("Skipping (not enough data)\n")
        continue

    # Convert and sort
    city_df["Date"] = pd.to_datetime(city_df["Date"])
    city_df = city_df.sort_values("Date")

    # Rename for Prophet
    city_df.rename(columns={"Date": "ds", "AQI": "y"}, inplace=True)

    # 3. TRAIN MODEL
    model = Prophet()
    model.fit(city_df)

    # 4. FUTURE DATES (next 10 days)
    future = model.make_future_dataframe(periods=10)

    # 5. PREDICT
    forecast = model.predict(future)

    # Keep only last 10 days
    output = forecast[["ds", "yhat"]].tail(10)

    output["City"] = city

    all_results.append(output)
    print("Done\n")

# 6. COMBINE ALL CITIES
final_df = pd.concat(all_results)

# Clean column names
final_df.rename(columns={
    "ds": "Date",
    "yhat": "Predicted_AQI"
}, inplace=True)

# Keep AQI realistic
final_df["Predicted_AQI"] = final_df["Predicted_AQI"].clip(10, 500)

# 7. SAVE FILE
final_df.to_csv("all_cities_aqi.csv", index=False)

print(" All cities AQI prediction saved as all_cities_aqi.csv\n")
