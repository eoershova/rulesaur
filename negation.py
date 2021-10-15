from utils import read_file
from base_form_error import unpack_match, get_token_attribute

lexical_negators = read_file('lexical_negators.txt').split('\n')
SHORT_FORMS_OF_TO_BE = ["'s", "'m", "'re"]
FULL_FORMS_OF_TO_BE_TO_NEGATION_MAPPING = {
                                            "am": "am not",
                                           "are": "aren't",
                                           "is": "isn't",
                                           "was": "wasn't",
                                           "were": "weren't"}

SHORT_FORMS_OF_TO_HAVE_TO_NEGATION_MAPPING = {
    "'s": " has not",
    "'ve": " have not",
    "'d": " had not"
}

EVERY_DERIVATIVES_TO_NEGATION_MAPPING = {
    "everyone": "no one",
    "everybody": "nobody"
}

AUXILIARY_TO_NEGATION_MAPPING = {
    "should": "shouldn't",
    "shall": "shall not",
    "can": "can't",
    "must": "mustn't",
    "have": "haven't",
    "has": "hasn't",
    "do": "don't",
    "does": "doesn't",
    "could": "couldn't",
    "may": "may not",
    "might": "might not",
    "will": "won't",
    "would": "wouldn't",
    "am": "am not",
    "are": "aren't",
    "is": "isn't",
    "was": "wasn't",
    "were": "weren't",
    "had": "hadn't"
}

SOME_DERIVATIVES = ["some", "somebody", "someone", "something"]

# lexical negation in form of never, nowhere etc
negation_pattern_1 = [
    {
        "RIGHT_ID": "lexal_negative",
        "RIGHT_ATTRS": {"LEMMA": {"IN": lexical_negators}}
    }]

# positive polarity items that cannot me negated
negation_pattern_2 = [{
    "RIGHT_ID": "pp_item",
    "RIGHT_ATTRS": {"LEMMA": {"IN": ['somewhat', 'already']}}
}]

# verb + not"
negation_pattern_3 = [
    {
        "RIGHT_ID": "anchor_verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "not",
        "RIGHT_ATTRS": {"DEP": "neg"},
    }
]

# question with ?
negation_pattern_4 = [
    {
        "RIGHT_ID": "question_mark",
        "RIGHT_ATTRS": {"TEXT": "?"}
    }
]


def process_anti_patterns(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], 'sent')
    sent._.is_negatable = False


def fill_matcher(matcher):
    matcher.add("LEXICAL", [negation_pattern_1], on_match=process_anti_patterns)
    matcher.add("PPI", [negation_pattern_2], on_match=process_anti_patterns)
    matcher.add("VERB+NOT", [negation_pattern_3], on_match=process_anti_patterns)
    matcher.add("QUESTION", [negation_pattern_4], on_match=process_anti_patterns)
    return matcher


# to be is the only verb
negation_transformation_pattern_1 = [{
    "RIGHT_ID": "auxiliary",
    "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}, "LEMMA": {"IN": ["be"]}}
}]

# everyone/everybody + verbs excluding to be
negation_transformation_pattern_2 = [
    {
        "RIGHT_ID": "everybody",
        "RIGHT_ATTRS": {"LEMMA": {"IN": ["everybody", "everyone"]}}
    }]

# auxiliary is the only verb excluding to be
negation_transformation_pattern_3 = [{
    "RIGHT_ID": "auxiliary",
    "RIGHT_ATTRS": {"POS": {"IN": ["AUX"]}, "LEMMA": {"NOT_IN": ['be']}}
}]

# lexical verb
negation_transformation_pattern_4 = [
    {
        "RIGHT_ID": "lexical_verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
    }]


def check_verb_has_other_verbs_as_children(verb):
    children = get_token_attribute(verb, "children")
    for child in children:
        child_pos = get_token_attribute(child, "pos")
        if child_pos in ["VERB", "AUX"]:
            return True
    return False


def check_verb_has_auxiliary_verbs_as_children(verb):
    children = get_token_attribute(verb, "children")
    for child in children:
        child_pos = get_token_attribute(child, "pos")
        if child_pos in ["AUX"]:
            return True
    return False


def check_verb_has_other_verbs_as_ancestors(verb):
    ancestors = get_token_attribute(verb, "ancestors")
    for ancestor in ancestors:
        ancestor_pos = get_token_attribute(ancestor, "pos")
        if ancestor_pos in ["VERB", "AUX"]:
            return True
    return False


def format_white_space_after_token(token, substitute):
    token_text = get_token_attribute(token, "text")
    token_text_with_ws = get_token_attribute(token, "text_with_ws").lower()
    is_title = token_text.istitle()
    if is_title:
        substitute = substitute.capitalize()
    if token_text == token_text_with_ws:
        return substitute
    return substitute + " "


