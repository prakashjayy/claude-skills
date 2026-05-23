# ASCII/Unicode Diagram Templates

All diagrams go inside fenced code blocks in the markdown output.
Adapt these templates to the specific concept being explained.

**Allowed characters:**
- Box-drawing: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╯ ╰ ═ ║`
- Arrows: `→ ← ↑ ↓ ↔ ⇒ ⟹ ↗ ↘ ↙ ↖`
- Math: `∑ ∏ ∫ ∂ ∇ ≤ ≥ ≈ ≠ ∈ ∉ ⊂ ⊃ ∩ ∪ ⊗ ⊕ ∞`
- Superscript/subscript: `⁰¹²³⁴⁵⁶⁷⁸⁹ᵀ⁻ ₀₁₂₃₄₅₆₇₈₉`
- Greek: `α β γ δ ε ζ η θ λ μ ν π ρ σ τ φ χ ψ ω Σ Π Λ Φ Ω`

---

## 1. Probability & Distributions

### Joint → marginal → conditional

```
  ┌──────────────────────────────────┐
  │   P_{XY}(x, y)  (joint)         │
  │                                  │
  │   x ∈ 𝒳,  y ∈ 𝒴               │
  └──────────┬───────────────────────┘
             │
     ┌────────┴────────┐
     │ marginalize     │ marginalize
     │ over Y          │ over X
     ▼                 ▼
  P_X(x)           P_Y(y)
  = Σ_y P_{XY}(x,y)    = Σ_x P_{XY}(x,y)

  ──────────────────────────────────
  Conditional = Joint / Marginal:

  P_{X|Y}(x ∣ y)  =  P_{XY}(x, y)
                     ──────────────
                        P_Y(y)
```

### Bayesian network (directed graphical model)

```
  θ ──→ Z ──→ X
        │
        └──→ Y

  P_{θZXY}(θ,z,x,y)
    = P_θ(θ) · P_{Z|θ}(z|θ) · P_{X|Z}(x|z) · P_{Y|Z}(y|z)

  (each node is conditionally independent of non-descendants
   given its parents)
```

### Gaussian distribution shape

```
  p_X(x)
    │
    │          ╭───╮
    │        ╭─╯   ╰─╮
    │      ╭─╯         ╰─╮
    │   ╭──╯               ╰──╮
    └───┴──────────────────────── x
             μ-σ  μ  μ+σ

  p_X(x) = 𝒩(x; μ, σ²)
          =     1      · exp(−(x−μ)²)
             ──────────        ──────
             σ√(2π)             2σ²
```

---

## 2. Linear Algebra

### Matrix–vector multiplication

```
  y       =       A        ·   x
(m×1)          (m×n)         (n×1)

  ┌   ┐   ┌──────────────┐ ┌   ┐
  │y₁ │   │← row 1 of A→│ │x₁ │
  │y₂ │ = │← row 2 of A→│·│x₂ │
  │ ⋮ │   │      ⋮       │ │ ⋮ │
  │yₘ │   │← row m of A→│ │xₙ │
  └   ┘   └──────────────┘ └   ┘

  yᵢ = Σⱼ Aᵢⱼ xⱼ   (dot product of row i with x)
```

### SVD decomposition

```
       A           =    U    ·    Σ    ·   Vᵀ
    (m × n)           (m×r)    (r×r)    (r×n)

  ┌─────────┐      ┌──┐  ┌──────┐  ┌─────────┐
  │         │      │  │  │σ₁    │  │         │
  │    A    │  =   │U │· │  σ₂  │· │   Vᵀ   │
  │         │      │  │  │    ⋱ │  │         │
  └─────────┘      └──┘  └──────┘  └─────────┘
                  columns  diagonal   rows are
                  are left  singular  right
                  singular  values    singular
                  vectors             vectors

  r = rank(A),   σ₁ ≥ σ₂ ≥ … ≥ σᵣ > 0
```

### Eigendecomposition

```
  A · v  =  λ · v

  ┌──────────────────────────────┐
  │  v (eigenvector)             │
  │  ↑ same direction after A    │
  │                              │
  │  A·v                         │
  │  ↑ scaled by λ (eigenvalue)  │
  └──────────────────────────────┘

  A = Q Λ Qᵀ   (symmetric A)
  Q = [v₁ | v₂ | … | vₙ],  Λ = diag(λ₁, …, λₙ)
```

---

## 3. Calculus & Optimization

### Gradient descent on a loss landscape

```
  ℒ(θ)
    │
    │   ╲        local min
    │    ╲   ╭──╮     ╭─
    │     ╰──╯  ╰─────╯
    │              ↑
    └──────────────────── θ
                   θ*
                   
  Update rule:
  θ_{t+1} ← θ_t − η · ∇_θ ℒ(θ_t)
             ↑           ↑
           step size  gradient (points uphill)
                      negative → move downhill
```

### Chain rule (computation graph)

```
  x ──[f]──→ y ──[g]──→ z

  Forward:   y = f(x),   z = g(y)

  Backward:  dz    dz   dy
             ── = ── · ──  = g'(y) · f'(x)
             dx    dy   dx

  (gradient flows right to left through the graph)
```

### Gradient of a vector function (Jacobian)

```
  f: ℝⁿ → ℝᵐ

  J_f(x) ∈ ℝ^{m×n}

  ┌                      ┐
  │ ∂f₁/∂x₁  …  ∂f₁/∂xₙ │
  │    ⋮      ⋱     ⋮    │
  │ ∂fₘ/∂x₁  …  ∂fₘ/∂xₙ │
  └                      ┘
  
  (i,j) entry: how much output i changes per unit change in input j
