# Notation Reference

This file defines the notation system to use throughout the math primer.
The guiding principle: **subscripts name; arguments are values.**

---

## Probability and Distributions

### Basic rule
The subscript on `P` (or `p`, `f`, `μ`) identifies which random variable or
joint the distribution is *over*. The argument gives the *value* taken.

| Write this | Not this | Meaning |
|---|---|---|
| `P_X(x)` | `P(X = x)` or `p(x)` | Prob. that r.v. X takes value x |
| `P_{XY}(x, y)` | `P(X, Y)` | Joint distribution |
| `P_{X \| Y}(x \mid y)` | `P(X\|Y)` | Conditional distribution |
| `p_{X}(x)` | `p(x)` | Probability density of X at x |
| `p_{X \| Y}(x \mid y)` | `p(x\|y)` | Conditional density |

### Named distributions
When a distribution has a name, use it as a subscript modifier:

```
X ∼ 𝒩_{X}(μ, σ²)        — X is Gaussian with mean μ, variance σ²
P_{X}(x) = 𝒩(x; μ, σ²)  — evaluating the Gaussian density at x
```

### Multiple random variables
Use different Greek letters for different r.v. values when they must be
distinguished:

```
P_{XY}(α, β)    — α is the value of X, β is the value of Y
P_{X'X}(α', α)  — primed variable, primed value
```

---

## Expectations

```
𝔼_{X ∼ P_X}[f(X)]           — expectation of f(X) when X follows P_X
𝔼_{XY ∼ P_{XY}}[f(X, Y)]   — joint expectation
𝔼_{X ∼ P_X}[f(X) | Y = y]  — conditional expectation at fixed y
𝔼_θ[·]                       — expectation over parameter θ
```

When the distribution is clear from context, the subscript may be shortened:
```
𝔼_X[f(X)]   — acceptable shorthand when P_X is already defined
```

Never write `E[f(x)]` (lowercase x without subscript on E) — ambiguous.

---

## Divergences and Information Measures

| Quantity | Notation | Formula |
|---|---|---|
| KL divergence | `D_{KL}(P_X ∥ Q_X)` | `Σ_x P_X(x) log[P_X(x)/Q_X(x)]` |
| Shannon entropy | `H(P_X)` or `H(X)` | `−Σ_x P_X(x) log P_X(x)` |
| Cross-entropy | `H(P_X, Q_X)` | `−Σ_x P_X(x) log Q_X(x)` |
| Mutual information | `I(X; Y)` | `D_{KL}(P_{XY} ∥ P_X ⊗ P_Y)` |
| Conditional entropy | `H(X \| Y)` | `H(X, Y) − H(Y)` |

Note: `H(X \| Y)` is **conditional entropy** (a scalar), not `P_{X\|Y}`.

---

## Linear Algebra

### Matrices and vectors
```
x ∈ ℝ^d          — column vector, d-dimensional
A ∈ ℝ^{m×n}      — matrix with m rows, n columns
Aᵀ               — transpose
A⁻¹              — inverse (only if square and invertible)
A†               — Moore-Penrose pseudoinverse
```

### Norms
```
‖x‖₂             — Euclidean (L²) norm
‖x‖₁             — L¹ norm
‖A‖_F            — Frobenius norm
‖A‖₂             — spectral norm (largest singular value)
```

### Factorizations
```
A = U Σ Vᵀ        — SVD; always write dimensions: U ∈ ℝ^{m×r}, Σ ∈ ℝ^{r×r}, V ∈ ℝ^{n×r}
A = Q Λ Qᵀ        — eigendecomposition (symmetric A)
Av = λv          — eigenvalue equation; λ ∈ ℝ, v ∈ ℝ^n
```

---

## Calculus and Analysis

### Derivatives
```
∂ℒ/∂θ           — partial derivative of ℒ with respect to θ
∇_θ ℒ(θ)        — gradient (always subscript the variable!)
∇²_θ ℒ(θ)       — Hessian (n×n matrix of second partials)
J_f(x)          — Jacobian of f at x; J_f ∈ ℝ^{m×n} if f: ℝ^n → ℝ^m
δℒ/δf           — functional derivative
```

Never write `∇ℒ` without specifying what you're differentiating with respect to.

### Integrals
```
∫_𝒳 f(x) dP_X(x)     — Lebesgue integral w.r.t. measure P_X
∫_ℝ p_X(x) f(x) dx   — when density p_X exists
∑_{x ∈ 𝒳} P_X(x) f(x) — discrete version
```

---

## Sets and Spaces

```
ℝ^d          — d-dimensional real space
ℤ            — integers
ℕ            — natural numbers
𝒳            — generic sample/input space (calligraphic)
𝒴            — output/label space
Ω            — probability space / sample space
𝒫(𝒳)        — space of probability measures over 𝒳
L²(Ω)       — square-integrable functions on Ω
𝒞^k(Ω)     — k-times continuously differentiable functions
```

---

## Parameters and Models

```
θ ∈ Θ         — model parameters; Θ is the parameter space
θ*            — optimal parameters
θ_t           — parameters at step t (not θ^t)
ℒ(θ)          — loss/objective as function of θ
ℒ(θ; x)       — loss conditioned on input x
ℒ(θ; 𝒟)      — loss on dataset 𝒟
```

---

## Functions and Maps

```
f: 𝒳 → 𝒴        — f maps from 𝒳 to 𝒴
f ∘ g            — composition: (f ∘ g)(x) = f(g(x))
σ(·)             — sigmoid function (or other activation, defined on first use)
softmax_j(z)     — j-th output of softmax; subscript identifies the component
```

---

## Quick-check rules

Before writing any equation, verify:
1. Is every random variable `X` uppercase?
2. Is every realization value `x` lowercase?
3. Does every `P`, `p`, `𝔼`, `D_{KL}`, `H` have a subscript identifying the r.v.?
4. Does every gradient `∇` have a subscript identifying the differentiation variable?
5. Are matrix dimensions written out on first use?
