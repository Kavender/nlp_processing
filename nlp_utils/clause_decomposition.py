# further analysis, look int the following two repo
# https://github.com/mmxgn/clausiepy/blob/master/clausiepy/clausiepy.py
# https://github.com/NSchrading/intro-spacy-nlp/blob/master/subject_object_extraction.py
LIST_COPULAR_VERB = [
    "act",
    "appear",
    "be",
    "become",
    "come",
    "come out",
    "to be",
    "end up",
    "get",
    "go",
    "grow",
    "fall",
    "feel",
    "keep",
    "leave",
    "look",
    "prove",
    "remain",
    "seem",
    "smell",
    "sound",
    "stay",
    "taste",
    "turn",
    "turn up",
    "wind up",
    "live",
    "come",
    "go",
    "stand",
    "lie",
    "love",
    "do",
    "try",
    "to seem",
    "to appear",
]
LIST_COMPLEX_TRANSITIVE = [
    "bring",
    "catch",
    "drive",
    "get",
    "keep",
    "lay",
    "lead",
    "place",
    "put",
    "set",
    "sit",
    "show",
    "stand",
    "slip",
    "take",
]
LIST_APPOS = [
    "is",
    "his",
    "he",
    "has",
    "her",
    "she",
    "I",
    "have",
    "its",
    "it",
    "our",
    "we",
    "your",
    "you",
    "their",
    "they",
]


def tokenizer_appos_modifiers(nlp):
    dict_appos_mapping = {}
    for token in LIST_APPOS:
        dict_appos_mapping.setdefault(token, nlp(token)[0])
    return dict_appos_mapping


def is_negated(token):
    negations = {"no", "not", "n't", "never", "none"}
    for dep in list(token.lefts) + list(token.rights):
        if dep.lower_ in negations:
            return True
    return False


def has_dobj(clause):
    return len(clause["O"]) > 0


def has_iobj(clause):
    return len(clause["IO"]) > 0


def has_object(clause):
    return has_dobj(clause) or has_iobj(clause)


def has_complement(clause):
    return len(clause["C"]) > 0 or len(clause["XCOMP"]) > 0


def has_candidate_adverbial(clause):
    for verb in clause["V"]:
        for adv in clause["A"]:
            if adv in verb.subtree and adv.i > verb.i:
                return True
    else:
        return False


def has_known_non_ext_copular(nlp, clause):
    for verb in clause["V"]:
        if nlp(verb.text)[0].lemma_ in ["die", "walk"]:
            return True
    else:
        return False


def has_known_ext_copular(nlp, clause):
    for verb in clause["V"]:
        if nlp(verb.text)[0].lemma_ in LIST_COPULAR_VERB:
            return True
    else:
        return False


def is_known_copular(verb):
    return str(verb) in LIST_COPULAR_VERB


def has_potentially_complex_transitive(nlp, clause):
    for verb in clause["V"]:
        if nlp(verb.text)[0].lemma_ in LIST_COMPLEX_TRANSITIVE:
            return True
    else:
        return False


