import traceback

import numpy as np
from gensim.models import KeyedVectors
from nltk import WordNetLemmatizer

from sekg.constant.constant import PropertyConstant, DomainConstant, WikiDataConstance
from sekg.graph.exporter.graph_data import GraphData
from sekg.text.extractor.domain_entity.nlp_util import SpacyNLPFactory
from sekg.text.extractor.domain_entity.relation_detection import RelationType
from sekg.wiki.WikiDataItem import WikiDataItem
from sekg.wiki.fusion.base import GenericKGFusion
from sekg.wiki.search_domain_wiki.wikidata_searcher import AsyncWikiSearcher
from sekg.wiki.wiki_util import WikiDataPropertyTable

"""
For each noun concept C_A, we use the following process to extend relevant Wikidata concepts and relations. First,
we search Wikidata concepts with the name and alias of C_A and collect the top 10 matched concepts for each search as the 
candidate Wikidata concepts CandWC. Second, we remove those concepts that share no names or aliases with C_A from CandWC. Third, we determine the Wikidata concept that C_A can be linked to in the
following way: 1) if there are concepts in CandW_C whose topic relevance is higher than 0.95, link C_A to the candidate concept with the highest topic relevance; 2) otherwise, if there is a concept CW
that has the highest topic relevance in CandW_C and the context similarity betweenC_A andCW is higher than 0.85, linkC_A toCW ; 3)
otherwise, if there are concepts in CandW_C whose topic relevance is higher than 0.8 and whose context similarity with C_A is higher
than 0.9, choose the conceptCW that has the highest topic relevance among them and link C_A to CW
"""


