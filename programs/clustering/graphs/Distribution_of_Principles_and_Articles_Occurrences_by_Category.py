import matplotlib.pyplot as plt
import numpy as np

# Data
concepts = [
    "Controllability", "Foundational", "Personal Data", "Agency", "User",
    "Portability", "Sustainability", "Security", "Usability", "Flexibility",
    "Autonomy", "Technology", "Operability", "Zero-cost", "Acceptance", "Adoption", "Compliance", "Privacy"
]
concepts = concepts[::-1]

# Occurrence of unique principles (right side)
principles = np.array([7, 7, 6, 3, 2, 4, 5, 8, 4, 3, 4, 3, 3, 1, 1, 6, 2, 2])
principles = principles[::-1]

# Occurrence of unique articles (left side, but positive values)
articles = np.array([7, 3, 1, 1, 1, 3, 3, 7, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1])
articles = articles[::-1]

# Indices for the Y-axis
y = np.arange(len(concepts))

plt.figure(figsize=(12, 8))

# Academic green and light gray
gray = "#606060"
light_gray = "#D3D3D3"

# Horizontal bars
bars1 = plt.barh(y, principles, color=gray, edgecolor='black', label="Principles", height=0.6)
bars2 = plt.barh(y, -articles, color=light_gray, edgecolor='black', label="Articles", height=0.6)

# Grid lines
for i in y:
    plt.axhline(i, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# Value labels
for bar in bars1:
    plt.text(bar.get_width() - 0.5, bar.get_y() + bar.get_height()/2, str(int(bar.get_width())), 
             va='center', ha='right', fontsize=10, color='white')

for bar in bars2:
    plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, str(abs(int(bar.get_width()))), 
             va='center', ha='left', fontsize=10, color='black')

# Labels and layout
plt.xlabel("")
plt.ylabel("Categories", fontsize=16, fontweight='bold')
plt.title("")
plt.yticks(y, concepts)
plt.xticks([])
plt.axvline(0, color='black', linewidth=1)
plt.legend()
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Titles
plt.text(-max(articles) / 2, len(concepts) + 0.5, "Articles occurrence", fontsize=14, fontweight='bold', color=light_gray, ha='center')
plt.text(max(principles) / 2, len(concepts) + 0.5, "Principles occurrence", fontsize=14, fontweight='bold', color=gray, ha='center')

plt.show()
