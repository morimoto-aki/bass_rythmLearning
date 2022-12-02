'''隠れマルコフモデルに基づき学習するプログラム'''
import pickle
import hmmlearn
from hmmlearn import hmm
import numpy as np


def file_open():
    '''楽譜データをインポートする関数'''
    with open('src/data/notesinfo', 'rb') as p:
        return pickle.load(p)


def value_hmm():
    '''音価学習用の関数'''
    # 音符情報
    notes_info = file_open()
    # 音価情報array
    aquarter_length = np.array(notes_info)
    # すべての音価位置情報リスト
    lquarter_length_offset = []
    # すべての音価情報リスト
    lquarter_length_all = []
    # すべてのoffset情報リスト
    loffset_all = []
    # 音価情報リスト
    lquarter_length = []
    # 小節内の音価情報リスト
    lquarter_length_measure = []
    # 初期小節No
    measure = "1"
    # 初期状態確率リスト
    startprob_list = []
    # 出現確率リスト
    emmisionprob_list = []
    # 遷移確率リスト
    transmat_list = []
    # 潜在状態辞書
    states = {}
    # 観測値辞書
    observe_states = {}

    # データの精査
    # 小節ごとに分けたリストの生成
    for i, note in enumerate(aquarter_length):
        if measure == aquarter_length[i, 0]:
            lquarter_length_measure.append([aquarter_length[i, 3], aquarter_length[i, 4]])
            # print(aquarter_length[i, 1])

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

    # 音価情報辞書
    dquarter_length = {key: lquarter_length.count(key) for key in lquarter_length_all}
    # offset情報辞書
    doffset = {key: lquarter_length.count(key) for key in loffset_all}

    # 初期状態を求める
    for i, note_value_length in enumerate(lquarter_length):
        dquarter_length[note_value_length[0][1]] += 1

    for val in dquarter_length.values():
        startprob_list.append(val/sum(dquarter_length.values()))

    # 潜在状態を求める
    for i, length in enumerate(dquarter_length):
        states[length] = i
    inv_dict_states = {str(v): k for k, v in states.items()}

    # 観測値を求める
    for i, offset in enumerate(doffset):
        observe_states[offset] = i

    # 初期状態確率
    startprob = np.array(startprob_list)

    # 出現確立を求める
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

    # 遷移確率を求める
    for length in states:
        dic = dict.fromkeys(states, 0)
        indexes = [i for i, x in enumerate(lquarter_length_all) if x == length]
        lis = []
        prob_list = []
        for index in indexes:
            if lquarter_length_all[index] is not lquarter_length_all[-1]:
                next_length = lquarter_length_all[index + 1]
                lis.append(next_length)

        for offset in lis:
            dic[offset] += 1

        for val in dic.values():
            prob_list.append(val/sum(dic.values()))

        transmat_list.append(prob_list)
    transmat = np.array(transmat_list)

    # hmmlearn のインスタンス作成
    model = hmm.MultinomialHMM(n_components=len(states), init_params='', params='')
    model.n_features = len(observe_states)
    model.startprob_ = startprob
    model.transmat_ = transmat
    model.emissionprob_ = emmisionprob

    observes = ["1.75"]
    n_samples = 1
    observe_codes = np.array([observe_states[o] for o in observes]).reshape((len(observes), n_samples))
    # print(type(observe_codes[0][0]))

    # サンプル信号を 10 個出力する。
    # X, Z = model.sample(n_samples=10, currstate=observe_codes)
    # print(X)
    # print(Z)
    # print("--------------------------")
    # for i, o in enumerate(X):
    #    keys = [key for key, value in observe_states.items() if value == o[0]]
    #    print(i, ":", keys)
    # print("--------------------------")
    # for i, o in enumerate(Z):
    #    keys = [key for key, value in states.items() if value == o]
    #    print(i, ":", keys)

    # model.predict(observe_codes)
    print("--------------------------")
    # 推定
    logprob, decoded_codes = model.decode(observe_codes)
    decoded = [inv_dict_states[str(d)] for d in decoded_codes]
    print(decoded)
    print(f'{np.exp(logprob)=}')


