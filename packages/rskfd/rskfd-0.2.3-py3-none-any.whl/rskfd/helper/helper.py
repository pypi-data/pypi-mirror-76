# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 2020

(C) 2020, Florian Ramian
"""


def ShowLogFFT( data, fs = 1, MaxFftLength = 10000, bPlotRelative = True):
    """Helper function showing the magnitude of the FFT on a logarithmic scale.
    Signal length is limited to MaxFftLength to speed up FFT calculation.
    Input data is interpreted as Volts and converted to dBm."""

    import matplotlib.pyplot as plt
    import numpy
    limiterlen = min(MaxFftLength,len(data))

    plt.ion()
    plt.show()

    if bPlotRelative:
        mag = 20*numpy.log10(numpy.abs(numpy.fft.fftshift(numpy.fft.fft(data[:limiterlen]))))
        # normalize to mean
        meanmag = 10*numpy.log10( numpy.mean( numpy.power( 10, mag/10)))
        mag = mag - meanmag
    else:
        mag = 10*numpy.log10(numpy.power( numpy.abs( numpy.fft.fftshift( numpy.fft.fft( data[:limiterlen]))), 2)/50/limiterlen)+30
    
    freq = numpy.multiply( range( -limiterlen//2,(limiterlen+1)//2), fs/limiterlen)
    plt.plot(freq,mag)
    plt.grid( True)
    plt.xlabel( 'freq / Hz')
    if bPlotRelative:
        plt.ylabel( 'relative power / dB')
    else:
        plt.ylabel( 'power / dBm')
    plt.draw()
    plt.pause(.001)
    


if __name__ == "__main__":
    # execute only if run as a script
    pass   