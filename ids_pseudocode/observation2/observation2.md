# Observation 2 — IDS Model with UDS Traffic Filter

This module implements the two-stage IDS model used in **Observation 2**,  
which investigates the impact of UDS (Unified Diagnostic Services) traffic  
on intrusion detection performance.

---

## Research Question

> What happens when a CAN bus IDS is trained **without** aperiodic UDS normal traffic, 

The model is deliberately trained only on periodic CAN traffic.  
At test time, it encounters UDS normal traffic it has never seen —  
revealing whether the IDS misclassifies legitimate diagnostic frames as attacks.

---

## Filter Design

The core of Observation 2 is the **asymmetric train/test filter**.

### Train Filter

| Frames | Action | Reason |
|---|---|---|
| `Normal` + `ID < 0x700` | Keep | Standard periodic CAN traffic |
| `All attacks` + `ID < 0x700` | Keep | Standard attack patterns |
| `Fuzzing` + `ID >= 0x700` | Keep | UDS-range Fuzzing is a valid attack |
| `Normal` + `ID >= 0x700` | Remove | Aperiodic UDS diagnostic traffic — excluded from training |
| `UDS_Spoofing` (Label 5) | Remove | Out of scope for this observation |

```python
# ids.py implementation
df_label4_high_id = df[df["Label"] == 4][df["Arbitration_ID"] >= 1792]  # Fuzzing in UDS range
df_low_id         = df[df["Arbitration_ID"] < 1792]                      # all non-UDS frames
train = concat([df_label4_high_id, df_low_id])
train = train[train["Label"] != 5]                                        # remove UDS_Spoofing
```

### Test Filter

| Frames | Action | Reason |
|---|---|---|
| `Normal` + `ID >= 0x700` (UDS Normal) | Keep | **Intentionally kept** to measure FP rate on unseen traffic |
| All attack frames (Label 1–4) | Keep | Standard evaluation |
| `UDS_Spoofing` (Label 5) | Remove | Out of scope for this observation |

```python
# ids.py implementation
test = df[df['Label'] != 5]
```

> **Key asymmetry**: Train removes UDS Normal, Test keeps it.  
> This is intentional — the model is evaluated on traffic it was never trained on,  
> directly measuring false positive behavior in a realistic deployment scenario.

---

## Model Architecture

### Stage 1 — Binary Classification
- Task: Normal (0) vs Attack (1)
- Model: RandomForest
- Saved as: `{name}_C.pkl`

### Stage 2 — Multi-class Classification
- Task: Attack type identification (Normal / Flooding / Spoofing / Replay / Fuzzing)
- Model: RandomForest available as alternative
- Saved as: `{name}_S.pkl`
- RF hyperparameters: `n_estimators=130`, `max_depth=30`

---

## Execution Flow

```
1. define_file()
   ├── Load train_proc.csv / test_proc.csv
   ├── Apply filter_train()  →  periodic traffic only
   └── Apply filter_test()   →  UDS Normal retained

2. choice_action()
   ├── "Train XGBoost"  →  train_model_c() + train_model_s() + save_models()
   └── "Use Model"      →  use_model()  (load existing .pkl)

3. save_report()
   ├── Predict on test set
   ├── Save Binary report.txt   (Stage-1)
   └── Save Multi report.txt    (Stage-2)

4. choice_action()
   ├── "Save Label"    →  save_label()  (append predictions to test CSV)
   └── "Only Report"   →  skip

5. show_confusion_matrix()
   └── Plot and save confusion matrices as .jpg
```

---

## Output Files

```
report/IDS/{name}/
├── {name} Binary report.txt     ← Stage-1 Normal vs Attack
├── {name} Multi report.txt      ← Stage-2 per-class F1
└── {name}_labeled.csv           ← test data + Predict_Class + Predict_Label

IDS_Model/IDS/
├── {name}_C.pkl                 ← Stage-1 binary model
└── {name}_S.pkl                 ← Stage-2 multi-class model
```

---

## Expected Behavior

Because UDS Normal traffic is **excluded from training** but **included in testing**:

- The model has never learned what aperiodic diagnostic traffic looks like
- UDS Normal frames may be misclassified as attacks (false positives)
- This false positive rate is a key metric for Observation 2

| Metric | Expected |
|---|---|
| Normal (periodic) | High recall |
| Normal (UDS, aperiodic) | Lower recall — misclassified as attack |
| Fuzzing | High F1 |
| Replay / Spoofing | Lower F1 — harder to distinguish from Normal |

---

## Notes

- `Arbitration_ID >= 0x700` (1792) corresponds to the UDS diagnostic protocol range
- UDS frames are **aperiodic** — they do not follow fixed transmission intervals
- The `Frequency_diff` and `ID_Prev_Interver` features are most affected by UDS traffic
- RandomForest is available as an alternative to XGBoost via commented-out lines in `ids.py`
