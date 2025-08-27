import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

principi = [
    "Existence", "Control", "Access", "Transparency", "Persistence", "Portability",
    "Interoperability", "Consent", "Protection", "Minimization", "Self-generatable and independent",
    "Opt-in", "Opt-out", "Recoverable", "Simple", "Non-repudiatable", "Reliable", "Equivalent",
    "Autonomy", "Ownership", "Single Source", "Choosability", "Standard", "Cost", "Availability",
    "Disclosure", "Validity", "Freedom Information", "Participation", "Auditability", "Compliance",
    "Integrity", "Security", "Effectiveness", "Efficiency", "Manageability", "Privacy", "Trust",
    "Usability", "Identity Assurance", "Verification", "Counterfait Prevention", "Scalable",
    "Representation", "Equity and Inclusion", "Consistency", "Delegation", "Decentralization",
    "Identity Verification", "Secure Identity Transfer", "Secure Transactions", "Provability"
]

autori = [
    "Tobin and Reed", "Andrieu et al.", "Ferdous et al.", "Mühle et al.", "Gilani et al.",
    "Naik and Jenkins", "Sheldrake", "Toth and Kalman", "eSSIF-Lab", "ToIP", "Sovrin", "BkThDVr",
    "Glöckler et al.", "Pava-Díaz et al.", "Satybaldy et al.", "Stokkink and Pouwelse",
    "Čučko et al.", "Allen"
]

matrix = [
    [1,0,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1],  # Existence
    [1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],  # Control
    [1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1],  # Access
    [1,0,1,1,1,1,0,0,0,1,1,1,0,1,1,1,1,1],  # Transparency
    [1,0,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1],  # Persistence
    [1,0,1,0,1,1,0,1,0,1,1,1,1,1,1,1,1,1],  # Portability
    [1,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1],  # Interoperability
    [1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,1],  # Consent
    [1,0,1,1,1,1,0,0,1,1,0,1,0,1,1,1,1,1],  # Protection
    [1,1,1,1,1,0,0,0,1,1,1,1,0,1,0,1,1,1],  # Minimization
    [0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],  # Self-generatable and independent
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Opt-in
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Opt-out
    [0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],  # Recoverable
    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],  # Simple
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Non-repudiatable
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Reliable
    [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],  # Equivalent
    [0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0],  # Autonomy
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],  # Ownership
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],  # Single Source
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Choosability
    [0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0],  # Standard
    [0,1,1,0,1,1,0,0,0,0,0,0,1,0,0,0,1,0],  # Cost
]

additional_matrix = [
    [0,0,1,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0],  # Availability
    [0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0],  # Disclosure
    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],  # Validity
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],  # Freedom Information
    [0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],  # Participation
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],  # Auditability
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0],  # Compliance
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],  # Integrity
    [0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0],  # Security
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],  # Effectiveness
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],  # Efficiency
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],  # Manageability
    [0,0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0],  # Privacy
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0],  # Trust
    [0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0],  # Usability
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # Identity Assurance
    [0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0],  # Verification
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # Counterfeit Prevention
    [0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0],  # Scalable
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],  # Representation
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],  # Equity and Inclusion
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],  # Consistency
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],  # Delegation
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],  # Decentralization
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # Identity Verification
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # Secure Identity Transfer
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],  # Secure Transactions
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]   # Provability
]

matrix.extend(additional_matrix)

# Trasposizione
def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]

dati = transpose_matrix(matrix)

# Plot
fig, ax = plt.subplots(figsize=(20, 12))  # figura più grande

for i in range(len(autori)):
    for j in range(len(principi)):
        if dati[i][j] == 1:
            ax.scatter(j, i, s=120, color='black')

ax.set_xticks(range(len(principi)))
ax.set_xticklabels(principi, rotation=45, ha="right", fontsize=14)
ax.set_yticks(range(len(autori)))
ax.set_yticklabels(autori, fontsize=14)

legend_marker = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                               markersize=12, label="Instance of a principle")
plt.legend(handles=[legend_marker], loc="upper right", fontsize=18)

plt.xlabel("Principles", fontsize=20, fontweight='bold')
plt.ylabel("Authors", fontsize=20, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
