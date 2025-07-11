import numpy as np


from scipy.signal import resample_poly, butter, sosfilt


sample_rate = 2.4e6
decimation_factor = 10
intermediate_rate = int(sample_rate / decimation_factor)


target_rate = 44100  


def am_demodulate(iq):
    envelope = np.abs(iq)
    audio = envelope - np.mean(envelope)

    sos = butter(5, 5000, btype='low', fs=intermediate_rate, output='sos')
    audio = sosfilt(sos, audio)


    return dc_blocker(audio)


def dc_blocker(audio, alpha = 0.95):
     output = np.zeros_like(audio)
     for i in range(1, len(audio)):
          output[i] = alpha * (output[i-1] + audio[i] - audio[i-1])
     return output


def audio_stream_am(iq):
    buffer = np.array([], dtype=np.float32)
    chunk_size = 2048
    for iq_chunk in iq:
            if len(iq_chunk) < 10:
                continue
            audio = am_demodulate(iq_chunk)
            resampled = resample_poly(audio, target_rate, intermediate_rate)

            max_val = np.max(np.abs(resampled)) + 1e-9
            resampled = np.clip(resampled/max_val, -1.0, 1.0)

            buffer = np.concatenate((buffer, resampled.astype(np.float32)))

            while len(buffer) >= chunk_size:
                 yield buffer[:chunk_size]
                 buffer = buffer[chunk_size:]