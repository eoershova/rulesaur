import json
import unittest

from parameterized import parameterized
from tests.base_tester import BaseTester
from tests.utils.paths import TASK_2_TESTS_PATH, TASK_2_CACHED_PREDICTIONS_PATH


class Task3Tester(BaseTester):

    with open(TASK_2_TESTS_PATH, encoding='utf-8') as f:
        tests = json.load(f)

    def setUp(self) -> None:
        self.prediction = self._get_prediction_from_path(TASK_2_CACHED_PREDICTIONS_PATH)

    @parameterized.expand(tests)
    def test_volume(self, label):
        self._test_individual_cases(
            label=label
        )


if __name__ == "__main__":
    unittest.main()

