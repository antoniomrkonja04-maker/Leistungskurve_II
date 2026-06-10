from source.app import process_activity


def main():
    full_df, zones_df = process_activity(save_plot=True)
    print("\nZonen-Auswertung (1s / 5s / 10s / 20s / 1min / 5min / 20min / 30min):")
    print(zones_df.to_string(index=False))


if __name__ == "__main__":
    main()
