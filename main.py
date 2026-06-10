from source.app import process_activity


def main():
    # minimal launcher: reads data/activity.csv or activity.csv and writes power_curve_results.csv
    process_activity(save_plot=True)


if __name__ == "__main__":
    main()