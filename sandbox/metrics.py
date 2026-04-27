import numpy as np
import pandas as pd

print("metrics.py loaded successfully.")
def get_run_durations_by_direction(df, fps, angle_threshold, gradient_col='vx_um_s'):
    """Compute run durations separated by
      movement direction. This function 
      classifies runs based on angle 
      change and groups them by the sign 
      of the gradient-aligned velocity.

    Args:
        df: Pandas DataFrame .
        fps: Frame rate of the recording in frames per second.
        angle_threshold: Maximum allowed angle change (in degrees) for a frame to be considered part of a run.
        gradient_col: Name of the column representing velocity along the gradient direction, used to determine up versus down runs.

    Returns:
        A tuple (up_durs, down_durs) where each element is a list of run durations in seconds for runs moving up and down the gradient, respectively.
    """
    dt = 1.0 / fps
    df = df.copy()
    df['is_run'] = df['angle_change_deg'] < angle_threshold
    df['seg']    = (df['is_run'] != df['is_run'].shift(1)).cumsum()

    up_durs, down_durs = [], []
    for _, grp in df[df['is_run']].groupby('seg'):
        dur = len(grp) * dt
        if dur < 0.05: continue
        mean_vx = grp[gradient_col].mean()  # directly from stored col 6
        if mean_vx < 0:
            up_durs.append(dur)
        else:
            down_durs.append(dur)

    return up_durs, down_durs

def extract_clean(V, idx):
    """Clean and structure raw trajectory data 
    for a cell index. 

    Args:
        V: Structured container holding speed and parameter arrays, including 'Speeds' and 'Parameters' with an 'fps' field.
        idx: Integer index indicating which trajectory or cell to extract from the 'Speeds' data.

    Returns:
        A tuple of (df, fps) where df is a pandas DataFrame with cleaned trajectory data and fps is a float representing the frame rate in frames per second.
    """
    raw   = V['Speeds'][0, 0]
    cell  = raw[idx, 0]
    fps   = float(V['Parameters'][0, 0]['fps'][0, 0].item())

    mask      = ~np.isnan(cell[:, 9])   # angle_change_deg must exist
    raw_clean = cell[mask]

    df = pd.DataFrame({
        'frame'           : raw_clean[:, 0].astype(int),
        'time_s'          : raw_clean[:, 0] / fps,
        'x_um'            : raw_clean[:, 1],
        'y_um'            : raw_clean[:, 2],
        'z_um'            : raw_clean[:, 3],
        'vx_um_s'         : raw_clean[:, 5],   # col 6 (task) = index 5
        'vy_um_s'         : raw_clean[:, 6],   # col 7 (task) = index 6
        'vz_um_s'         : raw_clean[:, 7],   # col 8 (task) = index 7
        'speed_um_s'      : raw_clean[:, 8],   # col 9 (task) = index 8
        'angle_change_deg': raw_clean[:, 9],   # col 10 (task) = index 9
    }).reset_index(drop=True)

    return df, fps

def compute_msd(df):
        """
        Time-averaged MSD.

        MSD(τ) = (1/N) Σ |r(t+τ) - r(t)|²

        Parameters
        ----------
        df : DataFrame with columns x_um, y_um, z_um, time_s
            (already NaN-cleaned)

        Returns
        -------
        lags : array of time lags τ (seconds)
        msd  : array of MSD values (µm²)
        """
        dt = df['time_s'].iloc[1] - df['time_s'].iloc[0]   # frame interval (s)
        x  = df['x_um'].values
        y  = df['y_um'].values
        z  = df['z_um'].values
        lags, msd = [], []
        for lag in range(1, len(x) // 3):          # max lag = 1/3 of trajectory
            d2 = (x[lag:]-x[:-lag])**2 + \
                (y[lag:]-y[:-lag])**2 + \
                (z[lag:]-z[:-lag])**2
            msd.append(d2.mean())
            lags.append(lag * dt)
        return np.array(lags), np.array(msd)

def get_cw_bias(V, angle_threshold):
    biases = []
    for i in range(len(V['Speeds'][0, 0])):
        df, fps = extract_clean(V, i)
        if len(df) < 10: continue
        biases.append((df['angle_change_deg'] > angle_threshold).mean())
    return np.array(biases)

def get_cheyp(Kd, H, bias):
    """infer [CheY-P] from Hill equation inversion"""
    return Kd * (bias / (1 - bias)) ** (1 / H)
