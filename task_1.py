from spacy.matcher import DependencyMatcher

from negation import fill_matcher, fill_second_matcher
from pipeline import NLP


def prepare_matcher(nlp):
    matcher = DependencyMatcher(nlp.vocab)
    matcher = fill_matcher(matcher)
    return matcher


def prepare_second_matcher(nlp):
    matcher = DependencyMatcher(nlp.vocab)
    matcher = fill_second_matcher(matcher)
    return matcher


def set_sent_params(doc):
    for sent in doc.sents:
        if sent.get_extension("is_negatable") is None:
            sent.set_extension("is_negatable", default=True)
            sent.set_extension("negated_version", default=None)
            break


if __name__ == "__main__":
    print('hello!')
    while True:
        print('Enter the sentence, use empty sequence to stop')
        content = input()
        if not content:
            print('thanks for the attention, bye!')
            break
        doc = NLP(content)
        set_sent_params(doc)
        unnegatable_sents_detector = prepare_matcher(NLP)
        _ = unnegatable_sents_detector(doc)
        negation_premises_detector = prepare_second_matcher(NLP)
        _ = negation_premises_detector(doc)
        for sent in doc.sents:
            if sent._.negated_version is not None:
                print(sent._.negated_version)
            elif sent._.is_negatable:
                print("Sorry, could not add negation although it might be possible to do so")
            else:
                print("Could not add negation to the sentence that already has negation or positive polarity items")
            print()
