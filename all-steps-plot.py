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

# Function to plot the data and save it as an image
def plot_data_and_save(data, title, folder_path):
    if data is not None:
        plt.figure(figsize=(10,6))
        
        # Plot CathodeCurrent(uA) against RelativeMilliseconds with smaller dots
        plt.scatter(data['RelativeMilliseconds'], data['CathodeCurrent(uA)'], label='Cathode Current', s=5)

        # Plot AnodeCurrent(uA) against RelativeMilliseconds with smaller dots
        plt.scatter(data['RelativeMilliseconds'], data['AnodeCurrent(uA)'], label='Anode Current', s=5)
        
        # Calculate and display medians
        cathode_median = data['CathodeCurrent(uA)'].median()
        anode_median = data['AnodeCurrent(uA)'].median()
        plt.axhline(y=cathode_median, color='blue', linestyle='--', label=f'Cathode Median: {cathode_median:.2f}')
        plt.axhline(y=anode_median, color='orange', linestyle='--', label=f'Anode Median: {anode_median:.2f}')

        plt.xlabel('Relative Milliseconds')
        plt.ylabel('Current (uA)')
        plt.title(title)
        plt.legend()

        # Save the plot as an image in the specified folder
        plot_file_path = os.path.join(folder_path, f'{title}.png')
        plt.savefig(plot_file_path)
        plt.close()  # Close the plot to free up memory

# Function to select and plot CSV files from subfolders
def select_and_plot_csv():
    # Open file dialog to select a folder
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window
    folder_path = filedialog.askdirectory(title="Select Folder")
    
    if folder_path:
        # Create a folder to save plots
        plots_folder = os.path.join(folder_path, 'current_plots')
        os.makedirs(plots_folder, exist_ok=True)

        for folder_name in os.listdir(folder_path):
            folder_path_full = os.path.join(folder_path, folder_name)
            if os.path.isdir(folder_path_full):
                try:
                    int(folder_name)  # Check if folder name is an integer
                except ValueError:
                    continue  # Skip if not an integer
                
                csv_found = False
                for file_name in os.listdir(folder_path_full):
                    if "_Current_" in file_name and file_name.endswith(".csv"):
                        file_path_full = os.path.join(folder_path_full, file_name)
                        data = read_csv_file(file_path_full)
                        plot_data_and_save(data, f"Folder_{folder_name}", plots_folder)
                        csv_found = True
                        break  # Plot the first matching file and move to the next folder
                
                if not csv_found:
                    print(f"No CSV file found in folder {folder_name}")

# Main function
def main():
    select_and_plot_csv()

if __name__ == "__main__":
    main()