def add_not_token_to_sent(sent):
    proc_tokens = []
    for token in sent:
        token_text = get_token_attribute(token, "text")
        token_text_with_ws = get_token_attribute(token, "text_with_ws")
        if token_text in SHORT_FORMS_OF_TO_BE:
            proc_tokens.append(token_text_with_ws)
            proc_tokens.append(format_white_space_after_token(token, "not"))
        else:
            proc_tokens.append(token_text_with_ws)
    new_sent_text = "".join(proc_tokens)
    return new_sent_text


def negate_full_form_of_to_be(sent):
    proc_tokens = []
    for token in sent:
        token_text = get_token_attribute(token, "text")
        token_text_with_ws = get_token_attribute(token, "text_with_ws")
        to_be_mapping = FULL_FORMS_OF_TO_BE_TO_NEGATION_MAPPING.get(token_text)
        if to_be_mapping is not None:
            proc_tokens.append(format_white_space_after_token(token, to_be_mapping))
        else:
            proc_tokens.append(token_text_with_ws)
    new_sent_text = "".join(proc_tokens)
    return new_sent_text


def negate_to_be(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], "sent")
    if not sent._.is_negatable or sent._.negated_version is not None:
        return
    verb = matched_tokens[0]
    has_ancestors = check_verb_has_other_verbs_as_ancestors(verb)
    has_children = check_verb_has_other_verbs_as_children(verb)
    if has_ancestors or has_children:
        return
    verb_text = get_token_attribute(verb, "text")
    if verb_text in SHORT_FORMS_OF_TO_BE:
        sent._.negated_version = add_not_token_to_sent(sent)
    else:
        sent._.negated_version = negate_full_form_of_to_be(sent)


def negate_everyone_pattern(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], 'sent')
    if not sent._.is_negatable or sent._.negated_version is not None:
        return
    sent._.negated_version = remap_tokens(sent, EVERY_DERIVATIVES_TO_NEGATION_MAPPING)


def remap_tokens(sent, mapping_dict):
    proc_tokens = []
    for token in sent:
        token_text = get_token_attribute(token, "text").lower()
        token_text_with_ws = get_token_attribute(token, "text_with_ws")
        mapping = mapping_dict.get(token_text)
        if mapping is not None:
            proc_tokens.append(format_white_space_after_token(token, mapping))
        else:
            proc_tokens.append(token_text_with_ws)
    new_sent_text = "".join(proc_tokens)
    return new_sent_text


def negate_the_only_auxiliary(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], 'sent')
    if not sent._.is_negatable or sent._.negated_version is not None:
        return
    auxiliary = matched_tokens[0]
    has_ancestors = check_verb_has_other_verbs_as_ancestors(auxiliary)
    if has_ancestors:
        return
    sent._.negated_version = remap_tokens(sent, AUXILIARY_TO_NEGATION_MAPPING)


def match_to_do_form_and_lexical_verb(verb):
    verb_morph = get_token_attribute(verb, "morph")
    base_form = get_token_attribute(verb, "lemma")
    verb_text_with_whitespace = get_token_attribute(verb, "text_with_ws")
    base_form_with_whitespace = format_white_space_after_token(verb, base_form)
    if "Tense=Past" in verb_morph:
        negated_verb = f"didn't {base_form_with_whitespace}"
    else:
        if "Number=Sing" in verb_morph and ("Person=Three" in verb_morph or "Person=3" in verb_morph):
            negated_verb = f"doesn't {base_form_with_whitespace}"
        else:
            negated_verb = f"don't {verb_text_with_whitespace}"
    return negated_verb


def add_auxiliary_do_negation(sent, verb):
    negated_to_do_form = match_to_do_form_and_lexical_verb(verb)
    proc_tokens = []
    verb_index_in_doc = get_token_attribute(verb, "i")
    for token in sent:
        token_index_in_doc = get_token_attribute(token, "i")
        if token_index_in_doc == verb_index_in_doc:
            proc_tokens.append(negated_to_do_form)
        else:
            proc_tokens.append(lexical_remap(token))
    new_sent_text = "".join(proc_tokens)
    return new_sent_text


def lexical_remap(token):
    token_text = get_token_attribute(token, "text").lower()
    substitute = get_token_attribute(token, "text_with_ws")
    if token_text == "too":
        substitute = format_white_space_after_token(token, "either")
    elif token_text in SOME_DERIVATIVES:
        token_head = get_token_attribute(token, "head")
        token_head_dep = get_token_attribute(token_head, "dep")
        token_dep = get_token_attribute(token, "dep")
        if token_head_dep == "dobj" or token_dep == "dobj":
            substitute_word = token_text.replace("some", "any")
            substitute = format_white_space_after_token(token, substitute_word)
    return substitute