def pitch_hmm():
    '''音高学習用の関数'''
    # 音符情報
    notes_info = file_open()
    # 音符情報array
    notes_info_array = np.array(notes_info)
    # すべての度数no情報リスト
    lpitch_no = []
    # 初期小節No
    measure = "1"
    # 小節内No
    no_measure = 0
    # 音高情報リスト
    lpitch = []
    # 小節内の音高情報リスト
    lpitch_measure = []
    # すべての音高情報リスト
    lpitch_all = []
    # 小節内Noリスト
    lno_measure = []
    # 初期状態確率リスト
    startprob_list = []
    # 出現確率リスト
    emmisionprob_list = []
    # 遷移確率リスト
    transmat_list = []
    # 潜在状態辞書
    states = {}
    # 観測値辞書
    observe_states = {}

    # 小節ごとに分けたリストの生成
    for i, note in enumerate(notes_info_array):
        if measure == notes_info_array[i, 0]:
            no_measure += 1
            lpitch_measure.append([no_measure, notes_info_array[i, 9]])
            lno_measure.append(no_measure)

        else:
            lpitch.append(lpitch_measure)
            lpitch_measure = []
            measure = notes_info_array[i, 0]
            no_measure = 1
            lpitch_measure.append([no_measure, notes_info_array[i, 9]])
            lno_measure.append(no_measure)

        # 度数がまだ要素にないとき
        if note[9] not in lpitch_no:
            lpitch_no.append(note[9])
            lpitch_no.append([no_measure])

        # 度数がすでに要素にあるとき
        else:
            lpitch_no[lpitch_no.index(note[9]) + 1].append(no_measure)

        lpitch_all.append(note[9])

    # 音符情報辞書
    dpitch = {key: lpitch.count(key) for key in lpitch_all}
    # no情報辞書
    dno = {key: lpitch.count(key) for key in lno_measure}

    # 初期状態を求める
    for i, note_pitch in enumerate(lpitch):
        dpitch[note_pitch[0][1]] += 1

    for val in dpitch.values():
        startprob_list.append(val/sum(dpitch.values()))

    # 潜在状態を求める
    for i, pitch in enumerate(dpitch):
        states[pitch] = i
    inv_dict_states = {str(v): k for k, v in states.items()}

    # 観測値を求める
    for i, no in enumerate(dno):
        observe_states[no] = i

    # 初期状態確率
    startprob = np.array(startprob_list)

    # 出現確立を求める
    for pitch in states:
        dic = dict.fromkeys(observe_states, 0)
        lis = lpitch_no[lpitch_no.index(pitch) + 1]
        prob_list = []
        for offset in lis:
            dic[offset] += 1

        for val in dic.values():
            prob_list.append(val/sum(dic.values()))

        emmisionprob_list.append(prob_list)
    emmisionprob = np.array(emmisionprob_list)

    # 遷移確率を求める
    for length in states:
        dic = dict.fromkeys(states, 0)
        indexes = [i for i, x in enumerate(lpitch_all) if x == length]
        lis = []
        prob_list = []
        for index in indexes:
            if lpitch_all[index] is not lpitch_all[-1]:
                next_length = lpitch_all[index + 1]
                lis.append(next_length)

        for offset in lis:
            dic[offset] += 1

        for val in dic.values():
            prob_list.append(val/sum(dic.values()))

        transmat_list.append(prob_list)
    transmat = np.array(transmat_list)

    # hmmlearn のインスタンス作成
    model = hmm.MultinomialHMM(n_components=len(states), init_params='', params='')
    model.n_features = len(observe_states)
    model.startprob_ = startprob
    model.transmat_ = transmat
    model.emissionprob_ = emmisionprob
    observes = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7]
    n_samples = 1
    observe_codes = np.array([observe_states[o] for o in observes]).reshape((len(observes), n_samples))

    # 推定
    logprob, decoded_codes = model.decode(observe_codes)
    decoded = [inv_dict_states[str(d)] for d in decoded_codes]
    print(decoded)
    print(f'{np.exp(logprob)=}')


def main():
    '''main関数'''
    value_hmm()
    print("--------------------------")
    # pitch_hmm()


if __name__ == '__main__':
    main()
