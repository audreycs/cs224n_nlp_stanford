# Lecture 6: Vanishing Gradients, Fancy RNNs, Seq2Seq

## Key Notes

**Vanishing gradient problem**: When these are small, the gradient signal gets smaller and smaller as it backpropagates further.

<img src="pics/1.jpg"
     style="align: center"
     width="600" />

### Why is vanishing gradient a problem?

> Gradient signal from far away is lost because it’s much smaller than gradient signal from close-by. So, model weights are updated only with respect to near effects, not long-term effects.

<img src="pics/2.jpg"
     style="align: center"
     width="600" />

> Another explanatino: Gradient can be viewed as a measure of the effect of the past on the future.


Due to vanishing gradient, RNN-LMs are better at learning from **sequential recency** than **syntactic recency**, so they make this type of error more often than we'd like.

<br />

### Why is exploding gradient a problem?

If the gradient becomes too big, then the SGD update step becomes too big:

<img src="pics/3.jpg"
     style="align: center"
     width="300" />

This can cause bad updates:we take too large a step and reach a weird and bad parameter configuration (with large loss)
  - You think you’ve found a hill to climb, but suddenly you’re in lowa

In the worst case, this will result in Infor NaNin your network.

<br />
