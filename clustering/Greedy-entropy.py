import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
import seaborn as sns
import matplotlib.pyplot as plt

# Data dictionary where keys are principles and values are lists of counts
# corresponding to how each principle relates to different categories.
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

# List of categories (the "features" or groups) that correspond to counts in data
categories = [
    "Controllability", "Foundational", "Personal Data", "Agency", "User",
    "Portability", "Sustainability", "Security", "Usability", "Flexibility",
    "Autonomy", "Technology", "Operability", "Zero-cost", "Acceptance", "Adoption", "Compliance", "Privacy",
]

# Extract principle names from the data dictionary keys
principles = list(data.keys())

# Some lists in `data` may be shorter than categories; pad them with zeros for consistent length
for key in data:
    data[key] = data[key] + [0] * (len(categories) - len(data[key]))

# Create a DataFrame from the data, with principles as rows and categories as columns
df = pd.DataFrame(data, index=categories, columns=principles).T

# Define a function to compute entropy of a vector (row)
# Entropy measures the amount of uncertainty or diversity in distribution
def entropy(row):
    prob = row / np.sum(row)  # Convert counts to probabilities
    prob = prob[prob > 0]     # Remove zero probabilities to avoid log(0)
    return -np.sum(prob * np.log2(prob))  # Shannon entropy formula

# Calculate entropy for each principle (row-wise)
entropies = df.apply(entropy, axis=1)

# Define Jensen-Shannon divergence function between two probability distributions p and q
def js_divergence(p, q):
    p = p / np.sum(p)  # Normalize p to probabilities
    q = q / np.sum(q)  # Normalize q to probabilities
    m = 0.5 * (p + q)  # Mixture distribution
    # Compute JS divergence using symmetric KL divergence to mixture m
    return 0.5 * stats.entropy(p, m) + 0.5 * stats.entropy(q, m)

# Compute pairwise Jensen-Shannon distance matrix between principles
distance_matrix = squareform(pdist(df, metric=js_divergence))

# Perform hierarchical agglomerative clustering on the distance matrix
clustering = AgglomerativeClustering(n_clusters=5, metric='precomputed', linkage='average')
clusters = clustering.fit_predict(distance_matrix)

# Create a seaborn clustermap to visualize principles clustered by similarity
# Row clustering enabled, column clustering disabled
g = sns.clustermap(
    df,
    row_cluster=True,
    col_cluster=False,
    method='average',
    cmap='Blues',
    figsize=(10, 6)
)

# Rotate x-axis category labels for better readability
plt.setp(g.ax_heatmap.xaxis.get_majorticklabels(), rotation=45, ha="right")

# Remove the colorbar on the heatmap
g.ax_heatmap.collections[0].colorbar.remove()

# Set axis labels
g.ax_heatmap.set_xlabel("Categories", fontsize=12)
g.ax_heatmap.set_ylabel("Principles", fontsize=12)

# Display the plot
plt.show()

# Create a DataFrame mapping principles to their cluster assignments and print sorted by cluster
cluster_df = pd.DataFrame({"Principle": principles, "Cluster": clusters})
print(cluster_df.sort_values(by="Cluster"))
