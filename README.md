# PowerFlow — Automaton-Based Formal Verification and Recovery of Smart Grid Fault States

This is the experimental prototype for the Theory of Computation project.

## What it demonstrates

1. DFA/FSM transition verification
2. Valid and invalid event-sequence testing
3. BFS-based recovery-path search
4. FSM scalability benchmarking
5. Product automaton state-space analysis
6. Baseline vs automaton-verified transition blocking
7. CSV experimental results
8. Graph generation

## Important scope

This is a software-based Theory of Computation experiment.

It does NOT simulate real electrical voltage, current, protection relays, load flow, or physical grid hardware.

The experiment validates the formal automaton and recovery-verification layer.

## Project structure

```text
PowerFlow_Experiment/
│
├── powerflow.py
├── generate_graphs.py
├── requirements.txt
├── README.md
├── results/
└── graphs/
```

## Step 1 — Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\activate.bat
```

or run the Python commands directly without activating the environment.

## Step 2 — Install dependencies

```powershell
pip install -r requirements.txt
```

## Step 3 — Run the experiments

```powershell
python powerflow.py
```

This creates:

```text
results/
├── basic_validation.csv
├── large_sequence_summary.csv
├── recovery_benchmark.csv
├── scalability.csv
├── product_automaton.csv
└── baseline_comparison.csv
```

## Step 4 — Generate graphs

```powershell
python generate_graphs.py
```

This creates:

```text
graphs/
├── 01_sequence_verification.png
├── 02_recovery_scalability.png
├── 03_product_state_growth.png
├── 04_unsafe_transition_blocking.png
└── 05_recovery_path.png
```

## Step 5 — Check the results

Do not manually type experimental numbers into the report.

Copy the actual values produced by your run into Section 8.

The expected logical outcomes are:

- Valid sequences should be accepted.
- Invalid sequences should be rejected.
- FAULT should have a legal recovery path.
- The product automaton should have n² states for two components with n states each.
- PowerFlow should block invalid transitions.

Execution time values are machine-dependent and must be reported from your own run.

## Recommended screenshots

Take screenshots of:

1. Terminal showing the experiment completed.
2. `basic_validation.csv`.
3. `scalability.csv`.
4. `product_automaton.csv`.
5. The five generated graphs.
6. The Python code for the DFA and recovery algorithm.

## Suggested Section 8 structure

### 8.1 Experimental Setup
Python-based symbolic FSM simulator running on a personal computer.

### 8.2 Transition Verification
Report valid-sequence acceptance and invalid-sequence rejection.

### 8.3 Recovery Path Search
Report the shortest path from FAULT to NORMAL and average search time.

### 8.4 Scalability
Report recovery search time as the number of states increases.

### 8.5 Product Automaton
Report growth of the combined state space.

### 8.6 Baseline Comparison
Compare unsafe requests against the number blocked by PowerFlow.

### 8.7 Discussion
Explain that these experiments validate the formal verification mechanism, not physical electrical-grid performance.
