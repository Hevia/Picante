import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

# connects to microsoft wave synth
midiout.open_port(0)

note_on = [0x90, 0, 112] # channel 1, middle C, velocity 112
note_off = [0x80, 60, 0]
while True:
    midiout.send_message(note_on)
    time.sleep(1)
    midiout.send_message(note_off)
    note_on[1] = note_on[1] + 7
    if note_on[1] > 70:
        note_on[1] = note_on[1] - 40

del midiout
