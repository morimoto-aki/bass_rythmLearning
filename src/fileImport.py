import os

Path_score = []

path = "./music"
fileList = os.listdir(path)
# print(fileList)


def filePath():
    for filename in fileList:
        pathBass = path + "/" + filename + "/bass/"
        pathScore = path + "/" + filename + "/score/"
        pathOutput = path + "/" + filename + "/output/"

        Path_score.append(pathScore)

    return(Path_score)
