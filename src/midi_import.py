import pickle
import glob
from music21 import converter, instrument, note, chord
import file_import


def get_notes():
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    path = file_import.file_path()
    filepath = path[1] + "score.mid"
    notes = []

    for file in glob.glob(filepath):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
        except:  # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('src/data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes


get_notes()
