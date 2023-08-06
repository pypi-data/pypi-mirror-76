from gensim.models import Word2Vec
from gensim.models.keyedvectors import Word2VecKeyedVectors

from sekg.ir.doc.wrapper import PreprocessMultiFieldDocumentCollection

"""
    Here is some pretrain word2vec:
    https://github.com/3Top/word2vec-api

"""


class TunedWord2VecTrainer:
    @staticmethod
    def tune(corpus, pretrain_w2v_path, pretrain_binary=True, window=5, min_count=1, size=100, iter=3, alpha=0.0001):
        """
        tune the pretrained word2vec
        :param corpus:
        :param pretrain_w2v_path:
        :param pretrain_binary:
        :param window:
        :param min_count:
        :param size:
        :param iter: the iter can't be too much, otherwise the pretrained Word2Vec won't be helpful.
        :param alpha: the learning rate, the alpha. alpha the can't be too high.
        :return:
        """
        pretrained_word2vec_model = Word2VecKeyedVectors.load_word2vec_format(
            pretrain_w2v_path,
            binary=pretrain_binary)

        w2v = Word2Vec(window=window, min_count=min_count, size=size, iter=iter, alpha=alpha)
        w2v.build_vocab(corpus)
        training_examples_count = w2v.corpus_count
        w2v.build_vocab([list(pretrained_word2vec_model.vocab.keys())], update=True)

        w2v.intersect_word2vec_format(pretrain_w2v_path, binary=pretrain_binary, lockf=1.0)
        w2v.train(corpus, total_examples=training_examples_count, epochs=w2v.epochs)
        return w2v

    @staticmethod
    def tune_from_pre_doc_collection(preprocess_doc_collection: PreprocessMultiFieldDocumentCollection,
                                     pretrain_w2v_path, pretrain_binary=True,
                                     window=5, min_count=1, size=100, iter=3,
                                     alpha=0.0001):
        corpus = []
        preprocess_multi_field_doc_list = preprocess_doc_collection.get_all_preprocess_document_list()
        for docno, multi_field_doc in enumerate(preprocess_multi_field_doc_list):
            corpus.append(multi_field_doc.get_document_text_words())

        print("Start training embedding...")
        return TunedWord2VecTrainer.tune(corpus, pretrain_w2v_path, pretrain_binary=pretrain_binary,
                                         window=window, min_count=min_count, size=size, iter=iter,
                                         alpha=alpha)
