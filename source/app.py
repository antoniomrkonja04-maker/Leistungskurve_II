from pathlib import Path
import pandas as pd
from .power_curve import power_curve, power_curve_zones

POWER_COLUMNS = [
    "power",
    "watts",
    "PowerOriginal",
    "CalculatedAerobicEfficiencyPower",
    "power_w",
]


def find_power_column(df):
    """Return the first matching power column name, or None."""
    return next((col for col in POWER_COLUMNS if col in df.columns), None)


def process_activity(
    input_path=None,
    output_path=None,
    zones_output_path=None,
    time_s=1,
    tick_step=None,
    tick_style=None,
    save_plot=False,
):
    """Read activity CSV, compute full power curve and zone power curve, save both.

    Parameters
    ----------
    input_path : str or Path or None
        Path to input CSV. Defaults to activity.csv or data/activity.csv.
    output_path : str or Path or None
        Path for full power curve CSV. Defaults to power_curve_results.csv.
    zones_output_path : str or Path or None
        Path for zones CSV. Defaults to power_curve_results_zones.csv.
    time_s : float
        Sample interval in seconds (default: 1).
    tick_step : float or None
        X-axis tick spacing in seconds.
    tick_style : str or None
        'series' for 1-2-5 tick style.
    save_plot : bool
        If True, save plot to images/screenshot.png.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (full_curve_df, zones_df)
    """
    # Resolve input file
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
        raise ValueError(f"No power column found. Available columns: {list(df.columns)}")

    power = pd.to_numeric(df[power_col], errors="coerce").dropna()
    if power.empty:
        raise ValueError(f"No valid numeric power values found in column '{power_col}'")

    # Full power curve
    result_df = power_curve(
        power,
        time_s=time_s,
        tick_step=tick_step,
        tick_style=tick_style,
        save_plot=save_plot,
    )
    if output_path is None:
        output_path = Path("power_curve_results.csv")
    result_df.to_csv(output_path, index=False)
    print(f"Full power curve saved to '{output_path}'")

    # Zone power curve
    zones_df = power_curve_zones(power, time_s=time_s, save_plot=False)
    if zones_output_path is None:
        zones_output_path = Path("power_curve_results_zones.csv")
    zones_df.to_csv(zones_output_path, index=False)
    print(f"Zone power curve saved to '{zones_output_path}'")

    return result_df, zones_df
