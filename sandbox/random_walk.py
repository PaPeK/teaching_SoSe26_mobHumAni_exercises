import pandas as pd
import numpy as np
from mobha import generator

def main():
    timesteps = 10000
    standard_deviation = 1.

    paths = []
    for dist in ['gaussian', 'uniform', 'gaussian', 'square', 'square_symmetric', 'constant']:
        # generate 1D random walk
        rw = generator.RandomWalk1D(standard_deviation, distribution=dist)
        rw.walk(timesteps)
        paths.append(rw.path)


    # craete a pandas Dataframe
    paths = np.vstack(paths).T
    # add a np.nan row at the end (so some preprocessing is needed)
    paths = np.vstack([paths, np.nan * np.zeros((1, paths.shape[-1]))])
    df = pd.DataFrame(paths, columns=[f'walker{i}' for i in range(paths.shape[-1])])
    df.index.name = 'timestep'
    df.to_csv('../data/random_walker.csv')


if __name__ == "__main__":
    main()
