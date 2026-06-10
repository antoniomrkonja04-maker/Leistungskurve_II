import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker


def power_curve(power_data, time_s=1, durations=None, tick_step=None, tick_style=None, marker_size=3, minor_ticks=True, save_plot=False):
    """Compute the power curve and plot duration vs. maximum average power.

    Parameters
    - power_data: sequence of power samples
    - time_s: sample interval in seconds
    - durations: optional sequence of durations (seconds) to evaluate
    - tick_step: spacing for x-axis ticks in seconds (None -> automatic)
    - tick_style: 'series' for 1-2-5 ticks
    - save_plot: if True, save plot as 'screenshot.png'
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

    plot_power_curve(df, xticks=xticks, time_s=time_s, marker_size=marker_size, minor_ticks=minor_ticks, save_plot=save_plot)
    return df


def plot_power_curve(df, xticks=None, time_s=1, marker_size=3, minor_ticks=True, save_plot=False):
    """Plot power curve with logarithmic x-axis for better visualization."""
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Plot with logarithmic x-axis only (semilogx)
    ax.semilogx(df['duration_s'], df['power_w'], marker='o', markersize=marker_size, 
                linestyle='-', linewidth=2, color='#1f77b4', label='Power Curve')
    
    ax.set_xlabel('Duration (seconds)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Power (Watts)', fontsize=12, fontweight='bold')
    ax.set_title('Power Curve - Logarithmic Scale', fontsize=14, fontweight='bold')
    
    # Format x-axis with time strings
    def sec_to_str(s):
        s = int(round(s))
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        
        if h > 0:
            return f"{h}:{m:02d}:{sec:02d} h"
        elif m > 0:
            return f"{m}:{sec:02d} min"
        else:
            return f"{sec}s"
    
    # Set custom ticks for logarithmic scale
    log_ticks = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 30000]
    available_ticks = [t for t in log_ticks if t >= df['duration_s'].min() and t <= df['duration_s'].max()]
    
    if available_ticks:
        ax.set_xticks(available_ticks)
        ax.set_xticklabels([sec_to_str(t) for t in available_ticks], rotation=0)
    
    # Add grid
    ax.grid(True, which='both', linestyle='-', alpha=0.3, linewidth=0.8)
    ax.grid(True, which='minor', linestyle=':', alpha=0.2)
    
    # Add legend
    ax.legend(fontsize=10, loc='upper right')
    
    # Improve layout
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('screenshot.png', dpi=150, bbox_inches='tight')
        print("Plot saved as 'screenshot.png'")
    
    plt.show()
