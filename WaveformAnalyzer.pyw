import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tkinter as tk
from tkinter import filedialog

# Initializable variables
GUI_WIDTH = 400
GUI_HEIGHT = 300
BACKGROUND_COLOR = "#F4F6F7"
FONT = "Microsoft JhengHei Light"
FONT_SIZE = 12
FONT_COLOR = "black"
WAVES_TO_SKIP = 5
NUM_WAVES = 10
REVISION = 'Version 1 - 22 Apr 2024'

# Global variables
file_path = None
sampling_frequency = None
freq = 0
text_out = None
text_out_color = "#B03A2E"
ready_for_analysis = False

def select_file():
    global ready_for_analysis
    global file_path
    global freq
    file_path = filedialog.askopenfilename()
    if file_path:
    # Code for Successful File selection
        try:
            freq = int(sampling_frequency)
            text_out = ("File selected: " + os.path.basename(file_path) + 
                        '\nSampling Frequency: ' + sampling_frequency + ' Hz')
            text_out_color = "#2874A6"
            ready_for_analysis = True
            print(file_path)
            print(type(file_path))
    # Code for incorrect Sampling Frequency
        except:
            text_out = "Please input the Sampling Frequency\n(Must be a number)"
            text_out_color = "#B03A2E"
            ready_for_analysis = False
    # Code for selected file
    else:
        text_out = "No file was selected"
        text_out_color = "#B03A2E"
        ready_for_analysis = False
    update_text_out(text_out, text_out_color)

def update_sampling_frequency(event):
    global sampling_frequency
    sampling_frequency = entry_sampling_frequency.get()
    print("Input sampling frequency:", sampling_frequency)

def update_text_out(text_out, text_out_color):
    file_info_text.config(state=tk.NORMAL)
    file_info_text.delete(1.0, tk.END)
    file_info_text.tag_configure("center", justify='center')
    file_info_text.config(fg = text_out_color)
    file_info_text.insert(tk.END, text_out)
    file_info_text.tag_add("center", "1.0", tk.END)
    file_info_text.config(state=tk.DISABLED)  # Disable editing

def preprocess_data(data, waves_to_skip, num_waves):
    # Center data range around zero
    data = data - data.min() - data.ptp() / 2
    
    # Remove starting waves of data
    count = 0
    is_neg = False
    for i in range(len(data)):
        if data[i] < 0 or is_neg:
            is_neg = True
        if data[i] >= 0 and is_neg:
            count += 1
            is_neg = False
            if count >= waves_to_skip - 1:
                data = data[i:]
                break
    # Truncate to set number of waves
    count = 0
    is_neg = False
    for i in range(len(data)):
        if data[i] < 0 or is_neg:
            is_neg = True
        if data[i] >= 0 and is_neg:
            count += 1
            is_neg = False
            if count >= num_waves + 1:
                data = data[:i]
                break

    # Recenter data range around zero
    data = data - data.min() - data.ptp() / 2
    # Remove starting waves of data    
    is_neg = False

    for i in range(len(data)):
        if data[i] < 0 or is_neg:
            is_neg = True
        if data[i] >= 0 and is_neg:
            data = data[i:]
            break

    return data

