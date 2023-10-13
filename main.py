import pandas as pd
import time
import tqdm
import automata

# オートマトンの記載例
# fa1 = FiniteAutomaton((1, 2), 1, {1: "C", 2: "D"}, 
#                       {(1, "g"): 1, (1, "b"): 2, (2, "g"): 2, (2, "b"): 2})
# fa2 = FiniteAutomaton((1, 2, 3), 1, {1: "C", 2: "D", 3: "D"}, 
#                       {(1, "g"): 1, (1, "b"): 2, (2, "g"): 2, (2, "b"): 3, (3, "g"): 2, (3, "b"): 1})

# マシン・パラメータの設定
automaton_list = automata.make_automaton()
N = len(automaton_list)
delta_list = [round(i, 2) for i in [0.90, 0.95, 0.99]]
gain_list = [round(i * 0.1, 3) for i in range(15, 16)]
loss_list = [round(i * 0.2, 3) for i in range(1, 16)]
error_list = [round(i * 0.01, 2) for i in range(1, 21)]

# TODO: 計算済みのパラメータをスキップする処理を追加
cr_table = pd.read_csv("result/cr_table.csv", index_col=0)
id_set = set(cr_table.index)

# 利得計算
for delta in tqdm.tqdm(delta_list):
    for gain in tqdm.tqdm(gain_list, leave=False):
        for loss in tqdm.tqdm(loss_list, leave=False):
            payoff_table = {("C", "C"): 1, ("C", "D"): -loss,
                            ("D", "C"): 1 + gain, ("D", "D"): 0}
            for error in tqdm.tqdm(error_list, leave=False):
                # idの設定
                id = f"delta={delta}_gain={gain}_loss={loss}_error={error}"
                if id in id_set:
                    continue
                # エラー率の設定
                p, q, r, s = (1-error) ** 2, error * (1-error), error * (1-error), error ** 2
                t, u, v, w = error * (1-error), error ** 2, (1-error) ** 2, error * (1-error)
                signals = {(("C", "C"), ("g", "g")): p, (("C", "C"), ("g", "b")): q, 
                           (("C", "C"), ("b", "g")): r, (("C", "C"), ("b", "b")): s, 
                           (("C", "D"), ("g", "g")): t, (("C", "D"), ("g", "b")): u, 
                           (("C", "D"), ("b", "g")): v, (("C", "D"), ("b", "b")): w, 
                           (("D", "C"), ("g", "g")): w, (("D", "C"), ("g", "b")): v, 
                           (("D", "C"), ("b", "g")): u, (("D", "C"), ("b", "b")): t, 
                           (("D", "D"), ("g", "g")): s, (("D", "D"), ("g", "b")): r, 
                           (("D", "D"), ("b", "g")): q, (("D", "D"), ("b", "b")): p}
                
                payoff_list = [[None] * N for _ in range(N)]

                start_time = time.time()
                for i in tqdm.tqdm(range(N), leave=False):
                    for j in range(N):
                        payoff_1, _ = automata.calculate_payoff(automaton_list[i], automaton_list[j], signals, delta, payoff_table)
                        payoff_list[i][j] = payoff_1

                end_time = time.time()

                # 1行目に[1, 2, 3, ..., N]を追加
                payoff_list.insert(0, [i for i in range(1, N+1)])
                payoff_list[0].insert(0, None)
                # 1列目に[1, 2, 3, ..., N]を追加
                for i in range(1, N+1):
                    payoff_list[i].insert(0, i)
                # TODO: IDの変更・小数点管理
                # cr_table.csvに書き込み
                with open("result/cr_table.csv", "a") as f:
                    f.write(','.join([str(i) for i in [id, delta, gain, loss, error, round(end_time - start_time, 3)]]) + "\n")

                # csvファイルに書き込み
                with open(f"result/payoff/payoff_{id}.csv", "w") as f:
                    for row in payoff_list:
                        f.write(",".join([str(i) for i in row]) + "\n")
