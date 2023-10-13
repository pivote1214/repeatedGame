# %%
import pandas as pd
import automata

# パラメータ設定
delta_list = [0.95, 0.99]
error_list = [i * 0.01 for i in range(1, 21)]

automaton = automata.make_automaton()
N = len(automaton)
for delta in delta_list:
    for error in error_list:
        # 利得表の読み込み
        payoff = pd.read_csv(f'result/payoff_list_delta={delta}_error={error}.csv', index_col=0)
        ess_machines = []
        for i in range(N):
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
        
        # result/ess_list.csvに書き込み
        # error,delta,ess_1,ess_2,ess_3,...
        with open('result/ess_list.csv', 'a') as f:
            f.write(f'{error},{delta}')
            for ess in ess_machines:
                f.write(f',{ess}')
            f.write('\n')
