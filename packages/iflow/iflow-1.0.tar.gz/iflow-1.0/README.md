<!--# i-flow-->

<!--![i-flow logo](i-flow.gif)-->
<div align="center">

<img src="i-flow_crop.gif"  alt="i-flow-logo" width="500" height="200">
</div>

[![pipeline status](https://gitlab.com/i-flow/i-flow/badges/master/pipeline.svg)](https://gitlab.com/i-flow/i-flow/commits/master)
[![coverage report](https://gitlab.com/i-flow/i-flow/badges/master/coverage.svg)](https://gitlab.com/i-flow/i-flow/commits/master)

This project implements normalizing flows using [TensorFlow](https://tensorflow.org) for the purpose of multi-dimensional integration and sampling.

## Citation
If you use **i-flow** for your research, please cite:  
- *"i-flow: High-dimensional Integration and Sampling with Normalizing Flows"*,  
By Christina Gao, Joshua Isaaacson, Claudius Krause.  
Mach. Learn.: Sci. Technol. [DOI](https://doi.org/10.1088/2632-2153/abab62) <br>
[arXiv:2001.05486](https://arxiv.org/abs/2001.05486). 

## Table of Contents

[[_TOC_]]

## Importance Sampling

In high dimensional integration, Monte-Carlo (MC) techniques are required in order to obtain convergence of the integral in
a efficient manner (See the discussion of [curse of
dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality) for details). The na&iuml;ve MC approach would
be to uniformly sample points over the integration domain ($`\Omega`$) encompassing a volume $`V`$. The integral $`I`$ of a function $`f(x)`$ can then be estimated from
evaluating the function at $`N`$ random points and taking the mean, i.e.
```math
I = \int_\Omega f(x)\ dx \approx \frac{V}{N}\sum_{i=1}^{N} f(x_i) \equiv V \langle f \rangle_x,
```
and the uncertainty is determined by the standard deviation of the mean, i.e.
```math
\sigma_f \approx V \sqrt{\frac{\langle f^2\rangle_x - \langle f\rangle_x^2}{N-1}}.
```
To improve upon the uncertainty of the estimated integral, a technique known as **importance sampling** was
developed. The goal of importance sampling is the minimize the standard deviation by sampling points from a
distribution that is closer to the function $`f(x)`$ than the uniform distribution. Given a probability
distribution function $`g(x)`$
with cumulative distribution function $`G(x)`$, it is possible to transform the integral using the change of variable
formula, giving:
```math
I = \int_\Omega \frac{f(x)}{g(x)}\ dG(x) \approx \frac{V}{N}\sum_{i=1}^N
\frac{f(\tilde{x}_i)}{g(\tilde{x}_i)} \equiv V \langle f/g\rangle_G,
```
where $`\tilde{x}_i`$ is distributed according to $`g(x)`$. The standard deviation can be calculated in a similar method.
From this, it can easily be seen that if $`g(x) \rightarrow f(x)/I`$, then the uncertainty from this method would
produce an integral estimate with vanishing uncertainty. However, this would require to know the analytic solution
to the integral!

Therefore, the goal of importance sampling is to find a distribution $`g(x)`$ as close to $`f(x)`$ as possible that is
also easy to sample from.

## Normalizing Flows

A Normalizing Flow is a bijective transformation from a (usually simple) base distribution to a 
(usually more complicated) target distribution, i.e. a change of variables transformation. 
It is therefore able to describe arbitrary, high-dimensional probability disctributions of continuous
variables. The transformation is invertible and can therefore be used in two directions: In the one 
direction, we can infer the probability of a given sample point. In the other direction, we can sample 
random numbers according to the target distribution. Usually, Normalizing Flows are implemented usitilizing
Neural Networks, see [[1]](#references) for a review. Different architectures exist that are either fast
in inference and slow at sampling or the other way around. Since our application for numerical integration with 
importance sampling requires both directions to be fast, we use the architecture based on Coupling Layers that
was proposed in [[2]](#references). <br>

In a Coupling Layer, the $`N`$-dimensional is split in to two sets $`\vec{x}_a=\{ x_1, \ldots, x_n\}`$ and
$`\vec{x}_b=\{x_{n+1}, \ldots, x_N\}`$, where $`1 \leq n < N`$. One set remains untransformed, but is used as
input into a neural network. The other set is transformed based on a set of parameters determined from the output of
the neural network. In other words,
```math
x'_a = x_a, \quad\quad\quad\quad\quad\quad\ \  A\in[1,n]\quad\quad\  \\
x'_b = C(x_b; m(\vec{x}_a)),\quad\quad B\in[n+1,N]
```
with the inverse map given by: 
```math
x_a = x'_a,\quad\quad
x_b = C^{-1}(x'_b; m(\vec{x'}_a)) = C^{-1}(x'_b; m(\vec{x}_a)).
```
This leads to an analytic Jacobian independent on the gradient of the neural network $`m(\vec{x}_a)`$, and
can be calculated as:
```math
\left\lvert\frac{\partial c(\vec{x})}{\partial\vec{x}}\right\rvert^{-1}
= \left\lvert
\begin{pmatrix}
\vec{1} & 0 \\
\frac{\partial C}{\partial m}\frac{\partial m}{\partial \vec{x}_a} & \frac{\partial C}{\partial \vec{x}_b}
\end{pmatrix}
\right\rvert^{-1}
= \left\lvert \frac{\partial C(\vec{x}_b; m(\vec{x}_a))}{\partial \vec{x}_b} \right\rvert^{-1}.
```

Below is a graphical representation of single coupling layer, plus a permutation on the indices before being passed
into a subsequent layer.
<div align="center">
<img src="CL.png" width="500">
</div>


### Coupling Layers
Currently, there are three well tested and validated coupling layers implemented in the **i-flow** package. These are:
- [Linear Spline](#linear-spline)
- [Quadratic Spline](#quadratic-spline)
- [Rational Quadratic Spline](#rational-quadratic-spline)

#### Linear Spline

The linear spline is based on a piecewise linear function defining the CDF [[3]](#references).
Given $N$ dimensions and $K$ bins with a width of $w$ the PDF is defined as
$`q_i(t) = \{Q_{ij} | i \in [1,N], (j-1)w \leq t < jw, j \in [1, K]\}`$.
The CDF can be calculated by integrating the PDF, giving:
```math
C(x_i^B; Q) = \alpha Q_{ib} + \sum_{k=1}^{b-1} Q_{ik},
```
where $`b`$ is the bin in which $`x_i^B`$ occurs, and $`\alpha=\frac{x_i^B-(b-1)w}{w}`$.
The Jacobian for this calculation is straight forward to calculate and is:
```math
\left\lvert \frac{\partial C}{\partial x_B} \right\rvert = \prod_i Q_{ib}
```

#### Quadratic Spline

The quadratic spline is also based on a piecewise quadratic function defining the
CDF [[2]](#references). Given $`N`$ dimensions, $`K`$ bins with widths $`W_{ik}`$, and $`K+1`$ vertices
with heights $`V_{ik}`$, the PDF is defined as:
```math
q_i(t) = \begin{cases}
      \frac{V_{i2}-V_{i1}}{W_{i1}}t+V_{i1} & t < W_{i1} \\
      \frac{V_{i3}-V_{i2}}{W_{i2}}\left(t-W_{i1}\right)+V_{i2} & W_{i1} \leq t < W_{i1}+W_{i2} \\
      \quad\vdots & \\
      \frac{V_{i(K+1)}-V_{iK}}{W_{iK}}\left(t-\sum_{k=1}^{K-1}W_{ik}\right)+V_{iK} & \sum_{k=1}^{K-1} W_{ik} \leq t < 1 \\
      \end{cases}
```
Integrating the above to obtain the CDF gives:
```math
C(x_i^B; W, V) = \frac{\alpha^2}{2}\left(V_{ib+1}-V_{ib}\right) W_{ib} + V_{ib}W_{ib}\alpha + \sum_{k=1}^{b-1}\frac{V_{ik+1} + V_{ik}}{2} W_{ik},
```
with $`b`$ the solution to $`\sum_{k=1}^{b-1} W_{ik} \leq x_i^B < \sum_{k=1}^b W_{ik}`$,
and $`\alpha = \frac{x_i^B-\sum_{k=1}^{b-1}W_{ik}}{W_{ib}}`$ is the relative position of $`x_i^B`$ in bin $`b`$.

#### Rational Quadratic Spline

The rational quadratic spline was originally defined in [[4]](#references).
Given $`N`$ dimensions, $`K+1`$ knot points $`\{(x^{(k)}, y^{(k)}) \}_{k=0}^K`$ that are monotonically increasing, with
$`( x^{(0)}, y^{(0)} ) = (0, 0)`$ and $`( x^{(K)}, y^{(K)} ) = (1, 1)`$, and 
$`K+1`$ non-negative derivatives $`\{ d^{(k)} \}_{k=0}^K`$, the CDF can be calculated using the algorithm from
[[5]](#references), and is reproduced below.

First define bin widths $`w^{(k)} = x^{(k+1)} - x^{(k)}`$ and slopes $`s^{k}=\frac{y^{(k+1)}-y^{(k)}}{w^{(k)}}`$.
Given the point $`x`$, the bin in which $`x`$ falls is $`k`$, and the fractional distance $`x`$ is between the two
corresponding knots is $`\xi=\frac{x-x^{(k)}}{w^{(k)}}`$. From this, the CDF can be calculated from:
```math
g(x) = y^{(k)} + \frac{\left(y^{(k+1)} - y^{(k)}\right)\left[s^{(k)}\xi^2+d^{(k)}\xi\left(1-\xi\right)\right]}{s^{(k)}+\left[d^{(k+1)}+d^{(k)}-2s^{(k)}\right]\xi\left(1-\xi\right)}.
```

#### Futher documentation
Additional documentation can be found at: [doc](https://i-flow.gitlab.io/i-flow/)

## Installation

## Requirements

In order to run the **i-flow** program, there are a few additional packages that are required. The packages are:

1. [TensorFlow](https://tensorflow.org) (version 2.0 or newer)
2. [TensorFlow-Probability](https://www.tensorflow.org/probability) (version 0.8 or newer)
3. [Numpy](https://numpy.org) 
   
In order to run the tests provided in the paper and the [iflow_test.py](iflow_test.py) file, a few additional pacakges
are required. These are:

1. [Vegas](https://vegas.readthedocs.io/en/latest/) (to compare to the vegas algorithm)
1. [matplotlib](https://matplotlib.org) (for plotting the results)
2. [absl-py](https://abseil.io/docs) (for command line parsing)

## Usage 

## References
1. George Papamakarios, Eric Nalisnick,  Danilo Jimenez Rezende, Shakir Mohamed, and Balaji Lakshminarayanan.<br>
  Normalizing Flows for Probabilistic Modeling and Inference. arXiv:1912.02762 [link](https://arxiv.org/abs/1912.02762)  
2. Laurent Dinh, David Krueger, and Yoshua Bengio. <br>
NICE: non-linear independent components estimation. In *3rd International Conference on Learning Representations*, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Workshop Track Proceedings, 2015. arXiv:1410.8516 [link](http://arxiv.org/abs/1410.8516)  
3. Thomas M&uuml;ller, Brian Mcwilliams, Fabrice Rousselle, Markus Gross, and Jan Nov&aacute;k.<br>
  Neural Importance Sampling. *ACM Trans. Graph.,* 38(5), October 2019. [link](https://doi.org/10.1145/3341156)
4. Conor Durkan, Artur Bekasov, Iain Murray, and George Papamakarios.<br>
  Neural Spline Flows. *Advances in Neural Information Processing Systems,* 7511--7522, 2019. [link](http://arxiv.org/abs/1906.04032)
5. J. A. Gregory and R. Delbourgo.<br>
  Piecewise Rational Quadratic Interpolation to Monotonic Data.</br>
  *IMA Journal of Numerical Analysis*, 2(2):123-130, 04 1982. [link](https://doi.org/10.1093/imanum/2.2.123)
