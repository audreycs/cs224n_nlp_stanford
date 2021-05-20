import sys

assert sys.version_info[0] == 3
assert sys.version_info[1] >= 5

from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import pprint
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

plt.rcParams['figure.figsize'] = [10, 5]
import nltk

nltk.download('reuters')
from nltk.corpus import reuters
import numpy as np
import random
import scipy as sp
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA

START_TOKEN = '<START>'
END_TOKEN = '<END>'

np.random.seed(0)
random.seed(0)


def read_corpus(category="crude"):
    """ Read files from the specified Reuter's category.
        Params:
            category (string): category name
        Return:
            list of lists, with words from each of the processed files
    """
    files = reuters.fileids(category)
    return [[START_TOKEN] + [w.lower() for w in list(reuters.words(f))] + [END_TOKEN] for f in files]


def distinct_words(corpus):
    """ Determine a list of distinct words for the corpus.
        Params:
            corpus (list of list of strings): corpus of documents
        Return:
            corpus_words (list of strings): sorted list of distinct words across the corpus
            num_corpus_words (integer): number of distinct words across the corpus
    """
    word_set = set([j for i in corpus for j in i])
    corpus_words = list(word_set)
    corpus_words.sort()
    num_corpus_words = len(corpus_words)

    return corpus_words, num_corpus_words


def compute_co_occurrence_matrix(corpus, window_size=4):
    """ Compute co-occurrence matrix for the given corpus and window_size (default of 4).

        Note: Each word in a document should be at the center of a window. Words near edges will have a smaller
              number of co-occurring words.

              For example, if we take the document "<START> All that glitters is not gold <END>" with window size of 4,
              "All" will co-occur with "<START>", "that", "glitters", "is", and "not".

        Params:
            corpus (list of list of strings): corpus of documents
            window_size (int): size of context window
        Return:
            M (a symmetric numpy matrix of shape (number of unique words in the corpus , number of unique words in the corpus)):
                Co-occurence matrix of word counts.
                The ordering of the words in the rows/columns should be the same as the ordering of the words given by the distinct_words function.
            word2ind (dict): dictionary that maps word to index (i.e. row/column number) for matrix M.
    """
    words, num_words = distinct_words(corpus)
    M = np.zeros([num_words, num_words])
    word2ind = {w:index for index, w in enumerate(words)}

    for p in corpus:
        length = len(p)
        for i in range(length):
            id_i = word2ind[p[i]]
            left = max(i-window_size, 0)
            right = min(i+window_size, length-1)
            for j in range(left, right+1):
                id_j = word2ind[p[j]]
                if j != i:
                    M[id_i][id_j] += 1

    return M, word2ind


def reduce_to_k_dim(M, k=2):
    """ Reduce a co-occurence count matrix of dimensionality (num_corpus_words, num_corpus_words)
        to a matrix of dimensionality (num_corpus_words, k) using the following SVD function from Scikit-Learn:
            - http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html

        Params:
            M (numpy matrix of shape (number of unique words in the corpus , number of unique words in the corpus)): co-occurence matrix of word counts
            k (int): embedding size of each word after dimension reduction
        Return:
            M_reduced (numpy matrix of shape (number of corpus words, k)): matrix of k-dimensioal word embeddings.
                    In terms of the SVD from math class, this actually returns U * S
    """
    n_iters = 10  # Use this parameter in your call to `TruncatedSVD`
    print("Running Truncated SVD over %i words..." % (M.shape[0]))

    svd = TruncatedSVD(k, "randomized", n_iters)
    M_reduced = svd.fit_transform(M)

    print("Done.")
    return M_reduced


