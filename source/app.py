from pathlib import Path
import pandas as pd
from .power_curve import power_curve

POWER_COLUMNS = [
    "power",
    "watts",
    "PowerOriginal",
    "CalculatedAerobicEfficiencyPower",
    "power_w",
]


def find_power_column(df):
    return next((col for col in POWER_COLUMNS if col in df.columns), None)


def process_activity(input_path=None, output_path=None, time_s=1, tick_step=None, tick_style=None, save_plot=False):
    """Read activity data, compute power curve and save results."""
    if input_path is None:
        input_file = Path("activity.csv")
        alt_file = Path("data") / "activity.csv"
        if not input_file.exists() and alt_file.exists():
            input_file = alt_file
    else:
        input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)
    power_col = find_power_column(df)
    if power_col is None:
        raise ValueError(f"No power column found. Available: {list(df.columns)}")

    power = pd.to_numeric(df[power_col], errors="coerce").dropna()
    if power.empty:
        raise ValueError(f"No valid power values in '{power_col}'")

    result_df = power_curve(power, time_s=time_s, tick_step=tick_step, tick_style=tick_style, save_plot=save_plot)

    if output_path is None:
        output_path = Path("power_curve_results.csv")
    result_df.to_csv(output_path, index=False)
    return result_df
