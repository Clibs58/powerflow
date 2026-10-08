import csv
import random
import time
from collections import deque
from pathlib import Path

STATES = ["NORMAL", "OVERLOAD", "FAULT", "ISOLATED", "RECOVERY", "VALIDATED"]

EVENTS = [
    "LOAD_INCREASE",
    "FAULT_DETECTED",
    "ISOLATE",
    "REPAIR_COMPLETE",
    "CONTROLLED_REROUTE",
    "VALIDATE",
    "RECONNECT",
    "RECOVERY_OK",
]

TRANSITIONS = {
    ("NORMAL", "LOAD_INCREASE"): "OVERLOAD",
    ("OVERLOAD", "FAULT_DETECTED"): "FAULT",
    ("FAULT", "ISOLATE"): "ISOLATED",
    ("ISOLATED", "REPAIR_COMPLETE"): "RECOVERY",
    ("ISOLATED", "CONTROLLED_REROUTE"): "RECOVERY",
    ("RECOVERY", "VALIDATE"): "VALIDATED",
    ("VALIDATED", "RECONNECT"): "NORMAL",
    ("RECOVERY", "RECOVERY_OK"): "NORMAL",
}

ACCEPTING_STATE = "NORMAL"


def step(state, event):
    return TRANSITIONS.get((state, event))


def verify_sequence(sequence, start_state="NORMAL"):
    state = start_state
    trace = [state]

    for event in sequence:
        next_state = step(state, event)
        if next_state is None:
            return {
                "accepted": False,
                "final_state": state,
                "trace": trace,
                "rejected_event": event,
                "rejected_from": state,
            }
        state = next_state
        trace.append(state)

    return {
        "accepted": state == ACCEPTING_STATE,
        "final_state": state,
        "trace": trace,
        "rejected_event": None,
        "rejected_from": None,
    }


def recovery_path(start_state="FAULT"):
    graph = {}

    for (state, event), next_state in TRANSITIONS.items():
        graph.setdefault(state, []).append((event, next_state))

    queue = deque([(start_state, [])])
    visited = {start_state}

    while queue:
        state, path = queue.popleft()

        if state == ACCEPTING_STATE:
            return path

        for event, next_state in graph.get(state, []):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [event]))

    return None


def execute_recovery(start_state="FAULT"):
    path = recovery_path(start_state)
    if path is None:
        return None

    state = start_state
    trace = [state]

    for event in path:
        state = step(state, event)
        trace.append(state)

    return {
        "events": path,
        "trace": trace,
        "transitions": len(path),
    }


def valid_sequences():
    return [
        [
            "LOAD_INCREASE",
            "FAULT_DETECTED",
            "ISOLATE",
            "REPAIR_COMPLETE",
            "VALIDATE",
            "RECONNECT",
        ],
        [
            "LOAD_INCREASE",
            "FAULT_DETECTED",
            "ISOLATE",
            "CONTROLLED_REROUTE",
            "RECOVERY_OK",
        ],
    ]


def invalid_sequences():
    return [
        [
            "LOAD_INCREASE",
            "FAULT_DETECTED",
            "RECONNECT",
        ],
        [
            "LOAD_INCREASE",
            "FAULT_DETECTED",
            "VALIDATE",
        ],
        [
            "LOAD_INCREASE",
            "FAULT_DETECTED",
            "ISOLATE",
            "RECONNECT",
        ],
        [
            "RECONNECT",
        ],
        [
            "LOAD_INCREASE",
            "FAULT_DETECTED",
            "ISOLATE",
            "VALIDATE",
        ],
    ]


def run_basic_validation():
    rows = []

    for index, sequence in enumerate(valid_sequences(), 1):
        result = verify_sequence(sequence)
        rows.append({
            "category": "valid",
            "test_id": index,
            "expected": "accepted",
            "actual": "accepted" if result["accepted"] else "rejected",
            "correct": result["accepted"],
        })

    for index, sequence in enumerate(invalid_sequences(), 1):
        result = verify_sequence(sequence)
        rows.append({
            "category": "invalid",
            "test_id": index,
            "expected": "rejected",
            "actual": "rejected" if not result["accepted"] else "accepted",
            "correct": not result["accepted"],
        })

    return rows


def generate_random_valid_sequences(count, rng):
    sequences = []

    templates = valid_sequences()

    for _ in range(count):
        template = rng.choice(templates)
        sequences.append(list(template))

    return sequences


def mutate_sequence(sequence, rng):
    mutated = list(sequence)

    operations = ["replace", "delete", "insert"]
    operation = rng.choice(operations)

    if operation == "replace":
        position = rng.randrange(len(mutated))
        choices = [event for event in EVENTS if event != mutated[position]]
        mutated[position] = rng.choice(choices)

    elif operation == "delete" and len(mutated) > 1:
        position = rng.randrange(len(mutated))
        del mutated[position]

    else:
        position = rng.randrange(len(mutated) + 1)
        mutated.insert(position, rng.choice(EVENTS))

    return mutated


