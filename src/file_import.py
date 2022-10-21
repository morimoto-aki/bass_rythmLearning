'''全楽譜のファイルのパスを取得するプログラム'''
import os

path_list = []
PATH = "./music"
file_list = os.listdir(PATH)
# print(fileList)


def file_path():
    '''ファイルのパスを取得する関数'''
    for filename in file_list:
        path_score = PATH + "/" + filename + "/score/"
        path_list.append(path_score)

    return path_list


# print(file_path())
