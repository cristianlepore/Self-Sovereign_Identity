import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Recreating the data from the table in the image (simplified for example)
data = {
        "Existence and representation": [4, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Ownership and control":        [5, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Consent":                      [5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        "Access and availability":      [0, 3, 0, 1, 0, 3, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "Security and protection":      [0, 0, 1, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        "Persistence":                  [1, 1, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "Privacy and minimal disclosure":[2, 1, 1, 0, 1, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        "Portability":                  [0, 0, 1, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0, 0, 0, 1, 0, 0],
        "Transparency":                 [0, 0, 0, 0, 0, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "Interoperability":             [0, 0, 0, 0, 0, 3, 1, 0, 1, 2, 1, 1, 0, 0, 0, 1, 1, 0],
        "Cost":                         [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
        "Standard":                     [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        "Decentralization and Autonomy":[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        "Verifiability and Authenticity":[0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Usability and consistency":    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

categories = [
    "Controllability", "Foundational", "Personal Data", "Agency", "User",
    "Portability", "Sustainability", "Security", "Usability", "Flexibility",
    "Autonomy", "Technology", "Operability", "Zero-cost", "Acceptance", "Adoption", "Compliance", "Privacy",
]

occurrence = [7, 7, 6, 3, 2, 4, 5, 5, 5, 3, 4, 3, 3, 1, 1, 6, 2, 1]

# Crea il DataFrame
df = pd.DataFrame(data, index=categories)
# df_normalized = (df / 98) * 100

# Crea il grafico a barre in grigio
df.sum(axis=1).plot(
    kind="bar",
    figsize=(12, 6),
    color="#888888",           # Grigio medio
    edgecolor="black"
)

# Personalizzazioni del grafico
plt.title("")
plt.xlabel("Categories")
plt.ylabel("Occurrence of principles")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
