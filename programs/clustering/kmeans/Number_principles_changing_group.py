import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Dati
steps = np.array(list(range(1, 16)))
group_counts_clusters = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
group_counts_principles = np.array([0, 12, 3, 6, 1, 2, 2, 6, 1, 1, 1, 1, 1, 1, 1])

# Curva smussata
smooth_steps = np.linspace(steps.min(), steps.max(), 300)
spline = make_interp_spline(steps, group_counts_principles, k=3)
smooth_counts = spline(smooth_steps)

# Colori
gray_dark = '#4d4d4d'   # Grigio per la prima curva
blue_muted = '#336699'  # Blu sobrio e accademico

# Stile del grafico
fig, ax = plt.subplots(figsize=(10, 6))
plt.style.use('seaborn-v0_8-muted')

# Linea 1: Number of Clusters
ax.plot(steps, group_counts_clusters, marker='o', linestyle='-', color=gray_dark, label='Number of Clusters')

# Linea 2: Principles that Changed Group
ax.plot(smooth_steps, smooth_counts, linestyle='-', color=blue_muted, linewidth=2.2, label='Principles that Change Group')
ax.scatter(steps, group_counts_principles, color=blue_muted, edgecolor='black', zorder=5)

# Etichette
ax.set_xlabel('Values of the parameter k', fontsize=14, color=gray_dark)
ax.set_ylabel('Number of principles', fontsize=14, color=gray_dark)

# Ticks e griglia
ax.set_xticks(steps)
ax.tick_params(colors=gray_dark)
ax.grid(True, linestyle='--', linewidth=0.5, color='#cccccc', alpha=0.6)

# Legenda
ax.legend(fontsize=12, facecolor='white', edgecolor='#e0e0e0')

# Sfondo
fig.patch.set_facecolor('white')
plt.tight_layout()
plt.show()
