import re
import json

from unittest import TestCase


class BaseTester(TestCase):
    main_attributes = {'is_target'}

    @staticmethod
    def _get_prediction_from_path(path_to_prediction_json):
        with open(path_to_prediction_json, encoding='utf-8') as f:
            prediction = json.load(f)
        return prediction

    def _test_individual_cases(self, label):
        self._test_parsing_recall(
            pred_labels=self.prediction,
            corr_label=label
        )

    def _test_parsing_recall(self, pred_labels, corr_label):
        # print(corr_label['text'])
        # print(pred_labels)
        matching_parsed_text = [item for item in pred_labels if self.remove_spaces(item['text']) ==
                                self.remove_spaces(corr_label['text'])]
        matching_parsed_text = matching_parsed_text[0]
        pred_label = matching_parsed_text["is_target"]
        correct_label = corr_label["is_target"]
        error_message = f'\nFailed while parsing!' \
                        f'\n{corr_label["text"]} \n'\
                        f'must be assigned label {corr_label["is_target"]}'
        self.assertEqual(pred_label, correct_label, error_message)

    @staticmethod
    def remove_spaces(value: str):
        value_without_spaces = re.sub(r'[\s\n]', '', value)
        return value_without_spaces
