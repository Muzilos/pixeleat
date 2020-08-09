import sounddevice as sd
from scipy.io.wavfile import write
from numpy import array

class Sound:

    def __init__(self):
        self.fs = 44100  # Sample rate
        self.sound_array = [(1,1)]
        self.sound_index = 0
        self.stream = sd.InputStream(samplerate=self.fs)

    def record(self, seconds):
        self.sound_array = sd.rec(int(seconds * self.fs), samplerate=self.fs, channels=2)
        return self.sound_array

    def update_stream(self):
        available = self.stream.read_available
        self.sound_array = self.stream.read(available)
        # if self.sound_array[0].any():
        #     print(self.sound_array[:10])
        #     print()
        return self.sound_array

    def open_stream(self):
        self.stream.start()

    def write(self, filepath):
        write(filepath, self.fs, self.sound_array)  # Save as WAV file 

    def play(self):
        sd.play(self.sound_array)

    def play_current_bit(self):
        sd.play(self.sound_array[self.sound_index])

    def get_next(self, delay_ms=1):
        if self.sound_index < len(self.sound_array):
            delay = 1 / delay_ms
            next_item = self.sound_array[self.sound_index]
            self.sound_index += int(delay)
            print(next_item)
            return next_item, True
        else:
            return array([]), False
