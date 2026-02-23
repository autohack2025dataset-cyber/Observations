import os
import pickle


# ── Constants ─────────────────────────────────────────────────────────────────

ALL_CLASS    = ['Normal', 'Attack']
ALL_SUBCLASS = ['Normal', 'DoS', 'Spoofing', 'Replay', 'Fuzzing', 'UDS_Spoofing']

LABEL_MAP = {
    0: 'Normal', 1: 'DoS', 2: 'Spoofing',
    3: 'Replay',  4: 'Fuzzing',  5: 'UDS_Spoofing'
}


# ── Helper Functions ───────────────────────────────────────────────────────────

def load_data(train_path, test_path):
    """
    Load preprocessed train/test CSV files.
    Returns train_df, test_df.
    """
    pass


def filter_train(df):
    """
    Apply training data filter to remove non-periodic UDS normal traffic.

    Filter logic:
      - Keep  : Fuzzing frames with Arbitration_ID >= 0x700 (1792)
      - Keep  : All frames with Arbitration_ID < 0x700 (1792)
      - Remove: UDS_Spoofing (Label == 5)

    This ensures the model is trained on periodic CAN traffic only,
    deliberately excluding aperiodic UDS normal traffic.
    """
    pass


def filter_test(df):
    """
    Apply test data filter.
    Remove UDS_Spoofing (Label == 5) from test set.
    UDS normal traffic (Label == 0, ID >= 0x700) is kept to evaluate
    how well the model handles unseen aperiodic traffic.
    """
    pass


def extract_features(df):
    """
    Separate feature matrix and target labels from dataframe.
    Drop non-feature columns: Class, Label, Timestamp, Interface, Data.
    Returns X (features), y_class (binary), y_subclass (multi-class).
    """
    pass


def save_model(model, filepath):
    """ Serialize model to pickle file. """
    pass


def load_model(filepath):
    """ Load model from pickle file. """
    pass


# ── Model Training ─────────────────────────────────────────────────────────────

def train_binary(X_train, y_class):
    """
    Train Stage-1 binary classifier (Normal vs Attack).
    Returns trained model.
    """
    pass


def train_multiclass(X_train, y_subclass):
    """
    Train Stage-2 multi-class classifier (attack type identification).
    Returns trained model.
    """
    pass


# ── Evaluation ────────────────────────────────────────────────────────────────

def evaluate(clf_binary, clf_multi, X_test, y_class_true, y_subclass_true):
    """
    Generate classification reports for both stages.

    Binary report   : precision / recall / F1 for Normal vs Attack
    Multi report    : precision / recall / F1 per attack type
    Confusion matrix: plotted for both stages

    Saves reports as .txt and confusion matrix as .jpg.
    """
    pass


def save_labeled_csv(test_df, pred_class, pred_subclass, output_path):
    """
    Append prediction columns to test dataframe and save as CSV.
    Columns added: Predict_Class, Predict_Label.
    Used for downstream analysis without retraining.
    """
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    """
    Execution flow:

    1. Load preprocessed train/test data
    2. Apply train filter  (remove non-periodic UDS normal + UDS_Spoofing)
    3. Apply test filter   (remove UDS_Spoofing only)
    4. Extract features
    5. Choose action:
         (a) Train new models → save as .pkl
         (b) Load existing .pkl models
    6. Evaluate → save reports + confusion matrix
    7. (Optional) Save labeled CSV for downstream analysis
    """
    pass


if __name__ == "__main__":
    main()
