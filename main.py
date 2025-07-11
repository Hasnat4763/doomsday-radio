from PySide6.QtWidgets import QMainWindow, QApplication
from appui import Ui_Dialog as Ui_MainWindow
import sys
import sounddevice as sd
import threading
import numpy as np
import itertools
import queue
import time
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout

from decoding_methods.am_decoding import audio_stream_am
from decoding_methods.fm_decoding import audio_stream_fm
from sdr import sdriq

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if self.ui.spectrumplot.layout() is None:
            self.ui.spectrumplot.setLayout(QVBoxLayout())

        self.decode_thread = None
        self.running = False

        self.spectrumplotW = pg.PlotWidget()
        self.spectrumplotW.setYRange(-100,0)
        self.spectrumplotW.setLabel('bottom', 'Freq', units='kHz')
        self.spectrumplotW.setLabel('left', 'Power', units='dB')
        self.spectrumplotW.showGrid(x=True, y=True)

        self.ui.spectrumplot.layout().addWidget(self.spectrumplotW)
        self.spectrum_curve = self.spectrumplotW.plot(pen='y')

        self.buffer = np.array([], dtype = np.float32)
        self.volume = 0.5
        
        self.setWindowTitle("Doomsday Radio")
        self.radio_mode = "FM"
        self.current_value = 100
        self.audio_queue = queue.Queue(maxsize=10000)
        self.ui.freq_display.display(self.current_value)
        self.ui.freq_display.setDigitCount(8)
        self.ui.freq_increase.clicked.connect(self.increase_value)
        self.ui.freq_reduce.clicked.connect(self.decrease_value)
        self.ui.inputfreq.returnPressed.connect(self.input_freq)
        self.ui.AM.clicked.connect(self.radiodecodemode)
        self.ui.FM.clicked.connect(self.radiodecodemode)
        self.ui.decodemode.setText(self.radio_mode)

        self.ui.volumebar.setMinimum(0)
        self.ui.volumebar.setMaximum(100)
        self.ui.volumebar.setValue(50)
        self.ui.volumebar.valueChanged.connect(self.change_volume)

        self.start_audio_stream()
    def change_volume(self, value):
        self.volume = value / 100.0

    def start_audio_stream(self):
        if self.decode_thread and self.decode_thread.is_alive():
            self.running = False
            self.decode_thread.join()

        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

        self.playback_running = True
        self.running = True
        
        self.decode_thread = threading.Thread(target=self.demodulating, daemon=True)
        self.decode_thread.start()
        while self.audio_queue.qsize() < 25 and self.running:
            time.sleep(0.01)
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

    
    def demodulating(self):
        iq = sdriq(self.current_value)
        iq_chunk_plotting = np.array(list(itertools.islice(iq, 1024)))

        if self.radio_mode == "AM":
            audio_data = audio_stream_am(iq)
        elif self.radio_mode == "FM":
            audio_data = audio_stream_fm(iq)
        
        for audio_chunk in audio_data:
            self.update_spectrum(iq_chunk_plotting)
            if not self.running:
                break    
            try:
                self.audio_queue.put(audio_chunk, timeout=1)
            except queue.Full:
                pass

    def update_spectrum(self, iq):
        if len(iq) < 256:
            return
        window = np.hanning(len(iq))
        iq_window = iq * window

        fft = np.fft.fft(iq_window)
        power = 20 * np.log10(np.abs(fft[:len(fft)//2]) + 1e-6)

        freq = np.linspace(0, 44100/2, len(power))
        self.spectrum_curve.setData(freq, power)
    
    def sounddevice_stream_af(self):
        with sd.OutputStream(
            samplerate=44100,
            channels=1,
            dtype='float32',
            blocksize=2048,
            callback = self.audio_stream
        ): 
            while self.running:
                time.sleep(0.1)


    def audio_stream(self, outdata, frames, status):
        if status:
            print(status, file=sys.stderr)
        while len(self.buffer) < frames:
            try:
                audio_chunk = self.audio_queue.get(timeout=0.01)
                self.buffer = np.concatenate((self.buffer, audio_chunk))

            except queue.Empty:
                break

        if len(self.buffer) >= frames:
            output_data = self.buffer[:frames] * self.volume
            self.buffer = self.buffer[frames:]
            outdata[:,0] = output_data
        else:
            outdata.fill(0)
            if len(self.buffer) > 0:
                print(f"Buffer underrun: have {len(self.buffer)}, need {frames}")
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())