import os
import matplotlib.pyplot as plt
import numpy as np

def main(folder_path):
    total_img_count = 0
    folder_count = 0
    img_counts = []

    for root, dirs, files in os.walk(folder_path):
        if len(files) > 2:
            if "Frontal" in root:
                continue
            img_count = len([file for file in files if file.endswith(".jpg")])
            folder_count += 1
            total_img_count += img_count
            img_counts.append(img_count)

    ratio = total_img_count / folder_count
    print(f"Total folder count: {folder_count}")
    print(f"Total img count: {total_img_count}")
    print(f"Ratio: {ratio}")

    print(f"Min: {min(img_counts)}, Path of min: {os.path.join(folder_path, str(min(img_counts)))}")
    print(f"Max: {max(img_counts)}, Path of max: {os.path.join(folder_path, str(max(img_counts)))}")

    # Determine the number of bins dynamically using Freedman-Diaconis rule
    bin_width = 2 * (np.percentile(img_counts, 75) - np.percentile(img_counts, 25)) / (len(img_counts) ** (1/3))
    num_bins = int((max(img_counts) - min(img_counts)) / bin_width)

    # Plotting histogram
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(img_counts, bins=num_bins, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Distribution of Image Counts')
    plt.xlabel('Number of Images')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Customizing x-axis limits to exclude outliers
    plt.xlim(0, np.percentile(img_counts, 95)*1.5)  # Adjust the percentile as needed

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main(folder_path="UMUT/database/HELEN_FOLDERED_without_errors")
