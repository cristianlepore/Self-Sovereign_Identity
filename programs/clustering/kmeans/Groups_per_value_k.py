import matplotlib.pyplot as plt

# Data: number of groups per step
steps = list(range(1, 16))
group_counts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(steps, group_counts, marker='o', linestyle='-', color='b', label='Number of Clusters')

# Customize the plot
ax.set_title('', fontsize=16)
ax.set_xlabel('Values of the parameter k', fontsize=14)
ax.set_ylabel('Number of clusters', fontsize=14)
ax.set_xticks(steps)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