def plot_embeddings(M_reduced, word2ind, words):
    """ Plot in a scatterplot the embeddings of the words specified in the list "words".
        NOTE: do not plot all the words listed in M_reduced / word2ind.
        Include a label next to each point.

        Params:
            M_reduced (numpy matrix of shape (number of unique words in the corpus , 2)): matrix of 2-dimensioal word embeddings
            word2ind (dict): dictionary that maps word to indices for matrix M
            words (list of strings): words whose embeddings we want to visualize
    """
    figure(figsize=(8, 6), dpi=80)
    indexs = [word2ind[w] for w in words]
    embeddings = M_reduced[indexs]
    x = embeddings[:, 0]
    y = embeddings[:, 1]
    plt.plot(x, y, marker='X', color='red', linestyle='None')

    for i, txt in enumerate(words):
        plt.annotate(txt, (x[i], y[i]))

    plt.show()


def load_embedding_model():
    """ Load GloVe Vectors
        Return:
            wv_from_bin: All 400000 embeddings, each lengh 200
    """
    import gensim.downloader as api
    wv_from_bin = api.load("glove-wiki-gigaword-200")
    # print("Loaded vocab size %i" % len(wv_from_bin.vocab.keys()))
    return wv_from_bin


def get_matrix_of_vectors(wv_from_bin, required_words=['barrels', 'bpd', 'ecuador', 'energy', 'industry', 'kuwait', 'oil', 'output',
                                          'petroleum', 'iraq']):
    """ Put the GloVe vectors into a matrix M.
        Param:
            wv_from_bin: KeyedVectors object; the 400000 GloVe vectors loaded from file
        Return:
            M: numpy matrix shape (num words, 200) containing the vectors
            word2ind: dictionary mapping each word to its row number in M
    """
    import random
    words = list(wv_from_bin.vocab.keys())
    print("Shuffling words ...")
    random.seed(224)
    random.shuffle(words)
    words = words[:10000]
    print("Putting %i words into word2ind and matrix M..." % len(words))
    word2ind = {}
    M = []
    curInd = 0
    for w in words:
        try:
            M.append(wv_from_bin.word_vec(w))
            word2ind[w] = curInd
            curInd += 1
        except KeyError:
            continue
    for w in required_words:
        if w in words:
            continue
        try:
            M.append(wv_from_bin.word_vec(w))
            word2ind[w] = curInd
            curInd += 1
        except KeyError:
            continue
    M = np.stack(M)
    print("Done.")
    return M, word2ind


if __name__ == "__main__":
    '''for part1'''
    # reuters_corpus = read_corpus()
    # M_co_occurrence, word2ind_co_occurrence = compute_co_occurrence_matrix(reuters_corpus)
    # M_reduced_co_occurrence = reduce_to_k_dim(M_co_occurrence, k=2)
    #
    # # Rescale (normalize) the rows to make them each of unit-length
    # M_lengths = np.linalg.norm(M_reduced_co_occurrence, axis=1)
    # M_normalized = M_reduced_co_occurrence / M_lengths[:, np.newaxis]  # broadcasting
    #
    # words = ['barrels', 'bpd', 'ecuador', 'energy', 'industry', 'kuwait', 'oil', 'output', 'petroleum', 'iraq']
    #
    # plot_embeddings(M_normalized, word2ind_co_occurrence, words)

    '''for part2'''
    wv_from_bin = load_embedding_model()
    # M, word2ind = get_matrix_of_vectors(wv_from_bin)
    # M_reduced = reduce_to_k_dim(M, k=2)
    #
    # # Rescale (normalize) the rows to make them each of unit-length
    # M_lengths = np.linalg.norm(M_reduced, axis=1)
    # M_reduced_normalized = M_reduced / M_lengths[:, np.newaxis]  # broadcasting
    #
    # words = ['barrels', 'bpd', 'ecuador', 'energy', 'industry', 'kuwait', 'oil', 'output', 'petroleum', 'iraq']
    # plot_embeddings(M_reduced_normalized, word2ind, words)

    # find polysemes and homonyms
    print(wv_from_bin.most_similar(positive=['child', 'lamb'], negative=['adult']))

    print(wv_from_bin.most_similar(positive=['woman', 'worker'], negative=['man']))
    print(wv_from_bin.most_similar(positive=['man', 'worker'], negative=['woman']))


