import matplotlib.pyplot as plt
import numpy as np

principi = [
    "Portability", "Persistence", "Cost", 
    "Access and availability", "Usability and consistency", "Security and protection",
    "Consent", "Transparency", "Verifiability and Authenticity",
    "Decentralization and Autonomy", "Standard", "Interoperability",
    "Ownership and control", "Existence and representation", "Privacy and minimal disclosure"
]

avg_values = [4.92, 4.70, 4.55, 4.18, 4.07, 4.07, 4.00, 3.77, 3.74, 3.18, 2.96, 2.74, 2.70, 2.63, 1.04]

sd_values = [0.38, 1.05, 1.88, 1.91, 1.47, 1.35, 1.53, 1.59, 1.27, 0.91, 1.13, 1.54, 0.76, 1.38, 0.19]

x = np.arange(len(principi))
width = 0.6

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(x, avg_values, width, yerr=sd_values, capsize=5, color='lightgray', edgecolor='black')

ax.set_ylabel('Avarage', fontsize=13)
ax.set_xlabel('Principles', fontsize=13)
ax.set_title('')
ax.set_xticks(x)
ax.set_xticklabels(principi, rotation=45, ha='right', fontsize=13)
ax.set_ylim(0, 6)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # spostamento verticale
                textcoords="offset points",
                ha='center', va='bottom')

incidenza_media = sum((sd / avg) * 100 for sd, avg in zip(sd_values, avg_values)) / len(avg_values)
print(f"L'incidenza media della deviazione standard è: {incidenza_media:.2f}%")

plt.tight_layout()
plt.show()
