# Given data
principi = [
    "Portability", "Persistence", "Cost", 
    "Access and availability", "Usability and consistency", "Security and protection",
    "Consent", "Transparency", "Verifiability and Authenticity",
    "Decentralization and Autonomy", "Standard", "Interoperability",
    "Ownership and control", "Existence and representation", "Privacy and minimal disclosure"
]

avg_values = [4.92, 4.70, 4.55, 4.18, 4.07, 4.07, 4.00, 3.77, 3.74, 3.18, 2.96, 2.74, 2.70, 2.63, 1.04]

sd_values = [0.38, 1.05, 1.88, 1.91, 1.47, 1.35, 1.53, 1.59, 1.27, 0.91, 1.13, 1.54, 0.76, 1.38, 0.19]

avg_values = [4.92, 4.70, 4.55, 4.18, 4.07, 4.07, 4.00, 3.77, 3.74, 3.18, 2.96, 2.74, 2.70, 2.63, 1.04]
sd_values = [0.38, 1.05, 1.88, 1.91, 1.47, 1.35, 1.53, 1.59, 1.27, 0.91, 1.13, 1.54, 0.76, 1.38, 0.19]

# Compute S values
s_values = [avg - sd for avg, sd in zip(avg_values, sd_values)]

# Min-Max Normalization
s_min = min(s_values)
s_max = max(s_values)
s_values_normalized = [(s - s_min) / (s_max - s_min) for s in s_values]

# Combine results into a list of tuples
s_results = list(zip(principi, s_values, s_values_normalized))

# Sort results by normalized S value in descending order
s_results_sorted = sorted(s_results, key=lambda x: x[2], reverse=True)

# Print the sorted results
for principle, s_value, s_norm in s_results_sorted:
    print(f"{principle}: S = {s_value:.2f}, Normalized S = {s_norm:.2f}")
