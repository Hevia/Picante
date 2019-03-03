import time
import rtmidi
import numpy as np
import random
import asyncio
from typing import Callable, Any, List

# File for input
f = open('output.txt', 'r')

# Setting up Music Theory
key_roots = {
    "C": 48,
    "Db": 49,
    "D": 50,
    "Eb": 51,
    "E": 52,
    "F": 53,
    "Gb": 54,
    "G": 55,
    "Ab": 56,
    "A": 57,
    "Bb": 58,
    "B": 59
}

major_pentatonic = [0, 2, 4, 7, 9, 12, 0]
minor_blues = [0, 3, 5, 6, 7, 10, 12]
major_scale = [0, 2, 4, 5, 7, 9, 11]
minor_scale = [0, 2, 3, 5, 7, 8, 10]
scales = np.array([major_pentatonic, major_scale, minor_scale])

# chords in terms of intervals
minor_7 = [0, 7, 10, 15]
major_7 = [0, 7, 11, 16]
dom_7 = [4, 10, 12, 19]
dim_7 = [2, 9, 11, 17]

# what chords correspond to scales I to VII
major_chords = np.array([major_7, minor_7, minor_7, major_7, dom_7, minor_7, dim_7])

# Set up priority of chords
chord_priority = [0, 3, 4, 1, 5, 2, 6]

# Set tempo
tempo = 120
subdivs = 16
num_inst = 5
midiout = rtmidi.MidiOut()
# print(midiout.get_ports())

# Port 2 on Windows | Port 1 on Linux
midiout.open_port(1)

subdivisions = subdivs / 4
counter = 0

# Create Note Map that dictates what will play
note_map = np.zeros((subdivs, num_inst))

# Set REST TIME between subdivisions
bpm = sleep_time = 60 / (tempo * subdivisions)
offset = 0

for i in range(0, subdivs, 2):
    note_map[i, 2] = 1
for i in range(4, subdivs, 8):
    note_map[i, 1] = 1
for i in range(0, subdivs, 4):
    note_map[i, 0] = 1

note_map[0, 3] = 1
note_map[8, 3] = 1

for i in range(0, subdivs, 1):
    note_map[i, 4] = 1

key = key_roots["Ab"]
scale = 0
key_notes = key + scales[scale]
playing_chord = -1
playing_note = -1
melody_note = 0
chord_root = 0
octave = 0
intensity = 0


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def send_note_one(note):
    midiout.send_message([0x90, note, 112])
    midiout.send_message([0x80, note, 0])


def send_note_two(on, note):
    if on:
        midiout.send_message([0x91, note, 112])
    else:
        midiout.send_message([0x81, note, 0])


def play_chord_two(on, chord):
    if on:
        global playing_chord
        if playing_chord != -1:
            for n in major_chords[playing_chord]:
                send_note_two(False, key_notes[playing_chord] + n)
        playing_chord = chord
    else:
        playing_chord = -1
    for n in major_chords[chord]:
        send_note_two(on, key_notes[chord] + n)


def play_note_three(on, note):
    global playing_note
    if on:
        if playing_note != -1:
            midiout.send_message([0x82, playing_note, 0])
        playing_note = note + octave * 12
        midiout.send_message([0x92, note + octave * 12, 112])
    else:
        midiout.send_message(([0x82, note + octave * 12, 0]))
        playing_note = -1


def update_note_map():
    # updating notes
    # Gonna be super fucking complicated
    melody_note_change = random.randint(-4, 4)
    intensity_change = random.randint(-1, 1)
    global melody_note
    melody_note = (melody_note + melody_note_change) % 7
    note_on = random.randint(0, 1)
    length_note = random.randint(2, 8)
    global intensity
    intensity = clamp(intensity + intensity_change, 0, 15)
    global octave
    global chord_root
    global chord_priority
    if intensity < 5:
        octave = 1
        chord_root = chord_priority[random.randint(0, 2)]
    elif intensity < 10:
        octave = 2
        chord_root = chord_priority[random.randint(0, 4)]
    else:
        octave = 3
        chord_root = chord_priority[random.randint(0, 6)]

def get_data(bytes_to_read=0):
	if bytes_to_read == 0:
		return f.read()
	else:
		return f.read(bytes_to_read)

for i in range(64):
    sleep_time = max([0, (bpm - offset)])
    time.sleep(sleep_time)

    # start timer
    t0 = time.time()

    # if counter % subdivisions == 0:
    update_note_map()

    if counter >= subdivs:
        counter = 0

    # Kick Drum
    if note_map[counter, 0] == 1:
        send_note_one(36)

    # Snare Druem
    if note_map[counter, 1] == 1:
        send_note_one(40)

    # Hi Hats
    if note_map[counter, 2] == 1:
        send_note_one(42)

    # Chords
    if note_map[counter, 3] == 1:
        play_chord_two(True, chord_root)
    elif note_map[counter, 3] == -1:
        play_chord_two(False, chord_root)

    # Lead Melody
    if note_map[counter, 4] == 1:
        play_note_three(True, key_notes[melody_note])
    elif note_map[counter, 4] == -1:
        play_note_three(False, key_notes[melody_note])

    t1 = time.time()

    offset = t1 - t0
    counter = counter + 1

if playing_note != -1:
    midiout.send_message([0x82, key + playing_note, 0])
midiout.close_port()
