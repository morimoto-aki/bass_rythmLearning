'''xml形式の楽譜をインポートするプログラム'''
import pickle
import csv
from music21 import converter, instrument, note, chord
import file_import

path_list = file_import.file_path()


class Note:
    """音符情報用のクラス"""
    measureNumber = 0
    pitch = 0
    offset = 0
    quarterLength = 0
    fullName = 0
    tie = 0
    notehead = 0

    def set(self, element):
        """音符情報setメソッド"""
        self.measureNumber = element.measureNumber
        self.pitch = element.pitch
        self.offset = element.offset
        self.quarterLength = element.quarterLength
        self.fullName = element.fullName
        if element.tie != None:
            self.tie = element.tie.type
        else:
            self.tie = element.tie
        self.notehead = element.notehead

    def get(self):
        """音符情報getメソッド"""
        noteinfo = [self.measureNumber, self.pitch, self.offset,
                    self.quarterLength, self.fullName, self.tie, self.notehead]
        return noteinfo


def get_notes():
    '''楽譜をcsvにする関数'''
    path = file_import.file_path()
    filepath = path[1]
    notes = []

    note_list = [["measure", "pitch", "offset", "quarterLength", "fullName", "tie", "notehead"]]

    for file in filepath:
        xml = converter.parse(file)
        print("Parsing %s" % file)
        notes_to_parse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(xml)
            notes_to_parse = s2.parts[0].recurse()
        except:  # file has notes in a flat structure
            notes_to_parse = xml.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                noteobj = Note()
                noteobj.set(element)
                noteinfo = noteobj.get()
                notes.append(noteinfo)
                note_list.append(noteinfo)
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('src/data/notesinfo.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list)


def main():
    '''main関数'''
    get_notes()


if __name__ == '__main__':
    main()
