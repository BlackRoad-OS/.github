# Linear Algebra - Function Spaces

## Function Space Definition

The set of all functions from X to a field K:

```
K^X = { f : X → K }
```

This is a **vector space** of functions.

## Operations on Function Spaces

### Addition of Functions
```
(f + g)(x) := f(x) + g(x)
```

### Scalar Multiplication
```
(λ · f)(x) := λ · f(x)
```

### Pointwise Multiplication
```
(f * g)(x) := f(x) · g(x)
```

## Key Property: Scalar-Product Associativity

**Proposition 2.2:**

```
λ · (a * b) = (λ · a) * b = a * (λ · b)
```

### Proof

Starting from the left side:

```
(λ · (f * g))(x) = λ · ((f * g)(x))
                  = λ · (f(x) · g(x))
                  = (λ · f(x)) · g(x)
                  = ((λ · f) * g)(x)
```

And from the right side:

```
= f(x) · (λ · g(x))
= (f * (λ · g))(x)
```

This shows scalar multiplication can "pass through" the pointwise product to either factor.

## Why This Matters

This property establishes that **K^X is an algebra over K** -- not just a vector space, but one with a compatible multiplication operation. This is fundamental to:

- **Functional analysis**
- **Operator theory**
- **Quantum mechanics** (operators on Hilbert spaces)
- **Signal processing** (function spaces)

## Connections

- Function spaces connect to [Quantum Mechanics](../physics/quantum-mechanics.md) (wave functions live in Hilbert space)
- Scalar properties relate to [Modular Arithmetic](modular-arithmetic.md) through ring theory
- [Complex Numbers](complex-numbers.md) form the field K in quantum mechanics
