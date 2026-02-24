# Observation 1 — IDS Model 

Two-stage intrusion detection system for CAN bus traffic using machine learning.  
Trained and evaluated on the **AutoHack IDS Dataset**.

---

## Overview

| Stage | Task | Output |
|---|---|---|
| **Stage 1 (Binary)** | Normal vs Attack | `0` Normal / `1` Attack |
| **Stage 2 (Multi-class)** | Attack type identification | 6 attack classes |

### Attack Classes

| Code | Class | Description |
|---|---|---|
| 0 | `Normal` | Normal periodic CAN traffic |
| 1 | `DoS` | Denial of Service attack |
| 2 | `Spoofing` | CAN ID spoofing attack |
| 3 | `Replay` | Replay attack |
| 4 | `Fuzzing` | Random frame injection |
| 5 | `UDS_Spoofing` | UDS-based spoofing (diagnostic protocol) |

---

## Data Filter Design

A key design decision in this work is the **asymmetric train/test filter** for UDS traffic.

### Train Filter
| Condition | Action | Reason |
|---|---|---|
| `Arbitration_ID >= 0x700` + `Label == Normal` | **Remove** | Aperiodic UDS normal traffic — not representative of periodic CAN behavior |
| `Arbitration_ID >= 0x700` + `Label == Fuzzing` | **Keep** | UDS-range Fuzzing is a valid attack pattern |
| `Label == UDS_Spoofing (5)` | **Remove** | Excluded from training scope |
| All other frames | **Keep** | Standard periodic CAN traffic |

### Test Filter
| Condition | Action | Reason |
|---|---|---|
| `Label == UDS_Spoofing (5)` | **Remove** | Excluded from evaluation scope |
| `Label == Normal` + `Arbitration_ID >= 0x700` | **Keep** | Kept to measure false positive rate on unseen UDS normal traffic |

> This asymmetric filter is intentional: by withholding UDS normal traffic from training,  
> we can measure how the model handles aperiodic diagnostic traffic at test time —  
> a key evaluation scenario for real-world IDS deployment.

---

## Pipeline

```
train_proc.csv ──▶ filter_train() ──▶ train_binary()      ──▶ clf_binary.pkl
                                  └──▶ train_multiclass()  ──▶ clf_multi.pkl

test_proc.csv  ──▶ filter_test()  ──▶ evaluate()
                                       ├── Binary report.txt
                                       ├── Multi report.txt
                                       ├── confusion_matrix.jpg
                                       └── labeled.csv  (Predict_Class, Predict_Label)
```

---

## Function Reference

### Data

| Function | Description |
|---|---|
| `load_data(train_path, test_path)` | Load preprocessed train/test CSV files |
| `filter_train(df)` | Apply train filter (remove non-periodic UDS normal + UDS_Spoofing) |
| `filter_test(df)` | Apply test filter (remove UDS_Spoofing only) |
| `extract_features(df)` | Separate feature matrix X and target labels y |

### Model

| Function | Description |
|---|---|
| `train_binary(X, y)` | Train Stage-1 binary classifier |
| `train_multiclass(X, y)` | Train Stage-2 multi-class classifier |
| `save_model(model, path)` | Serialize model to `.pkl` |
| `load_model(path)` | Load model from `.pkl` |

### Evaluation

| Function | Description |
|---|---|
| `evaluate(clf_b, clf_m, X, y_c, y_s)` | Generate reports and confusion matrices |
| `save_labeled_csv(df, pred_c, pred_s, path)` | Save test data with prediction columns appended |

---

## Input Features

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

## Output Files

```
report/IDS/{name}/
├── {name} Binary report.txt     ← Stage-1 classification report
├── {name} Multi report.txt      ← Stage-2 classification report
└── {name}_labeled.csv           ← Test data + Predict_Class + Predict_Label

IDS_Model/IDS/
├── {name}_C.pkl                 ← Stage-1 binary model
└── {name}_S.pkl                 ← Stage-2 multi-class model
```

---

## Notes

- **UDS Traffic (0x700–0x7FF)**: Frames in the 700-series correspond to UDS (Unified Diagnostic Services) diagnostic protocol messages. These are aperiodic by nature and behave differently from standard periodic CAN traffic, making them a critical edge case for IDS evaluation.
- **Model choice**: XGBoost is used by default. Random Forest parameters are provided as commented alternatives (`rf_n_estimators`, `rf_max_depth`).
- **Labeled CSV**: Saving predictions alongside raw test data enables fast re-evaluation and visualization without retraining.
