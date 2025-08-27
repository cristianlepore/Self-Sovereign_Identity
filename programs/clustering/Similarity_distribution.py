import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_similarity(matrix, algorithms):
    matrix = np.array(matrix)
    
    mean_similarity = np.mean(matrix)
    
    variance = np.var(matrix)
    std_dev = np.std(matrix)
    
    tsne_index = algorithms.index("t-SNE")
    mean_tsne_similarity = np.mean(matrix[tsne_index, :])
    
    np.fill_diagonal(matrix, -np.inf)  # Ignoriamo la diagonale (autocorrelazione)
    most_similar_indices = np.unravel_index(np.argmax(matrix), matrix.shape)
    least_similar_indices = np.unravel_index(np.argmin(matrix), matrix.shape)
    most_similar = (algorithms[most_similar_indices[0]], algorithms[most_similar_indices[1]])
    least_similar = (algorithms[least_similar_indices[0]], algorithms[least_similar_indices[1]])
    
    avg_similarities = np.mean(matrix, axis=1)
    independent_algorithm = algorithms[np.argmin(avg_similarities)]
    
    flattened_values = matrix[matrix != -np.inf].flatten()  # Escludiamo la diagonale
    plt.figure(figsize=(8, 6))
    sns.histplot(flattened_values, bins=10, kde=True)
    plt.xlabel("Similarity")
    plt.ylabel("Frequency")
    plt.title("")
    plt.show()
    
    return {
        "Media delle Similarità": mean_similarity,
        "Varianza": variance,
        "Deviazione Standard": std_dev,
        "Similarità Media con t-SNE": mean_tsne_similarity,
        "Algoritmi Più Simili": most_similar,
        "Algoritmi Meno Simili": least_similar,
        "Cluster Indipendente": independent_algorithm
    }

# Esempio di utilizzo:
similarity_matrix = [
    [1, 0.57, 0.36, 0.35, 0.37, 0.34, 0.45],
    [0.57, 1, 0.47, 0.32, 0.36, 0.40, 0.43],
    [0.36, 0.47, 1, 0.17, 0.15, 0.22, 0.23],
    [0.35, 0.32, 0.17, 1, 0.74, 0.79, 0.88],
    [0.37, 0.36, 0.15, 0.74, 1, 0.90, 0.70],
    [0.34, 0.40, 0.22, 0.79, 0.90, 1, 0.73],
    [0.45, 0.43, 0.23, 0.88, 0.70, 0.73, 1]
]

algorithms = ["Greedy 25th", "Greedy 50th", "Greedy 75th", "KMNS", "Louvain", "Greedy + Entropy", "t-SNE"]

results = analyze_similarity(similarity_matrix, algorithms)
print(results)
