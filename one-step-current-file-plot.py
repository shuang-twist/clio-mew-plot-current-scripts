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
        fig, ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(left=0.3)  # Adjust space for radio buttons

        # Store scatter plot objects
        cathode_all = ax.scatter(data['RelativeMilliseconds'], data['CathodeCurrent(uA)'], 
                                label='Cathode Current', s=5)
        anode_all = ax.scatter(data['RelativeMilliseconds'], data['AnodeCurrent(uA)'], 
                              label='Anode Current', s=5)

        # Group by RelativeMilliseconds and calculate medians
        grouped = data.groupby('RelativeMilliseconds', as_index=False).agg({
            'CathodeCurrent(uA)': 'median',
            'AnodeCurrent(uA)': 'median'
        })

        # Median scatter plots (initially hidden)
        cathode_median = ax.scatter(grouped['RelativeMilliseconds'], grouped['CathodeCurrent(uA)'], 
                                   s=40, color='blue', label='Cathode Median', alpha=0.7, visible=False)
        anode_median = ax.scatter(grouped['RelativeMilliseconds'], grouped['AnodeCurrent(uA)'], 
                                 s=40, color='orange', label='Anode Median', alpha=0.7, visible=False)

        # Calculate statistics
        cathode_non_zero = data[data['CathodeCurrent(uA)'] != 0]['CathodeCurrent(uA)']
        anode_non_zero = data[data['AnodeCurrent(uA)'] != 0]['AnodeCurrent(uA)']

        # Horizontal lines (always visible)
        cathode_line = ax.axhline(cathode_non_zero.median(), color='blue', linestyle='--', 
                                 label=f'Cathode Median: {cathode_non_zero.median():.2f}')
        anode_line = ax.axhline(anode_non_zero.median(), color='orange', linestyle='--', 
                               label=f'Anode Median: {anode_non_zero.median():.2f}')

        # Configure plot
        ax.set_xlabel('Relative Milliseconds')
        ax.set_ylabel('Current (uA)')
        ax.set_title('Current vs. Time')
        ax.legend()

        # Radio buttons for statistic selection
        ax_radio_stat = plt.axes([0.05, 0.4, 0.2, 0.15])
        radio_stat = RadioButtons(ax_radio_stat, ('Median', 'Mean'))
        
        # Radio buttons for plot type
        ax_radio_plot = plt.axes([0.05, 0.2, 0.2, 0.15])
        radio_plot = RadioButtons(ax_radio_plot, ('all points', 'median'))

        def update_plot_type(label):
            """Toggle between raw data and median points"""
            if label == 'all points':
                cathode_all.set_visible(True)
                anode_all.set_visible(True)
                cathode_median.set_visible(False)
                anode_median.set_visible(False)
            else:
                cathode_all.set_visible(False)
                anode_all.set_visible(False)
                cathode_median.set_visible(True)
                anode_median.set_visible(True)
            
            # Update legend with visible elements
            handles = [a for a in [cathode_all, anode_all, cathode_median, anode_median, cathode_line, anode_line] 
                      if a.get_visible()]
            ax.legend(handles=handles)
            plt.draw()

        def update_lines(label):
            """Update horizontal reference lines"""
            if label == 'Median':
                cathode_line.set_ydata([cathode_non_zero.median()])
                cathode_line.set_label(f'Cathode Median: {cathode_non_zero.median():.2f}')
                anode_line.set_ydata([anode_non_zero.median()])
                anode_line.set_label(f'Anode Median: {anode_non_zero.median():.2f}')
            else:
                cathode_line.set_ydata([cathode_non_zero.mean()])
                cathode_line.set_label(f'Cathode Mean: {cathode_non_zero.mean():.2f}')
                anode_line.set_ydata([anode_non_zero.mean()])
                anode_line.set_label(f'Anode Mean: {anode_non_zero.mean():.2f}')
            
            # Update legend with visible elements
            handles = [a for a in [cathode_all, anode_all, cathode_median, anode_median, cathode_line, anode_line] 
                      if a.get_visible()]
            ax.legend(handles=handles)
            plt.draw()

        # Connect both sets of radio buttons
        radio_stat.on_clicked(update_lines)
        radio_plot.on_clicked(update_plot_type)

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
