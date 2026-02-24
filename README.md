# IDS Pseudocode — AutoHack Dataset

This repository provides an IDS (Intrusion Detection System) implementation guide  
based on the **AutoHack dataset**.  
The pseudocode is designed to ensure reproducibility of experiments described in the paper.

---

## Repository Structure

```
ids_pseudocode/
├── preprocessing/
│   ├── preprocessing.py       ← Feature extraction skeleton
│   └── preprocessing.md       ← Preprocessing pipeline description
├── observation1/
│   ├── observation1.py        ← Attack classification difficulty analysis
│   └── observation1.md
├── observation2/
│   ├── observation2.py        ← UDS traffic filter experiment
│   └── observation2.md
├── observation3/
│   ├── observation3.py        ← Multi-bus training comparison
│   └── observation3.md
└── README.md
```

---

## Dataset

All experiments use the **AutoHack IDS Dataset**.

```
Interface/
├── train/
│   ├── autohack_train_data_interface.csv
│   └── autohack_train_label_interface.csv
└── test/
    ├── autohack_test_data_interface.csv
    └── autohack_test_label_interface.csv
```

| Label | Class | Description |
|---|---|---|
| 0 | Normal | Periodic CAN traffic |
| 1 | DoS | Denial of Service (Flooding) |
| 2 | Spoofing | CAN ID spoofing |
| 3 | Replay | Replay attack |
| 4 | Fuzzing | Random frame injection |
| 5 | UDS_Spoofing | UDS-based spoofing |

---

## Preprocessing

> `preprocessing/preprocessing.py` · `preprocessing/preprocessing.md`

Converts raw CAN bus log CSV files into feature-engineered datasets  
for IDS model training and evaluation.

**Output**: `train_proc.csv` / `test_proc.csv`

| Feature | Description |
|---|---|
| `Arbitration_ID` | CAN ID (hex → int) |
| `DLC` | Data Length Code |
| `Prev_Interver` | Global inter-arrival time |
| `ID_Prev_Interver` | Per-ID inter-arrival time |
| `Data_Prev_Interver` | Per-(ID, Data) inter-arrival time |
| `ID_Frequency` | Same-ID count in 10s rolling window |
| `Data_Frequency` | Same-(ID, Data) count in 10s rolling window |
| `Frequency_diff` | ID_Frequency − Data_Frequency |

---

## Observations

### Observation 1 — Attack Classification Difficulty

> `observation1/observation1.py` · `observation1/observation1.md`

Analyzes classification difficulty across attack types using RF and XGBoost.  
Demonstrates that Replay and Spoofing attacks are significantly harder to detect  
than DoS and Fuzzing due to their similarity to normal periodic traffic.

---

### Observation 2 — UDS Traffic Filter

> `observation2/observation2.py` · `observation2/observation2.md`

Investigates the impact of UDS (Unified Diagnostic Services) traffic  
on IDS detection performance.

The model is trained **without** aperiodic UDS normal traffic (Arbitration_ID ≥ 0x700),  
then evaluated **with** it — measuring false positive rate on unseen diagnostic traffic.

| | Train | Test |
|---|---|---|
| UDS Normal (ID ≥ 0x700) | ❌ Excluded | ✅ Included |
| UDS_Spoofing (Label 5) | ❌ Excluded | ❌ Excluded |

---

### Observation 3 — Multi-Bus Analysis

> `observation3/observation3.py` · `observation3/observation3.md`

Compares per-bus training against a combined model trained on all buses.

| Experiment | Training Data | Evaluation |
|---|---|---|
| Per-bus | Single bus (B-CAN / C-CAN / P-CAN) | Same bus |
| Combined | All buses | Per-bus breakdown |

---

## Reproducibility

The pseudocode skeletons in this repository define the exact experiment structure  
used in the paper. Each `pass` block corresponds to an implementation step  
described in the accompanying `.md` file.

To reproduce results:
1. Run `preprocessing/preprocessing.py` to generate `train_proc.csv` / `test_proc.csv`
2. Run each observation script using the preprocessed files as input
