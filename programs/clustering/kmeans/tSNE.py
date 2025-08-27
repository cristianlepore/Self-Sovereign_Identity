import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.patheffects as pe

# Data setup (same as provided)
data = {
        "Existence and representation": [4, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Ownership and control":        [5, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Consent":                      [5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        "Access and availability":      [0, 3, 0, 1, 0, 3, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "Security and protection":      [0, 0, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        "Persistence":                  [1, 1, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "Privacy and minimal disclosure":[2, 1, 1, 0, 1, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        "Portability":                  [0, 0, 1, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0],
        "Transparency":                 [0, 0, 0, 0, 0, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "Interoperability":             [0, 0, 0, 0, 0, 3, 1, 0, 1, 2, 1, 1, 0, 0, 0, 1, 1, 0],
        "Cost":                         [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
        "Standard":                     [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        "Decentralization and Autonomy":[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        "Verifiability and Authenticity":[0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Usability and consistency":    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

categories = [
    "Controllability", "Foundational", "Personal Data", "Agency", "User",
    "Portability", "Sustainability", "Security", "Usability", "Flexibility",
    "Autonomy", "Technology", "Operability", "Zero-cost", "Acceptance", "Adoption", "Compliance", "Privacy",
]

df = pd.DataFrame(data, index=categories)
df_transposed = df.T

# Apply t-SNE to reduce dimensions
tsne = TSNE(n_components=2, perplexity=5, random_state=42)
tsne_results = tsne.fit_transform(df_transposed)

# Apply KMeans clustering
num_clusters = 5  # Number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
clusters = kmeans.fit_predict(tsne_results)

# Define distinct colors for each cluster
cluster_colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2']  # Red, Blue, Green, Yellow, Purple

# Plot the results with bigger text
plt.figure(figsize=(12, 8))

for i in range(num_clusters):
    cluster_points = tsne_results[clusters == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                c=[cluster_colors[i]], label=f'Cluster {i + 1}', s=150)  # punti più grandi

principles = df.columns
label_fontsize = 16  # font più grande per i label

for i, principle in enumerate(principles):
    plt.text(tsne_results[i, 0], tsne_results[i, 1], principle, 
             fontsize=label_fontsize, ha='right',
             path_effects=[pe.withStroke(linewidth=3, foreground="white")])  # contorno bianco per leggibilità

plt.xlabel("Dimension 1", fontsize=16)
plt.ylabel("Dimension 2", fontsize=16)
plt.legend(fontsize=14)
plt.tight_layout()
plt.show()
