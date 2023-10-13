# %%
import os
import pandas as pd

# dir_path内のファイルの名前を変更
dir_path = './result/payoff/'
file_list = os.listdir(dir_path)

# cr_tableを読み込む
# TODO: パラメータの桁数設定・idの微調整
cr_table = pd.read_csv("result/cr_table.csv")
# idの変更
for ind in cr_table.index:
    delta, gain, loss, error = cr_table.loc[ind, "id"].split("_")
    id = f"delta={delta[:3]}_gain={gain[:3]}_loss={loss[:3]}_error={error[:3]}"
    cr_table.loc[ind, "id"] = id

# payoffファイルの名前を変更
for file_name in file_list:
    if file_name[:6] == 'payoff':
        continue
    delta, gain, loss, error = file_name.split("_")
    id = f"delta={delta[:3]}_gain={gain[:3]}_loss={loss[:3]}_error={error[:3]}"
    new_file_name = 'payoff_' + id
    os.rename(dir_path + file_name, dir_path + new_file_name + '.csv')

# cr_tableを保存
cr_table.to_csv("result/new_cr_table.csv", index=False)

# %%
