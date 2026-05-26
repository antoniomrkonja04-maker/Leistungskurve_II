import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_power_curve(power_data, time_resolution_s=1):
    """
    Berechnet die Power Curve.
    
    power_data: eine pandas Series oder ein numpy Array mit Wattwerten
    time_resolution_s: wie viele Sekunden ein Messpunkt dauert (z.B. 1 wenn jede Zeile 1 Sekunde ist)
    
    Gibt ein DataFrame zurück mit:
    - time_s: Dauer in Sekunden
    - power_w: beste mittlere Leistung für diese Dauer
    """

    # alles in numpy array 
    power = np.array(power_data, dtype=float)
    n = len(power)  # wie viele Datenpunkte haben wir insgesamt

    # Ergebnisse für die Power Curve
    result_times = []
    result_powers = []

    #alle Fenstergrößen von 1 bis n durchgehen
    for window in range(1, n + 1):
        
        # wie lange ist dieses Fenster in Sekunden
        duration = window * time_resolution_s
        
        # jetzt berechnen wir den Durchschnitt für alle möglichen Positionen dieses Fensters
        # z.B. bei window=3: Durchschnitt von [0:3], [1:4], [2:5], ...
        averages = []
        for i in range(n - window + 1):
            avg = np.mean(power[i : i + window])
            averages.append(avg)
        
        # das Maximum aller Durchschnitte ist die beste Leistung für diese Dauer
        best = max(averages)
        
        result_times.append(duration)
        result_powers.append(best)

    # alles in ein DataFrame packen
    df = pd.DataFrame({
        "time_s": result_times,
        "power_w": result_powers
    })

    return df


def plot_power_curve(df, save_path=None):
    """
    Plottet die Power Curve aus dem DataFrame.
    df muss die Spalten 'time_s' und 'power_w' haben.
    Mit save_path kann man den Plot als PNG speichern.
    """

    # Plot erstellen
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df["time_s"], df["power_w"], color="steelblue", linewidth=2)

    # Achsenbeschriftungen
    ax.set_xlabel("Dauer [s]", fontsize=13)
    ax.set_ylabel("Leistung [W]", fontsize=13)
    ax.set_title("Power Curve", fontsize=15, fontweight="bold")

    # logarithmische x-Achse weil die Kurve sonst links sehr gequetscht aussieht
    ax.set_xscale("log")

    ax.grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()

    # speichern oder anzeigen
    if save_path != None:
        plt.savefig(save_path, dpi=150)
        print("Plot wurde gespeichert unter: " + save_path)
    else:
        plt.show()

    plt.close()
