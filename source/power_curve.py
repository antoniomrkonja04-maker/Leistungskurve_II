import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker


def power_curve(power_data, time_s=1, durations=None, tick_step=None, tick_style=None, marker_size=6, minor_ticks=True):
    """Compute the power curve and plot duration vs. maximum average power.

    Parameters
    - power_data: sequence of power samples
    - time_s: sample interval in seconds
    - durations: optional sequence of durations (seconds) to evaluate
    - tick_step: spacing for x-axis ticks in seconds (None -> automatic)
    - tick_style: 'series' for 1-2-5 ticks
    """
    power = np.asarray(power_data, dtype=float)
    max_duration = len(power) * time_s

    if durations is None:
        durations = np.arange(time_s, max_duration + 1, time_s)
    else:
        durations = np.asarray(durations, dtype=int)

    durations = np.unique(durations[(durations >= time_s) & (durations <= max_duration)])
    if durations.size == 0:
        return pd.DataFrame(columns=['duration_s', 'power_w'])

    n_samples = (durations // time_s).astype(int)
    powers = [np.max(np.convolve(power, np.ones(n) / n, mode='valid')) for n in n_samples]

    df = pd.DataFrame({'duration_s': durations, 'power_w': powers})

    # determine x-axis ticks
    if tick_style == 'series':
        # 1-2-5 series: 1,2,5,10,20,50,... up to max_duration
        ticks = []
        base = [1, 2, 5]
        exp = 0
        while True:
            added = False
            for b in base:
                val = b * (10 ** exp)
                if val <= max_duration:
                    ticks.append(val)
                    added = True
            if not added:
                break
            exp += 1
        xticks = np.array(sorted(set(ticks)))
        xticks = xticks[xticks >= durations.min()]
    else:
        # determine tick step (in seconds) - allow fractional seconds
        if tick_step is None:
            tick_step = max(time_s, max_duration / 5.0)
        tick_step = float(tick_step)
        if tick_step <= 0:
            tick_step = max(time_s, 1.0)
        xticks = np.arange(durations.min(), durations.max() + tick_step, tick_step)

    plot_power_curve(df, xticks=xticks, time_s=time_s, marker_size=marker_size, minor_ticks=minor_ticks)
    return df


def plot_power_curve(df, xticks=None, time_s=1, marker_size=6, minor_ticks=True):
    ax = df.plot(x='duration_s', y='power_w', marker='o', figsize=(10, 6), grid=True, title='Power Curve', markersize=marker_size)
    ax.set_xlabel('Duration (s)')
    ax.set_ylabel('Power (W)')
    if xticks is not None and len(xticks) > 1:
        ax.set_xticks(xticks)
        # format tick labels as time strings (mm:ss or hh:mm:ss)
        def sec_to_str(s):
            s = int(round(s))
            h, rem = divmod(s, 3600)
            m, sec = divmod(rem, 60)
            if h > 0:
                return f"{h}:{m:02d}:{sec:02d}"
            else:
                return f"{m}:{sec:02d}"

        labels = [sec_to_str(x) for x in xticks]
        ax.set_xticklabels(labels)
    # add minor ticks for better resolution of points
    if minor_ticks:
        # choose a reasonable minor step: half of the major spacing, but at least time_s
        if len(xticks) > 1:
            major_step = float(xticks[1] - xticks[0])
        else:
            major_step = max(1.0, time_s)
        minor_step = max(time_s, major_step / 2.0)
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(minor_step))
        ax.grid(which='minor', linestyle=':', alpha=0.4)
    plt.tight_layout()
    plt.show()
