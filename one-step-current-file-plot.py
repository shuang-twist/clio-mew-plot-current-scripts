import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
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
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=0.3)  # Adjust space for radio buttons

        # Scatter plots for Cathode and Anode currents
        ax.scatter(data['RelativeMilliseconds'], data['CathodeCurrent(uA)'], label='Cathode Current', s=5)
        ax.scatter(data['RelativeMilliseconds'], data['AnodeCurrent(uA)'], label='Anode Current', s=5)

        # Calculate statistics
        cathode_non_zero = data[data['CathodeCurrent(uA)'] != 0]['CathodeCurrent(uA)']
        anode_non_zero = data[data['AnodeCurrent(uA)'] != 0]['AnodeCurrent(uA)']

        # Add initial horizontal lines for median (default)
        cathode_line = ax.axhline(cathode_non_zero.median(), color='blue', linestyle='--', label=f'Cathode Median: {cathode_non_zero.median():.2f}')
        anode_line = ax.axhline(anode_non_zero.median(), color='orange', linestyle='--', label=f'Anode Median: {anode_non_zero.median():.2f}')

        # Configure the plot
        ax.set_xlabel('Relative Milliseconds')
        ax.set_ylabel('Current (uA)')
        ax.set_title('Current vs. Time')
        ax.legend()

        # Add radio buttons for user to choose
        ax_radio = plt.axes([0.05, 0.4, 0.2, 0.15])  # Position for radio buttons [left, bottom, width, height]
        radio_buttons = RadioButtons(ax_radio, ('Median', 'Mean'))

        def update_lines(label):
            """Update only the horizontal lines based on selected statistic."""
            if label == 'Median':
                # Wrap scalar values in lists to create sequences
                cathode_line.set_ydata([cathode_non_zero.median()])
                cathode_line.set_label(f'Cathode Median: {cathode_non_zero.median():.2f}')
                anode_line.set_ydata([anode_non_zero.median()])
                anode_line.set_label(f'Anode Median: {anode_non_zero.median():.2f}')
            elif label == 'Mean':
                cathode_line.set_ydata([cathode_non_zero.mean()])
                cathode_line.set_label(f'Cathode Mean: {cathode_non_zero.mean():.2f}')
                anode_line.set_ydata([anode_non_zero.mean()])
                anode_line.set_label(f'Anode Mean: {anode_non_zero.mean():.2f}')

            ax.legend()
            plt.draw()

        radio_buttons.on_clicked(update_lines)  # Connect radio buttons to update function

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
