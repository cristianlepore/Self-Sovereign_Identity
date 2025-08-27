import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

principles = [
    "Persistence", "Usability and consistency", "Existence and persistence", "Portability", "Access and availability", "Cost", "Transparency", "Security and protection", "Decentralization and autonomy", "Verifiability and authenticity", "Consent", "Privacy and minimal disclosure", "Ownership and control",
    "Interoperability", "Standard"
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
    [0,1,1,1,1,1,1,1,8,8,8,8,8,8,8],  # Decentralization and autonomy
    [0,0,0,0,0,0,0,0,0,0,0,11,11,11,11],  # Privacy and minimal disclosure
    [0,1,1,1,1,1,1,1,1,9,9,9,9,9,9],  # Verifiability and authenticity
    [0,1,1,3,3,5,5,3,3,3,3,3,3,3,3]  # Portability
]

fig, ax = plt.subplots(figsize=(15, 10))
for i, principle in enumerate(principles):
    ax.plot(steps, group_assignments[i], marker="o", alpha=0.8, linewidth=2)

ax.set_title("", fontsize=20, weight='bold')  # font titolo più grande
ax.set_xlabel("Values of the parameter k", fontsize=18)
ax.set_ylabel("Groups", fontsize=18)
ax.set_xticks(steps)
ax.set_yticks(range(0, 15))
ax.grid(visible=True, alpha=0.3)

ax.text(16, 15, "Principles", fontsize=16, fontweight="bold", verticalalignment='bottom')

y_positions = range(0, 15)
for y_pos, principle in zip(y_positions, principles):
    ax.text(16, y_pos, principle, verticalalignment='center', fontsize=14)  # font più grande per le scritte a fianco

plt.tight_layout()
plt.show()
