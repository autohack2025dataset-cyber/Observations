# CAN Bus IDS Preprocessing

Preprocessing pipeline for the **AutoHack IDS Dataset**.  
Converts raw CAN bus log files into feature-engineered datasets for intrusion detection model training.

---

## Dataset Structure

```
dataset/
└── AutoHack_Dataset/
    └── Interface/
        ├── train/
        │   ├── autohack_train_data_interface.csv
        │   └── autohack_train_label_interface.csv
        └── test/
            ├── autohack_test_data_interface.csv
            └── autohack_test_label_interface.csv
```

### Raw Data Format

| Column | Type | Example | Description |
|---|---|---|---|
| `Interface` | str | `C-CAN` | CAN bus interface (P-CAN / B-CAN / C-CAN) |
| `Timestamp` | float | `0.00059` | Capture time in seconds |
| `Arbitration_ID` | hex str | `"329"` | CAN frame identifier |
| `DLC` | int | `8` | Data Length Code (0–8 bytes) |
| `Data` | hex str | `"40 B2 81 14"` | Payload bytes (space-separated hex) |
| `Label` | str | `"Normal"` | Attack class label |

### Label Classes

| Label | Code | Description |
|---|---|---|
| `Normal` | 0 | Normal periodic CAN traffic |
| `DoS` | 1 | Denial of Service (Flooding) attack |
| `Spoofing` | 2 | CAN ID spoofing attack |
| `Replay` | 3 | Replay attack |
| `Fuzzing` | 4 | Random frame injection |
| `Spoofing_UDS_*` | 5 | UDS-based spoofing (diagnostic protocol) |

---

## Processing Pipeline

### Step 1 — Label Encoding
String labels are mapped to integer class codes for model input.

```
"Normal" → 0,  "DoS" → 1,  "Spoofing" → 2,
"Replay" → 3,  "Fuzzing" → 4,  "Spoofing_UDS_*" → 5
```

### Step 2 — Data Field Conversion
The `Data` field (space-separated hex bytes) is parsed into a single integer value.

```
"40 B2 81 14"  →  remove spaces  →  "40B28114"  →  int(0x40B28114)
```

Missing values are filled with `"00"` before conversion.

### Step 3 — Arbitration ID Conversion
The `Arbitration_ID` hex string is converted to integer.

```
"7FF"  →  2047
"329"  →  809
```

> ⚠️ Direct `int()` conversion without base=16 will cause errors. Always use `int(x, 16)`.

### Step 4 — Time Interval Features
Three inter-arrival time (IAT) features are computed to capture periodicity patterns.

| Feature | Description |
|---|---|
| `Prev_Interver` | Time elapsed since the **previous frame** (global, any ID) |
| `ID_Prev_Interver` | Time elapsed since the **previous frame with the same Arbitration_ID** |
| `Data_Prev_Interver` | Time elapsed since the **previous frame with the same (ID, Data) pair** |

- NaN values (first occurrence per group) are filled with `TIME_SIZE` (default: 10s)
- `ID_Prev_Interver` captures the **periodicity** of each CAN ID
- `Data_Prev_Interver` captures **payload repetition patterns**

### Step 5 — Rolling Frequency Features
Frequency of occurrence within a sliding time window (`WINDOW_SIZE = 10s`).

| Feature | Description |
|---|---|
| `ID_Frequency` | Count of frames with the **same Arbitration_ID** in the last 10s |
| `Data_Frequency` | Count of frames with the **same (ID, Data) pair** in the last 10s |
| `Frequency_diff` | `ID_Frequency − Data_Frequency` |

- High `ID_Frequency` with low `Data_Frequency` → many different payloads for the same ID → potential Fuzzing
- `Frequency_diff` quantifies payload diversity per ID

### Step 6 — Cleanup
Drop intermediate and raw columns that are no longer needed:
`DateTime`, `Timestamp`, `Data`, `Interface`

---

## Output Features

| Feature | Type | Description |
|---|---|---|
| `Arbitration_ID` | int | CAN ID (hex → int) |
| `DLC` | int | Data Length Code |
| `Prev_Interver` | float | Global inter-arrival time |
| `ID_Prev_Interver` | float | Per-ID inter-arrival time |
| `Data_Prev_Interver` | float | Per-(ID, Data) inter-arrival time |
| `ID_Frequency` | float | Same-ID count in 10s window |
| `Data_Frequency` | float | Same-(ID,Data) count in 10s window |
| `Frequency_diff` | float | ID_Frequency − Data_Frequency |
| `Label` | int | Attack class (0–5) |

---

## Output Files

```
source/
└── AutoHack2025/
    ├── train_proc.csv
    └── test_proc.csv
```

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `TIME_SIZE` | `10` | Fill value for NaN intervals (seconds) |
| `WINDOW_SIZE` | `"10s"` | Rolling window size for frequency features |

---

## Notes

- **UDS Traffic (0x700–0x7FF)**: Arbitration IDs in the 700-series correspond to UDS (Unified Diagnostic Services) diagnostic protocol messages. These are **aperiodic** by nature and play a key role in IDS dataset quality analysis.
- **Interface separation**: The raw dataset contains three CAN bus interfaces (P-CAN, B-CAN, C-CAN). The `Interface` column is dropped after processing but can be used for per-bus analysis before the cleanup step.
