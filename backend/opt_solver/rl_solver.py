import gym
import numpy as np
from gym import spaces
from stable_baselines3 import A2C


class FireControlEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self,enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix,
                 alpha_t=0, alpha_v=1, alpha_d=0, alpha_c=0):
        super(FireControlEnv, self).__init__()
        self.M = len(weapons)
        self.N = len(enemies)

        self.d_matrix = d_matrix
        self.t_matrix = t_matrix
        self.v_matrix = v_matrix
        self.u_matrix = u_matrix
        self.c_matrix = c_matrix
        self.reward = 0

        self.alpha_t = alpha_t
        self.alpha_v = alpha_v
        self.alpha_d = alpha_d
        self.alpha_c = alpha_c

        # step variable
        self.obs = np.concatenate([self.d_matrix, self.t_matrix,
                                   self.v_matrix, self.u_matrix, self.c_matrix], axis=0)
        self.done = False
        self.history = None
        self.count = 0

        # action and observation space
        self.total_shot = np.sum(self.u_matrix, dtype=int)
        self.action_space = spaces.Box(low=0, high=1, shape=(self.total_shot * self.N,))
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.obs.size,), dtype=np.float32)

    def step(self, action):
        action_matrix = np.zeros((self.M, self.N))
        action_idx = 0

        for weapon_idx, u in enumerate(self.u_matrix):
            for _ in range(u):
                action_matrix[weapon_idx][np.argmax(action[action_idx:action_idx+self.N])] += 1
                action_idx += self.N

        reward = 0
        total_cost = 0
        for e_id, sources in enumerate(action_matrix.T):
            survive_prob = 1
            if e_id == self.N-1: continue
            for w_id, num in enumerate(sources):
                survive_prob *= (1 - self.d_matrix[w_id])**num
                total_cost += self.c_matrix[w_id]
            survive_prob = 1 - survive_prob
            reward += self.v_matrix[e_id] * self.t_matrix[e_id]**self.alpha_t * survive_prob**self.alpha_d
        reward /= total_cost**self.alpha_c

        self.reward = reward
        self.done = True
        info = {'reward': reward,
                'action_matrix': action_matrix}
        return self.obs, reward, self.done, info

    def reset(self):
        # if self.count % self.TIME_TO_RESET == 0 and self.count:
        #     self.save_history()
        #     self.history = None

        # step variable
        self.done = False
        # self.count += 1

        return self.obs



    def close(self):
        pass

