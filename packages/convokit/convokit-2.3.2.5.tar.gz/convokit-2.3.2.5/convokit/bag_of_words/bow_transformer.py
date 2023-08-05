from convokit import Corpus, CorpusObject, Transformer
from typing import Callable
from sklearn.feature_extraction.text import CountVectorizer as CV

class BoWTransformer(Transformer):
    """
    Bag-of-Words Transformer for annotating a Corpus's objects with the bag-of-words vectorization
    of some textual element.

    - For utterances, this would be the utterance text.
    - For conversations, this would be joined texts of all the utterances in the conversation
    - For speakers, this would be the joined texts of all the utterances by the speaker

    Compatible with any type of vectorizer (e.g. bag-of-words, TF-IDF, etc)

    Runs on the Corpus's Speakers, Utterances, or Conversations (as specified by obj_type)

    :param obj_type: "speaker", "utterance", or "conversation"
    :param vectorizer: a sklearn vectorizer object; default is CountVectorizer(min_df=10, max_df=.5, ngram_range(1, 1),
        binary=False, max_features=15000)
    :param vector_name: the name of the metadata key to store the vector under
    :param text_func: an optional (lambda) function to extract the textual element from the Corpus object, see
        defaults above.

    """
    def __init__(self, obj_type: str, vectorizer=None, vector_name="bow_vector",
                 text_func: Callable[[CorpusObject], str] = None):

        if vectorizer is None:
            print("Initializing default unigram CountVectorizer...", end="")
            self.vectorizer = CV(decode_error='ignore', min_df=10, max_df=.5,
                                 ngram_range=(1, 1), binary=False, max_features=15000)
            print("Done.")
        else:
            self.vectorizer = vectorizer

        self.obj_type = obj_type
        self.vector_name = vector_name

        if text_func is None:
            if obj_type == "utterance":
                self.text_func = lambda utt: utt.text
            elif obj_type == "conversation":
                self.text_func = lambda convo: " ".join(utt.text for utt in convo.iter_utterances())
            elif obj_type == "speaker":
                self.text_func = lambda speaker: " ".join(utt.text for utt in speaker.iter_utterances())
            else:
                raise ValueError("Invalid corpus object type. Use 'utterance', 'conversation', or 'speaker'")
        else:
            self.text_func = text_func

    def fit(self, corpus: Corpus, y=None, selector: Callable[[CorpusObject], bool] = lambda x: True):
        """
        Fit the Transformer's internal vectorizer on the Corpus objects' texts, with an optional selector that filters for objects to be fit on.

        :param corpus: the target Corpus
        :param selector: a (lambda) function that takes a Corpus object and returns True or False (i.e. include / exclude). By default, the selector includes all objects of the specified type in the Corpus.
        :return: the fitted BoWTransformer
        """
        # collect texts for vectorization
        docs = []
        for obj in corpus.iter_objs(self.obj_type, selector):
            docs.append(self.text_func(obj))

        self.vectorizer.fit(docs)
        return self

    def transform(self, corpus: Corpus, selector: Callable[[CorpusObject], bool] = lambda x: True) -> Corpus:
        """
        Annotate the corpus objects with the vectorized representation of the object's text, with an optional
        selector that filters for objects to be transformed. Objects that are not selected will get a metadata value
        of 'None' instead of the vector.

        :param corpus: the target Corpus
        :param selector: a (lambda) function that takes a Corpus object and returns True or False (i.e. include / exclude). By default, the selector includes all objects of the specified type in the Corpus.

        :return: the target Corpus annotated
        """
        for obj in corpus.iter_objs(self.obj_type):
            if selector(obj):
                obj.meta[self.vector_name] = self.vectorizer.transform([self.text_func(obj)])
            else:
                obj.meta[self.vector_name] = None

        return corpus

    def fit_transform(self, corpus: Corpus, y=None, selector: Callable[[CorpusObject], bool] = lambda x: True) -> Corpus:
        self.fit(corpus, selector=selector)
        return self.transform(corpus, selector=selector)

    def get_vocabulary(self):
        """
        Get the vocabulary of the vectorizer object
        """
        return self.vectorizer.get_feature_names()
