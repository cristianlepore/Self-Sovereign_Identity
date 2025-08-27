import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import os

# Main function
def kmeans_clustering(file_path, n_clusters):
    """
    Applies the K-Means algorithm to a CSV dataset.

    :param file_path: Path to the CSV file.
    :param n_clusters: Number of clusters (k).
    """
    # Read and load data
    data = pd.read_csv(file_path)
    
    # Select numerical columns
    numerical_columns = data.select_dtypes(include=[np.number]).dropna(axis=1, how='all')
    
    # Fill NaN values with 0 (if necessary)
    cleaned_data = numerical_columns.fillna(0)
    
    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
    clusters = kmeans.fit_predict(cleaned_data)
    
    # Add cluster results to the original dataset
    data['Clustering'] = clusters
    
    # Save the dataset with clusters in a new file
    output_file = "Output.csv"
    data.to_csv(output_file, index=False)
    print(f"Clustering completed! Results saved in: {output_file}")
    print(data[['Clustering']].value_counts().sort_index())

# Run the program
if __name__ == "__main__":
    # Path to the Downloads folder
    # Set the correct path for your configuration
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads/SSI_principles/definition/program/clustering/kmeans/")
    file_path = os.path.join(download_folder, "Input.csv")
    
    # Number of clusters (k)
    n_clusters = 5
    
    # Execute the function
    kmeans_clustering(file_path, n_clusters)
