import numpy as np
import SoapySDR
from SoapySDR import *
import time
from collections import deque

server_ip = ""
server_port = "1234"
ip_defined = False





sample_rate = 2.4e6
decimation_factor = 10
effective_rate = sample_rate // decimation_factor

buffer_size = 32768
output_size = 4096
def ip_port(x,y):
    global server_ip, server_port, ip_defined, sdr, rxStream
    server_ip = x
    server_port = y
    ip_defined = True

    if ip_defined == True:
        sdr = SoapySDR.Device(f"rtltcp={server_ip}:{server_port}")
        sdr.setSampleRate(SOAPY_SDR_RX, 0, sample_rate)


        try:
            sdr.writeSetting("bufflen", "32768")
        except:
            pass

        sdr.setFrequency(SOAPY_SDR_RX, 0, 100400e3)
        rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
        sdr.activateStream(rxStream)
        time.sleep(1.0)

def sdriq(frequency_hz):

    sdr.setFrequency(SOAPY_SDR_RX, 0, frequency_hz * 1e3)
    buff = np.zeros(buffer_size, dtype=np.complex64)
    iq_buffer = deque()
    buffer_samples = 0
    

    sample_count = 0
    
    while True:
       
        sr = sdr.readStream(rxStream, [buff], len(buff), timeoutUs=2000000)
        
        if sr.ret > 0:

            iq = buff[:sr.ret:decimation_factor]
            

            iq_buffer.extend(iq)
            buffer_samples += len(iq)
            sample_count += len(iq)
            

            while buffer_samples >= output_size:

                output_samples = np.array([iq_buffer.popleft() for _ in range(output_size)])
                buffer_samples -= output_size
                yield output_samples
                
        else:
            print(f"SDR readStream error: {sr.ret}")
            time.sleep(0.01)