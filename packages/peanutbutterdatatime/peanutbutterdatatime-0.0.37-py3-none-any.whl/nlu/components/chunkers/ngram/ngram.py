import nlu.pipe_components
from sparknlp.annotator import *

class NGram:
    @staticmethod
    def get_default_model():
        return NGramGenerator() \
            .setInputCols(["token", "pos"]) \
            .setOutputCol("ngrams") \
            .setN(2) \
            .setEnableCumulative(True) \
