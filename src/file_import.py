'''全楽譜のファイルのパスを取得するプログラム'''
import glob


def file_path():
    '''ファイルのパスを取得する関数'''

    midipath_list = glob.glob("music/midi/*.mid")
    xmlpath_list = glob.glob("music/xml/*.xml")

    return midipath_list, xmlpath_list


# print(file_path())
