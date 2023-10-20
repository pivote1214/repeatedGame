# %%
from operator import le
import tqdm
import pandas as pd
import automata

# 利得表のディレクトリのパス
path = "/Users/pivote1214/Library/CloudStorage/OneDrive-筑波大学/ドキュメント/repeatedGame"

# 対応表の読み込み
cr_table = pd.read_csv(f'{path}/cr_table.csv', index_col=0)
id_list = cr_table.index
# オートマトンの作成
automaton = automata.make_automaton()

N = len(automaton)
for id in tqdm.tqdm(id_list):
    # 利得表の読み込み
    payoff = pd.read_csv(f'{path}/payoff/payoff_{id}.csv', index_col=0)
    # ESS machineの判定
    ess_machines = []
    for i in tqdm.tqdm(range(N), leave=False):
        judge = True
        payoff_self = payoff.iloc[i, i]
        for j in range(N):
            if i == j:
                continue
            # ESS-(1)
            if payoff_self < payoff.iloc[j, i]:
                judge = False
                break
            elif payoff_self == payoff.iloc[j, i]:
                # ESS-(2)
                if payoff.iloc[i, j] < payoff.iloc[j, j]:
                    judge = False
                    break
                elif payoff.iloc[i, j] == payoff.iloc[j, j]:
                    # ESS-(3)
                    if len(automaton[i].states) > len(automaton[i].states):
                        judge = False
                        break
    
        if judge:
            ess_machines.append(i+1)
    
    # cr_tableに書き込み
    for num, ess_machine in enumerate(ess_machines):
        cr_table.loc[id, f'ESS_{num+1}'] = ess_machine

# cr_tableの書き込み
cr_table.to_csv(f'{path}/cr_table_ess.csv')
