"""
Functions used for testing:
    - Printing and ploting test outputs
    - Generating input data
"""
import math
import numpy as np
import wave
import struct
import pandas as pd


def func_generator(func_name="sin", freq=16000.0, amp=1.0, phase=0.0, offset=0.0):
    """
    Factory for generating arbitrary functions

    :param func_name: Keyword
    :param freq: Frequency
    :param amp: Amplitude
    :param phase: Phase in radians
    :param offset: Offset value
    :return: Function with one float argument
    """

    def sin_func(t):
        return amp * math.sin(2 * math.pi * freq * t + phase)

    def const_func(t):
        return amp

    def linear_func(t):
        return amp * t + offset

    if func_name == "sin":
        return sin_func
    if func_name == "const":
        return const_func
    if func_name == "linear":
        return linear_func


def func_to_nparray(func=math.sin, t_min=0.0, t_max=2.0 * math.pi, size=16000, fixed_size=False):
    """
    Returns numpy array of a function with the given range at 16KHz sampling rate

    :param func: Function for tabulating
    :param t_min: Start time
    :param t_max: End time
    :param fixed_size: Does function produces fixed size array
    :param size: Size of the fixed array, and inverse dt
    :return: Numpy array
    """
    dt = 1.0 / size
    if fixed_size is False:
        data_pts = int(t_max / dt)
    else:
        data_pts = size
    return np.asarray([func(i * dt) if t_min <= i * dt < t_max else 0.0 for i in range(data_pts)])


def make_wav(samples, filename):
    """
    Prints data to wav file sampled at 16KHz as uint16

    :param samples: Numpy array
    :param filename: File to print data to
    :return: None
    """
    wav = wave.open(filename, 'w')
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(16000)

    for i in samples:
        value = struct.pack('<h', int(i))
        wav.writeframes(value)

    wav.close()


def nparray_to_fft(data, sample_rate=16000):
    """
    Compute the one-dimensional discrete Fourier Transform for real input.

    :param data: nparray of float falues
    :param sample_rate: Sample rate, 16KHz default
    :return: nparray frequencies vector, nparrat Fourier transform vector
    """
    n = data.shape[0]
    yf = (2 / n) * np.abs(np.fft.rfft(data))
    xf = np.linspace(0.0, sample_rate / 2, n / 2 + 1)
    return xf, yf


def nparray_to_fft_spectrum(data, sample_rate=16000, window=320, offset=160):
    """
    Compute the spectrum discrete Fourier Transform for real input.

    :param offset: Window moving offset
    :param window: Window size for calculation of fft
    :param data: nparray of float falues
    :param sample_rate: Sample rate, 16KHz default
    :return: nparray frequencies vector, nparrat Fourier transform vector
    """
    n = data.shape[0]
    spec_pts = int((n / offset) - 1)
    yf = np.zeros((spec_pts, offset + 1), dtype=float)
    for i in range(spec_pts):
        left = i * offset
        right = left + window
        yf[i] = (2 / window) * np.abs(np.fft.rfft(data[left:right]))
    return yf


def nparray_to_calc_spectrum(sig_li, size, sample_rate=16000, window=320, offset=160):
    """
    Calculates the spectrum acording to given data.

    :param offset: Window moving offset
    :param window: Window size for calculation of fft
    :param sample_rate: Sample rate, 16KHz default
    :return: nparrat Fourier transform vector
    """
    n = size
    spec_pts = int(round(n / offset) - 1)
    yc = np.zeros((spec_pts, offset + 1), dtype=float)
    idf = 2 * offset / sample_rate
    for i in range(spec_pts):
        left = i * offset
        right = left + window
        for j in range(len(sig_li["tmin"])):
            if (left + offset > sig_li["tmin"][j] * sample_rate
                    and right - offset < sig_li["tmax"][j] * sample_rate):
                ifreq = int(sig_li["freq"][j] * idf)
                diff = sig_li["freq"][j] * idf - ifreq
                yc[i][ifreq] = sig_li["amp"][j] * (1 - diff)
                yc[i][ifreq + 1] = sig_li["amp"][j] * diff
    return yc


def load_spice_out(file_name):
    """
    Loads spice output file and returs pandas object

    :param file_name: LTSpice output file name
    :return: Pandas object
    """
    return pd.read_csv(file_name, delimiter='\t', comment='#', dtype=float)
