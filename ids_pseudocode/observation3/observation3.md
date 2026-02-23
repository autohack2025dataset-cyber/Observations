# Observation 3 — Multi-Bus bus Analysis

Investigate whether training an IDS **per-bus** outperforms a **combined model**  
trained on all CAN bus buses simultaneously.

---

## Research Question

> Does mixing traffic from multiple CAN bus buses degrade IDS performance?

Each bus (B-CAN / C-CAN / P-CAN) carries different traffic patterns.  
A combined model must generalize across all three, which may cause domain confusion.

---

## Experiment Design

| Experiment | Training Data | Test Data | Purpose |
|---|---|---|---|
| **Per-bus** | Single bus only | Same bus | Per-bus performance baseline |
| **Combined** | All buses | Per-bus breakdown | Measure domain confusion |

---

## Input

Preprocessed features from `preprocessing.py`:

| Feature | Description |
|---|---|
| `Arbitration_ID` | CAN ID (hex → int) |
| `DLC` | Data Length Code |
| `Prev_Interver` | Global inter-arrival time |
| `ID_Prev_Interver` | Per-ID inter-arrival time |
| `Data_Prev_Interver` | Per-(ID, Data) inter-arrival time |
| `ID_Frequency` | Same-ID count in 10s window |
| `Data_Frequency` | Same-(ID, Data) count in 10s window |
| `Frequency_diff` | ID_Frequency − Data_Frequency |

---

## Models

| Model | Key Parameters |
|---|---|
| **RF** | n_estimators=100, max_depth=20 |
| **XGBoost** | n_estimators=100, max_depth=10, learning_rate=0.1 |

---

## Pipeline

```
train_proc.csv / test_proc.csv
  │
  ├── Per-bus loop  [B-CAN / C-CAN / P-CAN]
  │     train_and_evaluate_bus()
  │       ├── Filter by bus
  │       ├── LabelEncoder + StandardScaler (fit on train only)
  │       ├── Train/Val split (80/20, stratified)
  │       └── RF + XGBoost → evaluate
  │
  └── Combined training
        train_and_evaluate_combined()
          ├── Train on all buses
          ├── Evaluate on full test set
          └── Per-bus breakdown
                for each bus: mask test predictions → metrics
```

---

## Label Classes

| Code | Class |
|---|---|
| 0 | Normal |
| 1 | DoS |
| 2 | Spoofing |
| 3 | Replay |
| 4 | Fuzzing |
| 5 | UDS_Spoofing |

---

## Output

```
Console:
  ├── Per-bus summary  →  bus × model → Precision / Recall / F1
  └── Combined model breakdown  →  model × bus → same metrics
```

---

## Notes

- `StandardScaler` is fit on train data only to prevent data leakage
- Stratified split preserves class distribution in train/val
- Per-bus breakdown of the combined model is the core comparison for Observation 3
