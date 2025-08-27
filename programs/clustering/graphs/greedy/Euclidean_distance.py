import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Dati di input (come prima)
data_list = [
    [4, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 3, 0, 1, 0, 3, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [2, 1, 1, 0, 1, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 3, 1, 0, 1, 2, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

categories = [
    "Existence and persistence", "Ownership and control", "Access and availability",
    "Transparency", "Persistence", "Portability", "Interoperability",
    "Consent", "Security and protection", "Privacy and minimal disclosure",
    "Cost", "Standard", "Decentralization and Autonomy",
    "DD", "Usability and consistency"
]

# Convert to DataFrame
df = pd.DataFrame(data_list, index=categories)

# Calcola la matrice delle distanze Euclidee
distance_matrix = squareform(pdist(df, metric='euclidean'))

# Stampa esplicita della matrice risultante
print("Matrice delle distanze Euclidee:")
print(pd.DataFrame(distance_matrix, index=categories, columns=categories))

# Crea la heatmap con seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(distance_matrix, annot=True, cmap='YlGnBu', xticklabels=categories, yticklabels=categories, cbar=True)
plt.title("")

# Etichette assi
plt.xlabel("Principles", fontsize=12)
plt.ylabel("Principles", fontsize=12)

# Ruota le etichette sull'asse X
plt.xticks(rotation=45, ha='right')

plt.show()

# Calcolo percentili sulle distanze nella parte superiore della matrice
distances = distance_matrix[np.triu_indices(len(categories), k=1)]
percentili = np.percentile(distances, [25, 50, 75])

print(f"25° percentile: {percentili[0]:.3f}")
print(f"50° percentile (mediana): {percentili[1]:.3f}")
print(f"75° percentile: {percentili[2]:.3f}")
