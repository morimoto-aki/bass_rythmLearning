'''xml形式の楽譜をインポートするプログラム'''
import pickle
import csv
from music21 import converter, instrument, note, chord
import file_import


def get_notes():
    '''楽譜をcsvにする関数'''
    path = file_import.file_path()
    filepath = path[1]
    notes = []
    note_list = [["measure", "pitch", "offset", "offsetMeasure",
                  "quarterLength", "fullName", "notehead"]]
    measure_no = 0
    offset_measure = 0
    tie_quarter_length = 0

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
            if isinstance(element, note.Note) or isinstance(element, note.Rest):
                if element.measureNumber is not measure_no:
                    measure_no = element.measureNumber
                    offset_measure = element.offset

                if element.tie is not None:
                    tie = element.tie.type
                    if tie == "start":
                        tie_quarter_length = str(element.quarterLength)
                        offset = element.offset
                    elif tie == "stop":
                        noteinfo = [str(element.measureNumber), str(element.pitch), str(offset), str(offset - offset_measure),
                                    tie_quarter_length + "+" + str(element.quarterLength), str(element.fullName), str(element.notehead)]
                        notes.append(noteinfo)
                        note_list.append(noteinfo)

                elif element.isRest:
                    noteinfo = [str(element.measureNumber), "Rest", str(element.offset), str(element.offset - offset_measure),
                                str(element.quarterLength), str(element.fullName), ""]
                    notes.append(noteinfo)
                    note_list.append(noteinfo)

                else:
                    noteinfo = [str(element.measureNumber), str(element.pitch), str(element.offset), str(element.offset - offset_measure),
                                str(element.quarterLength), str(element.fullName), str(element.notehead)]
                    notes.append(noteinfo)
                    note_list.append(noteinfo)

            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

            elif isinstance(element, note.Rest):
                print("rest")

    with open('src/data/notesinfo.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list)

    with open('src/data/notesinfo', 'wb') as filepath:
        pickle.dump(notes, filepath)


def main():
    '''main関数'''
    get_notes()


if __name__ == '__main__':
    main()
