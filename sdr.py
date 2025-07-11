import numpy as np
import SoapySDR
from SoapySDR import *
import time

server_ip = "62.45.168.247"
server_port = "7878"


sample_rate = 1.024e6
decimation_factor = 10
sdr = SoapySDR.Device(f"rtltcp={server_ip}:{server_port}")
sdr.setSampleRate(SOAPY_SDR_RX, 0, sample_rate)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream)
time.sleep(1.0)

def sdriq(i):
    freq = i * 1e3
    sdr.setFrequency(SOAPY_SDR_RX, 0, freq)

    buff = np.zeros(8192, dtype=np.complex64)
    iq_buffer = []

    while True:
        sr = sdr.readStream(rxStream, [buff], len(buff), timeoutUs=2000)
        if sr.ret > 0:
            iq = buff[:sr.ret]
            iq = iq[::decimation_factor]
            iq_buffer = np.concatenate([iq_buffer, iq]) if len(iq_buffer) > 0 else iq
            if len(iq_buffer) >= 4096:
                yield iq_buffer[:4096]
                iq_buffer = iq_buffer[4096:]
        else:
            time.sleep(0.01)
            print(f"SDR readStream error: {sr.ret}")