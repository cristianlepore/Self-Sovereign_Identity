import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.table import Table

# Dati della tabella
dati = {
    "Category": ["Allen's principles", "Extending 24 principles"],
    "Frequency": ["≈ 80% of authors", "< 10% of authors"],
    "Authors": ["≈ 13 authors", "< 2 authors"]
}

# Creazione del DataFrame
df = pd.DataFrame(dati)

# Creazione della figura
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis('tight')
ax.axis('off')

# Creazione della tabella
tabella = ax.table(cellText=df.values, 
                   colLabels=df.columns, 
                   cellLoc='center', 
                   loc='center',
                   colColours=["lightgray"] * len(df.columns))  # Colore per l'header

# Impostare il testo in grassetto per l'intestazione e aumentare la dimensione del carattere
for (i, j), cell in tabella.get_celld().items():
    if i == 0:  # Header row
        cell.set_text_props(weight='bold', fontsize=30)
    else:
        cell.set_text_props(fontsize=30)

# Salvataggio come immagine
plt.savefig("tabella.png", dpi=300, bbox_inches='tight')

# Mostra l'immagine
plt.show()
