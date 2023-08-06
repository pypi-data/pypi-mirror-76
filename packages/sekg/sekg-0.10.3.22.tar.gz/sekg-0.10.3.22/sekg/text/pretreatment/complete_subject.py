from sekg.text.spacy_pipeline.pipeline import PipeLineFactory
from sekg.util.dependency_tree_util import DependencyTreeUtil


class CompleteSubject:
    def __init__(self, nlp=None):
        if nlp is None:
            self.nlp = PipeLineFactory.full_pipeline()
        else:
            self.nlp = nlp

    def clean_pure_code_sentence(self, text: str):
        text = text.strip()
        if text.find(" ") < 0:
            return ""
        if text.find(".java") >= 0:
            return ""
        if text.find(">") >= 0 and text.find("<") >= 0 and text.find(";") >= 0:
            return ""
        if text.find("=") >= 0:
            return ""
        if text.find("(") >= 0 and text.find(";") >= 0:
            return ""

        return text

    def get_sentence_list_with_doc(self, doc):
        l = []
        for sent in doc.sents:
            clean = self.clean_pure_code_sentence(sent.text)
            if clean == "":
                continue
            l.append(sent)
        return l

    def complete_subject_by_name_for_doc(self, full_text, candidate_subject_name, spacy_doc=None,
                                         candidate_verb_set=None):
        """
        candidate_verb_set是从类下面所有的method名称或者method自己的名字里面抽取出的所有动词
        :param full_text:
        :param candidate_subject_name:
        :param spacy_doc:
        :param candidate_verb_set:
        :return:
        """
        if spacy_doc is not None:
            test_doc = spacy_doc
        else:
            test_doc = self.nlp(full_text)
        result = []
        for index, sent in enumerate(test_doc.sents):
            if index == 0:
                ## for long text, only try to complete the first sentence.
                result.append(
                    self.complete_subject_for_sentence(sent.text, candidate_subject_name, sent, candidate_verb_set))
            else:
                result.append(sent.text)

        return " ".join(result)

    def how_many_upper(self, input_text):
        """
        有多少个大写字符
        :param input_text:
        :return:
        """
        n = 0
        for l, r in zip(input_text.lower(), input_text):
            if l != r:
                n += 1
        return n

    def is_declarative_sentence(self, sentence):
        """
        check whether a sentence is
        :return:
        """
        # todo: complete this method to consider more situation
        if sentence[-1] == "?" or sentence[-1] == "!":
            return False
        return True

    def special_verb_subject_case(self, subject_span):
        """
        处理特殊情况 e.g. parse String to int. 会认为 parse String是主语，主要问题是parse理解成了名称NNP
        :return:
        """
        if subject_span is None:
            return False
        subject_doc = self.nlp(subject_span.text)
        for each in subject_doc:
            if each.tag_ == "NNP" and each.lemma_ == "parse":
                return True
        return False

    def complete_subject_for_sentence(self, sentence, candidate_subject_name, sent_doc=None, candidate_verb_set=None):
        """

        :param candidate_verb_set:
        :param sent_doc:
        :param sentence:
        :param candidate_subject_name:
        :return:补全后的句子
        """
        if not self.is_declarative_sentence(sentence):
            return sentence
        if candidate_verb_set is None:
            candidate_verb_set = set()
        candidate_verb_set.add("return")
        candidate_verb_set.add("create")
        candidate_verb_set.add("construct")
        candidate_verb_set.add("get")
        candidate_verb_set.add("set")
        subject = DependencyTreeUtil.get_subject_exclude_verb(sent_doc, candidate_verb_set)
        # for subject completor, it only check the sentence, it assume the sentence parsing is correct.
        special_case_1 = self.special_verb_subject_case(subject)
        if subject is not None and not special_case_1:
            return sentence

        predicate = DependencyTreeUtil.get_main_predicate_with_candidate_verbs(sent_doc, candidate_verb_set)
        if sent_doc[0].pos_ == "ADV" and sent_doc[0].tag_ == "EX":
            return sentence
        # is_vbn = DependencyTreeUtil.is_vbn(sent_doc)
        if predicate is None:
            append_str = candidate_subject_name + " is "
        else:
            append_str = candidate_subject_name + " "

        f = str(sentence[0]).lower()
        first_token = sent_doc[0]
        if self.how_many_upper(first_token.text) >= 1:
            sentence = append_str + f + sentence[1:]
        else:
            sentence = append_str + sentence

        return sentence
