import pandas as pd
import cvxpy as cp
import numpy as np
from rl_solver import get_rl_policy
import xlwings as xw

sheet_name = {'main': '情境輸入與結果',
              't_sheet': '資料-威脅度',
              'q_sheet': '資料-毀傷度',
              'v_sheet': '資料-敵方價值',
              'u_sheet': '資料-彈藥數', 
              't_default': '資料-預設威脅度',
              'q_default': '資料-預設毀傷度',
              'v_default': '資料-預設敵方價值',
              'u_default': '資料-預設彈藥數', }

policy_mode = {"max_q":"最大毀傷度", "max_t":"最大威脅毀傷度", "max_v":"最大價值毀傷度", "min_u": "最小成本策略", "mixture": "綜合策略"}




def get_matrix_size(filepath):
    weapons = pd.read_excel(filepath, sheet_name=sheet_name['main'])['Weapon'].dropna()
    enemies = pd.read_excel(filepath, sheet_name=sheet_name['main'])['Enemy'].dropna()
    return len(weapons), len(enemies)

@xw.func
def load_matrix(filepath, default=True):
    enemies = pd.read_excel(filepath, sheet_name=sheet_name['main'], header=None).iloc[2].dropna()
    weapons = pd.read_excel(filepath, sheet_name=sheet_name['main'], header=None).iloc[5].dropna()
    T = pd.read_excel(filepath, sheet_name=sheet_name['t_sheet'], index_col=0).dropna()
    Q = pd.read_excel(filepath, sheet_name=sheet_name['q_sheet'], index_col=0).dropna()
    V = pd.read_excel(filepath, sheet_name=sheet_name['v_sheet']).dropna()
    U = pd.read_excel(filepath, sheet_name=sheet_name['u_sheet'], dtype=int).dropna()
    M = len(weapons)
    N = len(enemies)
    WandE = weapons.to_frame().merge(enemies.to_frame(), how='cross')
    t_matrix = np.zeros((M, N))
    q_matrix = np.zeros((M, N))
    v_matrix = np.zeros((N, 1))
    u_matrix = np.zeros((M, 1), dtype=int)
    q_matrix[1] = np.ones(N)
    for idx, (w, e) in WandE.iterrows():
        t_matrix[idx // N][idx % N] = T[e][w]
        q_matrix[idx // N][idx % N] = Q[e][w]
    for idx, e in enumerate(enemies):
        v_matrix[idx] = V[e]
    for idx, w in enumerate(weapons):
        u_matrix[idx] = U[w]

    return enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix

def get_policy(enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix, mode=policy_mode["max_t"], alpha_v=0, alpha_q=0, alpha_t=0, alpha_u=0):
    M = len(weapons)
    N = len(enemies)
    X = cp.Variable((M, N), boolean=True)
    # constraints = [cp.sum(x) < u_matrix[i] for i, x in enumerate(X)]
    constraints = []
    for i, x in enumerate(X):
        constraints += [cp.sum(x) <= u_matrix[i], cp.sum(x) >= 1]
    if mode == policy_mode['max_t'] or mode == policy_mode['min_u']:
        if mode == policy_mode['max_t']:
            object = cp.Maximize(cp.sum(t_matrix.T @ cp.multiply(q_matrix, X)))
        else:
            object = cp.Maximize(-cp.sum(u_matrix.T @ cp.multiply(q_matrix, X)))
        prob = cp.Problem(object, constraints)
        result = prob.solve(solver=cp.GLPK_MI, verbose=False)
        action = X.value
    elif mode != policy_mode['mixture']:
        action = get_rl_policy(enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix, alpha_v=mode==policy_mode['max_v'], alpha_u=mode==policy_mode['max_q'])
    else:
        action = get_rl_policy(enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix,alpha_v= alpha_v, alpha_u=alpha_u, alpha_t=alpha_t, alpha_q=alpha_q)

    policy = []
    for i, goal in enumerate(action):
        policy.append([f"E{j + 1}. {enemies[j]}" for j, g in enumerate(goal) if g])
    policy = pd.DataFrame(policy).T
    return policy, action


if __name__ == '__main__':
    print("Fire Control Policy")
