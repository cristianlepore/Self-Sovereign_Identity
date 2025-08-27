import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Original order of principles (left side)
principles_left = [
    "Access and availability", "Existence and persistence", "Security and protection", "Interoperability", 
    "Ownership and control", "Persistence", "Cost", "Standard", "Usability and consistency", "Transparency", 
    "Consent", "Decentralization and Autonomy", "Privacy and minimal disclosure", "Verifiability and Authenticity", 
    "Portability"
]

# Desired order of principles (right side)
principles_right = [
    "Persistence", "Usability and consistency", "Existence and persistence", "Portability", 
    "Access and availability", "Cost", "Transparency", "Security and protection", 
    "Decentralization and autonomy", "Verifiability and authenticity", "Consent", 
    "Privacy and minimal disclosure", "Ownership and control", "Interoperability", "Standard"
]

steps = np.arange(1, 16)

group_assignments = np.array([
    [0,1,1,3,4,4,4,4,4,4,4,4,4,4,4],  
    [0,1,2,2,2,2,2,2,2,2,2,2,2,2,2],  
    [0,0,0,0,0,0,0,7,7,7,7,7,7,7,7],  
    [0,1,1,3,3,5,5,3,3,3,3,3,3,13,13], 
    [0,1,2,2,2,2,2,2,2,2,2,2,12,12,12], 
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
    [0,1,1,3,3,3,6,5,5,5,5,5,5,5,5],  
    [0,1,1,3,3,3,6,5,5,5,5,5,5,5,14],  
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  
    [0,1,1,3,3,3,3,6,6,6,6,6,6,6,6],  
    [0,1,2,2,2,2,2,2,2,2,10,10,10,10,10],  
    [0,1,1,1,1,1,1,1,8,8,8,8,8,8,8],  
    [0,0,0,0,0,0,0,0,0,0,0,11,11,11,11],  
    [0,1,1,1,1,1,1,1,1,9,9,9,9,9,9],  
    [0,1,1,3,3,5,5,3,3,3,3,3,3,3,3]  
])

# Define colors for groups
unique_groups = np.unique(group_assignments)
colors = plt.cm.tab20(np.linspace(0, 1, len(unique_groups)))
color_map = {group: color for group, color in zip(unique_groups, colors)}

# Sort principles at each step
sorted_indices = np.argsort(group_assignments, axis=0)

# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

# Plot interpolated lines
for i, principle in enumerate(principles_left):
    y_positions = np.array([np.where(sorted_indices[:, j] == i)[0][0] for j in range(len(steps))])
    
    # Use moderate smoothing without extreme curvature
    x_smooth = np.linspace(steps.min(), steps.max(), 200)
    spline = make_interp_spline(steps, y_positions, k=2)
    y_smooth = spline(x_smooth)

    # Get primary color for the line
    main_group = group_assignments[i, len(steps) // 2]
    ax.plot(x_smooth, y_smooth, color=color_map[main_group], linewidth=1, alpha=0.8)

    # Add scatter points
    for step_idx, step in enumerate(steps):
        group = group_assignments[i, step_idx]
        ax.scatter(step, y_positions[step_idx], color=color_map[group], marker='o', s=20, zorder=3)  # Reduced size

# Left-side labels (original order)
ax.set_yticks(range(len(principles_left)))
ax.set_yticklabels(principles_left, fontsize=8)
ax.set_ylabel("")

# Right-side labels (desired order)
ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())  
ax2.set_yticks(range(len(principles_right)))
ax2.set_yticklabels(principles_right, fontsize=8)
ax2.set_ylabel("")
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()

# Graph title and labels
ax.set_title("", fontsize=14, weight='bold')
ax.set_xlabel("Values of the parameter k", fontsize=10)
ax.set_xticks(steps)
ax.grid(visible=True, alpha=0.3)

# Remove chart borders
for spine in ax.spines.values():
    spine.set_visible(False)
for spine in ax2.spines.values():
    spine.set_visible(False)

# Add boundary lines
ax.axvline(x=steps[0], color='black', linewidth=1, linestyle='--', alpha=0.7)
ax.axvline(x=steps[-1], color='black', linewidth=1, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
