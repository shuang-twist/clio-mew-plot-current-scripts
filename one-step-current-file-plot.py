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
def plot_data(data, option='Median'):
    if data is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=0.3)  # Adjust space for radio buttons
        
        # Scatter plots for Cathode and Anode currents
        ax.scatter(data['RelativeMilliseconds'], data['CathodeCurrent(uA)'], label='Cathode Current', s=5)
        ax.scatter(data['RelativeMilliseconds'], data['AnodeCurrent(uA)'], label='Anode Current', s=5)

        # Calculate statistics
        cathode_non_zero = data[data['CathodeCurrent(uA)'] != 0]['CathodeCurrent(uA)']
        anode_non_zero = data[data['AnodeCurrent(uA)'] != 0]['AnodeCurrent(uA)']

        # Add horizontal lines for mean or median based on option
        if option == 'Median':
            ax.axhline(cathode_non_zero.median(), color='blue', linestyle='--', label=f'Cathode Median: {cathode_non_zero.median():.2f}')
            ax.axhline(anode_non_zero.median(), color='orange', linestyle='--', label=f'Anode Median: {anode_non_zero.median():.2f}')
        elif option == 'Mean':
            ax.axhline(cathode_non_zero.mean(), color='blue', linestyle='--', label=f'Cathode Mean: {cathode_non_zero.mean():.2f}')
            ax.axhline(anode_non_zero.mean(), color='orange', linestyle='--', label=f'Anode Mean: {anode_non_zero.mean():.2f}')

        # Configure the plot
        ax.set_xlabel('Relative Milliseconds')
        ax.set_ylabel('Current (uA)')
        ax.set_title('Current vs. Time')
        ax.legend()

        # Add radio buttons for interactivity
        ax_radio = plt.axes([0.05, 0.4, 0.2, 0.15])  # Position for radio buttons [left, bottom, width, height]
        radio_buttons = RadioButtons(ax_radio, ('Non-zero Median', 'Non-zero Mean'))

        def update_plot(label):
            """Update the plot based on selected statistic."""
            ax.clear()  # Clear the current axes
            
            # Re-plot scatter points
            ax.scatter(data['RelativeMilliseconds'], data['CathodeCurrent(uA)'], label='Cathode Current', s=5)
            ax.scatter(data['RelativeMilliseconds'], data['AnodeCurrent(uA)'], label='Anode Current', s=5)

            # Add updated horizontal lines
            if label == 'Non-zero Median':
                ax.axhline(cathode_non_zero.median(), color='blue', linestyle='--', label=f'Cathode Median: {cathode_non_zero.median():.2f}')
                ax.axhline(anode_non_zero.median(), color='orange', linestyle='--', label=f'Anode Median: {anode_non_zero.median():.2f}')
            elif label == 'Non-zero Mean':
                ax.axhline(cathode_non_zero.mean(), color='blue', linestyle='--', label=f'Cathode Mean: {cathode_non_zero.mean():.2f}')
                ax.axhline(anode_non_zero.mean(), color='orange', linestyle='--', label=f'Anode Mean: {anode_non_zero.mean():.2f}')

            # Update labels and legend
            ax.set_xlabel('Relative Milliseconds')
            ax.set_ylabel('Current (uA)')
            ax.set_title('Current vs. Time')
            ax.legend()
            
            plt.draw()  # Redraw the figure

        radio_buttons.on_clicked(update_plot)  # Connect radio buttons to update function

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
