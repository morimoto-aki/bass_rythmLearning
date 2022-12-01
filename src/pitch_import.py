'''xml形式の楽譜をインポートし調によってわけるプログラム'''
import pickle
import csv
from music21 import converter, instrument, note, chord, interval, pitch
import file_import


def get_notes():
    '''楽譜をcsvにする関数'''
    path = file_import.file_path()
    filepath = path[1]
    notes_major = []
    notes_minor = []
    note_list_major = []
    note_list_minor = []
    title_list = ["measure", "pitch", "root", "chord", "interval"]
    root = ""
    chord_name = ""
    quality = ""
    octave = 2

    # リストに項目名追加
    note_list_major.append(title_list)
    note_list_minor.append(title_list)

    for file in filepath:
        xml = converter.parse(file)
        print("Parsing %s" % file)
        notes_to_parse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(xml)
            notes_to_parse = s2.parts[0].recurse().notesAndRests
        except:  # file has notes in a flat structure
            notes_to_parse = xml.flat.notes

        for element in notes_to_parse:
            if isinstance(element, chord.Chord):
                root = element.pitchNames[0]
                chord_name = element.figure
                quality = element.quality

            if isinstance(element, note.Note) or isinstance(element, note.Rest):
                if quality == "major":
                    p1 = pitch.Pitch(root + str(octave))
                    if element.tie is not None:
                        tie = element.tie.type
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        if tie == "start":
                            tie_quarter_length = str(element.quarterLength)
                            offset = element.offset
                        elif tie == "stop":
                            noteinfo = [str(element.measureNumber), str(
                                element.pitch), root, chord_name, interval_name]
                            notes_major.append(noteinfo)
                            note_list_major.append(noteinfo)

                    elif element.isRest:
                        noteinfo = [str(element.measureNumber), "Rest", root, chord_name, "Rest"]
                        notes_major.append(noteinfo)
                        note_list_major.append(noteinfo)

                    elif element.notehead is "x":
                        noteinfo = [str(element.measureNumber), "x", root, chord_name, "x"]
                        notes_major.append(noteinfo)
                        note_list_major.append(noteinfo)

                    else:
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        noteinfo = [str(element.measureNumber), str(
                            element.pitch), root, chord_name, interval_name]
                        notes_major.append(noteinfo)
                        note_list_major.append(noteinfo)

                elif quality == "minor":
                    p1 = pitch.Pitch(root + str(octave))
                    if element.tie is not None:
                        tie = element.tie.type
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        if tie == "start":
                            tie_quarter_length = str(element.quarterLength)
                            offset = element.offset
                        elif tie == "stop":
                            noteinfo = [str(element.measureNumber), str(
                                element.pitch), root, chord_name, interval_name]
                            notes_minor.append(noteinfo)
                            note_list_minor.append(noteinfo)

                    elif element.isRest:
                        noteinfo = [str(element.measureNumber), "Rest", root, chord_name, "Rest"]
                        notes_minor.append(noteinfo)
                        note_list_minor.append(noteinfo)

                    elif element.notehead is "x":
                        noteinfo = [str(element.measureNumber), "x", root, chord_name, "x"]
                        notes_minor.append(noteinfo)
                        note_list_minor.append(noteinfo)

                    else:
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        noteinfo = [str(element.measureNumber), str(
                            element.pitch), root, chord_name, interval_name]
                        notes_minor.append(noteinfo)
                        note_list_minor.append(noteinfo)

    with open('src/data/notesinfo_major.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list_major)

    with open('src/data/notesinfo_minor.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list_minor)

    with open('src/data/notesinfo_major', 'wb') as filepath:
        pickle.dump(notes_major, filepath)

    with open('src/data/notesinfo_minor', 'wb') as filepath:
        pickle.dump(notes_minor, filepath)


def main():
    '''main関数'''
    get_notes()


if __name__ == '__main__':
    main()
