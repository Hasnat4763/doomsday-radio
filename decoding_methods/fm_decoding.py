import numpy as np
from scipy.signal import lfilter

decimation = 5
audio_rate = 20000

class FMDemodulator:
    def __init__(self, decimation=5, audio_rate=20000, dc_alpha=0.999):
        self.decimation = decimation
        self.audio_rate = audio_rate
        self.dc_alpha = dc_alpha
        
        self.dc_b = np.array([1, -1], dtype=np.float32)
        self.dc_a = np.array([1, -dc_alpha], dtype=np.float32)

        self.prev_sample = 1 + 0j
        self.buffer = np.array([], dtype=np.float32)
        self.dc_state = np.zeros(1, dtype=np.float32)
        self.temp_phase = None
        self.temp_audio = None
    
    def dc_blocker_stateful(self, audio):
        filtered_audio, self.dc_state = lfilter(
            self.dc_b, self.dc_a, audio, zi=self.dc_state
        )
        return filtered_audio
    
    def process_chunk(self, iq_chunk):
        if len(iq_chunk) < 10:
            return None

        magnitude = np.abs(iq_chunk)
        magnitude = np.maximum(magnitude, 1e-9)
        iq_normalized = iq_chunk / magnitude

        iq_extended = np.concatenate([[self.prev_sample], iq_normalized])

        phase_diff = np.angle(iq_extended[1:] * np.conj(iq_extended[:-1]))

        self.prev_sample = iq_chunk[-1]
        
        if len(phase_diff) >= decimation:
            audio = phase_diff[::decimation]  
        else:
            audio = phase_diff

        audio = self.dc_blocker_stateful(audio)
        
        audio_float32 = np.clip(audio * 0.3, -1.0, 1.0).astype(np.float32)
        
        return audio_float32


def audio_stream_fm(iq_stream, chunk_size=2048, target_buffer_size=8192):

    prev_sample = 1 + 0j
    buffer = np.array([], dtype=np.float32)
    dc_state = np.zeros(1, dtype=np.float32)
    
    dc_b = np.array([1, -1], dtype=np.float32)
    dc_a = np.array([1, -0.999], dtype=np.float32)
    

    startup_buffer_size = target_buffer_size * 2
    startup_complete = False
    
    print(f"Building initial buffer (target: {startup_buffer_size} samples)...")
    
    for iq_chunk in iq_stream:
        if iq_chunk is None or len(iq_chunk) < 5:
            continue
        

        iq_chunk = iq_chunk / (np.abs(iq_chunk) + 1e-9)
        
        iq_extended = np.concatenate([[prev_sample], iq_chunk])
        phase_diff = np.angle(iq_extended[1:] * np.conj(iq_extended[:-1]))
        prev_sample = iq_chunk[-1]
        

        audio = phase_diff[::decimation]
        
        if len(audio) > 0:

            audio, dc_state = lfilter(dc_b, dc_a, audio, zi=dc_state)
            
            audio = np.clip(audio * 0.3, -1.0, 1.0).astype(np.float32)
            
            buffer = np.concatenate([buffer, audio])
        

        if not startup_complete:
            if len(buffer) >= startup_buffer_size:

                startup_complete = True
            else:
                continue
        

        while len(buffer) >= target_buffer_size + chunk_size:
            yield buffer[:chunk_size]
            buffer = buffer[chunk_size:]
        

        if len(buffer) > target_buffer_size * 4:

            while len(buffer) >= chunk_size:
                yield buffer[:chunk_size]
                buffer = buffer[chunk_size:]


