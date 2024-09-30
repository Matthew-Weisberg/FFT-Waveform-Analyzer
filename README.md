# FFT Waveform Analyzer

## About the Project
This project is an application I created in my professional career to help calculate and visualize the frequency and amplitude of vibrating motion. The harmonic motion of home electronic devices were being measured with a Keyence laser displacement sensor, and its accompanying software had no features with which to analyze the data it recorded. It would return results as a downloadable CSV and my teammembers would manually try to identify time points of peaks and valleys of the data in a simple spreadsheet software to measure ampltidue and frequency. This was a time consuming and non-repeatable process, and the nature of the product we were designing would require many repetitions of this type of measurement. I found that an automated application could perform such a task repeatably and free up a lot of engineering hours. 

The goal was to allow a user to select a local CSV file and provide the sampling frequency at which the data was measured, and the application would analyze it with a fast-fourier transform and return a visual graphic of both the data and information including the dominant frequency and peak-to-peak amplitude of the data.

## Getting Started
This code uses [Python](https://www.python.org/) with the following packages:
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)
- [os](https://docs.python.org/3/library/os.html)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

## Usage
The application is a simple interface designed for ease of use. 

![FFT Waveform Analyzer Interface](https://github.com/user-attachments/assets/5bb709c9-6917-408c-b796-5ee75c865980)

Below is an example of harmonic data measured by the Keyence system. The output csv only contains a singular data column with a measured displacement value in mm for each consecutive timestep.

![Sample Harmonic Data](https://github.com/user-attachments/assets/d99f9c4d-0bb4-4487-99a0-12e661ca59fa)

In order to use the Analyzer application, perform the following steps:
1. Input the sampling frequency of the data in Hz.
2. Click the *Select Waveform CSV* button to open a file dialog and choose the csv to analyze.
3. Click *Run Analysis*, and if the data is in an acceptable form, it will produce the output analyzed data.

#### GUI when sampling frequency is specified and CSV is selected

![Sample Analyzer Input](https://github.com/user-attachments/assets/bac766fc-b4a7-4d28-9891-b32d9c80be29)

#### Output analysis of sample data shown above

![Sample Analyzer Output](https://github.com/user-attachments/assets/02019667-cff3-4f1c-a8b6-e327fc26dcb7)

### USAGE NOTES ON VERSION 1.0.0
- The application checks that a sampling frequency is input prior to CSV selection. It will output red text stating that a sampling frequency has not been input if done in reverse order. Reselect the CSV once the frequency has been entered.
- The Keyence measurement system outputs the data in mm and in the 3rd column of it's CSVs and thus the application is hardcoded to analyze the data in its third column and assumes all data is in mm.
- If there is an error in the analysis or if the data is set up incorrectly, the application will simply not produce an output image.

## Analysis Details
This is a step-by-step description of data in a CSV is analyzed when after it has been read in within an input sampling frequency value.
#### Data Preprocessing
1. Center the data to its midrange. This is done by subtracting its minimum value and then subtracting half its peak-to-peak value.
2. Remove the first 5 waves of data. In order to remove noise at the start of the measurement: a loop counts for the first 5 times the data crosses from negative to positive, finds that index and removes data from the start to that index. 5 is a hardcoded value that can be changed and is recorded in the output image.
3. Truncate to the next 10 waves of data. A subsection of the data is selected: again, a loop counts for the next 10 times the data crosses from negative to positive and truncates the data up to that point. 10 is a hardcoded value that can be changed and is recorded in the output image.
4. After truncation, the data subsection is recentered to its new midrange with the method in step 1. This removes an offset in the event that the data drifts over the entire measurement time.
5. If the start of the data subsection is below zero, then it removes all points until it crosses to positive, thus improving the chances for the subsection wave to start with a 0 time offset.
#### Fast Fourier Transform Analysis
6. It uses Numpy's built in np.fft.fft functionality on the subsection of data. I uses np.fft.fftfreq with the user's input sampling to retrieve the output frequencies to match to its output amplitudes.
7. It finds the index dominant (max) frequency in the fft output and uses it to retrieve the actual frequency value from the fftfreq output.
8. The output image plots the subsection data with a generated sine wave with the frequency of the found maximum frequency and overlays it. This is for a sanity check to the user to make sure the analyzed data makes sense.
9. It normalizes the fft output and plots the percent contribution vs frequency in the top right.
10. It creates a table with the key output values inclduing peak-to-peak amplitude, the dominant frequency, and important hard coded parameters.
