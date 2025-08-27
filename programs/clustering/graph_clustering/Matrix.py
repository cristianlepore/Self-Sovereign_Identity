import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# CSV Data (Replace with actual CSV content)
csv_data = """Graph Theory,,Existence and persistence,Consent,Ownership and control,Security and protection,Persistence,Privacy and minimal disclosure,Access and availability,Transparency,Portability,Interoperability,Cost,Standard,Decentralization and Autonomy,Verifiability and Authenticity,Usability and consistency
Existence and persistence,, ,6,7,1,3,4,4,,1,,,,2,,2
Consent,,6,,6,,3,4,4,,2,1,,,3,,2
Ownership and control,,7,6,,,2,4,3,,,,,,2,,1
Security and protection,,1,,,,6,5,2,1,1,1,,,,2,
Persistence,,3,3,2,6,,7,3,2,2,1,1,1,2,2,
Privacy and minimal disclosure,,4,4,4,5,7,,3,1,2,1,,,2,2,1
Access and availability,,4,4,3,2,3,3,,5,2,4,1,,2,2,2
Transparency,,,,,1,2,1,5,,4,6,4,4,,1,1
Portability,,1,2,,1,2,2,2,4,,8,2,3,1,,
Interoperability,,,1,,1,1,1,4,6,8,,2,3,1,,1
Cost,,,,,,1,,1,4,2,2,,4,1,,
Standard,,,,,,1,,,4,3,3,4,,,,
Decentralization and Autonomy,,2,3,2,,2,2,2,,1,1,1,,,,1
Verifiability and Authenticity,, ,,,2,2,2,2,1,,,,,,,
Usability and consistency,,2,2,1,,,1,2,1,,1,,,1,,
"""

# Load the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# Clean the DataFrame by setting the first column as index and removing unnecessary columns
df_cleaned = df.set_index(df.columns[0]).drop(columns=["Unnamed: 1"], errors='ignore')
df_cleaned.index.name = None

# Convert all values to numeric, coercing errors to NaN
df_cleaned = df_cleaned.apply(pd.to_numeric, errors='coerce')

# Plot the heatmap with adjusted label alignment
plt.figure(figsize=(12, 8))
sns.heatmap(
    df_cleaned, 
    annot=True, 
    cmap="coolwarm", 
    fmt=".0f", 
    linewidths=0.5, 
    annot_kws={"size": 8}  # Smaller font for annotations
)

# Adjust font sizes and label alignment
plt.title("", fontsize=14)
plt.xlabel("Principles", fontsize=8, labelpad=8)  # Add x-axis label
plt.ylabel("Principles", fontsize=8, labelpad=8)  # Add y-axis label
plt.xticks(rotation=45, fontsize=8, ha="right")  # Align x-axis labels
plt.yticks(rotation=0, fontsize=8)

plt.show()
