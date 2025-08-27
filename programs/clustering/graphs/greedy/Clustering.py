import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Creazione dei dati
data = {
    "25th": [
        "Existence and persistence", "Ownership and control", "Access and availability", 
        "Decentralization and Autonomy", "Persistence", "Portability", "Interoperability", 
        "Verifiability and authenticity", "Consent", "Security and protection", 
        "Privacy and minimal disclosure", "Cost", "Standard", "Usability and consistency", 
        "Transparency"
    ],
    "50th": [
        "Existence and persistence", "Ownership and control", "Access and availability", 
        "Decentralization and Autonomy", "Usability and consistency", "Transparency", "Portability", 
        "Consent", "Security and protection", "Privacy and minimal disclosure", 
        "Verifiability and authenticity", "Interoperability", "Persistence", "Cost", "Standard"
    ],
    "75th": [
        "Existence and persistence", "Ownership and control", "Access and availability", 
        "Transparency", "Portability", "Interoperability", "Consent", "Cost", "Standard", 
        "Decentralization and Autonomy", "Verifiability and authenticity", "Usability and consistency", 
        "Security and protection", "Privacy and minimal disclosure", "Persistence"
    ]
}

# Creazione del DataFrame
df = pd.DataFrame.from_dict(data, orient='index').transpose()

# Creazione della figura
plt.figure(figsize=(10, 6))
ax = plt.gca()

# Palette di colori personalizzata
colors = sns.color_palette("pastel", 5)  # 5 gruppi di colori

# Definizione dei gruppi per la prima colonna
color_mapping_col1 = [
    colors[0]] * 4 + [
    colors[1]] * 2 + [
    colors[2]] * 2 + [
    colors[3]] * 6 + [
    colors[4]]

# Definizione dei gruppi per la seconda colonna
color_mapping_col2 = [
    colors[0]] * 5 + [
    colors[1]] * 6 + [
    colors[2]] * 2 + [
    colors[3]] * 2

# Definizione dei gruppi per la terza colonna
color_mapping_col3 = [
    colors[0]] * 12 + [
    colors[1]] * 2 + [
    colors[2]]

# Creazione delle celle colorate
cell_colors = [[color_mapping_col1[i], color_mapping_col2[i], color_mapping_col3[i]] + ["white"] * (len(df.columns) - 3) for i in range(len(df))]

ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='left', loc='center', 
                 cellColours=cell_colors)

# Formattazione dell'header
table.auto_set_font_size(False)
table.set_fontsize(10)
for (i, key) in enumerate(df.columns):
    table[0, i].set_text_props(weight='bold')
    table[0, i].set_linewidth(0)

# Rimuovere i bordi delle celle
table.scale(1, 1.2)
for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_linewidth(0)
    else:
        cell.set_linewidth(0.5)

# Aggiunta della legenda con tutti i cluster
import matplotlib.patches as mpatches
legend_patches = [mpatches.Patch(color=colors[i], label=f'Cluster {i+1}') for i in range(len(colors))]
plt.legend(handles=legend_patches, loc='lower center', ncol=len(colors), frameon=False)

plt.show()
