from pathlib import Path

BASE_DIR = Path("..")
ENV_FILE = ".env"

DATASET_DIR = BASE_DIR / "data"
RAW_DIR = DATASET_DIR / "raw"
TRAIN_TEST = RAW_DIR / "kaggle/diabetes.csv"

PROCESSED_DIR = DATASET_DIR / "processed"
TRAIN_TEST_PROCESSED = PROCESSED_DIR / "diabetes.csv"

PLOTS = BASE_DIR / "plots"
SAVE_MODELS = BASE_DIR / "models"

EDA_ARTIFACTS = BASE_DIR / "artifacts" / "eda"
PREPROCESSING_ARTIFACTS = BASE_DIR / "artifacts" / "preprocessing"
ML_ARTIFACTS = BASE_DIR / "artifacts" / "ml"
DL_ARTIFACTS = BASE_DIR / "artifacts" / "dl"


def path_maker(filename: str, path: Path) -> Path:
    """
    Creates a file path by combining the given directory and filename.
    If the directory does not exist, it is created.

    Parameters:
    filename (str): The name of the file.
    path (Path): The directory where the file should be located.

    Returns:
    Path: The full path to the file.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path / filename
