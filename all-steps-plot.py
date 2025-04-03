import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from matplotlib.widgets import RadioButtons

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
        # Dictionary to store data for combined plotting
        data_dict = {}

        integer_folder_names = []
        for folder_name in os.listdir(folder_path):
            folder_path_full = os.path.join(folder_path, folder_name)
            if os.path.isdir(folder_path_full):
                try:
                    folder_number = int(folder_name)  # Check if folder name is an integer
                    integer_folder_names.append(folder_number)
                except ValueError:
                    continue  # Skip if not an integer
                
                for file_name in os.listdir(folder_path_full):
                    if "_Current_" in file_name and file_name.endswith(".csv"):
                        file_path_full = os.path.join(folder_path_full, file_name)
                        data = read_csv_file(file_path_full)
                        if data is not None:
                            data_dict[folder_number] = data  # Use integer as key
                        break  # Process the first matching CSV file in the folder

        # Sort the folder names numerically (small to large)
        integer_folder_names.sort()

        print(integer_folder_names)

        # Dynamically calculate height for radio button area based on number of items
        base_height = 0.15  # Base height for up to 5 items
        threshold = 5       # Number of items before increasing height
        additional_height_per_item = 0.03  # Additional height per item beyond threshold

        if len(integer_folder_names) > threshold:
            total_height = base_height + (len(integer_folder_names) - threshold) * additional_height_per_item
        else:
            total_height = base_height

        # Ensure total height does not exceed figure limits (e.g., max 0.8)
        total_height = min(total_height, 0.8)

        # Create a figure and axes for radio buttons and plot
        fig = plt.figure(figsize=(10, 6))
        
        # Define axes for radio buttons with dynamic height
        ax_radio_stat = plt.axes([0.05, 0.4, 0.2, total_height])
        radio_stat = RadioButtons(ax_radio_stat, [str(num) for num in integer_folder_names])  # Convert integers to strings for labels

        # Define axes for plotting (right side of the figure)
        ax_plot = plt.axes([0.3, 0.1, 0.6, 0.8])

        def update_fig(label):
            # Clear only the plot area (ax_plot)
            ax_plot.clear()
            
            # Get data for selected folder (convert label back to integer)
            folder_number = int(label)
            if folder_number in data_dict:
                # Extract data
                data = data_dict[folder_number]
                
                # Plot Cathode Current
                ax_plot.scatter(data['RelativeMilliseconds'], 
                                data['CathodeCurrent(uA)'], 
                                label=f'{folder_number} - Cathode', 
                                s=5, color='blue')
                
                # Plot Anode Current
                ax_plot.scatter(data['RelativeMilliseconds'], 
                                data['AnodeCurrent(uA)'], 
                                label=f'{folder_number} - Anode', 
                                s=5, color='orange')

                ax_plot.set_xlabel('Relative Milliseconds')
                ax_plot.set_ylabel('Current (uA)')
                ax_plot.set_title(f'Currents for Folder {folder_number}')
                ax_plot.legend()
                
                # Redraw only the updated plot area
                fig.canvas.draw_idle()
            else:
                print(f"No data found for Folder {folder_number}")

        # Connect radio button clicks to update_fig function
        radio_stat.on_clicked(update_fig)

        plt.show()  # Show the plot window

# Main function
def main():
    select_and_plot_csv()

if __name__ == "__main__":
    main()
