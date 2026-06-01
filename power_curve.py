import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_power_curve(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['duration_s'], df['power_w'], marker='o')
    plt.xscale('log')
    plt.xlabel('Duration (s)')
    plt.ylabel('Power (W)')
    plt.title('Power Curve')
    plt.grid()
    plt.show()


def power_curve(power_data, time_s=1, durations=None):
    power = np.asarray(power_data, dtype=float)
    durations_total = len(power) * time_s

    if durations is None:
        durations = np.arange(1, durations_total + 1)
    else:
        durations = np.asarray(durations, dtype=int)

    results = []
    for dur_s in durations:
        if dur_s < 1 or dur_s > durations_total:
            continue

        n_samples = int(dur_s / time_s)
        if n_samples < 1 or n_samples > len(power):
            continue

        rolling_avg = np.convolve(power, np.ones(n_samples) / n_samples, mode='valid')
        max_avg = np.max(rolling_avg)
        results.append({"duration_s": dur_s, "power_w": max_avg})

    df = pd.DataFrame(results)
    plot_power_curve(df)
    return df

