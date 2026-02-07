# Math & CS Notes Repository

A structured collection of study notes spanning pure mathematics, theoretical computer science, physics, programming, networking, and AI architecture.

## Contents

### Math
- [Complex Numbers](math/complex-numbers.md) -- Conjugates, Euler's formula, Taylor expansion of e^(ix)
- [Modular Arithmetic](math/modular-arithmetic.md) -- Definition, clock arithmetic, congruence properties
- [Linear Algebra](math/linear-algebra.md) -- Function spaces K^X, scalar-product associativity proof

### Theoretical Computer Science
- [The Halting Problem](theoretical-cs/halting-problem.md) -- Turing's undecidability proof, h/h+ construction, self-reference
- [Paradoxes & Self-Reference](theoretical-cs/paradoxes.md) -- Liar paradox, Cantor diagonalization, Monty Hall Trolley Problem

### Physics
- [Quantum Mechanics](physics/quantum-mechanics.md) -- Schrodinger equation, wave functions, Hilbert space

### Programming
- [Python Mutability](programming/python-mutability.md) -- References vs copies, list aliasing, += rebinding behavior

### Networking
- [VLAN Configuration](networking/vlan-configuration.md) -- Cisco switch commands, access/trunk modes
- [IPv4 Subnetting](networking/ipv4-subnetting.md) -- Complete CIDR table, binary calculations, private ranges, IPv4 classes
- [DNS](networking/dns.md) -- Resolution flow, hierarchy, record types

### AI Architecture
- [Agentic Patterns](ai-architecture/agentic-patterns.md) -- Multi-agent patterns: parallel, sequential, loop, router, aggregator, network, hierarchical

### Puzzles & Misc
- [Connect All 9](puzzles/connect-nine.md) -- Classic dot puzzle, triangular numbers (termial)
- [Orbital Mechanics](puzzles/orbital-mechanics.md) -- Planetary orbits, Kepler's laws

## Topic Map

```
                    ┌─────────────────┐
                    │  Complex Numbers│
                    └────────┬────────┘
                             │ Euler's formula
                             ▼
                    ┌─────────────────┐         ┌──────────────┐
                    │    Quantum      │────────→ │ Linear       │
                    │    Mechanics    │  Hilbert │ Algebra      │
                    └─────────────────┘  space   └──────────────┘
                                                        │
                    ┌─────────────────┐                 │ finite fields
                    │    Modular      │ ←───────────────┘
                    │    Arithmetic   │
                    └────────┬────────┘
                             │ binary math
                             ▼
                    ┌─────────────────┐
                    │ IPv4 Subnetting │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │  VLAN    DNS    │
                    └─────────────────┘

  ┌─────────────────┐         ┌──────────────────┐
  │ Halting Problem  │────────→│ Paradoxes &      │
  │ (Turing 1936)    │ self-  │ Self-Reference   │
  └──────────────────┘ ref    └──────────────────┘

  ┌─────────────────┐         ┌──────────────────┐
  │ Python           │ shared │ Agentic          │
  │ Mutability       │ state  │ Architectures    │
  └──────────────────┘────────└──────────────────┘
```

## Source

Notes transcribed from handwritten pages, reference images, and community discussions (r/askmath, r/trolleyproblem, r/askastronomy, r/PythonLearnersHub, networks.baseline, leadgenman).
