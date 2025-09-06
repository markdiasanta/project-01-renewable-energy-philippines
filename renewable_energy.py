import pandas as pd
import matplotlib.pyplot as plt

# importing the dataset
ps = pd.read_csv(
    'power_source.csv',
    delimiter='\t',
    encoding='utf-16'
)

# Initial data exploration to understand the structure and content of the dataset.
ps.info()
print (ps.head())
print (ps.tail())

# converting all columns except to int after removing commas
for col in ps.columns: 
    ps[col] = ps[col].astype(str).str.replace(',', '').astype(int)

# Checking the data again after conversion
ps.info()
print (ps.head())
print (ps.tail())

# Save the cleaned data to a new CSV file
ps.to_csv('cleaned_power_source.csv', index=False, encoding='utf-8')

# Plot line chart for all fuel sources to visualize trends over time
ps.set_index("Years")[["Biomass", "Coal", "Geothermal", "Hydro", 
                       "Natural Gas", "Oil-based", "Solar", "Wind"]].plot(
    kind="line", figsize=(12,6)
)
plt.title("Philippines Power Generation by Fuel Source (1990–2020)")
plt.ylabel("Power Generated (GWh)")
plt.legend(title="Fuel Source")
plt.grid(True, linestyle="--", alpha=0.5)

# Plot area chart for all fuel sources to visualize composition over time
ps.set_index("Years")[["Biomass", "Coal", "Geothermal", "Hydro", 
                       "Natural Gas", "Oil-based", "Solar", "Wind"]].plot(
    kind="area", stacked=True, figsize=(12,6), alpha=0.8
)
plt.title("Philippines Energy Mix Composition (1990–2020)")
plt.ylabel("Power Generated (GWh)")

# Define energy groups
renewables = ["Biomass", "Geothermal", "Hydro", "Solar", "Wind"]
fossil = ["Coal", "Natural Gas", "Oil-based"]

# Calculate group totals
ps["Renewables"] = ps[renewables].sum(axis=1)
ps["Fossils"] = ps[fossil].sum(axis=1)

# Calculate total (Renewables + Fossils only, ignoring Grand Total for clarity)
ps["Total"] = ps["Renewables"] + ps["Fossils"]

# Compute % share per energy group
ps["Renewables %"] = (ps["Renewables"] / ps["Total"]) * 100
ps["Fossils %"] = (ps["Fossils"] / ps["Total"]) * 100

# Plot line chart to show the growth of energy groups
ax = ps.plot(x="Years", 
             y=["Renewables", "Fossils"], 
             kind="line", 
             figsize=(10,6)
             )
labels = [
    f"Renewables: ({', ' .join(renewables)})",
    f"Fossils: ({', '.join(fossil)})"
]
ax.legend(labels=labels, title="Energy Groups")
plt.title("Renewables vs Fossil Fuels (1990–2020)")
plt.ylabel("Power Generated (GWh)")

# Plot % Share to show the share of energy groups
ax = ps.plot(
    x="Years",
    y=["Renewables %", "Fossils %"],
    kind="line",
    figsize=(10,6)
)
ax.legend(labels, title="Energy Groups")
plt.title("Renewables vs Fossil Fuels Share (%) (1990–2020)")
plt.ylabel("Share of Total Power Generation (%)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()