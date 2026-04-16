import numpy as np
import pandas as pd

from mobha import generator


def main():
    timesteps = 10000
    standard_deviation = 1.0
    turning_angle_standard_deviation = 0.3

    paths = []
    for dist in ["gaussian", "uniform", "constant"]:
        walker = generator.RandomWalk2D(standard_deviation, distribution=dist)
        walker.walk(timesteps)
        paths.append(walker.path)

    correlated_walker = generator.CorrelatedRandomWalk2D(
        step_size=standard_deviation,
        turning_angle_standard_deviation=turning_angle_standard_deviation,
    )
    correlated_walker.walk(timesteps)
    paths.append(correlated_walker.path)

    path_array = np.hstack(paths)
    path_array = np.vstack([path_array, np.nan * np.zeros((1, path_array.shape[-1]))])
    columns = [f"walker{i}_{axis}" for i in range(len(paths)) for axis in ("x", "y")]
    df = pd.DataFrame(path_array, columns=columns)
    df.index.name = "timestep"
    df.to_csv("../data/random_walker2D.csv")


if __name__ == "__main__":
    main()
