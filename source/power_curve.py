import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ZONE_DURATIONS = [1, 5, 10, 20, 60, 300, 1200, 1800]


def power_curve(
    power_data,
    time_s=1,
    durations=None,
    tick_step=None,
    tick_style=None,
    marker_size=3,
    minor_ticks=True,
    save_plot=False,
):
    """Compute the power curve and plot duration vs. maximum average power.

    Parameters
    ----------
    power_data : array-like
        Sequence of power samples in Watts (Pandas Series or NumPy array).
    time_s : float
        Sample interval in seconds (default: 1).
    durations : array-like or None
        Optional sequence of durations in seconds to evaluate.
        If None, all integer multiples of time_s up to the recording length are used.
    tick_step : float or None
        Spacing for x-axis ticks in seconds. None = automatic.
    tick_style : str or None
        'series' for 1-2-5 tick style.
    marker_size : int
        Size of plot markers (default: 3).
    minor_ticks : bool
        Show minor grid ticks (default: True).
    save_plot : bool
        If True, save plot to images/screenshot.png.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns 'duration_s' and 'power_w'.
    """
    power = np.asarray(power_data, dtype=float)
    power = np.nan_to_num(power, nan=0.0)
    max_duration = len(power) * time_s

    if durations is None:
        durations = np.arange(time_s, max_duration + 1, time_s)
    else:
        durations = np.asarray(durations, dtype=float)

    durations = np.unique(durations[(durations >= time_s) & (durations <= max_duration)])
    if durations.size == 0:
        return pd.DataFrame(columns=["duration_s", "power_w"])

    cumsum = np.concatenate(([0.0], np.cumsum(power)))
    n_samples = np.round(durations / time_s).astype(int)
    powers = [
        float(np.max((cumsum[n:] - cumsum[:-n]) / n))
        for n in n_samples
    ]

    df = pd.DataFrame({"duration_s": durations, "power_w": powers})

    # x-axis ticks
    if tick_style == "series":
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
        if tick_step is None:
            tick_step = max(time_s, max_duration / 5.0)
        tick_step = float(tick_step)
        if tick_step <= 0:
            tick_step = max(time_s, 1.0)
        xticks = np.arange(durations.min(), durations.max() + tick_step, tick_step)

    plot_power_curve(
        df,
        xticks=xticks,
        time_s=time_s,
        marker_size=marker_size,
        minor_ticks=minor_ticks,
        save_plot=save_plot,
    )
    return df


def power_curve_zones(power_data, time_s=1, save_plot=False):
    """Compute the power curve only for fixed zone durations.

    Zones: 1 s, 5 s, 10 s, 20 s, 1 min, 5 min, 20 min, 30 min.

    Parameters
    ----------
    power_data : array-like
        Sequence of power samples in Watts.
    time_s : float
        Sample interval in seconds (default: 1).
    save_plot : bool
        If True, save plot to images/screenshot.png.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns 'duration_s' and 'power_w'.
    """
    power = np.asarray(power_data, dtype=float)
    power = np.nan_to_num(power, nan=0.0)
    max_duration = len(power) * time_s

    valid_durations = [d for d in ZONE_DURATIONS if d <= max_duration]
    if not valid_durations:
        return pd.DataFrame(columns=["duration_s", "power_w"])

    cumsum = np.concatenate(([0.0], np.cumsum(power)))
    results = []
    for d in valid_durations:
        n = int(round(d / time_s))
        max_power = float(np.max((cumsum[n:] - cumsum[:-n]) / n))
        results.append({"duration_s": d, "power_w": max_power})

    df = pd.DataFrame(results)

    plot_power_curve(df, time_s=time_s, save_plot=save_plot)
    return df


def plot_power_curve(
    df, xticks=None, time_s=1, marker_size=3, minor_ticks=True, save_plot=False
):
    """Plot power curve with logarithmic x-axis."""
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.semilogx(
        df["duration_s"],
        df["power_w"],
        marker="o",
        markersize=marker_size,
        linestyle="-",
        linewidth=2,
        color="#1f77b4",
        label="power_w",
    )

    ax.set_xlabel("Duration (s)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Power (W)", fontsize=12, fontweight="bold")
    ax.set_title("Power Curve", fontsize=14, fontweight="bold")

    def sec_to_str(s):
        s = int(round(s))
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        if h > 0:
            return f"{h}:{m:02d}:{sec:02d}"
        elif m > 0:
            return f"{m}:{sec:02d}"
        else:
            return f"{sec}s"

    log_ticks = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 30000]
    available_ticks = [
        t for t in log_ticks
        if t >= df["duration_s"].min() and t <= df["duration_s"].max()
    ]
    if available_ticks:
        ax.set_xticks(available_ticks)
        ax.set_xticklabels([sec_to_str(t) for t in available_ticks])

    ax.grid(True, which="both", linestyle="-", alpha=0.3, linewidth=0.8)
    if minor_ticks:
        ax.grid(True, which="minor", linestyle=":", alpha=0.2)

    ax.legend(fontsize=10, loc="upper right")
    plt.tight_layout()

    if save_plot:
        out = Path("images")
        out.mkdir(exist_ok=True)
        path = out / "screenshot.png"
        plt.savefig(path, dpi=150, bbox_inches="tight")
        print(f"Plot saved as '{path}'")

    plt.show()
