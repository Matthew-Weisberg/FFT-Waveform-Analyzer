# FFT Waveform Analyzer

## About the project
This project is an application I created in my professional career to help calculate and visualize the frequency and amplitude of vibrating motion. The motion of test home electronic devices was being captured with a Keyence laser displacement sensor and its accompanying software had no features with which to analyze the data it recorded. It would return downloadable results as a csv and teammembers would manually try to identify time points of peaks and valleys in simple spreadsheet softwares to measure ampltidue and frequency. This was a time consuming and non-repeatable process, and the nature of the product we were designing would require often repetitions of this type of measurement. I found that an automated application could perform such a task repeatably and free up a lot of engineering hours. 

The goal was to allow a user to select a local csv file and provide the sampling frequency at which the data was measured, and the application would analyze it with a fast-fourier transform and return a visual graphic of both the data and information including the dominant frequency and peak-to-peak amplitude of the data.

## Getting Started
This code uses [Python](https://www.python.org/) with the following packages:
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)
- [os](https://docs.python.org/3/library/os.html)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

To use this file without downloading any of the above, please download the Standalone folder labeled  **Standalone FFT Waveform Analyzer.** Inside the folder is a shortcut icon for an executable created with PyInstaller that can be used as a standalone application on any Windows 10+ computer.

## Usage
![FFT Waveform Analyzer Main Page Image](https://github.com/user-attachments/assets/d4a3d473-f8f0-4dc3-8c4e-82f5d18a1a0e)

The application is a simple interface designed for ease of use. 

...