```

---

## 4. Information Theory

### Entropy: uncertainty of a distribution

```
  H(P_X) = −Σ_x P_X(x) log₂ P_X(x)      [bits]

  ───────────────────────────────────────
  Uniform P_X           Peaked P_X
  (maximum uncertainty)  (minimum uncertainty)

     P_X(x)                 P_X(x)
     │                      │
   1/n│───────────          1│─
     │                      │ │
     └──────────── x         └──────────── x
     H = log₂(n)            H ≈ 0
```

### KL divergence: asymmetry illustrated

```
  D_{KL}(P_X ∥ Q_X) = Σ_x P_X(x) log[P_X(x)/Q_X(x)]

  Interpretation: extra bits needed to encode P_X
                  using a code optimized for Q_X

  P_X: ─────────╮               D_{KL}(P∥Q) is large:
                 │ ← big gap     P has mass where Q doesn't
  Q_X:   ───────╯

  ⚠ NOT symmetric: D_{KL}(P∥Q) ≠ D_{KL}(Q∥P)
```

### Mutual information

```
  I(X; Y)  =  H(X)  −  H(X|Y)
           =  H(Y)  −  H(Y|X)
           =  D_{KL}(P_{XY} ∥ P_X ⊗ P_Y)

  ┌─────────────────────────────┐
  │   H(X)          H(Y)        │
  │  ┌────────────────────┐     │
  │  │     ┌────┐         │     │
  │  │ H(X │ ┤I(X│Y)├ │ Y)│     │
  │  │     └────┘         │     │
  │  └────────────────────┘     │
  └─────────────────────────────┘
  I(X;Y) = overlap of information in X and Y
```

---

## 5. Neural Networks

### Feedforward layer

```
  Input x ∈ ℝ^{d_in}          Output h ∈ ℝ^{d_out}

  ┌──┐                          ┌──┐
  │x₁│ ─╮                   ╭─ │h₁│
  │x₂│  ├──[W ∈ ℝ^{d_out×d_in}]─┤  │h₂│
  │x₃│ ─╯    + b ∈ ℝ^{d_out} ╰─ │h₃│
  └──┘    then σ(·) applied       └──┘

  h = σ(Wx + b)
```

### Scaled dot-product attention

```
  Q ∈ ℝ^{n×d}   K ∈ ℝ^{n×d}   V ∈ ℝ^{n×d}
  (n queries)    (n keys)        (n values)

        QKᵀ
  A =  ─────        [n×n attention weights]
         √d

  A_softmax = softmax(A)    [rows sum to 1]

  Output = A_softmax · V    [n×d weighted sum of values]

  ┌────┐     ┌────┐
  │ Q  │ ──→ │    │  ┌────┐    ┌────────┐
  └────┘     │QKᵀ │→ │soft│ → │Output  │
  ┌────┐  ┌→ │/√d │  │max │    │=A_s·V  │
  │ K  │──┘  └────┘  └────┘    └────────┘
  └────┘                              ↑
  ┌────┐ ──────────────────────────── │
  │ V  │ ─────────────────────────────┘
  └────┘
```

### Residual connection

```
  x ──────────────────────────────→ (+) ──→ x + F(x)
  │                                  ↑
  └──→ [Layer F: norm→linear→act] ───┘

  Gradient of (x + F(x)) w.r.t. x:
  ∂/∂x [x + F(x)] = I + ∂F/∂x

  The identity term I ensures gradient ≥ 1,
  preventing vanishing gradients in deep networks.
```

---

## 6. Variational / Probabilistic Models

### Encoder–decoder (VAE structure)

```
  x ──→ [Encoder q_{Z|X}] ──→ z ──→ [Decoder p_{X|Z}] ──→ x̂

  Training objective (ELBO):
  ℒ(θ, φ; x) = 𝔼_{Z∼q_{Z|X}(·|x)}[log p_{X|Z}(x|z)]
               ─────────────────────────────────────
               reconstruction term

               − D_{KL}(q_{Z|X}(·|x) ∥ p_Z(·))
               ──────────────────────────────────
               regularisation term (keeps z near prior)
```

### MCMC: Markov chain sampling

```
  State space 𝒳

  z₀ ──→ z₁ ──→ z₂ ──→ … ──→ zₜ
  (init)        (burn-in)       (converged samples from P_Z)

  Transition kernel T(z' | z):  P_{Z_{t+1}|Z_t}(z' ∣ z)
  Detailed balance: P_Z(z) · T(z' | z) = P_Z(z') · T(z | z')
  guarantees stationary dist = P_Z
```

---

## 7. Prerequisite dependency tree template

Use this for the **Prerequisites map** section at the top of each primer:

```
  [Paper's core concept]
  ├── [Mid-level concept A]
  │   ├── [Foundational concept 1]
  │   └── [Foundational concept 2]
  └── [Mid-level concept B]
      ├── [Foundational concept 3]
      └── [Foundational concept 4]
          └── [Base concept — calculus/linalg level]
```

Label each node with the section number where it is explained in the primer.

---

## Diagram checklist

Before writing a diagram, verify:
- [ ] Every symbol is defined in the surrounding text
- [ ] Matrix/tensor dimensions are labelled: `A ∈ ℝ^{m×n}`
- [ ] Arrows have direction labels or the direction is obvious from the layout
- [ ] No standalone Greek letters without context (define them)
- [ ] Diagram and surrounding text use identical notation (both follow NOTATION.md)
