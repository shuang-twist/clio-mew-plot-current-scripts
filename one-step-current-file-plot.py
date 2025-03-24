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

# Function to plot the data
def plot_data(data):
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
        plt.title('Current vs. Time')
        plt.legend()
        plt.show()

# Function to select and plot the CSV file
def select_and_plot_csv():
    # Open file dialog to select a CSV file
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter window
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    
    if file_path:
        data = read_csv_file(file_path)
        plot_data(data)

# Main function
def main():
    select_and_plot_csv()

if __name__ == "__main__":
    main()
