import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create data dictionary with 3 columns representing percentiles (25th, 50th, 75th)
# Each column contains a list of principles ordered by some ranking
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

# Convert the dictionary to a pandas DataFrame, transpose to get proper orientation
df = pd.DataFrame.from_dict(data, orient='index').transpose()

# Create a matplotlib figure and axis
plt.figure(figsize=(10, 6))
ax = plt.gca()

# Define a pastel color palette with 5 colors (to represent different clusters/groups)
colors = sns.color_palette("pastel", 5)

# Define color mappings for each of the first three columns to group similar items by color
color_mapping_col1 = (
    [colors[0]] * 4 +   # First 4 rows get color 0
    [colors[1]] * 2 +   # Next 2 rows get color 1
    [colors[2]] * 2 +   # Next 2 rows get color 2
    [colors[3]] * 6 +   # Next 6 rows get color 3
    [colors[4]]         # Last row gets color 4
)

color_mapping_col2 = (
    [colors[0]] * 5 +   # First 5 rows get color 0
    [colors[1]] * 6 +   # Next 6 rows get color 1
    [colors[2]] * 2 +   # Next 2 rows get color 2
    [colors[3]] * 2     # Last 2 rows get color 3
)

color_mapping_col3 = (
    [colors[0]] * 12 +  # First 12 rows get color 0
    [colors[1]] * 2 +   # Next 2 rows get color 1
    [colors[2]]         # Last row gets color 2
)

# Create a list of cell colors for the whole DataFrame
# For each row, assign colors for first 3 columns, and white for remaining columns (if any)
cell_colors = [
    [color_mapping_col1[i], color_mapping_col2[i], color_mapping_col3[i]] + ["white"] * (len(df.columns) - 3)
    for i in range(len(df))
]

# Remove axes (no ticks or labels)
ax.axis('tight')  # Fit the axis tightly around the table
ax.axis('off')    # Hide the axis

# Create a table plot with:
# - cellText from DataFrame values
# - column labels
# - left-aligned text in cells
# - cell background colors from cell_colors
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='left',
    loc='center',
    cellColours=cell_colors
)

# Formatting the table header
table.auto_set_font_size(False)
table.set_fontsize(10)

# Make header bold and remove border lines from header cells
for (i, key) in enumerate(df.columns):
    table[0, i].set_text_props(weight='bold')
    table[0, i].set_linewidth(0)

# Scale the table cells to adjust height
table.scale(1, 1.2)

# Set border thickness of cells:
# - No border on header row
# - Thin border on all other cells
for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_linewidth(0)
    else:
        cell.set_linewidth(0.5)

# Add a legend below the table indicating cluster colors
import matplotlib.patches as mpatches

legend_patches = [
    mpatches.Patch(color=colors[i], label=f'Cluster {i+1}')
    for i in range(len(colors))
]

plt.legend(
    handles=legend_patches,
    loc='lower center',
    ncol=len(colors),
    frameon=False
)

# Show the final table plot
plt.show()
