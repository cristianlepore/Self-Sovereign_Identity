import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import community as community_louvain  # Louvain clustering algorithm
from io import StringIO

# Define CSV data as a multiline string
# (Replace with your actual CSV file content if needed)
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

# Load the CSV string data into a pandas DataFrame using StringIO
df = pd.read_csv(StringIO(csv_data))

# Prepare the DataFrame:
# - Set the first column as the index (principle names)
# - Remove any unwanted columns such as "Unnamed: 1" if they exist
# - Remove the name of the index to keep the DataFrame tidy
# - Convert all entries to numeric, coercing invalid values to NaN
df_cleaned = df.set_index(df.columns[0]).drop(columns=["Unnamed: 1"], errors='ignore')
df_cleaned.index.name = None
df_cleaned = df_cleaned.apply(pd.to_numeric, errors='coerce')

# Create an empty undirected graph
G = nx.Graph()

# Extract node names from the DataFrame index (principles)
principles = df_cleaned.index.tolist()

# Add each principle as a node to the graph
G.add_nodes_from(principles)

# Add edges to the graph based on DataFrame values
# Iterate only over upper triangle (i < j) to avoid duplicates and self-loops
for i, principle1 in enumerate(principles):
    for j, principle2 in enumerate(principles):
        if i < j:
            weight = df_cleaned.iloc[i, j]
            # Add edge only if weight exists and is positive
            if not pd.isna(weight) and weight > 0:
                G.add_edge(principle1, principle2, weight=weight)

# Apply the Louvain method to find communities (clusters) within the graph
partition = community_louvain.best_partition(G)

# Count how many clusters were found
num_clusters = len(set(partition.values()))

# Generate a color palette with one distinct color per cluster
cluster_colors = sns.color_palette("husl", num_clusters)

# Assign each node a color based on its cluster membership
node_colors = [cluster_colors[partition[node]] for node in G.nodes()]

# Extract edge weights for visual thickness (scaled down by half)
edge_widths = [d["weight"] / 2 for (_, _, d) in G.edges(data=True)]

# Create a matplotlib figure for plotting
plt.figure(figsize=(12, 10))

# Calculate node positions using a force-directed layout for clarity
pos = nx.spring_layout(G, seed=42, k=0.4)

# Draw edges with transparency and thickness proportional to weights
nx.draw_networkx_edges(G, pos, alpha=0.6, width=edge_widths, edge_color="gray")

# Draw nodes colored by their cluster with black edges and fixed size
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, edgecolors="black")

# Add labels to nodes with a smaller font size and bold style
nx.draw_networkx_labels(G, pos, font_size=6, font_weight="bold")

# Create legend handles to describe cluster colors
legend_labels = {i: f"Cluster {i+1}" for i in range(num_clusters)}
handles = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=cluster_colors[i], markersize=10)
    for i in range(num_clusters)
]

# Add legend to the plot, placing it automatically at the best location
plt.legend(handles, legend_labels.values(), title="Clusters", loc="best", fontsize=8)

# Remove the frame around the plot for a cleaner look
plt.gca().set_frame_on(False)

# Display the final graph visualization
plt.show()
