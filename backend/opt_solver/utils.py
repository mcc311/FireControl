from os import listdir
import subprocess, os, platform
import numpy as np




def find_filenames(path_to_dir='.', prefix='', suffix=''):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix) and filename.startswith(prefix)]


def generate_random_tester(M, N, dir='data/'):
    q_matrix = np.random.uniform(0, 1, (M, N))
    t_matrix = np.random.uniform(0, 1, (M, N))
    v_matrix = np.random.uniform(0, 1, (1, N))
    np.savetxt(f'{dir}q_matrix_{M}x{N}.csv', q_matrix)
    np.savetxt(f'{dir}t_matrix_{M}x{N}.csv', t_matrix)
    np.savetxt(f'{dir}v_matrix_{1}x{N}.csv', v_matrix)


def open_with_os(filepath):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


if __name__ == '__main__':
    pass
