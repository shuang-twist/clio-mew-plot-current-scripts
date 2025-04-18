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

# Function to plot CSVs and return median data
def plot_csvs_side_by_side(data_dict, output_path):
    folder_numbers = sorted(data_dict.keys())
    n = len(folder_numbers)
    if n == 0:
        print("No valid CSV files to plot.")
        return

    median_records = []

    fig, axs = plt.subplots(1, n, figsize=(5 * n, 6), sharey=True)
    if n == 1:
        axs = [axs]  # Make it iterable

    for ax, folder_num in zip(axs, folder_numbers):
        data = data_dict[folder_num]
        cathode = data['CathodeCurrent(uA)']
        anode = data['AnodeCurrent(uA)']

        ax.scatter(data['RelativeMilliseconds'], cathode, s=5, label='Cathode')
        ax.scatter(data['RelativeMilliseconds'], anode, s=5, label='Anode')

        # Horizontal lines
        cathode_med = cathode[cathode != 0].median()
        anode_med = anode[anode != 0].median()
        ax.axhline(cathode_med, color='blue', linestyle='--', label=f'{cathode_med:.2f}')
        ax.axhline(anode_med, color='orange', linestyle='--', label=f'{anode_med:.2f}')

        # Save medians
        median_records.append({
            'Folder': folder_num,
            'CathodeMedian(uA)': cathode_med,
            'AnodeMedian(uA)': anode_med
        })

        ax.set_title(f'{folder_num}')
        ax.set_xlabel('ms')
        ax.legend()

    # Save the medians to a CSV
    median_df = pd.DataFrame(median_records)
    output_file = os.path.join(output_path, "Calculated_medians_from_the_plot.csv")
    median_df.to_csv(output_file, index=False)
    print(f"Medians saved to: {output_file}")
    
    axs[0].set_ylabel('Current (uA)')
    fig.suptitle('Current vs Time for Each Folder with Calculated Median', fontsize=16)
    plt.tight_layout()
    plt.show()

    # Save the medians to a CSV
    median_df = pd.DataFrame(median_records)
    output_file = os.path.join(output_path, "Calculated_medians_from_the_plot.csv")
    median_df.to_csv(output_file, index=False)
    print(f"Medians saved to: {output_file}")

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

                for file_name in os.listdir(subfolder_path):
                    if "_Current_" in file_name and file_name.endswith(".csv"):
                        file_path_full = os.path.join(subfolder_path, file_name)
                        data = read_csv_file(file_path_full)
                        if data is not None:
                            data_dict[folder_number] = data
                        break  # Only first matching CSV
        plot_csvs_side_by_side(data_dict, folder_path)

# Main function
if __name__ == "__main__":
    select_and_plot_all_subfolder_csvs()
