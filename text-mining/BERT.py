import spacy

# Load the language model
nlp = spacy.load("en_core_web_trf")

def split_sentences(text):
    doc = nlp(text)
    sub_sentences = []

    for sent in doc.sents:
        current_sentence = []
        for token in sent:
            # If we encounter a coordinating conjunction or a period, we split
            if token.text in {'.'}:
                if current_sentence:
                    sub_sentences.append(" ".join(current_sentence).strip())
                    current_sentence = []
                continue
            current_sentence.append(token.text)
        
        # Add the last part if it's not empty
        if current_sentence:
            sub_sentences.append(" ".join(current_sentence).strip())

    return sub_sentences


def analyze_sentence(sentence):
    doc = nlp(sentence)

    print("Syntactic Analysis:")
    for token in doc:
        print(f"{token.text:<20} -> {token.dep_:<10} (Head: {token.head.text}) - POS: {token.pos_}")

    print("\nRecognized Entities:")
    if doc.ents:
        for ent in doc.ents:
            print(f"{ent.text:<40} -> {ent.label_}")

    print("\nROOT and the first two immediate children of ROOT:")
    root = find_root(doc)
    if root:
        print(f"ROOT: {root.text} -> {root.dep_} - POS: {root.pos_}")
        children = list(root.children)
        if len(children) > 0:
            print(f"First child: {children[0].text} -> {children[0].dep_} (Head: {children[0].head.text})")
        if len(children) > 1:
            print(f"Second child: {children[1].text} -> {children[1].dep_} (Head: {children[1].head.text})")
    else:
        print("ROOT not found.")
    
    svos = extract_svos(doc, root)

    print("\nMain SVO Relation:")
    if svos:
        for subj, verb, obj in svos:
            print(f"{subj} -- {verb} --> {obj}")
    else:
        print("No relation found.")


def extract_svos(doc, root):
    svos = []

    if root:
        if root.pos_ == "VERB" or root.pos_ == "AUX":  # Case 1: ROOT is a verb
            subj = find_all_downstream(root, {"nsubj", "nsubjpass"})
            obj = find_all_downstream(root, {"obj", "dobj", "attr", "acomp", "pobj"}) 
            extended_verb = root.lemma_
            for s in subj:
                for o in obj:
                    svos.append((s if s else "—", extended_verb, o if o else "—"))
        elif root.pos_ == "NOUN":  # Case 2-3: ROOT is a subject
            verb = find_verb(root, {"VERB", "AUX"})
            obj = find_all_downstream(root, {"obj", "dobj", "attr", "acomp", "pobj"}) 
            for v in verb:
                for o in obj:
                    svos.append((root.text, v if v else "—", o if o else "—"))
        
        # Case 3: recursively find ALL verbs/AUX in the subtree and apply extract_svos
        for token in root.subtree:
            if token != root and token.pos_ in {"VERB", "AUX"}:
                svos += extract_svos(doc, token)

    return svos


def find_verb(token, target_deps, pos_=None, root=None):
    """
    Explores the entire syntactic tree starting from the ROOT of the sentence.
    Recursively searches descendants to find all tokens with one of the target dependencies
    and optionally a specific POS. If 'pobj' is among the target dependencies, it also includes tokens 
    that do not share the head with the ROOT.
    """
    root = token.doc[:].root  # gets the root of the sentence
    queue = [root]
    visited = set()
    found_tokens = []

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current.pos_ in target_deps:
            if pos_ is None or current.pos_ == pos_:
                found_tokens.append(current.text)
                break

        for child in current.children:
            queue.append(child)

    return found_tokens


def find_all_downstream(token, target_deps, pos_=None, root=None):
    """
    Explores the entire syntactic tree starting from the ROOT of the sentence.
    Recursively searches descendants to find all tokens with one of the target dependencies
    and optionally a specific POS. If 'pobj' is among the target dependencies, it also includes tokens 
    that do not share the head with the ROOT.
    """
    root = token.doc[:].root  # gets the root of the sentence
    queue = [root]
    visited = set()
    found_tokens = []

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if current.dep_ in target_deps:
            if pos_ is None or current.pos_ == pos_:
                # If 'pobj' is among the targets, skip the check on the head
                if 'pobj' in target_deps or current.head == root:
                    found_tokens.append(current.text)
                    break

        for child in current.children:
            queue.append(child)

    return found_tokens


def find_root(doc):
    for token in doc:
        if token.dep_ == "ROOT":
            return token
    return None


# Example text
text = "Each guest must receive a badge that uniquely and truthfully represents their specific contribution."

split_sentences = split_sentences(text)

for sentence in split_sentences:
    print("\n*************************")
    print("\nAnalysis of the sentence:", sentence)
    analyze_sentence(sentence)
