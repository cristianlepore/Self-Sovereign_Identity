import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import community as community_louvain  # Louvain clustering
from io import StringIO

# CSV Data (Replace with actual CSV content)
csv_data = """Graph Theory,,Existence and persistence,Consent,Ownership and control,Security and protection,Persistence,Privacy and minimal disclosure,Access and availability,Transparency,Portability,Interoperability,Cost,Standard,Decentralization and Autonomy,Verifiability and Authenticity,Usability and consistency
Existence and persistence,, ,6,7,1,3,4,4,,1,,,,2,,2
Consent,,6,,6,,3,4,4,,2,1,,,3,,2
Ownership and control,,7,6,,,2,4,3,,,,,,2,,1
Security and protection,,1,,,,6,5,2,1,1,1,,,,2,
Persistence,,3,3,2,6,,7,3,2,2,1,1,1,2,2,
Privacy and minimal disclosure,,4,4,4,5,7,,3,1,2,1,,,2,2,1
Access and availability,,4,4,3,2,3,3,,5,2,4,1,,2,2,2
Transparency,,,,,1,2,1,5,,4,6,4,4,,1,1
Portability,,1,2,,1,2,2,2,4,,8,2,3,1,,
Interoperability,,,1,,1,1,1,4,6,8,,2,3,1,,1
Cost,,,,,,1,,1,4,2,2,,4,1,,
Standard,,,,,,1,,,4,3,3,4,,,,
Decentralization and Autonomy,,2,3,2,,2,2,2,,1,1,1,,,,1
Verifiability and Authenticity,, ,,,2,2,2,2,1,,,,,,,
Usability and consistency,,2,2,1,,,1,2,1,,1,,,1,,
"""

# Load the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# Clean the DataFrame: Set first column as index and remove unnecessary columns
df_cleaned = df.set_index(df.columns[0]).drop(columns=["Unnamed: 1"], errors='ignore')
df_cleaned.index.name = None
df_cleaned = df_cleaned.apply(pd.to_numeric, errors='coerce')

# Create a graph
G = nx.Graph()

# Add nodes (principles)
principles = df_cleaned.index.tolist()
G.add_nodes_from(principles)

# Add edges based on heatmap values
for i, principle1 in enumerate(principles):
    for j, principle2 in enumerate(principles):
        if i < j:  # Avoid duplicate edges
            weight = df_cleaned.iloc[i, j]
            if not pd.isna(weight) and weight > 0:  # Add edges only if weight is valid
                G.add_edge(principle1, principle2, weight=weight)

# Apply Louvain clustering to detect communities
partition = community_louvain.best_partition(G)

# Determine the number of clusters
num_clusters = len(set(partition.values()))

# Generate distinct colors for each cluster
cluster_colors = sns.color_palette("husl", num_clusters)

# Assign a color to each node based on its cluster
node_colors = [cluster_colors[partition[node]] for node in G.nodes()]

# Extract edge weights for thickness representation
edge_widths = [d["weight"] / 2 for (u, v, d) in G.edges(data=True)]  # Scale edge thickness

# Draw the graph
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42, k=0.4)  # Force-directed layout

# Draw edges with varying thickness
nx.draw_networkx_edges(G, pos, alpha=0.6, width=edge_widths, edge_color="gray")

# Draw nodes with cluster colors
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, edgecolors="black")

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=6, font_weight="bold")

# Add legend for clusters
legend_labels = {i: f"Cluster {i+1}" for i in range(num_clusters)}
handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=cluster_colors[i], markersize=10) for i in range(num_clusters)]
plt.legend(handles, legend_labels.values(), title="Clusters", loc="best", fontsize=8)

# Remove frame around the plot
plt.gca().set_frame_on(False)

# Show the plot
plt.show()
