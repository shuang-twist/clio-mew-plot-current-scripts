import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

# Function to read the CSV file
def read_csv_file(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return None

# Function to plot grouped medians for CSVs side by side with shared y-axis
def plot_csvs_side_by_side(data_dict):
    folder_numbers = sorted(data_dict.keys())
    n = len(folder_numbers)
    if n == 0:
        print("No valid CSV files to plot.")
        return

    fig, axs = plt.subplots(1, n, figsize=(5 * n, 6), sharey=True)
    if n == 1:
        axs = [axs]  # Make it iterable

    for ax, folder_num in zip(axs, folder_numbers):
        data = data_dict[folder_num]

        # Group by 'Group' and calculate median
        grouped = data.groupby('Group', as_index=False).agg({
            'CathodeCurrent(uA)': 'median',
            'AnodeCurrent(uA)': 'median'
        })

        # Scatter plots for grouped medians
        ax.scatter(grouped['Group'], grouped['CathodeCurrent(uA)'], s=20, label='Cathode Median', color='blue')
        ax.scatter(grouped['Group'], grouped['AnodeCurrent(uA)'], s=20, label='Anode Median', color='orange')

        ax.set_title(f'{folder_num}')
        ax.set_xlabel('Group')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

    axs[0].set_ylabel('Current (uA)')
    fig.suptitle('Median Current per Group for Each Folder', fontsize=16)
    plt.tight_layout()
    plt.show()

# Function to select folder and extract data
def select_and_plot_all_subfolder_csvs():
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
                    continue  # Skip non-integer folder names

                # Look for the first matching "_Current_" CSV
                for file_name in os.listdir(subfolder_path):
                    if "_Current_" in file_name and file_name.endswith(".csv"):
                        file_path_full = os.path.join(subfolder_path, file_name)
                        data = read_csv_file(file_path_full)
                        if data is not None:
                            data_dict[folder_number] = data
                        break  # Only the first matching CSV
        plot_csvs_side_by_side(data_dict)

# Main function
if __name__ == "__main__":
    select_and_plot_all_subfolder_csvs()
