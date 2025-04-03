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

        # Dictionary to store data for combined plotting
        data_dict = {}

        for folder_name in os.listdir(folder_path):
            folder_path_full = os.path.join(folder_path, folder_name)
            if os.path.isdir(folder_path_full):
                try:
                    int(folder_name)  # Check if folder name is an integer
                except ValueError:
                    continue  # Skip if not an integer
                
                for file_name in os.listdir(folder_path_full):
                    if "_Current_" in file_name and file_name.endswith(".csv"):
                        file_path_full = os.path.join(folder_path_full, file_name)
                        data = read_csv_file(file_path_full)
                        if data is not None:
                            data_dict[f"Folder_{folder_name}"] = data
                        break  # Process the first matching CSV file in the folder

        # Plot all data on one figure
        if data_dict:
            plt.figure(figsize=(12, 8))
            
            for label, data in data_dict.items():
                # Plot CathodeCurrent(uA) against RelativeMilliseconds with smaller dots
                plt.scatter(data['RelativeMilliseconds'], 
                            data['CathodeCurrent(uA)'], 
                            label=f'{label} - Cathode', s=5)
                
                # Plot AnodeCurrent(uA) against RelativeMilliseconds with smaller dots
                plt.scatter(data['RelativeMilliseconds'], 
                            data['AnodeCurrent(uA)'], 
                            label=f'{label} - Anode', s=5)

            plt.xlabel('Relative Milliseconds')
            plt.ylabel('Current (uA)')
            plt.title('Combined Plot of Cathode and Anode Currents')
            plt.legend()
            
            # Save and show the combined plot
            combined_plot_path = os.path.join(plots_folder, "combined_plot.png")
            plt.savefig(combined_plot_path)
            plt.show()
        else:
            print("No valid CSV files found.")

# Main function
def main():
    select_and_plot_csv()

if __name__ == "__main__":
    main()
