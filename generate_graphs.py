import csv
from pathlib import Path
import matplotlib.pyplot as plt

RESULTS = Path("results")
GRAPHS = Path("graphs")
GRAPHS.mkdir(exist_ok=True)


def read_csv(name):
    with (RESULTS / name).open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def graph_validation():
    rows = read_csv("large_sequence_summary.csv")[0]

    labels = [
        "Valid accepted",
        "Invalid rejected",
    ]

    values = [
        float(rows["valid_acceptance_rate"]),
        float(rows["invalid_rejection_rate"]),
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.ylabel("Rate (%)")
    plt.title("PowerFlow Sequence Verification")
    plt.ylim(0, 105)
    plt.tight_layout()
    plt.savefig(GRAPHS / "01_sequence_verification.png", dpi=200)
    plt.close()


def graph_scalability():
    rows = read_csv("scalability.csv")

    x = [int(row["states"]) for row in rows]
    y = [float(row["average_search_ms"]) for row in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o")
    plt.xlabel("Number of Automaton States")
    plt.ylabel("Average BFS Search Time (ms)")
    plt.title("Recovery Search Scalability")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAPHS / "02_recovery_scalability.png", dpi=200)
    plt.close()


def graph_product():
    rows = read_csv("product_automaton.csv")

    x = [int(row["component_states"]) for row in rows]
    y = [int(row["product_states"]) for row in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o")
    plt.xlabel("States per Component")
    plt.ylabel("Product Automaton States")
    plt.title("Product Automaton State-Space Growth")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAPHS / "03_product_state_growth.png", dpi=200)
    plt.close()


def graph_baseline():
    rows = read_csv("baseline_comparison.csv")[0]

    labels = [
        "Baseline unsafe actions",
        "PowerFlow blocked",
    ]

    values = [
        int(rows["baseline_unsafe_actions"]),
        int(rows["powerflow_blocked"]),
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.ylabel("Number of Requests")
    plt.title("Unsafe Transition Blocking")
    plt.tight_layout()
    plt.savefig(GRAPHS / "04_unsafe_transition_blocking.png", dpi=200)
    plt.close()


def graph_recovery_path():
    rows = read_csv("recovery_benchmark.csv")[0]
    path = rows["path"].split(" -> ")

    values = list(range(len(path)))

    plt.figure(figsize=(8, 5))
    plt.plot(values, marker="o")
    plt.xticks(values, path, rotation=25)
    plt.ylabel("Recovery Step")
    plt.title("Shortest Recovery Path from FAULT")
    plt.tight_layout()
    plt.savefig(GRAPHS / "05_recovery_path.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    graph_validation()
    graph_scalability()
    graph_product()
    graph_baseline()
    graph_recovery_path()
    print("Graphs generated inside the graphs folder.")
