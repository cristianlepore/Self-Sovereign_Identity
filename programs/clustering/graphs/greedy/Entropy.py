import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
import seaborn as sns
import matplotlib.pyplot as plt

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

principles = list(data.keys())

for key in data:
    data[key] = data[key] + [0] * (len(categories) - len(data[key]))

df = pd.DataFrame(data, index=categories, columns=principles).T

def entropy(row):
    prob = row / np.sum(row)  # Convert to probabilities
    prob = prob[prob > 0]  # Avoid log(0)
    return -np.sum(prob * np.log2(prob))

entropies = df.apply(entropy, axis=1)

def js_divergence(p, q):
    p = p / np.sum(p)
    q = q / np.sum(q)
    m = 0.5 * (p + q)
    return 0.5 * stats.entropy(p, m) + 0.5 * stats.entropy(q, m)

distance_matrix = squareform(pdist(df, metric=js_divergence))

clustering = AgglomerativeClustering(n_clusters=5, metric='precomputed', linkage='average')
clusters = clustering.fit_predict(distance_matrix)

g = sns.clustermap(df, row_cluster=True, col_cluster=False, method='average', cmap='Blues', figsize=(10, 6))

plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=45, ha="right")

g.ax_heatmap.collections[0].colorbar.remove()

g.ax_heatmap.set_xlabel("Categories", fontsize=12)
g.ax_heatmap.set_ylabel("Principles", fontsize=12)

plt.show()

cluster_df = pd.DataFrame({"Principle": principles, "Cluster": clusters})
print(cluster_df.sort_values(by="Cluster"))
