import numpy as np
import copy
import matplotlib.pyplot as plt


def normSquare(_x):  # _x의 norm 의 제곱을 구함.
    _s = 0
    for _i in _x:
        _s += _i ** 2
    return _s


def variance(_mu, _s):  # 분산을 구함.
    V = 0
    for _i in range(len(_mu)):
        for cor in _s[_i]:
            V += normSquare(np.array(cor) - np.array(_mu[_i]))
    return V
    pass  # V is float


def get_reset_s(s, _mu, coord):  # 업데이트 된 새로운 집합 S를 반환함.
    new_s = []
    for _ in range(len(s)):
        new_s.append([])
    for _i in coord:
        _j = 0
        min_mu = -1
        for _d in range(len(_mu)):
            dis_mu = normSquare(np.array(_i) - np.array(_mu[_d]))
            if min_mu > dis_mu or min_mu == -1:
                _j = _d
                min_mu = dis_mu
        new_s[_j].append(_i)
    return new_s
    pass


def update_mu(_mu, _s):
    before_mu = copy.deepcopy(_mu)
    k = 0
    print(_s)
    for s_i in _s:
        su = np.array((0.0, 0.0))
        for _i in s_i:
            su += np.array(_i) / len(s_i)
        # _mu[k] = copy.deepcopy(su)
        for _m in range(len(_mu[k])):
            _mu[k][_m] = su[_m]
        k += 1
    if before_mu == _mu:
        return False
    return True


############################################## MAIN
k = 3
colors = ['#FF7363', '#E8935A', '#FACF71', '#EBD750', '#D1FF63']

k = int(input('input k (1<=k<=%d) : ' % (len(colors))))
if not (1 <= k <= 5):
    k = 2
S = []  # k개의 집합 Si로 이루어져있음.
mu = []  # 각 클러스터의 중심점 mu k개

numData = int(input('input num of data (300 recommended) : '))
if numData <= 5:
    numData = 5
half = int(numData / 2)

x = np.array((np.random.normal(-0.6, 0.3, half), np.random.normal(0.2, 0.5, half + numData % 2)))
x = np.resize(x, numData)
y = np.array((np.random.normal(-0.6, 0.3, half), np.random.normal(0.6, 0.3, half + numData % 2)))
y = np.resize(y, numData)

data = []
for i in range(numData):  # x 데이터와 y 데이터를 tuple 형태로 합침.
    data.append((x[i], y[i]))
print(data)

for i in range(k):  # 각 클러스트의 초기값을 랜덤으로 초기화 함.
    mu.append([np.random.random(), np.random.random()])

for i in range(k):  # 집합 S 공간 만듦
    S.append([])

ret = True
while ret:
    S = get_reset_s(S, mu, data)
    ret = update_mu(mu, S)

x_data = []
y_data = []
for s in S:
    x_tmp = []
    y_tmp = []
    for si in s:
        x_tmp.append(si[0])
        y_tmp.append(si[1])
    x_data.append(x_tmp)
    y_data.append(y_tmp)

# before plot
plt.figure('before')
plt.title('BEFORE')
plt.xlabel('x')
plt.ylabel('y')
plt.scatter(x, y, c='#ff0000', marker='.')
plt.show()

# after plot
plt.figure('after')
plt.title('AFTER')
plt.xlabel('x')
plt.ylabel('y')
for n in range(len(x_data)):
    plt.scatter(x_data[n], y_data[n], c=colors[n], marker='.')
print(mu)
print('Variance : ', variance(mu, S))
mu_x = [v[0] for v in mu]
mu_y = [v[1] for v in mu]
plt.plot(mu_x, mu_y, 'r*')
plt.show()
