import os

Path_score = []

path = "./music"
fileList = os.listdir(path)
# print(fileList)


def filePath():
    for filename in fileList:
        pathScore = path + "/" + filename + "/score/"

        Path_score.append(pathScore)

    return(Path_score)
