from collections import Counter
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from scipy.stats import chi2_contingency 
import statistics
import matplotlib.pyplot as plt
import numpy as np
filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.csv")])
df = pd.read_csv(filename)
def calculate_mode(data):
    frequency = Counter(data)
    max_frequency = max(frequency.values(), default=0)
    mode = [num for num, freq in frequency.items() if freq == max_frequency]
    return int(max(mode)) if max_frequency > 1 else None
def upload_file():
    column_names = df.columns.tolist()
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True)
    listbox.delete(0, tk.END)
    for name in column_names:
      listbox.insert(tk.END, name)
def median_smoothing(data, num_bins):
    bin_size = len(data) // num_bins

    mean_smoothed = []

    for i in range(0, len(data), bin_size):
        bin_data = data[i:i+bin_size]

        bin_median = sorted(bin_data)[len(bin_data) // 2]

        mean_smoothed.extend([bin_median] * len(bin_data))

    return mean_smoothed


def mean_smoothing(data, num_bins):
    bin_size = len(data) // num_bins

    smoothed_data = []

    for i in range(0, len(data), bin_size):
        current_bin = data[i:i+bin_size]

        bin_mean = sum(current_bin) / len(current_bin)

        smoothed_data.extend([bin_mean] * len(current_bin))

    return smoothed_data



def boundary_smoothing(data, num_bins):
    bin_size = len(data) // num_bins

    smoothed_data = []

    for i in range(0, len(data), bin_size):
        current_bin = data[i:i+bin_size]

        bin_min = min(current_bin)
        bin_max = max(current_bin)

        smoothed_data.extend([bin_min, bin_max])

    return smoothed_data


def min_max_normalization(data):
    minimum = min(data)
    maximum = max(data)
    range_val = maximum - minimum
    normalized_byMinMax = [(x - minimum) / range_val for x in data]
    return normalized_byMinMax

def z_score_normalization(data):
    mean = np.mean(data)
    sd = np.std(data)
    normalized_zScoure = (data - mean) / sd
    return normalized_zScoure

def normalization_by_decimal_scaling(data):
    maximum = max(data)
    magnitude = len(str(int(maximum))) - 1
    pow_ = 10 ** magnitude
    normalized_decScal = [x / pow_ for x in data]
    return normalized_decScal


def calculate():
    try:
        A=entry.get()
        df[A].fillna(0, inplace=True)
        numbers = df[A].to_list()
        results = ""

        if var1.get():
            mean = statistics.mean(numbers)
            results += f"Mean: {mean}\n"

        if var2.get():
            std_dev = statistics.stdev(numbers)
            results += f"Standard Deviation: {std_dev}\n"

        if var3.get():
            median = statistics.median(numbers)
            results += f"Median: {median}\n"

        if var4.get():
            variance = statistics.variance(numbers)
            results += f"Variance: {variance}\n"

        if var5.get():
            bin_size_entry = entry_bin_size.get()
            if bin_size_entry.isdigit():
                bin_size = int(bin_size_entry)
                mean_smoothed = mean_smoothing(numbers, bin_size)
                results += f"Mean Smoothed: {mean_smoothed}\n"
            else:
                raise ValueError("bin size for smoothing must be a number.")
            
        if var6.get():
            bin_size_entry = entry_bin_size.get()
            if bin_size_entry.isdigit():
                bin_size = int(bin_size_entry)
                median_smoothed = median_smoothing(numbers, bin_size)
                results += f"Median Smoothed: {median_smoothed}\n"
            else:
                raise ValueError("bin size for smoothing must be a number.")
            
        if var7.get():
            bin_size_entry = entry_bin_size.get()
            if bin_size_entry.isdigit():
                bin_size = int(bin_size_entry)
                boundary_smoothed = boundary_smoothing(numbers, bin_size)
                results += f"Boundary Smoothed: {boundary_smoothed}\n"
            else:
                raise ValueError("bin size for smoothing must be a number.")
        # Show the box plot
        if var8.get():
            fig, ax = plt.subplots()
            ax.boxplot(numbers)
            ax.set_title('Box Plot of Numbers')
            plt.show()
        if var9.get():
                
            norm=min_max_normalization(numbers)
            results += f"min max normalization: {norm}\n"
        if var10.get():
                
            norm=z_score_normalization(numbers)
            results += f"z score normalization: {norm}\n"
        if var11.get():
                
            norm=normalization_by_decimal_scaling(numbers)
            results += f"normalization by decimal scaling: {norm}\n"
        if var12.get():
            mode=calculate_mode(numbers)
            results += f"Mode: {mode}\n"

        messagebox.showinfo("Result", results)

            
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Data Preprocessing")
button1 = tk.Button(root, text="Upload Excel File", command=upload_file)
button1.pack()
button1.pack(anchor='n')
label = tk.Label(root, text="Enter name of column:")
label.pack()
label.pack(anchor='w')


entry = tk.Entry(root)
entry.pack()
entry.pack(anchor='w')


var1 = tk.IntVar()
chk1 = tk.Checkbutton(root, text='Mean', variable=var1)
chk1.pack()
chk1.pack(anchor='w')

var2 = tk.IntVar()
chk2 = tk.Checkbutton(root, text='Standard Deviation', variable=var2)
chk2.pack()
chk2.pack(anchor='w')

var3 = tk.IntVar()
chk3 = tk.Checkbutton(root, text='Median', variable=var3)
chk3.pack()
chk3.pack(anchor='w')

var4 = tk.IntVar()
chk4 = tk.Checkbutton(root, text='Variance', variable=var4)
chk4.pack()
chk4.pack(anchor='w')

var12 = tk.IntVar()
chk12 = tk.Checkbutton(root, text='Mode', variable=var12)
chk12.pack()
chk12.pack(anchor='w')

var5 = tk.IntVar()
chk5 = tk.Checkbutton(root, text='Smoothing by mean', variable=var5)
chk5.pack()
chk5.pack(anchor='w')

var6 = tk.IntVar()
chk6 = tk.Checkbutton(root, text='Smoothing by median', variable=var6)
chk6.pack()
chk6.pack(anchor='w')

var7 = tk.IntVar()
chk7 = tk.Checkbutton(root, text='Smoothing by bounders', variable=var7)
chk7.pack()
chk7.pack(anchor='w')

label_bin_size = tk.Label(root, text="Enter bin size for smoothing:")
label_bin_size.pack()
label_bin_size.pack(anchor='w')

entry_bin_size = tk.Entry(root)
entry_bin_size.pack()
entry_bin_size.pack(anchor='w')

var8 = tk.IntVar()
chk8 = tk.Checkbutton(root, text='Box Plot', variable=var8)
chk8.pack()
chk8.pack(anchor='w')

var9 = tk.IntVar()
chk9 = tk.Checkbutton(root, text='min max normalization ', variable=var9)
chk9.pack()
chk9.pack(anchor='w')


var10 = tk.IntVar()
chk10 = tk.Checkbutton(root, text='z score normalization', variable=var10)
chk10.pack()
chk10.pack(anchor='w')


var11 = tk.IntVar()
chk11 = tk.Checkbutton(root, text='normalization by decimal scaling', variable=var11)
chk11.pack()
chk11.pack(anchor='w')

button = tk.Button(root, text="Calculate", command=calculate)
button.pack()
button.pack(anchor='w')



root.mainloop()