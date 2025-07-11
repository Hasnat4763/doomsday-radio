from scipy.signal import decimate

import numpy as np

decimation = 10
audio_rate = 44100



def dc_blocker(audio, prev_dc=0, alpha=0.999):
    dc_estimate = prev_dc
    output = np.zeros_like(audio)
    for i, sample in enumerate(audio):
        dc_estimate = alpha * dc_estimate + (1-alpha) * sample
        output[i] = sample - dc_estimate
    return output, dc_estimate

    

def audio_stream_fm(iq_W, chunk_size=2048):
    prev = 1 + 0j
    buffer = np.array([], dtype=np.float32)
    prev_dc = 0
    for iq in iq_W:
        if len(iq) < 30:
            continue
        W = iq[-1]
        iq = np.concatenate([[prev], iq])
        
        iq /= (np.abs(iq) + 1e-9)
        phase = np.angle(iq[1:] * np.conj(iq[:-1]))
        
        audio = decimate(phase, decimation, ftype='fir', zero_phase=False)

        audio, prev_dc = dc_blocker(audio, prev_dc)

        max_val = np.max(np.abs(audio))+ 1e-9

        audio_float32 = (audio / max_val * 0.9).astype(np.float32)
        buffer = np.concatenate((buffer, audio_float32))
        while len(buffer) >= chunk_size:
            yield buffer[:chunk_size]
            buffer = buffer[chunk_size:]
        prev = W
