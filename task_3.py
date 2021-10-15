import os
import json

from spacy.matcher import DependencyMatcher

from tests.utils.paths import CACHED_PREDICTIONS_DIR
from base_form_error import fill_matcher
from utils import check_file_exists, read_file
from pipeline import NLP


def prepare_matcher(nlp):
    matcher = DependencyMatcher(nlp.vocab)
    matcher = fill_matcher(matcher)
    return matcher


def set_sent_params(doc):
    for sent in doc.sents:
        if sent.get_extension("is_target") is None:
            sent.set_extension("is_target", default=False)
            break


if __name__ == "__main__":
    print('hello! please enter path to file')
    flag = True
    while flag:
        filename = input()
        if check_file_exists(filename):
            flag = False
        else:
            print('File not found, try another filepath')
    content = read_file(filename)
    matcher = prepare_matcher(NLP)
    doc = NLP(content)
    set_sent_params(doc)
    matches = matcher(doc)
    for sent in doc.sents:
        if sent._.is_target:
            print(sent.text)
    test_cache = []
    for sent in doc.sents:
        test_cache.append({"text": sent.text, "is_target": sent._.is_target})
    test_file_path = os.path.join(CACHED_PREDICTIONS_DIR, "task_3_cached_predictions.json")
    with open(test_file_path, 'w+', encoding="utf-8") as f:
        json.dump(test_cache, f, ensure_ascii=False, indent=2)
