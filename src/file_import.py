'''全楽譜のファイルのパスを取得するプログラム'''
import os
from constant import cons

path_list = []
file_list = os.listdir(cons.MUSUC_PATH)
# print(fileList)


def file_path():
    '''ファイルのパスを取得する関数'''
    for filename in file_list:
        path_score = cons.MUSUC_PATH + "/" + filename + "/score/"
        path_list.append(path_score)

    return path_list


# print(file_path())
