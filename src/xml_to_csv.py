'''xml形式の楽譜をcsvにするプログラム'''
import csv  # pylint: disable=unused-import
import pandas as pd  # pylint: disable=unused-import
from music21 import converter  # pylint: disable=unused-import
import file_import  # pylint: disable=unused-import

path_list = file_import.file_path()


def mxltransfer(path):
    '''楽譜をcsvにする関数'''
    scorepath = path + "score.xml"
    score = converter.parse(scorepath)

    NoteList = [["Note", "seconds", "offset", "duration", "measure", "Tie", "Ghost", "NoteValue"]]

    for el in score.recurse().notesAndRests:
        if(not el.isRest):
            Note = [el.name, el1, el.offset, el.duration, el.measureNumber,
                    el.tie, el.notehead is "x", el.quarterLength]
        if not el.isRest and el.notehead is not "x":
            if tie_Flag:
                NoteList.append(Note)
                if el.tie is not None:
                    tie_Flag = False

            else:
                if el.tie is None:
                    NoteList.append(Note)
                if el.tie is not None:
                    tie_Flag = True
        el1 = el.seconds + el1
    # print(s.metadata.title)
    title = score.metadata.title
    with open(path + "score.csv", 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(NoteList)


def main():
    '''main関数'''
    for path in path_list:
        mxltransfer(path)


if __name__ == '__main__':
    main()
