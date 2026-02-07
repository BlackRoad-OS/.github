# Quantum Mechanics

## The Schrodinger Equation

From the handwritten notes:

```
HΨ = iℏ (∂Ψ/∂t)
```

Where:
- **H** = Hamiltonian operator (total energy of the system)
- **Ψ** (Psi) = Wave function (describes the quantum state)
- **i** = Imaginary unit (√-1)
- **ℏ** = Reduced Planck's constant (h/2π ≈ 1.055 × 10⁻³⁴ J·s)
- **∂Ψ/∂t** = Partial derivative of the wave function with respect to time

## What It Means

The Schrodinger equation is the **fundamental equation of quantum mechanics**. It describes how the quantum state of a physical system changes over time.

### Left side: `HΨ`
- The Hamiltonian `H` acting on the wave function
- Represents the total energy (kinetic + potential) of the system
- `H` is a **linear operator** (connects to [Linear Algebra](../math/linear-algebra.md))

### Right side: `iℏ (∂Ψ/∂t)`
- How the wave function evolves in time
- The `i` makes the evolution **unitary** (preserves probability)
- The `ℏ` sets the scale of quantum effects

## Why Complex Numbers Are Essential

The `i` in the Schrodinger equation is not optional -- quantum mechanics **requires** complex numbers:

- Wave functions are complex-valued: `Ψ(x,t) ∈ ℂ`
- Probability = |Ψ|² (magnitude squared of complex number)
- Interference comes from complex phase: `e^(iθ)`

This connects directly to [Complex Numbers](../math/complex-numbers.md) and Euler's formula:

```
e^(ix) = cos(x) + i·sin(x)
```

## Wave Functions Live in Hilbert Space

- Hilbert space is an infinite-dimensional [function space](../math/linear-algebra.md)
- K^X = { f : X → K } where K = ℂ (complex numbers)
- Inner product: ⟨f|g⟩ = ∫ f*(x)·g(x) dx
- Operators (like H) act on this space

## Connections

- Complex numbers: [Complex Numbers](../math/complex-numbers.md) -- Euler's formula, e^(ix)
- Function spaces: [Linear Algebra](../math/linear-algebra.md) -- Hilbert space, operators
- Undecidability: [Halting Problem](../theoretical-cs/halting-problem.md) -- some quantum systems are undecidable too
