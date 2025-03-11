#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import warnings
from shapely.errors import ShapelyDeprecationWarning

# Suppress ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
# Suppress specific seaborn UserWarnings
warnings.filterwarnings("ignore", message=".*The figure layout has changed to tight.*")



# Example dataset of population by continent
data = {
    'Continent': ['Asia', 'Africa', 'Europe', 'North America', 'South America', 'Oceania'],
    'Population': [4641054775, 1340598147, 747636026, 592072212, 430759766, 43111704]
}

# Create a DataFrame
df = pd.DataFrame(data)

# --- Seaborn Visualizations ---

sns.set(style="whitegrid")
# --- 1. Heatmap: Population Table ---
plt.figure(figsize=(6, 4))
pivot_table = df.pivot_table(index='Continent', values='Population', aggfunc='sum')
sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='coolwarm', linewidths=0.5, cbar_kws={'label': 'Population'})
plt.title("Heatmap of Population by Continent", fontsize=16)
plt.show()

# 2. Pair Plot
# Since pairplot requires numerical data, adding an ID column to represent continents
df['ID'] = range(1, len(df) + 1)
sns.pairplot(df[['ID', 'Population']], diag_kind="kde", plot_kws={'color': 'blue'}, diag_kws={'fill': True})

plt.suptitle("Pair Plot of Population Data", y=1.02, fontsize=16)
plt.show()
 
# --- 2. Line Plot: Population by Continent ---
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='Continent', y='Population', marker='o', color='blue', label="Population")
plt.title("Population Trend by Continent", fontsize=16)
plt.xlabel("Continent", fontsize=12)
plt.ylabel("Population (in billions)", fontsize=12)
plt.legend()
plt.show()

# --- 3. Histogram: Population Distribution ---
plt.figure(figsize=(10, 6))
sns.histplot(df['Population'], bins=10, kde=True, color='teal')
plt.title("Population Histogram", fontsize=16)
plt.xlabel("Population (in billions)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.show()
# --- 4. Bar Plot: Population by Continent ---
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Continent', y='Population', palette='viridis')
plt.title("Bar Plot of Population by Continent", fontsize=16)
plt.xlabel("Continent", fontsize=12)
plt.ylabel("Population (in billions)", fontsize=12)
plt.show()



# --- Geopandas Visualization ---

# Load world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Add a "Continent" column to the world GeoDataFrame
continent_mapping = {
    'Asia': ['China', 'India', 'Russia', 'Indonesia', 'Japan', 'Pakistan'],
    'Africa': ['Nigeria', 'South Africa', 'Egypt', 'Kenya', 'Ethiopia'],
    'Europe': ['Germany', 'France', 'UK', 'Italy', 'Spain'],
    'North America': ['United States', 'Canada', 'Mexico'],
    'South America': ['Brazil', 'Argentina', 'Colombia', 'Peru', 'Venezuela'],
    'Oceania': ['Australia', 'New Zealand', 'Papua New Guinea']
}

# Create a continent column in the world DataFrame
def get_continent(country_name):
    for continent, countries in continent_mapping.items():
        if country_name in countries:
            return continent
    return None

world['Continent'] = world['name'].apply(get_continent)

# Merge population data with GeoDataFrame
merged = world.merge(df, how='left', on='Continent')

# World map showing population by continent
plt.figure(figsize=(15, 10))
merged.plot(column='Population', cmap='YlGnBu', legend=True, 
            legend_kwds={'label': "Population by Continent", 'orientation': "horizontal"},
            missing_kwds={'color': 'lightgrey'})
plt.title("World Map: Population by Continent", fontsize=16)
plt.axis('off')
plt.show()


# In[ ]:




