# Lecture 4: Language Models and Recurrent Neural Networks

This lecture mainly talks about Language Models and Rrcurrent Neural Networks (RNNs)

## Language Modeling

Informal Definition: Language Modeling is the task of predicting what word comes next.
```text
the student opened their ____
```

Formal Definition: Given a sequence of words, compute the probability distribution of the next word.

> Example of LM in our daily life: Google Search trys to complete the query when we are typing.

<br />

### n-gram Language models

n-gram definition: A n-gram is a chunk of n consecutive words.
- unigrams
- bigrams
- trigrams
- 4-grams
- ......
> Note the words order matters! "Lily has a dog" is different from "Dog has a Lily". 

<img src="pics/1.jpg"
     style="align: center"
     width="600" />

We should get n-grams probabilities to compute LM! How to? **Counting them in some large corpus of text.**

<br />

### Sparsity Problems with n-gram LMs

Many n-grams haven never appeared in corpus. Their probility will also be zero. How to solve this?
- Smoothing: Add small number to the count for every w.

And, what if the prefix words of a n-gram have never shown in corpus?

- Just condition on sub-words of the prefix words. This is called backoff.

> Typically we can't have n bigger than 5.

We can use n-gram LMs to generate text.

<br />

### Neural Language Model

An idea is fix-windows neural LM

Advantages of fix-windows neural LMs compared to n-grams LMs:
1. No sparsity problem
2. Don't need to store all observed n-grams

Remaining problems:
1. Fixed windows is too small.
2. Enlarging windows enlarges W.
3. Windows can never be large enought!
4. ......

<br />

## RNNs

RNNs can take sentences with any length in!

<img src="pics/2.jpg"
     style="align: center"
     width="600" />

RNNs advantages:
1. Can process any length input
2. Comiputation for step t use informantion from many steps back.
3. Model size doesn't increase for longer input.
4. Same weights applied on every timestep.

RNNs disadvantages:
1. Recurrent computation is slow.
2. In practice, difficult to access infomation from many steps back.

<br />

### Traning RNNs

calculate cross-entropy probability for evry step t.