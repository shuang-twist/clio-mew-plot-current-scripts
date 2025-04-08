import pandas as pd
import matplotlib.pyplot as plt
import os
from tkinter import filedialog, Tk

# Function to read CSV files from a folder
def read_csvs_from_folder(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]
    all_data = []
    for f in sorted(csv_files):
        try:
            df = pd.read_csv(os.path.join(folder_path, f))
            df['__source__'] = f  # Keep track of file source
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {f}: {e}")
    return all_data

# Function to plot all CSVs side by side
def plot_multiple_csvs(data_list):
    n_files = len(data_list)
    if n_files == 0:
        print("No CSV data to plot.")
        return

    fig, axs = plt.subplots(1, n_files, figsize=(6 * n_files, 6), sharey=True)
    if n_files == 1:
        axs = [axs]  # Ensure axs is iterable

    for ax, data in zip(axs, data_list):
        filename = data['__source__'].iloc[0]

        # Scatter plots
        ax.scatter(data['RelativeMilliseconds'], data['CathodeCurrent(uA)'], label='Cathode', s=5)
        ax.scatter(data['RelativeMilliseconds'], data['AnodeCurrent(uA)'], label='Anode', s=5)

        # Non-zero stats
        cathode_non_zero = data[data['CathodeCurrent(uA)'] != 0]['CathodeCurrent(uA)']
        anode_non_zero = data[data['AnodeCurrent(uA)'] != 0]['AnodeCurrent(uA)']

        # Reference lines
        ax.axhline(cathode_non_zero.median(), color='blue', linestyle='--',
                   label=f'Cathode Median: {cathode_non_zero.median():.2f}')
        ax.axhline(anode_non_zero.median(), color='orange', linestyle='--',
                   label=f'Anode Median: {anode_non_zero.median():.2f}')

        ax.set_title(filename)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Current (uA)')
        ax.legend()

    fig.suptitle('Current vs. Time Across CSV Files', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# Main function to select folder and plot
def select_folder_and_plot():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder with CSV Files")

    if folder_selected:
        data_list = read_csvs_from_folder(folder_selected)
        plot_multiple_csvs(data_list)

# Entry point
if __name__ == "__main__":
    select_folder_and_plot()
