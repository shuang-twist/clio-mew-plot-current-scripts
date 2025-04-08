import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Function to read the CSV file
def read_csv_file(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return None

# Function to plot the data grouped by 'Group'
def plot_data(data):
    if data is not None:
        fig, ax = plt.subplots(figsize=(12, 7))

        # Group by 'Group' and calculate median
        grouped = data.groupby('Group', as_index=False).agg({
            'CathodeCurrent(uA)': 'median',
            'AnodeCurrent(uA)': 'median'
        })

        # Scatter plots for grouped medians
        ax.scatter(grouped['Group'], grouped['CathodeCurrent(uA)'], 
                   label='Cathode Median', s=40, color='blue')
        ax.scatter(grouped['Group'], grouped['AnodeCurrent(uA)'], 
                   label='Anode Median', s=40, color='orange')

        # Configure plot
        ax.set_xlabel('Group')
        ax.set_ylabel('Current (uA)')
        ax.set_title('Median Current vs. Group')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Function to select and plot the CSV file
def select_and_plot_csv():
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])

    if file_path:
        data = read_csv_file(file_path)
        plot_data(data)

# Main function
if __name__ == "__main__":
    select_and_plot_csv()
