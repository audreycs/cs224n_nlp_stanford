# Lecture 7: Machine Translation, Sequence-to-Sequence and Attention

This lecture talks about:

- Machine Translation
- Sequence-to-sequence model
- Attention

<br />

## Machine Translation

**Machine Translation**: is the task of translating a sentence x from one language (the source language) to a sentence y in another language (the target language).

### Pre-Machine Translation

In 1950s: Early Machine Translation, mainly Russian -> English (motivated by the cold war!)

In 1990s-2010s: Statistic Machine Translation:
- **core idea**: Learn a probabilistic modelfrom data

How to learn translation model?:
- Need large amount of parallel data. -> To know word alignment.

word alignment can be: one-to-one, one-to-many, many-to-one, many-to-many

**Decoding for SMT**: Find the best target sentence

<img src="pics/1.jpg"
     style="align: center"
     width="600" />

<br />

### Neural Machine Translation

**Neural Machine Translation (NMT)**: is a way to do Machine Translation with a single end-to-end neural network

The neural network architecture is called a sequence-to-sequence model (aka seq2seq) and it involves two RNNs. We need two RNNs to handle the two different sentences.

The two RNNs: Encoder RNN and Decoder RNN

<img src="pics/2.jpg"
     style="align: center"
     width="600" />

Many NLP tasks can be phrased as sequence-to-sequence:

- Summarization (long text → short text)
- Dialogue (previous utterances → next utterance)
- Parsing (input text → output parse as sequence)
- Code generation (natural language → Python code)

**Greedy decoding**: take most probable word on each step.

<img src="pics/3.jpg"
     style="align: center"
     width="400" />

Problems with this method?

- Greedy decoding has no way to undo decisions! 

How to fix this?

- Exhaustive search decoding (far too expensive)

- Beam search decoding

#### Beam search decoding

**Core idea**: On each step of decoder, keep track of the k most probable partial translations (which we call hypotheses)

<img src="pics/4.jpg"
     style="align: center"
     width="600" />

Usually we continue beam search until:

- We reach timestep T (where T is some pre-defined cutoff), or
- We have at least n completed hypotheses (where n is pre-defined cutoff)

Problem with Beam search decoding: **longer hypotheses have lower scores**.

Fix this problem: **Normalize by length**.

<img src="pics/5.jpg"
     style="align: center"
     width="300" />

#### Advantages of NMT

- Better performance
     - More fluent
     - Better use of context
     - Better use of phrase similarities

- A single neural networkto be optimized end-to-end
     - No subcomponents to be individually optimized

- Requires much less human engineering effort
     - No feature engineering
     - Same method for all language pairs

#### Disadvantagesof NMT

- NMT is less interpretable
     - Hard to debug

- NMT is difficult to control
     - For example, can’t easily specify rules or guidelines for translation
     - Safety concerns!

<br />

### How do we evaluate Machine Translation?

**BLEU** (**B**i**l**ingual **E**valuation **U**nderstudy)

BLEU compares the machine-written translationto one or several human-written translation(s), and computes a similarity score based on:

- n-gram precision 
- Plusa penalty for too-short system translations

<br />

### MT progress over time

<img src="pics/6.jpg"
     style="align: center"
     width="600" />

<br />

### Many difficulties remain for MT:

- Out-of-vocabulary words
- Domain mismatch between train and test data
- Maintaining context over longer text
- Low-resource language pairs
- Failures to accurately capture sentence meaning
- Pronoun (or zero pronoun) resolution errors
- Morphological agreement errors

<br />

## Attention

Sequence-to-sequence: the bottleneck problem:

<img src="pics/7.jpg"
     style="align: center"
     width="600" />

Sequence-to-sequence with attention:

<img src="pics/8.jpg"
     style="align: center"
     width="600" />


<br />


# Assignment 4

## 1. Coding Part: Neural Machine Translation with RNNs

codes are in file `./a4/`.

(written) Explain one advantage and one disadvantage of dot product attention compared to multiplicative attention:

> Dot product attention is computationally easy and directly, the disadvantage is too easy to get the true informations. Multiplicative attention seems like a transition between dot product and additive attention.

(written) Explain one advantage and one disadvantage ofadditive attentioncompared to mul-tiplicative attention:

> The disadvantage of additive attention is that we need more hyperparameters to be tuned. But it can fit more complex situation and in experiment the additive attention always outperform the two others.

## 2. Analyzing NMT Systems

Why might it be important to model our Cherokee-to-English NMT problem at the subword-level vs. the whole word-level? (Hint:  Cherokee is a polysynthetic language.)

> Using word-level tokens leads to very large vocabulary sizes, especially for morphologically rich languages, where the number of surface forms per lemma is high. Large token vocabularies are impractical for the current neural architectures and hardware. Also normally word-level leads to degradation of translation quality.

Showing case: character-level and subword embeddings are often smaller than whole word embeddings

> Sentence: 'Bigger, faster, stronger, wiser, ...(more than 25 distinct adj.), taller and healthier are the comparatives of big, faster, wise, ..., tall and health.'

How  does  multilingual  training  help  in  improving  NMTperformance with low-resource languages?

> Multilingual models can help improve performance of low-resource languages by transferring from high-resource related languages they are trained jointly with. Like knowledge transfer.


<br />

# References

- https://github.com/ZacBi/CS224n-2019-solutions/blob/master/assignments/written%20part/a4_solution.md
