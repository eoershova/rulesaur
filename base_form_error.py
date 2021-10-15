from pipeline import NLP

# "auxiliary and finite verb"
base_form_error_pattern_0 = [
    {
        "RIGHT_ID": "anchor_verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB"], "NOT_IN": ["AUX"]},
                        "MORPH": {"NOT_IN": ["VerbForm=Inf", "Tense=Pres"]}},
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "auxiliary",
        "RIGHT_ATTRS": {"DEP": "aux", "POS": "AUX"},

    }]

# "auxiliary that applies to a verb and its coordinating conjunction"
base_form_error_pattern_2 = [{
        "RIGHT_ID": "anchor_verb",
        "RIGHT_ATTRS": {"POS": "VERB", "MORPH": {"IN": ["VerbForm=Inf"]}}
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "aux",
        "RIGHT_ATTRS": {"DEP": "aux", "POS": "AUX"},
    },
    {
        "LEFT_ID": "anchor_verb",
        "REL_OP": ">",
        "RIGHT_ID": "knitted_verb",
        "RIGHT_ATTRS": {"DEP": "conj", "POS": "VERB", "MORPH": {"NOT_IN": ["VerbForm=Inf"]}},
    }]

# "auxiliary that applies to another auxiliary"
base_form_error_pattern_3 = [
        {
            "RIGHT_ID": "anchor_auxiliary",
            "RIGHT_ATTRS": {"POS": "AUX"}
        },
        {
            "LEFT_ID": "anchor_auxiliary",
            "REL_OP": ">",
            "RIGHT_ID": "aux",
            "RIGHT_ATTRS": {"DEP": "aux", "POS": "AUX"},
        }
    ]


def get_token_attribute(token, attribute):
    directly_accessible_attributes = ['morph', 'text', 'text_with_ws', 'sent', 'children', 'ancestors', 'doc',
                                      'head', 'i', 'right_edge']
    if attribute in directly_accessible_attributes:
        return getattr(token, attribute)
    attribute_object_hash = getattr(token, attribute)
    attribute_object = NLP.vocab[attribute_object_hash]
    attribute_value = attribute_object.text
    return attribute_value


def check_form_propriety(auxiliary, verb):
    aux_verb_forms = {
        'have': ['Tense=Past', 'Aspect=Perf', 'VerbForm=Part'],
        'be': ['Tense=Past', 'Aspect=Prog'],
        'having': ['Tense=Past', 'Aspect=Perf', 'VerbForm=Part'],
    }
    verb_morph = get_token_attribute(verb, 'morph')
    auxiliary_lemma = get_token_attribute(auxiliary, 'lemma')
    ok_morph_features = aux_verb_forms.get(auxiliary_lemma)
    flag = False
    if ok_morph_features:
        for feature in ok_morph_features:
            if feature in verb_morph:
                flag = True
                break
    return flag


def unpack_match(doc, i, matches):
    match_id, matched_tokens_indexes = matches[i]
    matched_tokens = [doc[token_idx] for token_idx in matched_tokens_indexes]
    return matched_tokens


def process_pattern_2(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    sent = get_token_attribute(matched_tokens[0], "sent")
    if sent._.is_target:
        return
    inf, aux, non_inf = matched_tokens
    flag = check_form_propriety(aux, non_inf)
    if not flag:
        sent._.is_target = True


def process_pattern_3(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    aux_1, aux_2 = matched_tokens
    sent = get_token_attribute(aux_1, 'sent')
    if sent._.is_target:
        return
    sent._.is_target = True


def find_closest_verb(verb):
    children = get_token_attribute(verb, "children")
    children_idx = {}
    for child in children:
        child_pos = get_token_attribute(child, "pos")
        if child_pos in ["AUX", "VERB"]:
            child_index_in_doc = get_token_attribute(child, "i")
            children_idx[child_index_in_doc] = child
    children_sorted_by_index_in_doc = sorted(children_idx.items())
    verb_index_in_doc = get_token_attribute(verb, "i")
    closest_verb_token = None
    for child in reversed(children_sorted_by_index_in_doc):
        child_index, closest_verb_token = child
        if child_index < verb_index_in_doc:
            return closest_verb_token
    return closest_verb_token


def process_pattern_0(matcher, doc, i, matches):
    matched_tokens = unpack_match(doc, i, matches)
    verb, aux = matched_tokens
    sent = get_token_attribute(verb, "sent")
    if sent._.is_target:
        return
    closest_verb = find_closest_verb(verb)
    flag = check_form_propriety(closest_verb, verb)
    if not flag:
        sent._.is_target = True


def fill_matcher(matcher):
    matcher.add("AUX + (INFINITE VERB AND FINITE VERB)", [base_form_error_pattern_2], on_match=process_pattern_2)
    matcher.add("AUX + AUX", [base_form_error_pattern_3], on_match=process_pattern_3)
    matcher.add("AUX + FINITE VERB", [base_form_error_pattern_0], on_match=process_pattern_0)
    return matcher
