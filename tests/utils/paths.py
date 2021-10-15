from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_TESTS_DIR = BASE_DIR.joinpath('data')
RAW_DATA_DIR = DATA_TESTS_DIR.joinpath('raw_data')
CACHED_PREDICTIONS_DIR = DATA_TESTS_DIR.joinpath('cached_predictions')
TASK_3_CACHED_PREDICTIONS_PATH = CACHED_PREDICTIONS_DIR.joinpath('task_3_cached_predictions.json')
TASK_2_CACHED_PREDICTIONS_PATH = CACHED_PREDICTIONS_DIR.joinpath('task_2_cached_predictions.json')
TASK_3_TESTS_PATH = DATA_TESTS_DIR.joinpath('task_3_test_data.json')
TASK_2_TESTS_PATH = DATA_TESTS_DIR.joinpath('task_2_test_data.json')
