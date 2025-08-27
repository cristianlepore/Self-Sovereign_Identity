import matplotlib.pyplot as plt
import pandas as pd

# Data for the table
data = {
    "Attribute": [
        "Existence and representation", "Ownership and control", "Access and availability", 
        "Transparency", "Persistence", "Portability", "Interoperability", "Consent", 
        "Security and protection", "Privacy and minimal disclosure", "Standard", "Cost", 
        "Usability and Consistency", "Decentralization and Autonomy", "Verifiability and Authenticity", 
        "Self-generatable and independent", "Opt-in", "Opt-out", "Simple", "Non-repudiatable", 
        "Reliable", "Equivalent", "Single Source", "Validity", "Freedom Information", "Auditability", 
        "Integrity", "Effectiveness", "Efficiency", "Manageability", "Trust", "Scalable", 
        "Equity and Inclusion", "Delegation"
    ],
    "Value": [
        0.92, 0.50, 0.50, 0.85, 0.65, 0.65, 0.86, 0.50, 0.50, 0.19, 0.85, 0.92, 0.92, 0.85, 0.92, 
        0.23, 0.23, 0.23, 0.50, 0.23, 0.23, 0.50, 0.50, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 
        0.50, 0.65, 0.23, 0.23
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the bar chart (now vertical with principles on the X-axis)
plt.figure(figsize=(12, 8))  # Set the size of the plot
plt.bar(df["Attribute"], df["Value"], color='skyblue', edgecolor='black')  # Vertical bar chart with black borders

# Add labels and title
plt.ylabel('Entropy')
plt.xlabel('Principles')
plt.title('')

# Rotate X-axis labels to make them readable
plt.xticks(rotation=45, ha="right")

# Adjust the layout for better display
plt.tight_layout()

# Display the plot
plt.show()
