import numpy as np
from dimod import ConstrainedQuadraticModel, Integer, Binary, quicksum
from dwave.system import LeapHybridCQMSampler
import dkey

filename = 'menu.csv'

# 必要情報（メニュー名・価格・カロリー）のインポート
name = np.loadtxt(filename, delimiter=',', dtype='unicode', usecols=0)
price = np.loadtxt(filename, delimiter=',', dtype='uint64', usecols=2)
cal = np.loadtxt(filename, delimiter=',', dtype='uint64', usecols=3)
protein = np.loadtxt(filename, delimiter=',', dtype='float', usecols=4)
fat = np.loadtxt(filename, delimiter=',', dtype='float', usecols=5)
carbohydrate = np.loadtxt(filename, delimiter=',', dtype='float', usecols=6)
sodium = np.loadtxt(filename, delimiter=',', dtype='float', usecols=7)

# 定数設定
N_MENU = len(name)  # メニューの総数
P_MAX = 1000  # 最大注文料金

######################## PHASE 1 ########################
# モデルの記述・実行

# 問題（モデル）を設定
model = ConstrainedQuadraticModel()

# 変数を設定
x = [Binary(f'x_{i}') for i in range(N_MENU)]

# 目的関数を設定
model.set_objective(-quicksum(cal[i]*x[i]
                              for i in range(N_MENU)))

# 制約を追加
model.add_constraint(quicksum(price[i]*x[i]
                              for i in range(N_MENU)) <= P_MAX)

# モデルの実行
sampler = LeapHybridCQMSampler(endpoint=dkey.endpoint,
                               token=dkey.token)
sampleset = sampler.sample_cqm(model)
raw_solution = sampleset.first.sample

######################## PHASE 2 ########################
# 結果の表示

b = [raw_solution[f'x_{j}'] for j in range(N_MENU)]

# 価値、荷重、荷物の選択を表示
for i in range(N_MENU):
    if(b[i] == 1):
        print("%s %dyen %dcal." % (name[i], price[i], cal[i]))
print()
print("合計: {}yen".format(np.dot(price, b)))
print("総カロリー: {}cal.".format(np.dot(cal, b)))
print("総タンパク質: {}g.".format(np.dot(protein, b)))
print("総脂質: {}g.".format(np.dot(fat, b)))
print("総炭水化物: {}g.".format(np.dot(carbohydrate, b)))
print("総塩分: {}g.".format(np.dot(sodium, b)))
print("計算時間: %f sec." % model.Runtime)
