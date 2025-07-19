import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

# Load the dataset
data = pd.read_csv("trafficdata.csv")

# Convert Start_Time to datetime
data['Start_Time'] = pd.to_datetime(data['Start_Time'])

# Extract hour and part of day
data['Hour'] = data['Start_Time'].dt.hour
data['Part_of_Day'] = data['Hour'].apply(lambda h: 
    'Morning' if 5 <= h < 12 else
    'Afternoon' if 12 <= h < 17 else
    'Evening' if 17 <= h < 21 else
    'Night'
)

# ------------------ 📊 VISUALIZATIONS ------------------

# 1. Accidents by Weather Condition
plt.figure(figsize=(8,5))
sns.countplot(y='Weather_Condition', data=data, order=data['Weather_Condition'].value_counts().index)
plt.title("Accidents by Weather Condition")
plt.tight_layout()
plt.show()

# 2. Accidents by Road Condition
plt.figure(figsize=(8,5))
sns.countplot(y='Road_Condition', data=data, order=data['Road_Condition'].value_counts().index)
plt.title("Accidents by Road Condition")
plt.tight_layout()
plt.show()

# 3. Accidents by Time of Day
plt.figure(figsize=(7,5))
sns.countplot(x='Part_of_Day', data=data, order=['Morning','Afternoon','Evening','Night'])
plt.title("Accidents by Time of Day")
plt.tight_layout()
plt.show()

# 4. Severity by Weather Condition
plt.figure(figsize=(8,5))
sns.boxplot(x='Weather_Condition', y='Severity', data=data)
plt.title("Severity Distribution by Weather")
plt.tight_layout()
plt.show()

# ------------------ 🗺️ HOTSPOT MAP ------------------

# Create base map
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=8)

# Add heatmap layer
heat_data = [[row['Latitude'], row['Longitude']] for index, row in data.iterrows()]
HeatMap(heat_data).add_to(m)

# Save map to HTML
m.save("accident_hotspots_map.html")
print("🗺️ Hotspot map saved as 'accident_hotspots_map.html'")

