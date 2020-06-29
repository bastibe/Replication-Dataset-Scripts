"""test_signals

Generate test signals by mixing speech and noise at a speech-aware
SNR. And generate speech-like HTCs.

"""

import numpy
import resampy
from scipy import signal


def create_test_signal(speech, noise, noise_start, snr, samplerate=None):
    """Mix a speech and noise signal at a given SNR."""

    speech_signal = speech.signal
    speech_samplerate = speech_signal.metadata['samplerate']
    samplerate = samplerate or speech_samplerate
    if len(speech_signal.shape) > 1:  # convert to mono
        speech_signal = speech_signal[:, 0]
    if speech_samplerate != samplerate:  # resample
        speech_signal = resampy.resample(speech_signal, speech_samplerate, samplerate)

    noise_signal = noise.signal
    noise_samplerate = noise_signal.metadata['samplerate']
    if len(noise_signal.shape) > 1:  # convert to mono
        noise_signal = noise_signal[:, 0]
    if noise_samplerate != samplerate:  # resample
        noise_signal = resampy.resample(noise_signal, noise_samplerate, samplerate)

    noise_start = int(noise_start*samplerate)
    noise_signal = noise_signal[noise_start:noise_start+len(speech_signal)]

    return mix(speech_signal, noise_signal, snr, samplerate)


def create_htc(duration, basefrequency, modulation, lowpass_freq, samplerate):
    """Create a speech-like harmonic tone complex."""

    time = numpy.arange(samplerate*duration)/samplerate
    frequency = basefrequency * modulation**numpy.sin(2*numpy.pi * time)

    speech_signal = numpy.zeros(samplerate*duration)
    for harmonic in range(10):
        partial_frequency = frequency*(harmonic+1)
        if numpy.max(partial_frequency) > samplerate/2:
            break
        speech_signal += numpy.cos(numpy.cumsum(2*numpy.pi * partial_frequency / samplerate))

    filter_coeffs = signal.butter(1, lowpass_freq/(samplerate/2))
    return signal.lfilter(*filter_coeffs, speech_signal)


def mix(signal, noise, snr_db, samplerate):
    """Mix a signal and noise signal at a given signal to noise ratio."""

    signal_power = vad_power(signal, samplerate)
    noise_power = rms(noise)
    mix_signal = signal + noise/noise_power*signal_power / 10**(snr_db/20)
    return mix_signal/numpy.max(mix_signal)


def rms(signal):
    return numpy.mean(signal**2)**0.5


def vad_power(signal, samplerate, blocklength=0.02):
    """The power of a speech signal, only where there is speech.

    Calculate the signal level for short signal blocks, remove
    outliers, then define a threshold at halfway between the min and
    max level. The speech power is calculated from all signal values
    above that threshold.

    """
    # calculate signal level for short signal blocks:
    blocksize = int(samplerate*blocklength)
    levels = [20*numpy.log10(rms(signal[idx:idx+blocksize]))
              for idx in range(0, len(signal)-blocksize, blocksize)]
    # remove outliers:
    low, high = numpy.percentile(levels, [5, 95])
    no_outliers = numpy.array(levels)[(low < levels) & (levels < high)]
    # calculate threshold:
    threshold = (max(no_outliers) + min(no_outliers))/2
    # calculate signal power only where the signal is active:
    powers = [(10**(lvl/20))**2 for lvl in levels
              if lvl > threshold]
    return numpy.mean(powers)**0.5
