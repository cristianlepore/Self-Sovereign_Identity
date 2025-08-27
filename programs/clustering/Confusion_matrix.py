import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import normalized_mutual_info_score

# Dati forniti
principles = [
    "Existence and persistence", "Ownership and control", "Access and availability", "Decentralization and Autonomy",
    "Persistence", "Portability", "Interoperability", "Verifiability and authenticity", "Consent", 
    "Security and protection", "Privacy and minimal disclosure", "Cost", "Standard", "Usability and consistency", "Transparency"
]

clusters = {
    "Greedy 25th": [1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5],
    "Greedy 50th": [14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 16, 16, 17, 17],
    "Greedy 75th": [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 20],
    "KMNS": [6, 6, 7, 9, 8, 10, 10, 9, 6, 8, 8, 10, 10, 9, 10],
    "Louvain": [11, 11, 11, 11, 13, 12, 12, 13, 11, 13, 13, 12, 12, 11, 12],
    "Greedy + Entropy": [21, 21, 24, 21, 23, 22, 22, 23, 21, 23, 23, 22, 22, 24, 22],
}

methods = list(clusters.keys())
n_methods = len(methods)

nmi_matrix = np.zeros((n_methods, n_methods))

for i in range(n_methods):
    for j in range(n_methods):
        nmi_matrix[i, j] = normalized_mutual_info_score(clusters[methods[i]], clusters[methods[j]])

# Heatmap in scala di grigi
plt.figure(figsize=(8, 6))
sns.heatmap(nmi_matrix, annot=True, xticklabels=methods, yticklabels=methods, cmap="Greys", cbar=True)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
