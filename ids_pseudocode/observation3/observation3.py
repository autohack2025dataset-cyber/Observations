import os


# ── Constants ─────────────────────────────────────────────────────────────────

INTERFACES  = ['B-CAN', 'C-CAN', 'P-CAN']
MODEL_TYPES = ['RF', 'XGBoost']

LABEL_MAP = {
    0: 'Normal', 1: 'DoS', 2: 'Spoofing',
    3: 'Replay',  4: 'Fuzzing',  5: 'UDS_Spoofing'
}

# Feature columns from preprocessing.py
FEATURE_COLS = [
    'Arbitration_ID', 'DLC',
    'Prev_Interver', 'ID_Prev_Interver', 'Data_Prev_Interver',
    'ID_Frequency', 'Data_Frequency', 'Frequency_diff'
]
DROP_COLS = ['Label', 'Class', 'Interface', 'Timestamp', 'Data']


# ── Data Loading ──────────────────────────────────────────────────────────────

def load_data(train_path, test_path):
    """
    Load preprocessed train_proc.csv and test_proc.csv.
    Returns train_df, test_df.
    """
    pass


def extract_features(df):
    """
    Separate feature matrix X and label vector y from dataframe.
    Drop non-feature columns: Label, Class, Interface, Timestamp, Data.
    Returns X (features), y (Label).
    """
    pass


# ── Model ─────────────────────────────────────────────────────────────────────

class CANIDSModel:
    """Unified wrapper for RF / XGBoost / LSTM models."""

    def __init__(self, model_type='RF'):
        pass

    def build_model(self, input_dim, num_classes):
        """
        Build model architecture.

        RF      : RandomForestClassifier(n_estimators=100, max_depth=20)
        XGBoost : XGBClassifier(n_estimators=100, max_depth=10, lr=0.1)
        """
        pass

    def train(self, X_train, y_train, X_val=None, y_val=None):
        """
        Train the model.
        model.fit(X_train, y_train)
        """
        pass

    def predict(self, X_test):
        """
        Return predicted class indices.
        """
        pass

    def evaluate(self, X_test, y_test):
        """
        Compute accuracy, precision, recall, F1, confusion matrix, report.
        Returns metrics dict including y_pred for downstream per-interface breakdown.
        """
        pass


# ── Per-Interface Training ────────────────────────────────────────────────────

def train_and_evaluate_interface(train_df, test_df, interface_type, model_types=MODEL_TYPES):
    """
    Train and evaluate using only one interface's data.

    Steps:
      1. Filter train/test by Interface == interface_type
      2. extract_features() → X_train, X_test, y_train, y_test
      3. LabelEncoder + StandardScaler (fit on train only)
      4. Train/Val split (80/20, stratified)
      5. For each model_type: build → train → evaluate
    """
    pass


# ── Combined Training ─────────────────────────────────────────────────────────

def train_and_evaluate_combined(train_df, test_df, model_types=MODEL_TYPES):
    """
    Train on all interfaces combined, then break down results per interface.

    Steps:
      1. extract_features() on full train/test (no interface filter)
      2. LabelEncoder + StandardScaler (fit on train only)
      3. Train/Val split (80/20, stratified)
      4. For each model_type: build → train → evaluate
      5. Per-interface breakdown:
           for each interface in [B-CAN, C-CAN, P-CAN]:
               apply interface mask to y_test and y_pred → compute metrics
    """
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    """
    Execution flow:

    1. load_data() → train_df, test_df
    2. Per-interface loop:
         for interface in [B-CAN, C-CAN, P-CAN]:
             train_and_evaluate_interface()
    3. Combined training:
         train_and_evaluate_combined()    → includes per-interface breakdown
    4. Print summary table:
         interface × model → Accuracy / Precision / Recall / F1
    """
    pass


if __name__ == "__main__":
    main()
