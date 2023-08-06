import synacell.signal as signal
import random as rnd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.io import wavfile


def run_dft_signal():
    sig_cnt = 1
    sig_li = dict()
    sig_li["freq"] = []
    sig_li["amp"] = []
    sig_li["phase"] = []
    sig_li["tmin"] = []
    sig_li["tmax"] = []
    func_arr = np.zeros(16000)
    # Generate wav file
    for i in range(sig_cnt):
        freq = rnd.random()*3900.0 + 100.0
        amp = rnd.random()*1000.0
        phase = 2.0*math.pi*rnd.random()
        tmin = 0
        tmax = 1
        func = signal.func_generator(func_name="sin", freq=freq, amp=amp, phase=phase)
        func_arr += signal.func_to_nparray(func=func, t_min=tmin, t_max=tmax, size=16000,
                                           fixed_size=True)

    signal.make_wav(func_arr, f"./random_{sig_cnt}.wav")
    xf, yf = signal.nparray_to_fft(func_arr)

    fig, ax = plt.subplots(2, 1)
    fig.suptitle('Discrete Fourier transform')

    ax[0].plot([i * 1.0 / 16000.0 for i in range(16000)], func_arr)
    ax[0].set_title(f"Random func f(t) freq={freq:.2f}, amp={amp:.2f}")
    ax[0].grid(True)
    ax[0].legend()

    ax[1].plot(xf, yf, label="random func")
    ax[1].set_title(f"FFT window={320}, offset={160}")
    ax[1].grid(True)
    ax[1].legend()

    plt.show()


def run_dft_spectrogram():
    sig_cnt = 10
    sig_li = dict()
    sig_li["freq"] = []
    sig_li["amp"] = []
    sig_li["phase"] = []
    sig_li["tmin"] = []
    sig_li["tmax"] = []
    func_arr = np.zeros(16000)
    # Generate wav file
    for i in range(sig_cnt):
        freq = rnd.random()*3900.0 + 100.0
        sig_li["freq"].append(freq)
        amp = rnd.random()*1000.0
        sig_li["amp"].append(amp)
        phase = 2.0*math.pi*rnd.random()
        sig_li["phase"].append(phase)
        tmin = rnd.random()*0.25
        sig_li["tmin"].append(tmin)
        tmax = tmin + rnd.random()*0.5
        tmax = 1.0 if tmax > 1.0 else tmax
        sig_li["tmax"].append(tmax)
        func = signal.func_generator(func_name="sin", freq=freq, amp=amp, phase=phase)
        func_arr += signal.func_to_nparray(func=func, t_min=tmin, t_max=tmax, size=16000,
                                           fixed_size=True)
        print(f"freq={freq}, amp={amp}")

    signal.make_wav(func_arr, f"./random_{sig_cnt}.wav")
    func_arr = func_arr[0:8000]
    window = 320
    offset = 160
    yf = signal.nparray_to_fft_spectrum(func_arr, window=window, offset=offset)
    yc = signal.nparray_to_calc_spectrum(sig_li=sig_li, size=len(func_arr), window=window,
                                         offset=offset)

    fig, ax = plt.subplots(3, 1, sharex=True)
    fig.suptitle('Discrete Fourier transform')

    ax[0].plot([i * 1.0 / 16000.0 for i in range(len(func_arr))], func_arr, label="random func")
    ax[0].set_title("f(t)")
    ax[0].grid(True)
    ax[0].legend()

    # Color map for fft
    cm_spec = plt.get_cmap('jet')
    cm_spec.set_under(color=(0.0, 0.0, 0.0), alpha=1.0)
    cm_spec.set_over(color=(1.0, 1.0, 1.0), alpha=1.0)
    # Select rect of the form x0,x1,y0,y1
    ext = [0, len(func_arr)/16000, 4000, 0]

    # Draw spectrogram
    ax[1].imshow(
        yf[:, 0:80].transpose(),
        interpolation='none',
        norm=colors.PowerNorm(gamma=0.5, vmin=yf.min(), vmax=yf.max()),
        extent=ext,
        cmap=cm_spec,
        aspect='auto',
        vmin=0,
        vmax=1000
    )
    ax[1].set_title(f"FFT window={window}, offset={offset}")

    # Draw spectrogram
    ax[2].imshow(
        yc[:, 0:80].transpose(),
        interpolation='none',
        norm=colors.PowerNorm(gamma=0.5, vmin=yc.min(), vmax=yc.max()),
        extent=ext,
        cmap=cm_spec,
        aspect='auto',
        vmin=0,
        vmax=1000
    )
    ax[2].set_title(f"Calculated frequency amplitude window={window}, offset={offset}")

    plt.xlim(0, len(func_arr)/16000)

    plt.show()


def run_dft_spectrogram_wav(filename="../data/audio/down/03cf93b1_nohash_1.wav"):
    fs, data = wavfile.read(filename)
    yf = signal.nparray_to_fft_spectrum(data)

    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.suptitle('Discrete Fourier transform')

    ax[0].plot([i * 1.0 / 16000.0 for i in range(len(data))], data, label=f"{filename}")
    ax[0].set_title("f(t)")
    ax[0].grid(True)
    ax[0].legend()

    # Color map for fft
    cm_spec = plt.get_cmap('jet')
    cm_spec.set_under(color=(0.0, 0.0, 0.0), alpha=1.0)
    cm_spec.set_over(color=(1.0, 1.0, 1.0), alpha=1.0)
    # Select rect of the form x0,x1,y0,y1
    ext = [0, len(data) / 16000, 4000, 0]

    # Draw spectrogram
    ax[1].imshow(
        yf[:, 0:80].transpose(),
        interpolation='none',
        norm=colors.PowerNorm(gamma=0.5, vmin=yf.min(), vmax=yf.max()),
        extent=ext,
        cmap=cm_spec,
        aspect='auto',
        vmin=0,
        vmax=20000
    )
    ax[1].set_title(f"FFT window={320}, offset={160}")

    plt.xlim(0, len(data) / 16000)

    plt.show()


if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    # run_dft_signal()
    # run_dft_spectrogram()
    run_dft_spectrogram_wav()
