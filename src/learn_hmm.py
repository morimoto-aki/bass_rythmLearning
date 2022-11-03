'''隠れマルコフモデルに基づき学習するプログラム'''
import pickle
import numpy as np


def file_open():
    '''楽譜データをインポートする関数'''
    with open('src/data/notesinfo', 'rb') as p:
        return pickle.load(p)


def main():
    '''main関数'''
    note_value()


def note_value():
    '''音価学習用の関数'''
    notes_info = file_open()  # 音符情報
    lquarter_length_offset = []  # すべての音価位置情報リスト
    lquarter_length_all = []  # すべての音価情報リスト
    loffset_all = []  # すべてのoffset情報リスト
    aquarter_length = np.array(notes_info)  # 音価情報array
    lquarter_length = []  # 音価情報リスト
    lquarter_length_measure = []  # 小節内の音価情報リスト
    measure = "1"
    startprob_list = []  # 初期状態確率リスト
    emmisionprob_list = []  # 出現確率リスト
    states = {}  # 潜在状態辞書
    observe_states = {}  # 観測値辞書

    # データの精査
    # 小節ごとに分けたリストの生成
    for i, note in enumerate(aquarter_length):
        if measure == aquarter_length[i, 0]:
            lquarter_length_measure.append([aquarter_length[i, 3], aquarter_length[i, 4]])
            #print(aquarter_length[i, 1])

        else:
            lquarter_length.append(lquarter_length_measure)
            lquarter_length_measure = []
            measure = aquarter_length[i, 0]
            lquarter_length_measure.append([aquarter_length[i, 3], aquarter_length[i, 4]])

        lquarter_length_all.append(note[4])
        loffset_all.append(note[3])

        # 音価がまだ要素にないとき
        if note[4] not in lquarter_length_offset:
            lquarter_length_offset.append(note[4])
            lquarter_length_offset.append([note[3]])

        # 音価がすでに要素にあるとき
        else:
            lquarter_length_offset[lquarter_length_offset.index(note[4]) + 1].append(note[3])

    dquarter_length = {key: lquarter_length.count(key) for key in lquarter_length_all}  # 音価情報辞書
    doffset = {key: lquarter_length.count(key) for key in loffset_all}  # offset情報辞書

    # 初期状態を求める
    for i, note_value_length in enumerate(lquarter_length):
        dquarter_length[note_value_length[0][1]] += 1

    for val in dquarter_length.values():
        startprob_list.append(val/sum(dquarter_length.values()))

    # 潜在状態を求める
    for i, length in enumerate(dquarter_length):
        states[length] = i

    # 観測値を求める
    for i, offset in enumerate(doffset):
        observe_states[offset] = i

    # 初期状態確率
    #'1.75', '0.25+0.5', '0.5', '0.25+0.25', '0.25', '0.5+0.75', '0.75', '2.0', '3.0', '1.5+0.75'
    # , '1.0+0.75', '0.25+0.75', '2.0+0.75', '1.5', '0.5+0.25', '2.0+0.5', '1.0', '0.25+1.0', '1.5+0.5'
    startprob = np.array(startprob_list)

    # 出現確立を求める
    #'1.75', '0.25+0.5', '0.5', '0.25+0.25', '0.25', '0.5+0.75', '0.75', '2.0', '3.0', '1.5+0.75'
    # , '1.0+0.75', '0.25+0.75', '2.0+0.75', '1.5', '0.5+0.25', '2.0+0.5', '1.0', '0.25+1.0', '1.5+0.5'
    #'0.0', '2.0', '2.5', '3.0', '3.5', '2.25', '2.75', '1.0', '1.75', '0.75', '3.25', '0.25', '0.5', '1.25', '1.5', '3.75'
    for length in states:
        dic = dict.fromkeys(observe_states, 0)
        lis = lquarter_length_offset[lquarter_length_offset.index(length) + 1]
        prob_list = []
        for offset in lis:
            dic[offset] += 1

        for val in dic.values():
            prob_list.append(val/sum(dic.values()))

        emmisionprob_list.append(prob_list)

    emmisionprob = np.array(emmisionprob_list)

    print(emmisionprob)


if __name__ == '__main__':
    main()