def identify_head_auxiliary(verb):
    children = get_token_attribute(verb, "children")
    children_idx = {}
    for child in children:
        child_pos = get_token_attribute(child, "pos")
        if child_pos == "AUX":
            child_index_in_doc = get_token_attribute(child, "i")
            children_idx[child_index_in_doc] = child
    children_sorted_by_index_in_doc = sorted(children_idx.items())
    head_auxiliary_index_in_doc, head_auxiliary = children_sorted_by_index_in_doc[0]
    return head_auxiliary_index_in_doc, head_auxiliary


def map_short_form_to_full_by_lemma(head_auxiliary):
    head_auxiliary_lemma = get_token_attribute(head_auxiliary, "lemma")
    head_auxiliary_text = get_token_attribute(head_auxiliary, "text").lower()
    head_auxiliary_text_with_ws = get_token_attribute(head_auxiliary, "text_with_ws")
    formatted_not = format_white_space_after_token(head_auxiliary, "not")
    substitute = head_auxiliary_text_with_ws
    if head_auxiliary_lemma == "be":
        substitute = f"{head_auxiliary_text_with_ws}{formatted_not}"
    elif head_auxiliary_lemma in ["have", "'ve"]:
        substitute = SHORT_FORMS_OF_TO_HAVE_TO_NEGATION_MAPPING.get(head_auxiliary_text)
        substitute = format_white_space_after_token(head_auxiliary, substitute)
    elif head_auxiliary_lemma == "'d":
        substitute = "would"
        substitute = f" {substitute} {formatted_not}"
    return substitute


def negate_verb_auxiliary_combination(sent, verb):
    head_auxiliary_index_in_doc, head_auxiliary = identify_head_auxiliary(verb)
    head_auxiliary_text = get_token_attribute(head_auxiliary, "text").lower()
    proc_tokens = []
    for token in sent:
        token_index_in_doc = get_token_attribute(token, "i")
        if token_index_in_doc == head_auxiliary_index_in_doc:
            mapping = AUXILIARY_TO_NEGATION_MAPPING.get(head_auxiliary_text)
            if mapping is not None:
                substitute = format_white_space_after_token(head_auxiliary, mapping)
                proc_tokens.append(substitute)
            else:
                proc_tokens.append(map_short_form_to_full_by_lemma(head_auxiliary))
        else:
            proc_tokens.append(lexical_remap(token))
    new_sent_text = "".join(proc_tokens)
    return new_sent_text


def check_verb_has_verb_in_past_tense_in_extended_children(verb):
    children = list(get_token_attribute(verb, "children"))
    extended_children = [list(get_token_attribute(child, "children")) for child in children]
    extended_children.append(children)
    for extended_child in extended_children:
        for child in extended_child:
            child_lemma = get_token_attribute(child, "lemma")
            child_morph = get_token_attribute(child, "morph")
            child_pos = get_token_attribute(child, "pos")
            if ('Tense=Past' in child_morph or child_pos == "AUX") and child_lemma != "be":
                return True
    return False


def detect_wish_and_past_simple_construction(verb):
    has_past_tense_children = check_verb_has_verb_in_past_tense_in_extended_children(verb)
    verb_lemma = get_token_attribute(verb, "lemma")
    if verb_lemma == "wish" and has_past_tense_children:
        return True
    return False


def negate_sentence_with_lexical_verb(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], "sent")
    if not sent._.is_negatable or sent._.negated_version is not None:
        return
    verb = matched_tokens[0]
    has_children = check_verb_has_auxiliary_verbs_as_children(verb)
    skip_to_negate_with_next_match = detect_wish_and_past_simple_construction(verb)
    if skip_to_negate_with_next_match:
        return
    if has_children:
        sent._.negated_version = negate_verb_auxiliary_combination(sent, verb)
    else:
        sent._.negated_version = add_auxiliary_do_negation(sent, verb)


def fill_second_matcher(matcher):
    matcher.add("TO BE AS THE ONLY VERB", [negation_transformation_pattern_1], on_match=negate_to_be)
    matcher.add("EVERYONE NEEDING LEXICAL NEGATION", [negation_transformation_pattern_2], on_match=negate_everyone_pattern)
    matcher.add("AUXILIARY AS THE ONLY VERB", [negation_transformation_pattern_3], on_match=negate_the_only_auxiliary)
    matcher.add("SENTENCE WITH LEXICAL VERB", [negation_transformation_pattern_4], on_match=negate_sentence_with_lexical_verb)
    return matcher