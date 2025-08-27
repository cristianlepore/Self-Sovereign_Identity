import matplotlib.pyplot as plt
import numpy as np

# Definition of principles and steps
principles = [
    "Access and availability", "Existence and persistence", "Security and protection", "Interoperability", "Ownership and control", "Persistence", "Cost", "Standard", "Usability and consistency", "Transparency", "Consent", "Decentralization and Autonomy", "Privacy and minimal disclosure", "Verifiability and Authenticity", "Portability"
]

steps = list(range(1, 16))

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

# Identify changes between steps and assign to the next step
change_points = []
change_counts = [0] * len(principles)  # Counter for changes per principle

for step in range(len(steps) - 1):
    for i, principle in enumerate(principles):
        if group_assignments[i][step] != group_assignments[i][step + 1]:
            change_points.append((step + 2, i))  # Assigning to the next step
            change_counts[i] += 1  # Increment change counter

# Visualize changes in a graph
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(
    [x[0] for x in change_points], 
    [x[1] for x in change_points], 
    color='blue', 
    marker=(3, 0, 270),  # Triangle pointing left
    label='Principle that changed group\nfrom the previous step.'
)  
ax.set_xticks(steps)
ax.set_yticks(range(len(principles)))
ax.set_yticklabels(principles)
ax.set_xlabel("Values of the parameter k")
ax.set_ylabel("Principles")
ax.set_title("")

# Force the legend to the top-right corner on two lines
ax.legend(loc='upper right', fontsize=10, frameon=True)

# Add grid for better readability
ax.grid(True, linestyle='--', alpha=0.6)

# Add title for the occurrences column above the text on the left
ax.text(-0.5, -2, "", fontsize=10, fontweight='bold', color='black', horizontalalignment='center')

# Add change counts as text outside the left-hand side of the graph with reduced column width
for i, count in enumerate(change_counts):
    ax.text(-0.5, i, f"({count})", verticalalignment='center', fontsize=10, color='black')

# Adjust limits to fit the additional column
ax.set_xlim(-0.7, len(steps) + 2)

plt.xticks(rotation=0, ha='right')
plt.tight_layout()
plt.show()

# Print the changes
changes = {}
for step in range(len(steps) - 1):
    changed_principles = []
    for i, principle in enumerate(principles):
        if group_assignments[i][step] != group_assignments[i][step + 1]:
            changed_principles.append(principle)
    changes[f"Step {steps[step + 1]}"] = changed_principles  # Assigning to the next step

for transition, changed in changes.items():
    print(f"{transition}: {', '.join(changed) if changed else 'No changes'}")

# Print the total count of changes per principle
print("\nTotal number of changes per principle:")
for principle, count in zip(principles, change_counts):
    print(f"{principle}: {count}")
