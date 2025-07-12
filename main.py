from PySide6.QtWidgets import QMainWindow, QApplication
from appui import Ui_Dialog as Ui_MainWindow
import sys
import sounddevice as sd
import threading
import numpy as np
import queue
import time
from collections import deque


from decoding_methods.am_decoding import audio_stream_am
from decoding_methods.fm_decoding import audio_stream_fm


from sdr import sdriq, ip_port

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.iq_consumer_thread = None
        self.running = False
        self.volume = 1
        self.audio_buffer = deque()
        self.buffered_samples = 0
        self.ip_defined = False
        
        self.setWindowTitle("Doomsday Radio")
        self.radio_mode = "AM"
        self.current_value = 100400
    
        self.audio_queue = queue.Queue(maxsize=100)
        self.ui.freq_display.display(self.current_value)
        self.ui.freq_display.setDigitCount(8)
        self.ui.freq_increase.clicked.connect(self.increase_value)
        self.ui.freq_reduce.clicked.connect(self.decrease_value)
        self.ui.inputfreq.returnPressed.connect(self.input_freq)
        self.ui.ip.returnPressed.connect(self.change_ip_port)
        self.ui.port.returnPressed.connect(self.change_ip_port)

        self.ui.AM.clicked.connect(self.radiodecodemode)
        self.ui.FM.clicked.connect(self.radiodecodemode)
        self.ui.decodemode.setText(self.radio_mode)
        self.ui.volumebar.setMinimum(0)
        self.ui.volumebar.setMaximum(100)
        self.ui.volumebar.setValue(100)
        self.ui.volumebar.valueChanged.connect(self.change_volume)


        self.start_audio_stream()
    def change_ip_port(self):
        ip = self.ui.ip.text()
        port = self.ui.port.text()
        ip_port(ip, port)
        self.ip_defined = True
    def change_volume(self, value):
        self.volume = value / 100.0

    def start_audio_stream(self):
        if self.iq_consumer_thread and self.iq_consumer_thread.is_alive() and self.ip_defined:
            self.running = False
            self.iq_consumer_thread.join()

        self.playback_running = True
        self.running = True


        self.iq_consumer_thread = threading.Thread(target=self.iq_consumer, daemon=True)

        self.iq_consumer_thread.start()
        self.buffer_thread = threading.Thread(target=self.buffer_manager, daemon=True)
        self.buffer_thread.start()


        buffered_chunks = 0
        while buffered_chunks < 100:
            try:
                chunk = self.audio_queue.get(timeout=0.5)
                self.audio_buffer.append(chunk)
                self.buffered_samples += len(chunk)
                buffered_chunks += 1
            except queue.Empty:
                break

        self.audio_thread = threading.Thread(target=self.sounddevice_stream_af, daemon=True)
        self.audio_thread.start()



    def increase_value(self):
        self.current_value += 1
        self.ui.freq_display.display(self.current_value)



    def decrease_value(self):
        self.current_value -= 1
        self.ui.freq_display.display(self.current_value)


    def input_freq(self):
        text = self.ui.inputfreq.text()
        try:
            freq = float(text)
            if freq < 0:
                raise ValueError("Frequency must be non-negative")
            else:
                self.current_value = freq
                self.ui.freq_display.display(self.current_value)

        except ValueError:
            self.ui.freq_display.display(0)

    def radiodecodemode(self):
        button = self.sender()
        if button:
            self.radio_mode = button.text()
            self.ui.decodemode.setText(self.radio_mode)
            print(f"Radio mode set to: {self.radio_mode}")
            self.start_audio_stream()

    def iq_consumer(self):
        iq = sdriq(self.current_value)
        if self.radio_mode == "AM":
            audio_data = audio_stream_am(iq)
        elif self.radio_mode == "FM":
            audio_data = audio_stream_fm(iq)
        
        for audio_chunk in audio_data:
            if not self.running:
                break    
            try:
                self.audio_queue.put(audio_chunk, timeout=1)
            except queue.Full:
                pass

    
    def sounddevice_stream_af(self):
        with sd.OutputStream(
            samplerate=20000,
            channels=1,
            dtype='float32',
            blocksize=2048,
            callback = self.audio_stream
        ): 
            while self.running:
                time.sleep(0.1)


    def audio_stream(self, outdata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)

        output = np.zeros(frames, dtype=np.float32)
        samples_needed = frames
        
        while samples_needed > 0:
            if not self.audio_buffer:
                try:
                    chunk = self.audio_queue.get(timeout=0.05)
                    self.audio_buffer.append(chunk)
                    self.buffered_samples += len(chunk)
                except queue.Empty:
                    break
            if not self.audio_buffer:
                break

            chunk = self.audio_buffer[0]

            start_dix = frames - samples_needed
            take = min(len(chunk), samples_needed)
            output[start_dix: start_dix + take] = chunk[:take]

            samples_needed -= take
            if take == len(chunk):
                self.audio_buffer.popleft()
                self.buffered_samples -= take
            else:
                self.audio_buffer[0] = chunk[take:]
                self.buffered_samples -= take
            
        if samples_needed > 0:
            time.sleep(0.001)
        outdata[: , 0] = output * self.volume
    def buffer_manager(self):
        while self.running:
            try:
                chunk = self.audio_queue.get(timeout=0.1)
                self.audio_buffer.append(chunk)
                self.buffered_samples += len(chunk)
            except queue.Empty:
                continue


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())