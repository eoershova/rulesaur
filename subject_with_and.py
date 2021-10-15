from base_form_error import unpack_match, get_token_attribute
from negation import check_verb_has_auxiliary_verbs_as_children, identify_head_auxiliary


subject_with_and_pattern_1 = [
    {
        "RIGHT_ID": "anchor_verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, }
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "noun_subject",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "POS": {"IN": ["NOUN", "PROPN"]}},
    },
    {
        "LEFT_ID": "noun_subject",
        "REL_OP": ">",
        "RIGHT_ID": "and",
        "RIGHT_ATTRS": {"DEP": "cc", "LEMMA": "and"},
    },
    {
        "LEFT_ID": "noun_subject",
        "REL_OP": ">",
        "RIGHT_ID": "noun_subject_conj",
        "RIGHT_ATTRS": {"DEP": "conj", "POS": {"IN": ["NOUN", "PROPN"]}},
    }
]


def check_verb_is_singular_or_past(verb):
    verb_morph = get_token_attribute(verb, "morph")
    verb_lemma = get_token_attribute(verb, "lemma")
    if "Number=Sing" in verb_morph or ("Tense=Past" in verb_morph and verb_lemma != "be"):
        return True
    return False


def process_pattern(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], 'sent')
    verb = matched_tokens[0]
    has_auxiliary_children = check_verb_has_auxiliary_verbs_as_children(verb)
    if has_auxiliary_children:
        _, head = identify_head_auxiliary(verb)
        sent._.is_target = check_verb_is_singular_or_past(head)
    else:
        sent._.is_target = check_verb_is_singular_or_past(verb)


def fill_matcher(matcher):
    matcher.add("BASIC PATTERN", [subject_with_and_pattern_1], on_match=process_pattern)
    return matcher
