import matplotlib.pyplot as plt
import pandas as pd
import textwrap

def wrap_text(text, width=60):
    return "\n".join(textwrap.wrap(text, width))

data = {
    "Principles": [
        "Existence and representation",
        "Ownership and Control",
        "Access and Availability",
        "Transparency",
        "Persistence",
        "Portability",
        "Interoperability",
        "Consent",
        "Security and Protection",
        "Privacy and Minimal Disclosure",
        "Standard",
        "Cost",
        "Usability and Consistency",
        "Decentralization and Autonomy",
        "Verifiability and Authenticity"
    ],
    "Keywords (occurrences)": [
        "existence (4), independent (2), representation (2), form (2), ecosystem (1), legal (1), natural (1), physical (1), person (1), ensuring (1), independence (1), aspects (1), kernel (1), supported (1), accessible (1), create (1), intervention (1), third (1), party (1), characteristics (1), assert (1), quasi-representation (1)",
        
        "control (10), owners (4), claims (4), ultimate (2), authority (2), access (2), subject (2), personal (2), confidential (2), usage (2), sharing (2), Digital wallet (1)",

        "access (8), claims (2), solution (2), assertions (1), services (1), discrimination (1), ethnicity (1), gender (1), socio-economic (1), status (1), language (1), ecosystem (1), usability (1), accessibility (1), agents (1), components (1), rights (1), holders (1), consistency (1), retrieve (1), experience (1), systems (1), employees (1), location (1), device (1), tasks (1), places (1), attributes (1)",

        "systems (6), algorithms (6), open-source (4), transparent (4), independent (3), architecture (3), ecosystem (2), protocols (2), free (2), operate (2), managed (2), administered (2), network (2), stakeholders (1), verification (1), validation (1), licensing (1), incentives (1), components (1), governance (1)",
        
        "long-lived (3), owner (3), claims (2), persistent (2), modified (2)",

        "transportable (5), platform (3), services (3), control (3), transferable (2), ecosystem (2), systems (2), agents (2), persistence (2)",
        
        "interoperably (6), global (4), systems (4), solutions (3), providers (3), international (3), transport (2), layer (2), control (2), boundaries (2), protocols (2), ecosystem (2), compatible (2), enterprises (2), government (2), organisations (2), employed (2), securely (2), interact (2), exchanged (2), secured (2), protected (2), verified (2), standards (2), available (2), losing (2)",

        "disclosure (9), minimum (7), privacy (6), minimized (4), selective (3), correlation (3), claims (3), individuals (2), anonymity (2), pseudonymity (1), biometric (1), confidentiality (1), integrity (1), authenticity (1), nonrepudiation (1), robustness (1), transparency (1), empower (1), attributes (1), granularity (1), refusal (1), mechanism (1), underlying (1)",
        
        "rights (5), secure (3), protected (3), network (3), censorship-resistant (2), decentralized (2), encryption (2), cryptographic (1), confidentiality (1), integrity (1), authenticity (1), non-repudiation (1), transmitted (1), channel (1), ecosystem (1), empower (1), holders (1), motion (1), control (1), identifiers (1), keys (1), employ (1), end-to-end (1), interactions (1), prioritizing (1), systems (1), promote (1), freedom (1), environments (1), protocol (1), conflict (1), preserving (1), freedoms (1), authentication (1), independent (1), algorithms (1), force-resilient (1)",
        
        "disclosure (9), minimum (7), privacy (6), minimized (4), selective (3), correlation (3), claims (3), anonymity (2), pseudonymity (1), biometric (1), confidentiality (1), integrity (1), authenticity (1), nonrepudiation (1), robustness (1), transparency (1), ecosystem (1), empower (1), attributes (1), granularity (1), refusal (1), mechanism (1), underlying (1), correlation-independent (1), verification (1)",
        
        "open (3), standards (3), portability (2), interoperability (2), adoption (1), sustainability (1), persistence (1), entities (1), represented (1), exchanged (1), secured (1), protected (1), verified (1), public (1), royalty-free (1)",
        
        "cost (6), adoption (4), create (2), management (2), minimize (2), resources (2)",
        
        "user experience (5), recover (4), owners (3), credentials (3), usability (3), consistent (3), control (2), agents (2), ecosystem (1), expectations (2), complexity (1), interfaces (1), effectively (1), algorithms (1), holders (1), mobile/device (1), collaborating parties (1), resilient (1), technology platforms (1), birth certificates (1), mobile (1), intuitive (1), platforms (1), components (1), lost key (1)",
        
        "autonomy (3), party/parties (5), relying (2), entity (2), independent (1), administration (1), management (1), compliance (1), centralized (1), control (1), verify (1), represent (1)",
        
        "verifiable (3), owners (3), proof (2), credentials (2), verifiability (2), controlled (2), relying parties (2), authenticity (1), spoofing (1), preventing (1), ecosystem (1), objective (1), credential (1), cryptographically (1), secured (1), verification (1), empower (1), truthfully (1), evidence (1)"
    ],
    "Question": [
        "To what extent should users be able to have multiple identities?",
        
        "To what extent users must be the ultimate authority on their identity?",

        "To what extent should users have unrestricted access to and be able to retrieve their identity information from different locations?",

        "To what extent do you trust systems and algorithms to manage a network of identities?",
        
        "Should identities persist as long as users wish?",

        "Should an identity be transportable from one platform to another platform?",
        
        "To what extent should identities enable data exchange across providers without relying on a third-party entity?",

        "How often must a user consent to grant or deny access to their data to relying parties?",
        
        "Do you consider presenting digital identity certificates to be more secure than paper-based documents?",
        
        "Do you use techniques to minimize the disclosure of personal data and support pseudonymity to prevent correlation?",
        
        "Do open standards enable entities to be portable, interoperable, and persistent?",
        
        "To what extent decentralized identity help to minimize costs by easing the management of resources while reducing IT help desk reliance?",
        
        "How comfortable do you feel in using mobile wallets for managing identities?",
        
        "Do you agree that an identity system must fully support the autonomy of identity information?",
        
        "Do you agree that digital identities are controlled by the owner and that relying parties should receive objective evidence about the truthfulness of their owners?"
    ],
    "Rationale": [
        "Users should have the right to exist digitally without external validation.",
        "Users must retain control over their personal identity data to prevent misuse.",
        "Ensuring fair access to identity services is crucial for inclusion and rights.",
        "Transparency in identity systems helps build trust and accountability.",
        "Digital identities should not be arbitrarily revoked or altered by third parties.",
        "Users should be able to move their identities across platforms without restrictions.",
        "Interoperability allows different identity systems to function seamlessly.",
        "Users should have full awareness and choice in granting access to their identity data.",
        "Security measures must be in place to prevent unauthorized identity access.",
        "Privacy principles must ensure minimal exposure of personal information.",
        "Standards enable consistency, usability, and long-term sustainability.",
        "Identity systems should minimize costs for users and organizations.",
        "Usability ensures that digital identity solutions are accessible to all users.",
        "Decentralization prevents single points of failure and promotes autonomy.",
        "Verifiability ensures that identities remain trustworthy and authentic."
    ]
}

data["Keywords (occurrences)"] = [wrap_text(text, width=60) for text in data["Keywords (occurrences)"]]
data["Question"] = [wrap_text(text, width=80) for text in data["Question"]]
data["Rationale"] = [wrap_text(text, width=80) for text in data["Rationale"]]

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(16, 16))  
ax.axis("tight")
ax.axis("off")

table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="left", loc="center")

table.auto_set_font_size(False)
table.set_fontsize(8)
table.auto_set_column_width([0, 1, 2, 3])

for i in range(len(df) + 1):  
    for j in range(len(df.columns)):
        cell = table[i, j]
        if i == 0:
            cell.set_facecolor("#cccccc")  
            cell.set_text_props(weight="bold")
        elif i % 2 == 0:  # Alternating row colors
            cell.set_facecolor("#e6e6e6")  
        else:
            cell.set_facecolor("#f9f9f9")  

for i in range(1, len(df) + 1):  
    max_lines = max(
        df.iloc[i-1, :].apply(lambda x: len(str(x).split("\n")))
    )
    row_height = max(0.07, 0.025 * max_lines)  # Adjust row height dynamically
    for j in range(len(df.columns)):
        table[i, j].set_height(row_height)

plt.show()
