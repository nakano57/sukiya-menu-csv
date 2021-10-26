import numpy as np
from dimod import ConstrainedQuadraticModel, Integer, Binary, quicksum
from dwave.system import LeapHybridCQMSampler
import dkey

# 必要情報（メニュー名・価格・カロリー）のインポート
name = np.loadtxt('menu.csv', delimiter=',', dtype='unicode', usecols=0)
p = np.loadtxt('menu.csv', delimiter=',', dtype='uint64', usecols=2)
c = np.loadtxt('menu.csv', delimiter=',', dtype='uint64', usecols=3)

# 定数設定
N_MENU = len(name)  # メニューの総数
P_MAX = 300  # 最大注文料金

model = ConstrainedQuadraticModel()
x = [Binary(f'x_{i}') for i in range(N_MENU)]

model.set_objective(-quicksum(c[i]*x[i]
                              for i in range(N_MENU)))

model.add_constraint(quicksum(p[i]*x[i]
                              for i in range(N_MENU)) <= P_MAX)

sampler = LeapHybridCQMSampler(endpoint=dkey.endpoint,
                               token=dkey.token)
sampleset = sampler.sample_cqm(model)
raw_solution = sampleset.first.sample

b = [raw_solution[f'x_{j}'] for j in range(N_MENU)]

# 価値、荷重、荷物の選択を表示
for i in range(N_MENU):
    if(b[i] == 1):
        print("%s %dyen %dcal." % (name[i], p[i], c[i]))

print()
print("合計: {}yen".format(np.dot(p, b)))
print("総カロリー: {}cal.".format(np.dot(c, b)))
