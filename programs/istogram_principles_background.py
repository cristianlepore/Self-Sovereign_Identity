import matplotlib.pyplot as plt
import numpy as np

# Definizione dei livelli come lista di dizionari (colori in scala di grigio)
layers = [
    {"label": "Technical and Regulatory", "radius": 0.5, "color": 'lightgray'},
    {"label": "Legal and Social", "radius": 1.0, "color": 'gray'},
    {"label": "Ethical and Organizational", "radius": 1.5, "color": 'darkgray'}
]

# Termini chiave associati ai layer
keywords = {
}

# Inizializza il grafico
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.axis('off')

# Disegna i cerchi concentrici con trasparenza
for layer in layers:
    circle = plt.Circle((0, 0), layer["radius"], color=layer["color"], ec='black', alpha=0.4)
    ax.add_artist(circle)
    ax.text(0, layer["radius"] - 0.25, layer["label"], color='black',
            fontsize=12, ha='center', va='center', weight='bold')

# Etichette periferiche per "ETHICAL-SOCIAL LAYER" in grigio scuro
ethics_keywords = keywords.get("ETHICAL-SOCIAL LAYER", [])
angle_step = 360 / len(ethics_keywords) if ethics_keywords else 0
for i, word in enumerate(ethics_keywords):
    angle = np.deg2rad(i * angle_step)
    x = 2.3 * np.cos(angle)
    y = 2.3 * np.sin(angle)
    ax.text(x, y, word, ha='center', va='center', fontsize=11, color='dimgray')

# Etichette per "TECHNICAL LAYER" in grigio scuro
tech_keywords = keywords.get("TECHNICAL LAYER", [])
angle_step = 360 / len(tech_keywords) if tech_keywords else 0
for i, word in enumerate(tech_keywords):
    angle = np.deg2rad(i * angle_step + 30)
    x = 1.2 * np.cos(angle)
    y = 1.2 * np.sin(angle)
    ax.text(x, y, word, ha='center', va='center', fontsize=11, color='dimgray')

# Imposta limiti degli assi per mantenere proporzioni corrette
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)

# Titolo in grigio scuro
plt.show()
