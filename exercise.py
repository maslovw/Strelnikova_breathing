import pyaudio
import wave
import yaml
from time import time, sleep, strftime, gmtime, localtime
from pprint import pprint

class Sound():
    def __init__(self, sound1, sound2):
        self.load_waves(sound1, sound2)

    class Wave():
        def __init__(self, filename):
            self.wave = wave.open(filename, 'r')
            self.frame = self.wave.readframes(self.wave.getnframes())
            self.p = pyaudio.PyAudio()
            p = self.p

            wf = self.wave
            self.stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                  channels=wf.getnchannels(), rate=wf.getframerate (), output=True)
            frames = wf.getnframes()
            rate = wf.getframerate()
            self.duration = frames / float(rate)

        def play(self):
            self.stream.write(self.frame)


    def load_waves(self, sound1, sound2):
        self.cyclic = self.Wave(sound1)
        self.ending = self.Wave(sound2)

    def play_cyclic(self):
        self.cyclic.play()

    def play_ending(self):
        self.ending.play()

class SubExercise():
    def __init__(self, name, breaths, all, sound: Sound, timing):
        self.name = name
        self.breaths = breaths
        self.breaths_all = all
        self.count = 0
        self.sound = sound
        self.cyclic_time = timing['between_inhale']
        self.end_cycle_time = timing['between_cycles']
        self.end_time = timing['between_exercise']

    def cycle(self):
        self.count += 1
        print("\r{self.name}: {self.count}".format(**locals()), end='')

        if self.count >= self.breaths_all:
            self.sound.play_ending()
            self.sound.play_ending()
            return False

        if self.count % self.breaths != 0:
            self.sound.play_cyclic()
            sleep(self.cyclic_time)
        else:
            self.sound.play_ending()
            sleep(self.end_cycle_time)

        return True


class Exercise():
    def __init__(self):
        self.config = yaml.load(open('config.yml', 'r'))
        # pprint(self.config)
        sound1 = self.config['sound']['cyclic']
        sound2 = self.config['sound']['ending']
        self.sound = Sound(sound1, sound2)

    def run(self):
        time_start = time()
        exercises = self.config['exercises']
        breaths_def = 8
        breaths_all_def = 96
        for i, exercise in enumerate(exercises):
            name = exercise['name']
            breaths = exercise.get('cycle', breaths_def)
            breaths_all  = exercise.get('all', breaths_all_def)

            # changing default
            breaths_def = breaths
            breaths_all_def = breaths_all

            print("{:2d}: {}".format(i, name))
            e = SubExercise(name, breaths, breaths_all, self.sound, self.config['time'])
            if i > 0:
                sleep(self.config['time']['between_exercise'])
            while e.cycle():
                pass
            duration = time() - time_start
            print("\n", strftime("%H:%M:%S ", gmtime(duration)))

        print('The end')



if __name__ == '__main__':
    s = Exercise()
    s.run()