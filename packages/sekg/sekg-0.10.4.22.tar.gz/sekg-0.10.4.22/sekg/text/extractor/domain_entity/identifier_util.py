import re

from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

from sekg.text.extractor.domain_entity.nlp_util import SpacyNLPFactory
from sekg.text.extractor.domain_entity.relation_detection import RelationType
from sekg.text.extractor.domain_entity.word_util import WordUtil
from sekg.util.code import CodeElementNameUtil


class IdentifierInfoExtractor:
    """
        IdentifierInfoExtractor, extract use knowledge from some Identifier name,
        eg. class name, method name, variable name
    """

    # SPECIAL_VERB = {"get", "set", "parse", "push", "pop", "peak", "load", "flush", "init", "goto", "show", "finish",
    #                 "invoke",
    #                 "update", "open", "close", "import", "move", "post", "process", "lookup", "select", "clear",
    #                 "reload", "prepend", "print", "claim", "visit", "resize", "build", "convert"}
    IDENTIFIER_ENTITY = "##identifier##"  ## standing for the extractor itself

    def __init__(self):

        self.nlp = SpacyNLPFactory.create_spacy_nlp_for_identifier_extractor()

        self.stopwords = stopwords.words('english')
        self.stopwords.append("-PRON-")
        self.stopwords = set(self.stopwords)
        self.lemmatizer = WordNetLemmatizer()

        self.code_patterns = [
            re.compile(r'^(?P<ELE>[a-zA-Z0-9_]*[a-z0-9][A-Z][a-z]+[a-zA-Z0-9_]*)(<.*>)?$'),
            re.compile(r'^(?P<ELE>[a-zA-Z0-9_\.<>]+)\([a-zA-Z0-9_\,.<>)]*?$'),
            re.compile(r'^(?P<ELE>[a-zA-Z]{2,}(\.[a-zA-Z0-9_]+)+)(<.*>)?$')
        ]

        self.camel_cache = {}
        self.CODE_NAME_UTIL = CodeElementNameUtil()

    def uncamelize(self, camel_case):
        if camel_case in self.camel_cache:
            return self.camel_cache[camel_case]
        sub = self.CODE_NAME_UTIL.uncamelize_by_stemming(camel_case)
        self.camel_cache[camel_case] = sub
        return sub

    def pos_tag_for_method_name_from_method_doc(self, spacy_doc):
        """
        do the pos tag for method name
        :param spacy_doc: name
        :return: a Spacy Doc object
        """
        # fix the problem of 2 and 4 to represent 'to' and 'for'
        for i in range(0, len(spacy_doc)):
            if spacy_doc[i].text == "2" and i != 0 and len(spacy_doc) - 1:
                spacy_doc[i].lemma_ = "to"
                spacy_doc[i].pos_ = "ADP"
                spacy_doc[i].tag_ = "IN"

            if spacy_doc[i].text == "4" and i != 0 and len(spacy_doc) - 1:
                spacy_doc[i].lemma_ = "for"
                spacy_doc[i].pos_ = "ADP"
                spacy_doc[i].tag_ = "IN"

            if spacy_doc[i].text.lower() == "to":
                spacy_doc[i].lemma_ = "to"
                spacy_doc[i].pos_ = "ADP"
                spacy_doc[i].tag_ = "IN"

            if spacy_doc[i].text.lower() in ["id", "ID", "Id"]:
                spacy_doc[i].lemma_ = "id"
                spacy_doc[i].pos_ = "NOUN"
                spacy_doc[i].tag_ = "NN"

        parts = []
        current_part = []
        for token in spacy_doc:
            if token.pos_ == "ADP":
                if current_part:
                    parts.append(current_part)
                current_part = []
                parts.append([token])
            else:
                current_part.append(token)
        if current_part:
            parts.append(current_part)

        if len(parts) == 3 and parts[1][0].text == "2":
            self.__reannotation_for_tokens(parts[0], fix_to_noun_ending=True)
            self.__reannotation_for_tokens(parts[2], fix_to_noun_ending=True)
            return spacy_doc

        leading_tokens = parts[0]
        self.__reannotate_for_leading_part_tokens(leading_tokens)

        left_parts = parts[1:]
        if len(left_parts) == 0:
            return spacy_doc

        for tokens in left_parts:
            # 介词后面的作为独立的一部分，让spacy重新标注
            if len(tokens) == 1 and tokens[0].pos_ == "ADP":
                continue

            self.__reannotate_for_left_part_tokens_after_preposition(tokens)
        return spacy_doc

    def pos_tag_for_method_name(self, name):
        """
        do the pos tag for method name
        :param name: name
        :return: a Spacy Doc object
        """
        name = name.split("(")[0].split(".")[-1]
        uncamel = self.uncamelize(name).lower()
        spacy_doc = self.nlp(uncamel)
        return self.pos_tag_for_method_name_from_method_doc(spacy_doc)

    def __reannotate_for_leading_part_tokens(self, part):
        text = " ".join([token.text for token in part])
        # for "find or create" type, just use the default annotation, it is OK
        if "and" in text.lower() or "or" in text.lower():
            self.__reannotation_for_tokens(part)
            return
            # todo
        if len(part) == 1:
            # first part is a ADP(eg. To,By)
            if part[0].pos_ == "ADP":
                return
            # new_token = self.nlp(part[0].text)[0]
            # self.__update_annotation_for_token(part[0],new_token)
            if WordUtil.couldBeVerb(part[0].text):
                self.__set_token_to_verb_pos(part[0])
                return
            if WordUtil.couldBeNoun(part[0].text):
                self.__set_token_to_noun_pos(part[0])
                return
            if WordUtil.couldBeADJ(part[0].text):
                self.__set_token_to_adj_pos(part[0])
                return
            return

        if len(part) >= 1:
            ## 1. VERB + NOUN
            ## 2. VERB + NOUN +ADJ
            ## 3. VERB + ADJ
            ## 4. NOUN

            left_tokens = part
            if WordUtil.couldBeVerb(part[0].text):
                self.__set_token_to_verb_pos(part[0])
                left_tokens = part[1:]

            if WordUtil.couldBeNoun(left_tokens[-1].text):
                ## 1. VERB + NOUN
                ## 4. NOUN
                self.__reannotation_for_tokens(left_tokens, fix_to_noun_ending=True)
                return

            if WordUtil.couldBeADJ(left_tokens[-1].text):
                ## 2. VERB + NOUN +ADJ
                ## 3. VERB + ADJ
                self.__set_token_to_adj_pos(left_tokens[-1])
                left_tokens = left_tokens[:-1]
                self.__reannotation_for_tokens(left_tokens, fix_to_noun_ending=True)
                return

            self.__reannotation_for_tokens(left_tokens)

    def __reannotate_for_left_part_tokens_after_preposition(self, tokens):
        text = " ".join([token.text for token in tokens])
        # for "find or create" type, just use the default annotation, it is OK
        if "and" in text.lower() or "or" in text.lower():
            self.__reannotation_for_tokens(tokens)
            return
        if len(tokens) == 1:
            # ADP+NOUN
            if WordUtil.couldBeNoun(tokens[0].text):
                self.__set_token_to_noun_pos(tokens[0])
                return
            # ADP+ADJ
            if WordUtil.couldBeADJ(tokens[0].text):
                self.__set_token_to_adj_pos(tokens[0])
                return
            # others: annotate by default
            self.__reannotation_for_tokens(tokens)
            return

        if len(tokens) >= 1:
            ## 1. NOUN
            ## 2. NOUN +ADJ
            ## 3. ADJ
            ## 4. NOUN

            if WordUtil.couldBeNoun(tokens[-1].text):
                ## 1. NOUN
                ## 4. NOUN
                self.__reannotation_for_tokens(tokens, fix_to_noun_ending=True)
                return

            if WordUtil.couldBeADJ(tokens[-1].text):
                ## 2. VERB + NOUN +ADJ
                ## 3. VERB + ADJ
                self.__set_token_to_adj_pos(tokens[-1])

                self.__reannotation_for_tokens(tokens[:-1], fix_to_noun_ending=True)
                return

            self.__reannotation_for_tokens(tokens)

    def __reannotation_for_tokens(self, tokens, fix_to_noun_ending=False):
        if len(tokens) == 0:
            return
        text = " ".join([token.text for token in tokens])
        new_tokens = self.nlp(text)
        if len(new_tokens) != len(tokens):
            for token in tokens:
                new_token = self.nlp(token.text)[0]
                self.__update_annotation_for_token(token, new_token)
        else:
            for old_annotation_token, new_annotation_token in zip(tokens, new_tokens):
                self.__update_annotation_for_token(old_annotation_token, new_annotation_token)

        self.__fix_adj_like_verb_annotation(tokens)
        self.__fix_special_vocab_annotation(tokens)
        if fix_to_noun_ending and WordUtil.couldBeNoun(tokens[-1].text):
            self.__set_token_to_noun_pos(tokens[-1])

    def __fix_adj_like_verb_annotation(self, tokens):
        for token in tokens:
            if token.tag_ in ["VBD", "VBG", "VBN"]:
                self.__set_token_to_adj_pos(token)

    def __fix_special_vocab_annotation(self, tokens):
        for token in tokens:
            if token.text.lower() == "id":
                token.lemma_ = "id"
                token.pos_ = "NOUN"
                token.tag_ = "NN"

    def __update_annotation_for_token(self, old_annotation_token, new_annotation_token):
        old_annotation_token.lemma_ = new_annotation_token.lemma_
        old_annotation_token.pos_ = new_annotation_token.pos_
        old_annotation_token.tag_ = new_annotation_token.tag_

    def __set_token_to_verb_pos(self, old_annotation_token):
        # old_annotation_token.lemma_ = new_annotation_token.lemma_
        old_annotation_token.pos_ = "VERB"
        old_annotation_token.tag_ = "VB"

    def __set_token_to_noun_pos(self, old_annotation_token):
        # old_annotation_token.lemma_ = new_annotation_token.lemma_
        old_annotation_token.pos_ = "NOUN"
        old_annotation_token.tag_ = "NN"

    def __set_token_to_adj_pos(self, old_annotation_token):
        # old_annotation_token.lemma_ = new_annotation_token.lemma_
        old_annotation_token.pos_ = "ADJ"
        old_annotation_token.tag_ = "JJ"

    def __find_depending_verbs(self, np_tokens, spacy_doc):
        spacy_doc = [token for token in spacy_doc]
        result = []
        start_token = np_tokens[0]
        start_index = spacy_doc.index(start_token)

        for i in range(start_index - 1, -1, -1):
            if spacy_doc[i].tag_.find("V") >= 0:
                result.append(spacy_doc[i])
                if i - 2 < 0:
                    return result

                if spacy_doc[i - 1].text.lower() != "and" and spacy_doc[i - 1].text.lower() != "or":
                    return result

                if spacy_doc[i - 2].tag_.find("V") < 0:
                    return result
                result.append(spacy_doc[i - 2])
                return result

        return result

    def __find_adp_token_between_verb_and_np(self, spacy_doc, np_tokens, operation_token):
        spacy_doc = [token for token in spacy_doc]

        operation_token_index = spacy_doc.index(operation_token)
        start_token = np_tokens[0]
        start_index = spacy_doc.index(start_token)

        for i in range(start_index - 1, operation_token_index, -1):
            if spacy_doc[i].pos_ == "ADP":
                return spacy_doc[i]
        return None

    def __reextract_np_from_single_part(self, tokens):
        if len(tokens) == 0:
            return []

        text = " ".join([token.text for token in tokens]).lower()

        text = " ".join([token.text + "" + token.pos_ for token in tokens]).lower()
        total_nps = []
        current_np = []

        for index, token in enumerate(tokens):
            if token.pos_ == "ADP" and token.text.lower() == "of":
                if len(current_np) == 0:
                    current_np = []
                    continue

                if current_np[-1].pos_ not in ["PROPN", "NOUN"]:
                    current_np = []
                    continue

                current_np.append(token)
                continue
            if token.tag_ in ["WP$", "WDT", "WP"] or token.pos_ not in ["CCONJ", "ADJ", "PROPN", "NOUN"]:
                if len(current_np) == 0:
                    continue
                if current_np[-1].pos_ not in ["PROPN", "NOUN"]:
                    current_np = []
                    continue

                total_nps.append(current_np)
                current_np = []
                continue
            current_np.append(token)
            continue

        if len(current_np) != 0 and current_np[-1].pos_ in ["PROPN", "NOUN"]:
            total_nps.append(current_np)

        if len(total_nps) == 0:
            return []
        if len(total_nps) == 1:
            return total_nps

        return total_nps

    def __reextract_np_from_spacy_pos_doc(self, tokens):
        if len(tokens) == 0:
            return []

        parts = []
        current_part = []
        for token in tokens:
            if token.pos_ == "ADP" and token.text.lower() != "of":
                if current_part:
                    parts.append(current_part)
                current_part = []
            else:
                current_part.append(token)
        if current_part:
            parts.append(current_part)
        noun_phase_list = []

        for part in parts:

            nps = self.__reextract_np_from_single_part(part)
            if len(nps) > 0:
                noun_phase_list.extend(nps)
        return noun_phase_list

    def extract_from_method_name(self, method_name: str, mark_for_identifier_in_relation=IDENTIFIER_ENTITY):
        terms = set()
        operations = set()
        relations = set([])
        identifier_relations = set([])
        special_case = False
        # is XXX
        if method_name.find(".is") > 0:
            uncamel = self.uncamelize(method_name)
            search_obj = re.search(r"is \w+", uncamel, re.M | re.I)
            if search_obj:
                method_name = search_obj.group()
                end_part = method_name.replace("is ", "")
                special_case = True
                operation_relation_name = "operation_" + "check"
                identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, "if " + end_part))

        elif not special_case and method_name == "exists" or method_name.find(".exists(") > 0 or method_name.endswith(
                ".exists"):
            special_case = True
            operation_relation_name = "operation_" + "check"
            identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, "if exist"))
        elif not special_case and method_name == "len" or method_name.find(".len(") > 0 or method_name.endswith(".len"):
            operation_relation_name = "operation_" + "get"
            identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, "len"))
            special_case = True
        elif not special_case and method_name == "length" or method_name.find(".length(") > 0 or method_name.endswith(
                ".length"):
            operation_relation_name = "operation_" + "get"
            identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, "length"))
            special_case = True
        elif not special_case and method_name == "size" or method_name.find(".size(") > 0 or method_name.endswith(
                ".size"):
            special_case = True
            operation_relation_name = "operation_" + "get"
            identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, "size"))
        elif not special_case and method_name.find(".init(")>0:
            special_case = True
            operation_relation_name = "operation_" + "init"
            identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, "init"))

        elif not special_case and method_name.find(".to") > 0:
            search_obj = re.search(r"\.to\w+\(", method_name, re.M | re.I)
            if search_obj:
                method_name = search_obj.group()
                # toString的形式
                method_name = method_name.replace(" ", "")
                uncamel = self.uncamelize(method_name)
                special_case = True
                last_part = uncamel.replace(".to", "").replace("(", "")
                operation_relation_name = "operation_" + "convert to"
                identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, last_part))
        elif not special_case and method_name.find(".parse") > 0:
            uncamel = self.uncamelize(method_name)
            search_obj = re.search(r"parse \w+", uncamel, re.M | re.I)
            if search_obj:
                method_name = search_obj.group()
                end_part = method_name.replace("is ", "")
                special_case = True
                operation_relation_name = "operation_" + "parse"
                identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, end_part))

        if special_case:
            return terms, operations, relations, identifier_relations
        spacy_doc = self.pos_tag_for_method_name(method_name)
        noun_chunks = self.__reextract_np_from_spacy_pos_doc(spacy_doc)

        operations.update([token.text for token in spacy_doc if token.tag_.find("VB") >= 0])
        terms.update([" ".join([t.text for t in np_tokens]).lower() for np_tokens in noun_chunks])

        if len(noun_chunks) == 0:
            # 再去确认下有没有名词
            text = " ".join([token.text for token in spacy_doc]).lower()
            spacy_doc = self.pos_tag_for_method_name(text)
            for t in spacy_doc:
                # XX -> 	unknown
                if t.text.lower() == "long":
                    noun_chunks.append([t])
                    continue
                if t.text.lower().find("parse") < 0 and (str(t.tag_).startswith("N") or t.tag_ == "XX"):
                    noun_chunks.append([t])
        # group the operation by level, eg. "create and find", "create" and "find" are the same level.
        terms = self.filter_terms(terms)

        for np_tokens in noun_chunks:
            np = " ".join([t.text for t in np_tokens]).lower()
            operation_tokens = self.__find_depending_verbs(np_tokens, spacy_doc)

            for operation_token in operation_tokens:
                relations.add((np, RelationType.CAN_BE_OPERATED.value, operation_token.lemma_.lower()))

            for operation_token in operation_tokens:
                adp_token = self.__find_adp_token_between_verb_and_np(spacy_doc, np_tokens, operation_token)
                adp_text = ""
                if adp_token == None:
                    adp_text = ""
                else:
                    adp_text = adp_token.text

                relations.add((np, RelationType.CAN_BE_OPERATED.value, operation_token.lemma_.lower()))

                operation_relation_name = ("operation_" + operation_token.lemma_.lower() + " " + adp_text).strip()
                identifier_relations.add((mark_for_identifier_in_relation, operation_relation_name, np))

        for op in operations:
            identifier_relations.add((mark_for_identifier_in_relation, RelationType.INSTANCE_OF.value, op))
        if len(noun_chunks) == 0:
            for op in operations:
                identifier_relations.add((mark_for_identifier_in_relation, "operation_" + op, ""))

        return terms, operations, relations, identifier_relations

    def extract_knowledge_from_method_name(self, method_name: str):
        t, o, r, relations = self.extract_from_method_name(method_name)
        res = []
        for rel in relations:
            identifier, operation, name = rel
            if not str(operation).startswith("operation_"):
                continue
            verb = str(operation).replace("operation_", "")
            name = str(name).strip()
            msg = str(method_name) + " " + verb + " " + name
            res.append(msg)
        return res

    def extract_from_variable(self, variable, mark_for_identifier_in_relation=IDENTIFIER_ENTITY):
        """
        extract from variable name , eg. "String filePath"
        :param variable: s string that represent variable , eg. "String filePath", "java.lang.String filePath"
        :param mark_for_identifier_in_relation, the mark for the identifier itself in relations
        :return:
        """
        if not variable:
            return set(), set(), set()

        terms = set()
        variable = variable.split("<")[0].split(".")[-1].split(" ")[-1]
        if not variable:
            return set(), set(), set()
        uncamel = self.uncamelize(variable)
        for np in self.nlp(uncamel).noun_chunks:
            lemma = " ".join([token.text for token in np if token.lemma_ != "-PRON-"])
            if len(lemma) <= 1 or lemma.isdigit() == True:
                continue

            terms.add(lemma)

        terms = self.filter_terms(terms)

        relations = set()
        identifier_relations = set()

        if len(terms) == 1:
            terms_ = list(terms)[0]
            if terms_.lower() == uncamel.lower():
                identifier_relations.add((mark_for_identifier_in_relation, RelationType.REPRESENT.value, terms_))


        else:
            for lemma in terms:
                identifier_relations.add((mark_for_identifier_in_relation, RelationType.NAME_MENTION.value, lemma))
        return terms, relations, identifier_relations

    def extract_from_class_name(self, name, mark_for_identifier_in_relation=IDENTIFIER_ENTITY):
        """
        extract from class name or the name like class. eg. package name. example: java.lang.ArrayList-> Array List
        :param name:
        :param mark_for_identifier_in_relation, the mark for the identifier itself in relations

        :return:
        """
        if not name:
            return set(), set(), set()
        # todo: Error raise: IndexError: list index out of range
        name = name.split("<")[0].split(".")[-1].split(" ")[-1]
        if not name:
            return set(), set(), set()
        uncamel = self.uncamelize(name)

        terms = {uncamel}
        terms = self.filter_terms(terms)
        relations = set()
        identifier_relations = set()
        for lemma in terms:
            identifier_relations.add((mark_for_identifier_in_relation, RelationType.REPRESENT.value, lemma))
        return terms, relations, identifier_relations

    def __valid(self, term):
        term = str(term).lower()
        if len(term) <= 1 or term.isdigit():
            return False
        if term in self.stopwords:
            return False
        if len(set(term)) == 1:
            return False

        return True

    def filter_terms(self, terms):
        valid_terms = set()
        for t in terms:
            if self.__valid(t):
                valid_terms.add(t)

        return valid_terms

    # following is the version of wc to implement to extract relation from method name
    # def extract_from_method_name_wc_version(self, name):
    #     terms = set()
    #     operations = set()
    #     name = name.split("(")[0].split(".")[-1]
    #     uncamel = self.uncamelize(name).lower()
    #     words = uncamel.split()
    #     print("words", words)
    #
    #     spacy_doc = self.nlp(uncamel)
    #
    #     pos_tags = [token.pos_ for token in spacy_doc]
    #     lemma_words = [token.lemma_ for token in spacy_doc]
    #     np_index = {np.start: np.end for np in spacy_doc.noun_chunks}
    #     print("before fix the tags and lemma", pos_tags, lemma_words)
    #
    #     if len(words) == 1:
    #         if pos_tags[0] == "VERB":
    #             return set(), {words[0]}
    #         if pos_tags[0] == "NOUN":
    #             return {words[0]}, set()
    #
    #         return terms, {words[0]}
    #
    #     parts = []
    #     index = 0
    #     word_num = len(lemma_words)
    #     adj_flag = -1
    #     while index < word_num:
    #         if index in np_index:
    #             np_words = lemma_words[index: np_index[index]]
    #             if np_words[0] in self.SPECIAL_VERB:
    #                 parts.append((np_words[0], "VERB"))
    #                 np = " ".join(np_words[1:])
    #             else:
    #                 np = " ".join(np_words)
    #             if len(np) > 0:
    #                 if adj_flag >= 0:
    #                     np = lemma_words[adj_flag] + " " + np
    #                 parts.append((np, "NP"))
    #             index = np_index[index]
    #             adj_flag = -1
    #         elif lemma_words[index] in {"id", "ID", "Id"}:
    #             np = lemma_words[index]
    #             if adj_flag >= 0:
    #                 np = lemma_words[adj_flag] + " " + np
    #
    #             elif len(parts) > 0 and parts[-1][1] == "NP":
    #                 ele, tag = parts.pop()
    #                 np = "{} {}".format(ele, lemma_words[index])
    #             parts.append((np, "NP"))
    #             index += 1
    #             adj_flag = -1
    #         elif pos_tags[index] == "VERB" and lemma_words[index].endswith("ed"):
    #             adj_flag = index
    #             index += 1
    #         else:
    #             adj_flag = -1
    #             parts.append((lemma_words[index], pos_tags[index]))
    #             index += 1
    #     index = 0
    #     np_flag = -1
    #     of_flag = -1
    #     while index < len(parts):
    #         ele, tag = parts[index]
    #         if tag == "NP":
    #             if of_flag >= 0:
    #                 cur = parts.pop(index)[0]
    #                 of = parts.pop(index - 1)[0]
    #                 prev = parts.pop(index - 2)[0]
    #                 np = " ".join([prev, of, cur])
    #                 parts.append((np, "NP"))
    #                 index = index - 2
    #                 of_flag = -1
    #             else:
    #                 np_flag = index
    #                 index += 1
    #         elif ele == "of" and of_flag < 0 and np_flag >= 0:
    #             of_flag = index
    #             index += 1
    #         else:
    #             np_flag = -1
    #             of_flag = -1
    #             index += 1
    #     # print(parts)
    #     operations.update([ele for ele, tag in parts if tag == "VERB"])
    #     nps = {ele for ele, tag in parts if tag == "NP"}
    #     terms.update(nps)
    #     print("pos tags", parts)
    #
    #     return terms, operations


if __name__ == '__main__':
    line = "java.tool.Map.toString(too a)"
    searchObj = re.search(r"\.to\w+\(", line, re.M | re.I)
    if searchObj:
        print(searchObj.group())
