import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

# Function to read a CSV file
def read_csv_file(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return None

# Function to process and plot only median values
def plot_median_csvs_side_by_side(data_dict):
    folder_numbers = sorted(data_dict.keys())
    n = len(folder_numbers)
    if n == 0:
        print("No valid CSV files to plot.")
        return

    fig, axs = plt.subplots(1, n, figsize=(5 * n, 6), sharey=True)
    if n == 1:
        axs = [axs]  # Make iterable for consistency

    for ax, folder_num in zip(axs, folder_numbers):
        data = data_dict[folder_num]

        # Group by RelativeMilliseconds and compute medians
        grouped = data.groupby('RelativeMilliseconds', as_index=False).agg({
            'CathodeCurrent(uA)': 'median',
            'AnodeCurrent(uA)': 'median'
        })

        # Plot median data points
        ax.scatter(grouped['RelativeMilliseconds'], grouped['CathodeCurrent(uA)'],
                   s=20, color='blue', alpha=0.7, label='Cathode Median')
        ax.scatter(grouped['RelativeMilliseconds'], grouped['AnodeCurrent(uA)'],
                   s=20, color='orange', alpha=0.7, label='Anode Median')

        # Horizontal median lines (of non-zero raw data)
        cathode_non_zero = data[data['CathodeCurrent(uA)'] != 0]['CathodeCurrent(uA)']
        anode_non_zero = data[data['AnodeCurrent(uA)'] != 0]['AnodeCurrent(uA)']
        cathode_med = cathode_non_zero.median()
        anode_med = anode_non_zero.median()

        ax.axhline(cathode_med, color='blue', linestyle='--',
                   label=f'Cathode Med: {cathode_med:.2f}')
        ax.axhline(anode_med, color='orange', linestyle='--',
                   label=f'Anode Med: {anode_med:.2f}')

        ax.set_title(f'Folder {folder_num}')
        ax.set_xlabel('Relative Milliseconds')
        ax.legend()

    axs[0].set_ylabel('Current (uA)')
    fig.suptitle('Median Current vs Time per Folder', fontsize=16)
    plt.tight_layout()
    plt.show()

# Main flow: select folder, read "_Current_" CSVs, and plot
def select_and_plot_all_subfolder_medians():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")

    if folder_path:
        data_dict = {}
        for folder_name in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, folder_name)
            if os.path.isdir(subfolder_path):
                try:
                    folder_number = int(folder_name)
                except ValueError:
                    continue  # Skip non-integer folders

                # Look for the first "_Current_" CSV in the subfolder
                for file_name in os.listdir(subfolder_path):
                    if "_Current_" in file_name and file_name.endswith(".csv"):
                        full_path = os.path.join(subfolder_path, file_name)
                        data = read_csv_file(full_path)
                        if data is not None:
                            data_dict[folder_number] = data
                        break  # Only process first matching CSV
        plot_median_csvs_side_by_side(data_dict)

# Entry point
if __name__ == "__main__":
    select_and_plot_all_subfolder_medians()
