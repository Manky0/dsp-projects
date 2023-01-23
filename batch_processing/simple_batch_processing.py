'''
Search recursively all files with .wav extension and sub-directories, then store the paths of these files.
After that the code process each file to read the signal waveform and energy segments of (n = 100).
Finally we plot the signal waveform and energy segments in two plots, organizated with subplot(211)

The main module to read signals from the .wav files is the built in python wave, considering that we don't need to install anything new
this module was the best choice to begginers in python. As other options to extract the waveform from the files, we have the modules
scipy.wave or wavy (https://pypi.org/project/wavy/)

Credits:
- Dataset utilized to tests: https://www.kaggle.com/datasets/lazyrac00n/speech-activity-detection-datasets?resource=download

Authors:
- Giovanna Cunha
- Gabriel Moraes
- Valdinei Rodrigues
'''

import os
import wave
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
import math

wavFiles = []

# Search reursively the files and store in a list
for root, dirs, files in os.walk('../DataSet/'):
    for file in files:
        if (file.endswith('.wav')):
            wavFiles.append(os.path.join(root, file))

# Function to get the waveform data of each file
def getAudioData(wav_obj):
    n_samples = wav_obj.getnframes()
    sample_freq = wav_obj.getframerate()

    t_audio = n_samples/sample_freq

    signal_wave = wav_obj.readframes(n_samples)

    signal_array = np.frombuffer(signal_wave, dtype=np.int16)

    l_channel = signal_array[0::2]
    r_channel = signal_array[1::2]

    times = np.linspace(0, n_samples/sample_freq, num=n_samples)

    audioData = {'n_samples': n_samples, 'samples_freq': sample_freq, 'signal_array': signal_array, 'times': times, 't_audio': t_audio, 'r_channel': r_channel, 'l_channel': l_channel}
    return audioData

# Processes each file with a loop
for wavFile in wavFiles:
    # Here we could have utilized other options like scipy.wave or wavy
    wav_obj = wave.open(wavFile)
    audioData = getAudioData(wav_obj)

    # Define and store the data to plot segmental energy
    segment_size = 100
    # Looses a little of data in the end of audio because of math.floor
    segments_number = math.floor(len(audioData['signal_array'])/100)
    segments = np.empty([segments_number, math.floor(len(audioData['signal_array'])/100)])

    for i in range(segments_number):
        pointer = 0
        for j in range(segment_size*(i+1)-100, segment_size*(i+1)):
            segments[i, pointer] = audioData['signal_array'][j]
            pointer += 1

    energy = []
    for i in range(segments_number):
        energy.append((norm(segments[i])**2))

    # Plots all the data in two graphs organizated with subplot(211)
    plt.figure(i)
    plt.subplot(211)   
    plt.ylabel('Energy')
    plt.xlabel('Segments')
    plt.plot(energy)

    plt.title(f'Signal wave and energy segments of {wavFile}')
    plt.subplot(212)
    plt.ylabel('Amplitude')
    plt.xlabel('Samples')
    plt.plot(audioData['signal_array'])

    plt.show()


