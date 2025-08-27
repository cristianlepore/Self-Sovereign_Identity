import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Dati
principles = [
    "Access and availability", "Existence and persistence", "Security and protection", "Interoperability", "Ownership and control", "Persistence", "Cost", "Standard", "Usability and consistency", "Transparency", "Consent", "Decentralization and Autonomy", "Privacy and minimal disclosure",
    "Verifiability and Authenticity", "Portability"
]

steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

group_assignments = [
    [0,1,1,3,4,4,4,4,4,4,4,4,4,4,4],  # Access and availability
    [0,1,2,2,2,2,2,2,2,2,2,2,2,2,2],  # Existence and persistence
    [0,0,0,0,0,0,0,7,7,7,7,7,7,7,7],  # Security and protection
    [0,1,1,3,3,5,5,3,3,3,3,3,3,13,13], # Interoperability
    [0,1,2,2,2,2,2,2,2,2,2,2,12,12,12], # Ownership and control
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Persistence
    [0,1,1,3,3,3,6,5,5,5,5,5,5,5,5],  # Cost
    [0,1,1,3,3,3,6,5,5,5,5,5,5,5,14],  # Standard
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # Usability and consistency
    [0,1,1,3,3,3,3,6,6,6,6,6,6,6,6],  # Transparency
    [0,1,2,2,2,2,2,2,2,2,10,10,10,10,10],  # Consent
    [0,1,1,1,1,1,1,1,8,8,8,8,8,8,8],  # Decentralization and Autonomy
    [0,0,0,0,0,0,0,0,0,0,0,11,11,11,11],  # Privacy and minimal disclosure
    [0,1,1,1,1,1,1,1,1,9,9,9,9,9,9],  # Verifiability and Authenticity
    [0,1,1,3,3,5,5,3,3,3,3,3,3,3,3]  # Portability
]

# Colori per i gruppi
unique_groups = set(np.array(group_assignments).flatten())
colors = plt.cm.tab20(np.linspace(0, 1, len(unique_groups)))
color_map = {group: color for group, color in zip(unique_groups, colors)}

# Ordinamento dei principi per ogni step in base al gruppo
sorted_indices = []
for step in range(len(steps)):
    groups_at_step = [group_assignments[i][step] for i in range(len(principles))]
    sorted_indices.append(sorted(range(len(principles)), key=lambda x: groups_at_step[x]))

# Creazione del grafico
fig, ax = plt.subplots(figsize=(15, 10))

# Per memorizzare le posizioni verticali ordinate
sorted_positions = []
for step, indices in enumerate(sorted_indices):
    sorted_positions.append([principles[i] for i in indices])

# Tracciamento degli archi
for i, principle in enumerate(principles):
    for j in range(len(steps) - 1):
        # Determina le posizioni ordinate
        start_pos = sorted_indices[j].index(i)
        end_pos = sorted_indices[j + 1].index(i)
        
        x = [steps[j], steps[j + 1]]
        y = [start_pos, end_pos]
        group = group_assignments[i][j]
        ax.plot(x, y, color=color_map[group], linewidth=2, alpha=0.8)

# Personalizzazione del grafico
ax.set_title("Principles and Group Assignments Across Steps", fontsize=16, weight='bold')
ax.set_xlabel("Steps", fontsize=14)
ax.set_ylabel("Principles", fontsize=14)
ax.set_xticks(steps)
ax.set_yticks(range(len(principles)))
ax.set_yticklabels(principles, fontsize=10)
ax.grid(visible=True, alpha=0.3)

# Creazione della legenda
legend_elements = [plt.Line2D([0], [0], color=color_map[group], lw=4, label=f"Group {group}") for group in sorted(unique_groups)]
ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()