class WeightedScoreBasedGenericKGFusion(GenericKGFusion):
    INVALID_TEXTS = {"scientific article", "wikimedia template", "wikimedia list article", "wikipedia template",
                     "wikibase wikis", "wikimedia", "wikibase", "wikidata", "family", "singer", "music", "movie",
                     "book"}
    INVALID_SUBCLASS_ITEM_ID = set(["Q11424",  # film
                                    "Q15138389",  # wiki
                                    "Q7187",  # gene
                                    ])

    DEFAULT_FILTER_CONTEXT_SCORE = 0.8
    DEFAULT_FILTER_TOPIC_SCORE = 0.9

    DEFAULT_ACCEPTABLE_TOPIC_SCORE = 0.95
    DEFAULT_ACCEPTABLE_CONTEXT_SCORE = 0.85

    DEFAULT_PROXY_SERVER = "http://127.0.0.1:1080"

    DEFAULT_CONTEXT_SCORE_WEIGHT = 0.6
    DEFAULT_TOPIC_SCORE_WEIGHT = 0.4
    DEFAULT_FILTER_SUM_SCORE = 0.8

    def __init__(self, context_score_weight=DEFAULT_CONTEXT_SCORE_WEIGHT,
                 topic_score_weight=DEFAULT_TOPIC_SCORE_WEIGHT,
                 filter_sum_score=DEFAULT_FILTER_SUM_SCORE,
                 proxy_server=DEFAULT_PROXY_SERVER):
        # todo: fix this, remove this, use other lemmatizer way

        self.fetcher = AsyncWikiSearcher(proxy_server)
        self.graph_data = GraphData()
        self.wikidata_property_table = WikiDataPropertyTable.get_instance()
        self.embedding = {}
        self.context_score_weight = context_score_weight
        self.topic_score_weight = topic_score_weight
        self.filter_sum_score = filter_sum_score
        self.NLP = SpacyNLPFactory.create_simple_nlp_pipeline()
        self.lemmatizer = self.NLP.Defaults.create_lemmatizer()

    def init_wd_from_cache(self, title_save_path=None, item_save_path=None):
        self.fetcher.init_from_cache(title_save_path=title_save_path, item_save_path=item_save_path)
        print("Init from cache...")

    def export_wd_cache(self, title_save_path, item_save_path):

        self.fetcher.save(item_save_path=item_save_path, title_save_path=title_save_path)

    def load_word_embedding(self, emb_path):
        wv = KeyedVectors.load(emb_path)
        self.embedding = {k: wv[k] for k in wv.vocab.keys()}

    def init_graph_data(self, graph_data_path):
        self.graph_data = GraphData.load(graph_data_path)

    def fetch_wikidata_by_name(self, terms, title_save_path=None, item_save_path=None):
        """
                search with some terms and find the candidate wikidata item list for the term,
                 and cache all the possible wikidata item for the item.
                 eg. for term: "apple", we will search it in wikidata.org by API and get the returned
                 search result list(maybe 10 result). the search result for keywords will be cached.
                 And we we retrieve all 10 candidate wikidata item info.

                :param item_save_path: the wikidata item info cache path
                :param title_save_path:  the search result by title saving path
                :param terms: a list of str or a set of str standing for concepts.
                :return:
                """
        self.fetcher.init_from_cache(title_save_path=title_save_path, item_save_path=item_save_path)
        terms = {self.lemmatizer.noun(term)[0].lower() for term in terms}
        print("need to fetch %r term wiki titles, %r are already cache, actual %r need to fetch" % (
            len(terms), len(self.fetcher.title_cache.keys() & terms),
            len(terms) - len(self.fetcher.title_cache.keys() & terms)))

        term_titles = self.fetcher.search_title(terms)
        if title_save_path is not None:
            self.fetcher.save(title_save_path=title_save_path)

        ids = self.get_valid_wikidata_item(term_titles)
        term_wikiitems = self.fetch_wikidata_by_id(ids, item_save_path)
        return term_titles, term_wikiitems

    @staticmethod
    def is_need_to_fetch_wikidata_item(item):
        INVALID_TEXTS = ["scientific article", "wikimedia template", "wikimedia list article", "wikipedia template",
                         "wikibase wikis", "wikimedia"]

        snippet = item["snippet"].lower()
        for invalid_text in INVALID_TEXTS:
            if invalid_text in snippet:
                return False

        return True

    @staticmethod
    def get_valid_wikidata_item(term_titles):
        """
        some search results for wikidata are not need to search, for example, the item has "scientific article" in description.
        :param term_titles:
        :return:
        """
        valid_wikidata_ids = set([])

        for v in term_titles.values():
            for item in v:
                if WeightedScoreBasedGenericKGFusion.is_need_to_fetch_wikidata_item(item) == False:
                    continue
                valid_wikidata_ids.add(item["title"])

        return valid_wikidata_ids

    def fetch_wikidata_by_id(self, ids, item_save_path=None):

        print("need to fetch wikidata items num=%r, %r are already cache, actual %r need to fetch" % (
            len(ids), len(self.fetcher.item_cache.keys() & ids),
            len(ids) - len(self.fetcher.item_cache.keys() & ids)))

        term_wikiitems = self.fetcher.fetch_item(ids)
        if item_save_path is not None:
            self.fetcher.save(item_save_path=item_save_path)
        return term_wikiitems

    def compute_topic_vector(self):
        topic_words = []
        for node_id in self.graph_data.get_node_ids_by_label(DomainConstant.LABEL_DOMAIN_TERM):
            try:
                node_json = self.graph_data.get_node_info_dict(node_id=node_id)
                if not node_json:
                    continue
                node_properties = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES]
                if PropertyConstant.LEMMA in node_properties:
                    lemma = node_properties[PropertyConstant.LEMMA]
                    topic_words.append(lemma)

                aliases = node_properties.get(PropertyConstant.ALIAS, [])
                aliases_en = node_properties.get("aliases_en", [])
                description_en = node_properties.get("descriptions_en", "")
                name = node_properties.get("name", "")
                topic_words.extend(aliases)
                topic_words.extend(aliases_en)
                topic_words.append(description_en)
                topic_words.append(name)
            except:
                traceback.print_exc()
        topic_text = " ".join(topic_words).lower()

        if len(topic_text) == 0:
            return None
        words = [w for w in topic_text.split() if w]
        if len(words) == 0:
            return None
        vec_des = sum([self.embedding.get(w, np.zeros([100])) for w in words]) / len(words)

        return vec_des

    def compute_wikidata_vector(self, wikidata_item, term_wikiitems, domain_term_name=""):
        """
        if given the domain term name, the name containing in domain term will be exclude from the text
        :param wikidata_item:
        :param term_wikiitems:
        :param domain_term_name:
        :return:
        """
        relation_text = self.generate_relations_text(wikidata_item, term_wikiitems)
        description = wikidata_item.get_en_description()
        en_name = wikidata_item.get_en_name()
        en_aliases = wikidata_item.get_en_aliases()

        description = " ".join([en_name, " ".join(en_aliases), description, relation_text])

        # words = list(set(
        #     [token.lemma_.lower() for token in self.NLP(description) if
        #      token.is_digit == False and token.is_stop == False]))
        words = [token.lemma_.lower() for token in self.NLP(description) if
                 token.is_digit == False and token.is_stop == False and token.is_punct == False]
        # todo: fix this name

        removal_words = set(domain_term_name.lower().split())
        words = [w for w in words if w not in removal_words]

        if len(words) == 0:
            return None
        # todo: the size of vector should be adjust
        vec_des = sum([self.embedding.get(w, np.zeros([100])) for w in words]) / len(words)

        return vec_des

    def __score_topic(self, topic_vector, wikidata_item, term_wikiitems, domain_term_name=""):

        wikidata_vector = self.compute_wikidata_vector(wikidata_item, term_wikiitems, domain_term_name=domain_term_name)
        return self.compute_sim_for_two_vectors(wikidata_vector, topic_vector)

    def __score_context(self, node_json, wikidata_item, term_wikiitems):
        relation_text = self.generate_relations_text(wikidata_item, term_wikiitems)
        description = wikidata_item.get_en_description()
        en_name = wikidata_item.get_en_name()
        en_aliases = wikidata_item.get_en_aliases()

        description = " ".join([en_name, " ".join(en_aliases), description, relation_text])

        domain_term_name = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES][PropertyConstant.LEMMA]

        name = self.get_compare_name_for_domain_term(node_json)

        removal_words = set(domain_term_name.lower().split())

        if len(description) == 0 or len(name) == 0:
            return 0
        # words = list(set(
        #     [token.lemma_.lower() for token in self.NLP(description) if
        #      token.is_digit == False and token.is_stop == False]))
        words = [token.lemma_.lower() for token in self.NLP(description) if
                 token.is_digit == False and token.is_stop == False and token.is_punct == False]
        words = [w for w in words if w not in removal_words]

        if len(words) == 0:
            return 0
        vec_des = sum([self.embedding.get(w, np.zeros([100])) for w in words]) / len(words)
        # name_words = list(
        #     set([token.lemma_.lower() for token in self.NLP(name) if
        #          token.is_digit == False and token.is_stop == False]))
        name_words = [token.lemma_.lower() for token in self.NLP(name) if
                      token.is_digit == False and token.is_stop == False]

        if len(name_words) == 0:
            return 0
        vec_term = sum([self.embedding.get(w, np.zeros([100])) for w in name_words]) / len(name_words)

        return self.compute_sim_for_two_vectors(vec_des, vec_term)

    def compute_sim_for_two_vectors(self, vec_des, vec_term):
        norm_des = np.linalg.norm(vec_des)
        norm_term = np.linalg.norm(vec_term)
        if norm_des == 0 or norm_term == 0:
            return 0
        return 0.5 + vec_des.dot(vec_term) / (norm_des * norm_term) / 2

    def get_compare_name_for_domain_term(self, node_json):
        domain_term_id = node_json[GraphData.DEFAULT_KEY_NODE_ID]

        name = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES].get(PropertyConstant.LEMMA, "")
        aliases = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES].get(PropertyConstant.ALIAS, [])
        aliases_en = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES].get("aliases_en", [])

        other_names = [name]
        other_names.extend(aliases)
        other_names.extend(aliases_en)

        out_relations = self.graph_data.get_all_out_relations(node_id=domain_term_id)
        in_relations = self.graph_data.get_all_in_relations(node_id=domain_term_id)
        domain_term_node_ids = self.graph_data.label_to_ids_map[DomainConstant.LABEL_DOMAIN_TERM]
        id_set = set([])
        for (start_id, r, end_id) in out_relations:
            if end_id in domain_term_node_ids:
                id_set.add(end_id)
        for (start_id, r, end_id) in in_relations:
            if start_id in domain_term_node_ids:
                id_set.add(start_id)
        id_set.add(domain_term_id)
        for id in id_set:
            temp_node_json = self.graph_data.get_node_info_dict(node_id=id)
            other_names.append(temp_node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES].get(PropertyConstant.LEMMA, ""))
        name = " ".join(other_names)
        return name

    def add_wikidata_item(self, item: WikiDataItem):
        """
        add a new term to graph data
        :param term: the term added to GraphData
        :return: the node_id fo the added term node
        """
        ori_node_json = self.graph_data.find_one_node_by_property(WikiDataConstance.PRIMARY_PROPERTY_NAME,
                                                                  item.wd_item_id)
        if ori_node_json:
            # print(ori_node_json)
            # print('no new wiki node!! node %d has fused wiki_node %s' % (ori_node_json["id"], item.wd_item_id))
            return ori_node_json["id"]
        # print("add new wikinode %s" % (item.wd_item_id))
        node_labels = [WikiDataConstance.LABEL_WIKIDATA]
        node_properties = {
            WikiDataConstance.PRIMARY_PROPERTY_NAME: item.wd_item_id,
            WikiDataConstance.NAME: item.get_en_name(),
            PropertyConstant.ALIAS: set(item.get_en_aliases()),
        }
        item.get_relation_property_name_list()
        relation_property_set = set(item.relation_property_name_list)
        pure_property_set = set(item.get_non_relation_property_name_list())

        valid_property_dict = {}
        for p, v in item.data_dict.items():
            if p in relation_property_set:
                continue
            if p in pure_property_set:
                p = self.wikidata_property_table.property_id_2_name(p)
                if p == None:
                    continue
            valid_property_dict[p] = v
        wikidata_node_id = self.graph_data.add_node(node_labels=node_labels,
                                                    node_properties=dict(valid_property_dict, **node_properties),
                                                    primary_property_name=WikiDataConstance.PRIMARY_PROPERTY_NAME)
        return wikidata_node_id

    def fuse_wikidata_item(self, domain_id, item: WikiDataItem):
        """
        add WikiDataItem into to domian term node
        :domain_id: domain_term id
        :param term: the term added to GraphData
        :return: the node_id fo the added term node
        """
        node_properties = {
            WikiDataConstance.PRIMARY_PROPERTY_NAME: item.wd_item_id,
            WikiDataConstance.NAME: item.get_en_name(),
            PropertyConstant.ALIAS: set(item.get_en_aliases()),
        }
        item.get_relation_property_name_list()
        relation_property_set = set(item.relation_property_name_list)
        pure_property_set = set(item.get_non_relation_property_name_list())

        valid_property_dict = {}
        for p, v in item.data_dict.items():
            if p in relation_property_set:
                continue
            if p in pure_property_set:
                p = self.wikidata_property_table.property_id_2_name(p)
                if p == None:
                    continue
            valid_property_dict[p] = v

        self.graph_data.add_labels(WikiDataConstance.LABEL_WIKIDATA)
        self.graph_data.add_label_by_node_id(domain_id, WikiDataConstance.LABEL_WIKIDATA)
        domain_node_json = self.graph_data.get_node_info_dict(domain_id)
        domain_properties_json = domain_node_json[self.graph_data.DEFAULT_KEY_NODE_PROPERTIES]
        if domain_node_json:
            for k, v in dict(valid_property_dict, **node_properties).items():
                if k in domain_properties_json:
                    if v == domain_properties_json[k]:
                        pass
                    else:
                        if type(v) == set:
                            domain_properties_json[k] = v.union(domain_properties_json[k])
                        if type(v) == list:
                            domain_properties_json[k].extend(v)
                        if type(v) == str:
                            domain_properties_json[k + "_wiki"] = v
                else:
                    domain_properties_json[k] = v
        # print("fuse node %d and wiki node %s" % (domain_id, item.wd_item_id))
        # print("&" * 10)
        # print(self.graph_data.get_node_info_dict(domain_id))
        return domain_id

    def init_lemma(self):
        lemmatizer = WordNetLemmatizer()
        self.graph_data.create_index_on_property(PropertyConstant.LEMMA)

        for node_id in self.graph_data.get_node_ids_by_label(DomainConstant.LABEL_DOMAIN_TERM):
            node_json = self.graph_data.get_node_info_dict(node_id=node_id)

            if not node_json:
                continue

            node_properties = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES]

            lemma_domain_term_name = node_properties[DomainConstant.PRIMARY_PROPERTY_NAME]
            lemma_domain_term_name = lemma_domain_term_name.lower()
            lemma_domain_term_name = lemmatizer.lemmatize(lemma_domain_term_name, "n")
            node_properties[PropertyConstant.LEMMA] = lemma_domain_term_name

        self.graph_data.refresh_indexer()

    def fuse(self, ):
        # todo: this fusion has dependency on GraphData, not good.
        self.graph_data.create_index_on_property(WikiDataConstance.PRIMARY_PROPERTY_NAME)
        self.init_lemma()

        term_titles = self.fetcher.get_title_cache()
        # todo: by calling the method not access the field
        term_wikiitems = self.fetcher.get_item_cache()

        id_item = {}
        record = []
        topic_vector = self.compute_topic_vector()
        if topic_vector is None:
            print("error, topic vector is None, maybe the graph has not domain term")
            return
        for node_id in self.graph_data.get_node_ids_by_label(DomainConstant.LABEL_DOMAIN_TERM):
            try:
                node_json = self.graph_data.get_node_info_dict(node_id=node_id)
                if not node_json:
                    continue
                if WikiDataConstance.LABEL_WIKIDATA not in node_json["labels"]:
                    node_properties = node_json[GraphData.DEFAULT_KEY_NODE_PROPERTIES]
                    if PropertyConstant.LEMMA not in node_properties:
                        continue
                    lemma = ""
                    if PropertyConstant.ALIAS in node_properties:
                        alias_set = node_properties[PropertyConstant.ALIAS]
                    else:
                        alias_set = set()
                    if PropertyConstant.LEMMA in node_properties:
                        lemma = node_properties[PropertyConstant.LEMMA]
                        alias_set.add(lemma)
                        alias_set.add(lemma.lower())

                    if lemma.find(".") >= 0 or lemma.find("(") >= 0:
                        continue
                    items = set()
                    for lemma in alias_set:
                        if lemma not in term_titles:
                            continue
                        titles = term_titles[lemma]
                        for title in titles:
                            item = term_wikiitems.get(title["title"], None)
                            if item is None:
                                continue
                            wk_names = set()
                            for n in item.get_en_aliases():
                                wk_names.add(n)
                                wk_names.add(n.lower())

                            wk_names.add(item.get_en_name())
                            wk_names.add(item.get_en_name().lower())

                            if item is None or lemma not in wk_names:
                                continue
                            if self.is_valid_wikidata_item(item) is False:
                                continue
                            items.add(item)

                    if len(items) == 0:
                        continue
                    items = list(items)
                    sims = [(item, self.__score_context(node_json, item, term_wikiitems),
                             self.__score_topic(topic_vector, item, term_wikiitems,
                                                domain_term_name=lemma)) for item in items]

                    combined_sims = []

                    for item, context_score, topic_score in sims:
                        combined_sims.append((item, context_score, topic_score,
                                              context_score * self.context_score_weight + topic_score * self.topic_score_weight))

                    best_link_wikidata_item, best_context_score, best_topic_score, best_sum_score = max(combined_sims,
                                                                                                        key=lambda x: x[
                                                                                                            2])

                    is_link = False
                    if best_sum_score > self.filter_sum_score:
                        is_link = True

                    record.append({
                        "name": best_link_wikidata_item.get_en_name(),
                        "alias": best_link_wikidata_item.get_en_aliases(),
                        "description": best_link_wikidata_item.get_en_description(),
                        "wk relation text": self.generate_relations_text(best_link_wikidata_item, term_wikiitems),
                        "domain term": lemma,
                        "combine_score": best_sum_score,
                        "context_score": best_context_score,
                        "topic_score": best_topic_score,
                        "combined name": self.get_compare_name_for_domain_term(node_json),
                        "link": is_link,
                        "domain_id": node_id,
                        "wd_item_id": best_link_wikidata_item.wd_item_id
                    })

                    if best_link_wikidata_item == None:
                        continue
                    if is_link == False:
                        continue
                    # wikidata_node_id = self.add_wikidata_item(best_link_wikidata_item)
                    if is_link:
                        wikidata_node_id = self.fuse_wikidata_item(node_id, best_link_wikidata_item)
                        if wikidata_node_id == GraphData.UNASSIGNED_NODE_ID:
                            continue
                        id_item[wikidata_node_id] = best_link_wikidata_item
            except Exception:
                traceback.print_exc()
        self.build_relation_between_wikidata_node_in_graph(term_wikiitems)
        neighbours = set()
        for _id, item in id_item.items():
            for r in item.relation_property_name_list:
                end_id_set = self.get_wikidata_item_ids_by_relation(item, r)
                for e in end_id_set:
                    neighbours.add(e)
        self.graph_data.refresh_indexer()
        return neighbours, record

    def fuse_with_prefix_and_suffix(self):
        domain_ids = self.graph_data.get_node_ids_by_label(DomainConstant.LABEL_DOMAIN_TERM)
        wiki_ids = self.graph_data.get_node_ids_by_label(WikiDataConstance.LABEL_WIKIDATA)
        unfuse_domain = domain_ids - wiki_ids
        unfuse_wiki = wiki_ids - domain_ids
        relations_set = set()
        domain_wiki_map = {}
        relations = []
        domain_wiki_fuse = []
        lemmatizer = WordNetLemmatizer()

        clean_wiki_name_map = {}

        for wiki_id in wiki_ids:
            wiki_node_info = self.graph_data.get_node_info_dict(wiki_id)
            wiki_node_id = wiki_node_info[GraphData.DEFAULT_KEY_NODE_ID]
            wikidata_name = wiki_node_info[GraphData.DEFAULT_KEY_NODE_PROPERTIES][WikiDataConstance.NAME]
            aliases = wiki_node_info[GraphData.DEFAULT_KEY_NODE_PROPERTIES][PropertyConstant.ALIAS]

            clean_wiki_name_map[wiki_node_id] = set()
            clean_wikidata_name = lemmatizer.lemmatize(wikidata_name.lower(), "n")

            if len(clean_wikidata_name) > 2:
                clean_wiki_name_map[wiki_node_id].add((wikidata_name, clean_wikidata_name))
            for ali in aliases:
                clean_wiki_alise = lemmatizer.lemmatize(ali.lower(), "n")

                if len(clean_wiki_alise) > 2:
                    clean_wiki_name_map[wiki_node_id].add((ali, clean_wiki_alise))
            if not clean_wiki_name_map[wiki_node_id]:
                clean_wiki_name_map.pop(wiki_node_id)

        for domain_term_id in unfuse_domain:
            domain_node_info = self.graph_data.get_node_info_dict(domain_term_id)
            domain_name = domain_node_info[self.graph_data.DEFAULT_KEY_NODE_PROPERTIES][
                DomainConstant.PRIMARY_PROPERTY_NAME]
            domain_name_list = domain_name.lower().split(" ")
            domain_name = lemmatizer.lemmatize(domain_name.lower(), "n")

            for wikidata_node_id in clean_wiki_name_map:
                for wiki_name, clean_wiki_name in clean_wiki_name_map[wikidata_node_id]:
                    if domain_name == clean_wiki_name:
                        if domain_term_id not in domain_wiki_map:
                            domain_wiki_map[domain_term_id] = []
                            domain_wiki_map[domain_term_id].append(wikidata_node_id)
                        else:
                            domain_wiki_map[domain_term_id].append(wikidata_node_id)
                        domain_wiki_fuse.append(
                            {"domain_id": domain_term_id, "domain_name": domain_name, "wiki_id": wikidata_node_id,
                             "wiki_name": wiki_name})
                        continue
                    if len(domain_name_list) > 1:
                        if domain_name.startswith(clean_wiki_name + " "):
                            relations_set.add((domain_term_id, RelationType.PART_OF.value, wikidata_node_id))
                            relations.append(
                                {"domain_id": domain_term_id, "domain_name": domain_name,
                                 "relation": RelationType.PART_OF.value, "wiki_id": wikidata_node_id,
                                 "wiki_name": wiki_name})
                        if domain_name.endswith(" " + clean_wiki_name):
                            relations_set.add((domain_term_id, RelationType.IS_A.value, wikidata_node_id))
                            relations.append(
                                {"domain_id": domain_term_id, "domain_name": domain_name,
                                 "relation": RelationType.IS_A.value, "wiki_id": wikidata_node_id,
                                 "wiki_name": wiki_name})

        print("and new domian_wiki relation %d" % (len(relations_set)))
        for item in relations_set:
            s = item[0]
            r = item[1]
            e = item[2]
            self.graph_data.add_relation(s, r, e)

        # fuse wiki_node and domain_node , they have the same name
        for domain_id in domain_wiki_map:
            wiki_id = domain_wiki_map[domain_id][0]
            self.graph_data.merge_two_nodes_by_id(main_node_id=wiki_id, merged_node_id=domain_id,
                                                  main_alias_property=PropertyConstant.ALIAS,
                                                  merged_alias_property=PropertyConstant.ALIAS)

        return domain_wiki_fuse, relations

    @staticmethod
    def get_wikidata_item_ids_by_relation(wikidata_item: WikiDataItem, r):
        id_set = set([])
        end = wikidata_item.data_dict.get(r, [])
        if type(end) == list:
            for e in end:
                id_set.add(e)
        else:
            id_set.add(end)
        return id_set

    def generate_relations_text(self, wikidata_item, term_wikiitems):
        text = []
        for r in wikidata_item.relation_property_name_list:

            relation_name = self.wikidata_property_table.property_id_2_name(r)
            if relation_name == None:
                relation_name = r
            end = wikidata_item.data_dict[r]

            if type(end) == list:
                for e_wd_item_id in end:
                    if self.is_valid_wikidata_item_id(e_wd_item_id):
                        neibour_item = term_wikiitems.get(e_wd_item_id, None)
                        if neibour_item != None:
                            text.append(neibour_item.get_en_name())
                            # if relation_name in {"subclass of", "instance of", "part of"}:
                            #     text.append(neibour_item.get_en_description())
                            text.append(neibour_item.get_en_description())

                    else:
                        text.append(end)
                text.append(relation_name)

            else:
                if self.is_valid_wikidata_item_id(end):
                    neibour_item = term_wikiitems.get(end, None)
                    if neibour_item != None:
                        text.append(neibour_item.get_en_name())
                        # if relation_name in {"subclass of", "instance of", "part of"}:
                        #     text.append(neibour_item.get_en_description())
                        text.append(neibour_item.get_en_description())
                else:
                    text.append(end)
                text.append(relation_name)

        return " ".join(text)

    def is_valid_wikidata_item_id(self, wd_item_id):
        try:

            if wd_item_id.startswith("Q") and wd_item_id[1:].isdigit():
                return True
            return False
        except:
            return False

    def get_all_neighbours_id(self, item):
        neighbours = set()
        for r in item.relation_property_name_list:
            end = item.data_dict[r]
            if type(end) == list:
                for e in end:
                    if e[0] == "Q" or e[0] == "P":
                        neighbours.add(e)
            else:
                if end[0] == "Q" or end[0] == "P":
                    neighbours.add(end)

        return neighbours

    def get_all_neighbours_id_by_item_id(self, item_id):
        neighbours = set()
        item = self.fetcher.item_cache.get(item_id, None)
        if item == None:
            return set()
        for r in item.relation_property_name_list:
            end = item.data_dict[r]
            if type(end) == list:
                for e in end:
                    if e[0] == "Q" or e[0] == "P":
                        neighbours.add(e)
            else:
                if end[0] == "Q" or end[0] == "P":
                    neighbours.add(end)

        return neighbours

    def fetch_valid_wikidata_item_neibours_from_all_term_titles(self, item_save_path):
        """
        some search results for wikidata are not need to search, for example, the item has "scientific article" in description.
        :param term_titles:
        :return:
        """
        term_titles = self.fetcher.title_cache
        valid_wikidata_ids = GenericKGFusion.get_valid_wikidata_item(term_titles)
        nerbours = set([])

        for valid_id in valid_wikidata_ids:
            nerbours.update(self.get_all_neighbours_id_by_item_id(valid_id))
        return self.fetch_wikidata_by_id(nerbours, item_save_path)

    def add_wikidata_items(self, wd_item_ids):
        term_wikiitems = self.fetcher.item_cache
        self.graph_data.refresh_indexer()
        for wd_item_id in wd_item_ids:
            if wd_item_id in term_wikiitems:
                self.add_wikidata_item(term_wikiitems[wd_item_id])
        self.build_relation_between_wikidata_node_in_graph(term_wikiitems)

    def build_relation_between_wikidata_node_in_graph(self, term_wikiitems):
        wikidata_node_ids = self.graph_data.get_node_ids_by_label(WikiDataConstance.LABEL_WIKIDATA)
        wd_item_id_2_node_id_map = {}
        node_id_2_wd_item_id_map = {}
        for node_id in wikidata_node_ids:
            wikidata_node = self.graph_data.get_node_info_dict(node_id)
            wd_item_id = wikidata_node[GraphData.DEFAULT_KEY_NODE_PROPERTIES][WikiDataConstance.PRIMARY_PROPERTY_NAME]
            wd_item_id_2_node_id_map[wd_item_id] = node_id
            node_id_2_wd_item_id_map[node_id] = wd_item_id
        for start_wd_item_id, start_node_id in wd_item_id_2_node_id_map.items():
            start_wikidata_item = term_wikiitems.get(start_wd_item_id, None)
            if start_wikidata_item == None:
                continue
            for r_id in start_wikidata_item.relation_property_name_list:
                end_wd_ids = self.get_wikidata_item_ids_by_relation(start_wikidata_item, r_id)
                relation_name = self.wikidata_property_table.property_id_2_name(r_id)
                if relation_name == None:
                    continue

                for end_wd_id in end_wd_ids:
                    end_node_id = wd_item_id_2_node_id_map.get(end_wd_id, None)
                    if end_node_id == None:
                        continue
                    if start_node_id == end_node_id:
                        continue
                    self.graph_data.add_relation(start_node_id, relation_name, end_node_id)

    def save(self, graph_data_path):
        self.graph_data.save(graph_data_path)

    def is_valid_wikidata_item(self, item):
        for text in self.INVALID_TEXTS:
            en_name = item.get_en_name().lower()
            if text in en_name:
                return False
            description = item.get_en_description()
            if text in description:
                return False
        end_wd_ids = self.get_wikidata_item_ids_by_relation(item, "P31")

        for end_wd in end_wd_ids:
            if end_wd in self.INVALID_SUBCLASS_ITEM_ID:
                return False

        return True

    def fetch_wikidata_by_name_and_cache_neibours(self, terms, title_save_path, item_save_path):
        self.fetch_wikidata_by_name(terms, item_save_path=item_save_path, title_save_path=title_save_path)
        self.fetch_valid_wikidata_item_neibours_from_all_term_titles(item_save_path=item_save_path)

    def merge_domain_nodes_fuse_same_wiki_item(self, nodes):
        for i in range(1, len(nodes)):
            print("merge %d && %d !" % (nodes[0], nodes[i]))
            self.graph_data.merge_two_nodes_by_id(nodes[0], nodes[i], PropertyConstant.ALIAS, PropertyConstant.ALIAS)
            # print(self.graph_data.get_node_info_dict(nodes[0]))