def get_opt_policy(enemies, allies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix, checked, alpha_v=0, alpha_q=0, alpha_t=0, alpha_u=0):
    actions = {}
    e_num = len(enemies)
    a_num = len(allies)
    w_num = len(weapons)
    # 1_to_1
    if '1_to_1' in checked:
        n_fight = np.min([a_num, e_num - 1])
        if 't-first' in checked:  # 威脅度優先

            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]
            a_to_fight = np.random.choice(a_num, n_fight, replace=False)*2
            action = np.zeros((len(weapons), len(enemies)))
            for e, a in zip(e_to_fight, a_to_fight):
                action[[a, a+1], e] = 1
            action = (action.T * u_matrix).T
            actions['t-first'] = action
        if 'd-first' in checked:
            d_array = np.zeros(a_num)
            for w_id, d in enumerate(d_matrix):
                d_array[w_id//2] += d * u_matrix[w_id]
            a_to_fight = np.argpartition(d_array, -n_fight)[-n_fight:] * 2
            e_to_fight = np.argpartition(v_matrix, -n_fight)[-n_fight:]

            action = np.zeros((len(weapons), len(enemies)))
            for e, a in zip(e_to_fight, a_to_fight):
                action[[a, a+1], e] = 1
            action = (action.T * u_matrix).T
            actions['d-first'] = action

        if 'mix' in checked:
            d_array = np.zeros(a_num)
            for w_id, d in enumerate(d_matrix):
                d_array[w_id//2] += d * u_matrix[w_id]
            a_to_fight = np.argpartition(d_array, -n_fight)[-n_fight:] * 2
            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]

            action = np.zeros((len(weapons), len(enemies)))
            for e, a in zip(e_to_fight, a_to_fight):
                action[[a, a+1], e] = 1
            action = (action.T * u_matrix).T
            actions['mix'] = action
        if 't-cost' in checked:  # 威脅度優先
            cp_array = 1 / c_matrix
            for a_id in range(a_num):
                w_id = 2*a_id
                if cp_array[w_id] > cp_array[w_id+1]:
                    w_id += 1
                cp_array[w_id] = float('-inf')

            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.argpartition(cp_array, -n_fight)[-n_fight:]
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['t-cost'] = action
        if 'd-cost' in checked:  # 威脅度優先
            cp_array = d_matrix / c_matrix
            for a_id in range(a_num):
                w_id = 2*a_id
                if cp_array[w_id] > cp_array[w_id+1]:
                    w_id += 1
                cp_array[w_id] = float('-inf')

            e_to_fight = np.argpartition(v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.argpartition(cp_array, -n_fight)[-n_fight:]
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['d-cost'] = action
        if 'mix-cost' in checked:  # 威脅度優先
            cp_array = d_matrix / c_matrix
            for a_id in range(a_num):
                w_id = 2*a_id
                if cp_array[w_id] > cp_array[w_id+1]:
                    w_id += 1
                cp_array[w_id] = float('-inf')

            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.argpartition(cp_array, -n_fight)[-n_fight:]
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['mix-cost'] = action
        return actions
    elif '1_to_m' in checked:
        n_fight = np.min([w_num, e_num - 1])
        if 't-first' in checked:  # 威脅度優先

            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.random.choice(w_num, n_fight, replace=False)
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['t-first'] = action
        if 'd-first' in checked:
            w_to_fight = np.argpartition(d_matrix, -n_fight)[-n_fight:]
            e_to_fight = np.argpartition(v_matrix, -n_fight)[-n_fight:]

            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['d-first'] = action

        if 'mix' in checked:
            w_to_fight = np.argpartition(d_matrix, -n_fight)[-n_fight:]
            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]

            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['mix'] = action
        if 't-cost' in checked:  # 威脅度優先
            cp_array = 1 / c_matrix

            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.argpartition(cp_array, -n_fight)[-n_fight:]
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['t-cost'] = action
        if 'd-cost' in checked:  # 威脅度優先
            cp_array = d_matrix / c_matrix

            e_to_fight = np.argpartition(v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.argpartition(cp_array, -n_fight)[-n_fight:]
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['d-cost'] = action
        if 'mix-cost' in checked:  # 威脅度優先
            cp_array = d_matrix / c_matrix

            e_to_fight = np.argpartition(t_matrix * v_matrix, -n_fight)[-n_fight:]
            w_to_fight = np.argpartition(cp_array, -n_fight)[-n_fight:]
            action = np.zeros((len(weapons), len(enemies)))
            for e, w in zip(e_to_fight, w_to_fight):
                action[w, e] = 1
            action = (action.T * u_matrix).T
            actions['mix-cost'] = action
        return actions
    if 'n_to_m' in checked:
        def train(env):
            model = A2C("MlpPolicy", env, verbose=False)
            model.learn(total_timesteps=2000)
            record = []
            observation = env.reset()
            for _ in range(5000):
                action, _ = model.predict(observation)
                observation, reward, done, info = env.step(action)
                record.append((info["action_matrix"], reward))
                observation = env.reset()
            return max(record, key=lambda x: x[1])[0]

        if 't-first' in checked:
            env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix, alpha_t=1)
            actions['t-first'] = train(env)
        if 'd-first' in checked:
            env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix, alpha_d=1)
            actions['d-first'] = train(env)
        if 'mix' in checked:
            env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix, alpha_d=1, alpha_t=1)
            actions['mix'] = train(env)
        if 't-cost' in checked:
            env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix, alpha_c=1, alpha_t=1)
            actions['t-cost'] = train(env)
        if 'd-cost' in checked:
            env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix, alpha_c=1, alpha_d=1)
            actions['d-cost'] = train(env)
        if 'mix-cost' in checked:
            env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix, c_matrix,alpha_t=1, alpha_c=1, alpha_d=1)
            actions['mix-cost'] = train(env)
        return actions
    # env = FireControlEnv(enemies, weapons, t_matrix, d_matrix, v_matrix, u_matrix)
    # model = A2C("MlpPolicy", env, verbose=False)
    # model.learn(total_timesteps=2000)
    # record = []
    # observation = env.reset()
    # for _ in range(5000):
    #     action, _ = model.predict(observation)
    #     observation, reward, done, info = env.step(action)
    #     record.append((info["action_matrix"], reward))
    #     observation = env.reset()
    # return max(record, key=lambda x:x[1])[0]


if __name__ == '__main__':
    print("Fire Control Policy")