def fft_analysis(data, sample_rate, num_waves, waves_to_skip, filename):
    # Perform FFT
    fft_result = np.fft.fft(data)
    
    # Get frequencies corresponding to FFT result
    freqs = np.fft.fftfreq(len(data), 1/sample_rate)
    
    # Find principal frequency and its amplitude
    principal_freq_index = np.argmax(np.abs(fft_result))
    principal_freq = freqs[principal_freq_index]
    
    # Calculate number of samples for 4 cycles around the principal frequency
    num_samples = int(sample_rate / principal_freq * num_waves)
    
    # Generate sine wave with the principal frequency
    t_wave = np.linspace(0, num_waves / principal_freq, num_samples)
    amplitude = data.ptp() / 2
    sine_wave = amplitude * np.sin(2 * np.pi * principal_freq * t_wave)
    
    # Set seaborn style
    sns.set_style("whitegrid")
    
    # Create subplots
    fig = plt.figure(figsize=[12, 8])

    # Plot the FFT result
    ax1 = plt.subplot(2, 2, 2)
    ax1.plot(freqs, np.abs(fft_result) / np.abs(fft_result).max())
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Normalized Amplitude')
    ax1.set_title('Fast Fourier Transform')
    ax1.grid(True)
    ax1.set_xlim([0, freqs.max()])
    ax1.set_ylim([-0.005, 1.05])
    
    # Overlay sine wave onto original data
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(np.arange(num_samples) / sample_rate, 
             data[:num_samples], label='Original Data')
    ax2.plot(t_wave, sine_wave, 'r--', alpha=0.7, label=f'Fitted Sine Wave')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Original Data with Best Fit Sine Wave')
    ax2.grid(True)
    ax2.legend(loc=1)

    table = [['Wave Frequency', str(round(principal_freq, 3)) + ' Hz'],
             ['Peak to Peak Distance', str(round(data.ptp(), 4)) + ' mm'],
             ['Sampling Rate', str(sample_rate) + ' Hz'],
             ['Cycles Analyzed', str(num_waves)],
             ['Cycles Skipped', str(waves_to_skip)]]
    
    ax3 = plt.subplot(2, 2, 1)
    ax3.table(cellText = table,
              loc='center',
              cellLoc = 'center',
              in_layout = True,
              colWidths = [1/2, 1/4],
              fontsize =  250.0,
              bbox = [0.1, 0.2, 0.8, 0.6])
    ax3.axis('off')
    
    fig.suptitle('Waveform Analysis: ' + filename, 
                 fontsize=18)

    # Adjust layout
    plt.tight_layout()
    
    # Show plot
    plt.show()
    
    print("Principal Frequency:", principal_freq, "Hz")

def run_analysis():

    if ready_for_analysis:

        data = np.genfromtxt(file_path,
                             delimiter=',',
                             usecols=2)
    
        data = preprocess_data(data, WAVES_TO_SKIP, NUM_WAVES)

        fft_analysis(data, freq, NUM_WAVES, WAVES_TO_SKIP, os.path.basename(file_path))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Selection")

    # Set background color to the specified value
    root.configure(background=BACKGROUND_COLOR)

    # Calculate the position to open the window in the center
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - GUI_WIDTH) // 2
    y = (screen_height - GUI_HEIGHT) // 2

    # Set the geometry of the window
    root.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}+{x}+{y}")

    # Create a frame to hold all the widgets
    frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    title_label = tk.Label(frame, text="FFT Waveform Analyzer", bg=BACKGROUND_COLOR, fg=FONT_COLOR,
                                         font=(FONT, FONT_SIZE + 5, 'bold'))
    title_label.pack(pady=15)

    # Create a button to select the file
    button_select_file = tk.Button(frame, text="Select Waveform CSV", command=select_file,
                                    font=(FONT, FONT_SIZE), bg="white", fg=FONT_COLOR, bd=1, relief="raised")
    button_select_file.pack(pady=8)

    # Create a button to run analysis
    button_run_analysis = tk.Button(frame, text="Run Analysis", command=run_analysis,
                                     font=(FONT, FONT_SIZE), bg="white", fg=FONT_COLOR, bd=1, relief="raised")
    button_run_analysis.pack(pady=8)

    # Create input field for sampling frequency
    label_sampling_frequency = tk.Label(frame, text="Input sampling frequency", bg=BACKGROUND_COLOR, fg=FONT_COLOR,
                                         font=(FONT, FONT_SIZE))
    label_sampling_frequency.pack()

    entry_sampling_frequency = tk.Entry(frame, font=(FONT, FONT_SIZE))
    entry_sampling_frequency.pack()

    # Bind the event to update sampling frequency when typing
    entry_sampling_frequency.bind("<KeyRelease>", update_sampling_frequency)

    # Create text field to display file info
    file_info_text = tk.Text(frame, height=2, width=40, font=(FONT, FONT_SIZE),
                              bg=BACKGROUND_COLOR, bd=0)
    file_info_text.config(state=tk.DISABLED, fg=FONT_COLOR)  # Disable editing
    file_info_text.pack(pady=8)

    version_name = tk.Label(root, 
                            text=REVISION, 
                            bg=BACKGROUND_COLOR, 
                            fg=FONT_COLOR,
                            font=(FONT, FONT_SIZE-2),
                            anchor='sw')
    version_name.place(x=10,
                       y=GUI_HEIGHT - 30)

    root.mainloop()
