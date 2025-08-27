import matplotlib.pyplot as plt
import numpy as np
import random

# Data
authors = ["Tobin and Reed", "Andrieu et al.", "Ferdous et al.", "Mühle et al.", "Gilani et al.", "Naik and Jenkins", "Sheldrake", "Toth and Kalman", "eSSIF-Lab", "ToIP", "Sovrin", "BkThDVr", "Glöckler et al.", "Pava-Díaz et al.", "Satybaldy et al.", "Stokkink and Pouwelse", "Čučko et al.", "Allen"]

categories = {
    "Controllability":  [4, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 3, 0],
    "Foundational":     [0, 0, 4, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Personal Data":    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
    "Agency":           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
    "User":             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    "Portability":      [4, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    "Sustainability":   [0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    "Security":         [3, 0, 2, 3, 3, 0, 0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 2, 0],
    "Usability":        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
    "Flexibility":      [0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Autonomy":         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
    "Technology":       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    "Operability":      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    "Zero-cost":        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Acceptance":       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Adoption":         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
    "Compliance":       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    "Privacy":          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
}

# categories = {
#     "Controllability":  [4/10, 3/5, 1/13, 1/9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3/10, 0, 0, 3/15, 0],
#     "Foundational":     [0, 0, 4/13, 0, 6/12, 0, 4/5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     "Personal Data":    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6/10, 0, 0, 0, 0, 0, 0],
#     "Agency":           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3/11, 0, 0, 0, 0, 0, 0, 0],
#     "User":             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/9, 0, 0, 0, 0, 0],
#     "Portability":      [4/10, 0, 0, 3/9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4/10, 0, 0, 0, 0],
#     "Sustainability":   [0, 0, 3/13, 0, 3/12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6/15, 0],
#     "Security":         [3/10, 0, 3/13, 3/9, 3/12, 0, 0, 0, 0, 0, 4/11, 0, 0, 3/10, 0, 0, 2/15, 0],
#     "Usability":        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/10, 0, 0, 0, 0, 2/15, 0],
#     "Flexibility":      [0, 0, 3/13, 0, 3/12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     "Autonomy":         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4/11, 0, 0, 0, 0, 0, 0, 0],
#     "Technology":       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3/9, 0, 0, 0, 0, 0],
#     "Operability":      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3/9, 0, 0, 0, 0, 0],
#     "Zero-cost":        [0, 1/5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     "Acceptance":       [0, 1/5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     "Adoption":         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6/15, 0],
#     "Compliance":       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/9, 0, 0, 0, 0],
#     "Privacy":          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/15, 0],
# }


category_values = np.array(list(categories.values()))

x, y, sizes = [], [], []
scaling_factor = 250  # Adjust this to control bubble sizes

for j, category in enumerate(categories.keys()):
    for i, author in enumerate(authors):
        value = category_values[j, i]
        if value > 0:
            x.append(j)
            y.append(i)
            sizes.append(value * scaling_factor)

# Create bubble chart
plt.figure(figsize=(12, 8))
scatter = plt.scatter(x, y, s=sizes, alpha=0.5, edgecolors='black', linewidths=0.5, color='#6e6e6e')

# Add text inside bubbles
for j, category in enumerate(categories.keys()):
    for i, author in enumerate(authors):
        value = category_values[j, i]
        if value > 0:
            plt.text(j, i, str(value), fontsize=10, ha='center', va='center', color='black', fontweight='bold')

plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Labels and title
plt.xticks(ticks=range(len(categories)), labels=categories.keys(), rotation=45, ha='right')
plt.yticks(ticks=range(len(authors)), labels=authors)
plt.xlabel("Categories", fontsize=16, fontweight='bold')
plt.ylabel("Authors", fontsize=16, fontweight='bold')
plt.title("")

# Add legend at mid-height
from matplotlib.lines import Line2D

legend_labels = [
]

plt.legend(handles=legend_labels, title="Bubble Size = Number of Principles", loc="center right", bbox_to_anchor=(1.05, 0.5))

# Show chart
plt.show()