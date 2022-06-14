import gym
import numpy as np
from gym import spaces
from stable_baselines3 import A2C


class FireControlEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self,enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix,
                 alpha_t=0, alpha_v=0, alpha_q=0, alpha_u=0):
        super(FireControlEnv, self).__init__()
        self.M = len(weapons)
        self.N = len(enemies)

        self.q_matrix = q_matrix
        self.t_matrix = t_matrix
        self.v_matrix = v_matrix
        self.u_matrix = u_matrix.flatten()
        self.reward = 0

        self.alpha_t = alpha_t
        self.alpha_v = alpha_v
        self.alpha_q = alpha_q
        self.alpha_u = alpha_u

        # step variable
        self.obs = np.concatenate([self.q_matrix.flatten(), self.t_matrix.flatten(),
                                   self.v_matrix.flatten(), self.u_matrix.flatten()], axis=0)
        self.done = False
        self.history = None
        self.count = 0

        # action and observation space
        self.total_shot = np.sum(self.u_matrix, dtype=int)
        self.action_space = spaces.Box(low=0, high=1, shape=(self.total_shot * self.N, ))
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.obs.size,), dtype=np.float32)

    def step(self, action):
        action_matrix = np.zeros((self.M, self.N))
        action_idx = 0
        for weapon_idx, u in enumerate(self.u_matrix):
            for _ in range(u):
                action_matrix[weapon_idx][np.argmax(action[action_idx:action_idx+self.N])] += 1
                action_idx += self.N

        value = 0
        reward = 0
        if self.alpha_q or self.alpha_v:
            q_mul_x_matrix = (1 - self.q_matrix) ** action_matrix
            for v, col in zip(self.v_matrix.T, q_mul_x_matrix.T):
                survive_prob = 1
                for elem in col:
                    survive_prob *= elem
                if self.alpha_v:
                    value += (self.alpha_v * v[0] + self.alpha_q) * (1 - survive_prob)
        
        if self.alpha_t or self.alpha_u:
            reward += self.alpha_t * np.sum(self.t_matrix.T@action_matrix) - self.alpha_u*np.sum(action_matrix)

        reward += value
        self.reward = reward
        self.done = True
        info = {'reward': reward,
                'action_matrix': action_matrix,}
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

def get_rl_policy(enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix, alpha_v=0, alpha_q=0, alpha_t=0, alpha_u=0):
    env = FireControlEnv(enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix)
    model = A2C("MlpPolicy", env, verbose=False)
    model.learn(total_timesteps=2000)
    record = []
    observation = env.reset()
    for _ in range(5000):
        action, _ = model.predict(observation)
        observation, reward, done, info = env.step(action)
        record.append((info["action_matrix"], reward))
        observation = env.reset()
    return max(record, key=lambda x:x[1])[0]


if __name__ == '__main__':
    print("Fire Control Policy")