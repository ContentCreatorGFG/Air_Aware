import pandas as pd
import matplotlib.pyplot as plt

# real dataset
df = pd.read_csv("Data/city_day.csv")

print("Dataset Loaded Successfully!\n")

# Show first 5 rows
print("First 5 Rows:")
print(df.head())

# Show column names
print("\nColumns in Dataset:")
print(df.columns)

# info
print("\nDataset Info:")
print(df.info())

# Basic statistics
print("\nSummary Statistics:")
print(df.describe())

# Remove rows where AQI is missing
df = df.dropna(subset=["AQI"])

# Convert Date column to datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Example: AQI trend for one city (Delhi example)
city_data = df[df["City"] == "Delhi"]

# Extract year from Date
city_data["Year"] = city_data["Date"].dt.year

# Calculate yearly average AQI
yearly_avg = city_data.groupby("Year")["AQI"].mean()

plt.figure()
yearly_avg.plot(kind="bar")

plt.title("Yearly Average AQI - Delhi")
plt.xlabel("Year")
plt.ylabel("Average AQI")
plt.xticks(rotation=45)

plt.show()
