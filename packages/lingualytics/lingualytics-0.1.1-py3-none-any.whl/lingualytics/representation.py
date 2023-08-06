import pandas as pd
import collections

def calc_ngrams(text: str, n: int):
    return zip(*[text[i:] for i in range(n)])

def get_ngrams(s: pd.Series, n: int, delimiter: str = ' ', merge: bool = False):
    ngrams = collections.Counter(calc_ngrams(s.str.split(' '), n))
    if merge:
        ngrams = [(' '.join(i[0]),i[1]) for i in ngrams.most_common(n)]
    return ngrams