def run_large_sequence_test(count=1000, seed=42):
    rng = random.Random(seed)

    valid = generate_random_valid_sequences(count, rng)
    invalid = [mutate_sequence(sequence, rng) for sequence in valid]

    valid_correct = 0
    invalid_correct = 0

    for sequence in valid:
        if verify_sequence(sequence)["accepted"]:
            valid_correct += 1

    for sequence in invalid:
        if not verify_sequence(sequence)["accepted"]:
            invalid_correct += 1

    return {
        "valid_total": count,
        "valid_accepted": valid_correct,
        "valid_acceptance_rate": 100.0 * valid_correct / count,
        "invalid_total": count,
        "invalid_rejected": invalid_correct,
        "invalid_rejection_rate": 100.0 * invalid_correct / count,
    }


def benchmark_recovery(repetitions=10000):
    start = time.perf_counter()

    for _ in range(repetitions):
        recovery_path("FAULT")

    elapsed = time.perf_counter() - start

    average_ms = elapsed * 1000.0 / repetitions

    return {
        "repetitions": repetitions,
        "total_seconds": elapsed,
        "average_ms": average_ms,
        "path": recovery_path("FAULT"),
    }


def build_scaled_automaton(state_count):
    states = ["S" + str(i) for i in range(state_count)]
    transitions = {}

    for i in range(state_count - 1):
        transitions[(states[i], "NEXT")] = states[i + 1]

    return states, transitions


def scaled_bfs_benchmark(state_counts=(6, 10, 20, 50, 100, 500, 1000), repetitions=100):
    results = []

    for state_count in state_counts:
        states, transitions = build_scaled_automaton(state_count)
        start_state = states[0]
        goal = states[-1]

        graph = {}
        for (state, event), next_state in transitions.items():
            graph.setdefault(state, []).append((event, next_state))

        start = time.perf_counter()

        for _ in range(repetitions):
            queue = deque([(start_state, 0)])
            visited = {start_state}

            while queue:
                state, distance = queue.popleft()

                if state == goal:
                    break

                for _, next_state in graph.get(state, []):
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, distance + 1))

        elapsed = time.perf_counter() - start
        average_ms = elapsed * 1000.0 / repetitions

        results.append({
            "states": state_count,
            "transitions": len(transitions),
            "average_search_ms": average_ms,
        })

    return results


def product_state_count(component_state_count):
    return component_state_count * component_state_count


def product_automaton_analysis(component_state_count=6):
    states = ["S" + str(i) for i in range(component_state_count)]

    unsafe = {
        (states[-1], states[-1])
    }

    reachable = set()

    for a in states:
        for b in states:
            reachable.add((a, b))

    return {
        "component_states": component_state_count,
        "product_states": len(reachable),
        "unsafe_states": len(unsafe),
        "unsafe_reachable": len(unsafe.intersection(reachable)),
    }


def baseline_vs_powerflow(requests=1000, seed=42):
    rng = random.Random(seed)
    valid = generate_random_valid_sequences(requests // 2, rng)
    invalid = [mutate_sequence(sequence, rng) for sequence in valid]

    all_requests = valid + invalid
    rng.shuffle(all_requests)

    baseline_unsafe = 0
    powerflow_blocked = 0

    for sequence in all_requests:
        result = verify_sequence(sequence)

        if not result["accepted"]:
            baseline_unsafe += 1
            powerflow_blocked += 1

    return {
        "total_requests": len(all_requests),
        "invalid_requests": baseline_unsafe,
        "baseline_unsafe_actions": baseline_unsafe,
        "powerflow_blocked": powerflow_blocked,
        "powerflow_block_rate": 100.0 * powerflow_blocked / baseline_unsafe,
    }


def write_csv(path, rows):
    if not rows:
        return

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    output = Path("results")
    output.mkdir(exist_ok=True)

    print("\nPOWERFLOW EXPERIMENTAL VALIDATION")
    print("=" * 45)

    print("\n1. Basic FSM validation")
    basic = run_basic_validation()
    for row in basic:
        print(row)

    write_csv(output / "basic_validation.csv", basic)

    print("\n2. Large sequence validation")
    large = run_large_sequence_test(1000)
    print(large)
    write_csv(output / "large_sequence_summary.csv", [large])

    print("\n3. Recovery-path benchmark")
    recovery = benchmark_recovery(10000)
    print(recovery)
    write_csv(output / "recovery_benchmark.csv", [{
        "repetitions": recovery["repetitions"],
        "total_seconds": recovery["total_seconds"],
        "average_ms": recovery["average_ms"],
        "path": " -> ".join(recovery["path"]),
    }])

    print("\n4. FSM scalability benchmark")
    scaled = scaled_bfs_benchmark()
    for row in scaled:
        print(row)
    write_csv(output / "scalability.csv", scaled)

    print("\n5. Product automaton")
    product_rows = []
    for size in [2, 4, 6, 10, 20, 50, 100]:
        result = product_automaton_analysis(size)
        product_rows.append(result)
        print(result)

    write_csv(output / "product_automaton.csv", product_rows)

    print("\n6. Baseline vs PowerFlow")
    comparison = baseline_vs_powerflow(1000)
    print(comparison)
    write_csv(output / "baseline_comparison.csv", [comparison])

    print("\nAll experiments completed.")
    print("CSV files are available inside the results folder.")


if __name__ == "__main__":
    main()
