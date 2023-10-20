import pandas as pd
import time
import tqdm
from automata import make_automaton, make_k_mp, calculate_payoff

# オートマトンの記載例
# fa1 = FiniteAutomaton((1, 2), 1, {1: "C", 2: "D"}, 
#                       {(1, "g"): 1, (1, "b"): 2, (2, "g"): 2, (2, "b"): 2})
# fa2 = FiniteAutomaton((1, 2, 3), 1, {1: "C", 2: "D", 3: "D"}, 
#                       {(1, "g"): 1, (1, "b"): 2, (2, "g"): 2, (2, "b"): 3, (3, "g"): 2, (3, "b"): 1})

# マシン・パラメータの設定
automaton_list = make_automaton()
automaton_list += [make_k_mp(k) for k in range(3, 6)]
N = len(automaton_list)
delta_list = [round(i, 2) for i in [0.95, 0.99]]
gain_list = [round(i * 0.1, 3) for i in range(15, 16)]
loss_list = [round(i * 0.1, 3) for i in range(2, 31, 2)]
error_list = [round(i * 0.01, 2) for i in range(1, 21)]

# 結果の格納先の作成
path = "/Users/pivote1214/Library/CloudStorage/OneDrive-筑波大学/ドキュメント/repeatedGame/"
cr_table = pd.read_csv(path + "cr_table.csv", index_col=0)
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
                # payoffの読み込み
                payoff = pd.read_csv(path + f"payoff/payoff_{id}.csv", index_col=0)
                # indexとcolumnsのデータ型をintに変更
                payoff.index = payoff.index.astype(int)
                payoff.columns = payoff.columns.astype(int)
                
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
                
                for i in range(1054, 1057):
                    payoff_self = calculate_payoff(automaton_list[i], automaton_list[i], signals, delta, payoff_table)
                    payoff.at[i+1, i+1] = payoff_self[0]
                    for j in range(N):
                        payoff_1, payoff_2 = calculate_payoff(automaton_list[i], automaton_list[j], signals, delta, payoff_table)
                        payoff.at[i+1, j+1] = payoff_1
                        payoff.at[j+1, i+1] = payoff_2
                        
                payoff.to_csv(path + f"payoff/payoff_{id}.csv")
