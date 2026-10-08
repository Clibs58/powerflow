# PowerFlow: Automaton-Based Formal Verification and Recovery of Smart Grid Fault States

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

The expected logical outcomes are:

- Valid sequences should be accepted.
- Invalid sequences should be rejected.
- FAULT should have a legal recovery path.
- The product automaton should have n² states for two components with n states each.
- PowerFlow should block invalid transitions.

Execution time values are machine-dependent and must be reported from your own run.