class SentComponents(object):
    name = "sentence_decomposer"

    def __init__(self, nlp, appos_mapping, conservative=True):
        # maybe we want to pass in the merged doc after entity recognizer as well
        self.nlp = nlp
        self.appos_mapping = appos_mapping
        self.being_conservative = conservative

    def get_token_span(self, doc, token):
        return doc[token.left_edge.i : token.right_edge.i + 1]

    def empty_clause(self):
        return {"S": [], "V": [], "O": [], "IO": [], "XCOMP": [], "A": [], "C": []}

    def translate_clause(self, clause):
        """ Modifies clause so that relative clause indicators (whose, which, where)
            are resolved before subsequent processing """
        for n, token in enumerate(clause["S"]):
            # If you have a "which" or a "whose", replace it with the token pointed
            # by the relcl(relative clause) dependency of the antidescendant.
            if token.text.lower() in ["which", "who"]:
                if token.head.dep_ == "relcl":
                    clause["S"].remove(token)
                    clause["S"].insert(0, token.head.head)

        if "A" in clause:
            for n, token in enumerate(clause["A"]):
                if token.text.lower() in ["where"]:
                    if token.head.dep_ == "relcl":
                        clause["A"].remove(token)
                        clause["A"].insert(0, token.head.head.head)

        if "A?" in clause:
            for n, token in enumerate(clause["A?"]):
                if token.text.lower() in ["where"]:
                    if token.head.dep_ == "relcl":
                        clause["A?"].remove(token)
                        clause["A?"].insert(0, token.head.head.head)
        return clause

    def process_dependants(self, token, clause):
        dependants = [c for c in token.head.subtree if c not in token.subtree]
        for d in dependants:
            if d.dep_ in ["dobj"]:
                clause["O"].append(d)
            elif d.dep_ in ["iobj", "dative"]:
                clause["IO"].append(d)
            elif d.dep_ in ["ccomp", "acomp", "attr"]:
                clause["C"].append(d)
            elif d.dep_ in ["xcomp"]:
                if is_known_copular(d):
                    clause["XCOMP"].append(d.head)
                else:
                    clause["O"].append(d)
            elif d.dep_ in ["advmod", "advcl", "npadvmod"]:
                clause["A"].append(d)
            elif d.dep_ in ["oprd"] and d.head in clause["V"]:
                clause["A"].append(d)
            elif d.dep_ in ["prep"]:
                # Capture "prep_in(X, Y)". which is prep(X, in) and pobj(in, Y)
                for c in d.children:
                    if c.dep_ == "pobj":
                        clause["A"].append(d)
        return clause

    def clause_token(self, token, clause):

        if token.dep_ in ["nsubj", "nsubjpass", "attr"]:
            clause["S"].append(token)
            clause["V"].append(token.head)
            self.process_dependants(token, clause)
        elif token.dep_ in ["csubj"]:
            clause["S"].append(token)
            clause["V"].append(token.head)
            # Take dependants:
            dependants = [c for c in token.head.subtree if c not in token.subtree]
            for d in dependants:
                if d.dep_ in ["dobj"]:
                    clause["O"].append(d)
        elif token.dep_ in ["appos"]:
            # Subjects without a verb E.g. Sam is my brother in: Sam, my brother.
            clause["S"].append(token.head)
            clause["V"].append(self.appos_mapping["is"])
            clause["C"].append(token)
        elif token.dep_ in ["poss"]:
            # Subjects declaring possesion e.g. my brother: in: Sam, my brother.
            # !!! Next step is to move the Tokenization of the dictionary key words out of class
            # Because it's costly to repeat the calling of spacy pipeline for Tokenization
            if token.text.lower() == "his":
                clause["S"].append(self.appos_mapping["he"])
                clause["V"].append(self.appos_mapping["has"])
            elif token.text.lower() == "her":
                clause["S"].append(self.appos_mapping["she"])
                clause["V"].append(self.appos_mapping["has"])
            elif token.text.lower() == "my":
                clause["S"].append(self.appos_mapping["I"])
                clause["V"].append(self.appos_mapping["have"])
            elif token.text.lower() == "its":
                clause["S"].append(self.appos_mapping["it"])
                clause["V"].append(self.appos_mapping["has"])
            elif token.text.lower() == "our":
                clause["S"].append(self.appos_mapping["we"])
                clause["V"].append(self.appos_mapping["have"])
            elif token.text.lower() == "your":
                clause["S"].append(self.appos_mapping["you"])
                clause["V"].append(self.appos_mapping["have"])
            elif token.text.lower() == "their":
                clause["S"].append(self.appos_mapping["they"])
                clause["V"].append(self.appos_mapping["have"])
            else:
                clause["S"].append(token)
                clause["V"].append(self.appos_mapping["has"])
            clause["O"].append(token.head)
        elif token.dep_ in ["acl"]:
            # Create a synthetic from participial modifiers (partmod).
            clause["S"].append(token.head)
            new_sent = self.nlp("are {}".format(" ".join([t.text for t in token.subtree])))
            r = [t for t in new_sent if t.dep_ == "ROOT"][0]
            clause["V"].append(r)
            self.process_dependants(token, clause)
        return clause

    def define_clause_type(self, clause):
        type_ = "OTHER"
        if not has_object(clause):  # Q1
            if has_complement(clause):  # Q2
                type_ = "SVC"
            else:
                # Q3
                if not has_candidate_adverbial(clause):
                    type_ = "SV"
                else:
                    # Q4
                    if has_known_non_ext_copular(self.nlp, clause):
                        type_ = "SV"
                    else:
                        # Q5
                        if has_known_ext_copular(self.nlp, clause):
                            type_ = "SVA"
                        else:
                            # Q6: Cases we want conservative or non-conservative estimation
                            if self.being_conservative:
                                type_ = "SVA"
                            else:
                                type_ = "SV"
        else:
            # Q7
            if has_dobj(clause) and has_iobj(clause):
                type_ = "SVOO"
            else:
                # Q8
                if has_complement(clause):
                    type_ = "SVOC"
                else:
                    # Q9
                    if not has_candidate_adverbial(clause) and has_dobj(clause):
                        type_ = "SVO"
                    else:
                        # Q10
                        if has_potentially_complex_transitive(self.nlp, clause):
                            type_ = "SVOA"
                        else:
                            # Q11
                            if self.being_conservative:
                                type_ = "SVOA"
                            else:
                                type_ = "SVO"
        return type_

    def decompose_clause(self, doc):
        clauses = []
        # Check if root is not a verb
        print([t for t in doc if t.dep_ == "ROOT"])
        root = [t for t in doc if t.dep_ == "ROOT"][0]
        if root.pos_ != "VERB":
            doc = self.nlp("There is " + doc.text)

        clause = self.empty_clause()
        # Subjects of a verb
        for token in doc:
            clause_tokens = self.clause_token(token, clause)
            clause = self.translate_clause(clause_tokens)
            if any([len(clause[comp_type]) > 0 for comp_type in self.empty_clause()]):
                clauses.append(clause)
                clause = self.empty_clause()
        # Identify clause types
        for clause in clauses:
            clause_type = self.define_clause_type(clause)
            clause["type"] = clause_type
            if clause_type in ["SVC", "SVOO", "SVOC", "SV", "SVO"]:
                clause["A?"] = clause["A"]
                clause.pop("A", None)
        return clauses
