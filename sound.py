import sounddevice as sd
from scipy.io.wavfile import write
from numpy import array
import struct

class Sound:

    def __init__(self):
        self.fs = 44100  # Sample rate
        self.sound_array = [(1,1)]
        self.raw_sound_array = [1,1,1,0]
        self.sound_index = 0
        self.stream = sd.InputStream(samplerate=self.fs)
        self.raw_stream = sd.RawInputStream(samplerate=self.fs, blocksize=self.fs)

    def record(self, seconds):
        self.sound_array = sd.rec(int(seconds * self.fs), samplerate=self.fs, channels=2)
        return self.sound_array

    def update_stream(self):
        available = self.stream.read_available
        self.sound_array = self.stream.read(available)
        return self.sound_array

    def update_raw_stream(self):
        available = self.raw_stream.read_available
        raw_sound = self.raw_stream.read(available)
        sound_bytes = raw_sound[0][:]
        chunk = str(len(sound_bytes)) + 'B'
        if sound_bytes:
            self.raw_sound_array = struct.unpack(chunk, sound_bytes)[::3]
        return self.raw_sound_array

    def open_stream(self):
        self.stream.start()

    def open_raw_stream(self):
        self.raw_stream.start()

    def write(self, filepath):
        write(filepath, self.fs, self.sound_array)  # Save as WAV file 

    def play(self):
        sd.play(self.sound_array)

    def get_next(self, delay_ms=1):
        if self.sound_index < len(self.sound_array):
            delay = 1 / delay_ms
            next_item = self.sound_array[self.sound_index]
            self.sound_index += int(delay)
            return next_item, True
        else:
            return array([]), False
