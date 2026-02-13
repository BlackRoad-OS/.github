# Connect All 9 Puzzle

## The Problem

Given a 3x3 grid of 9 dots:

```
●  ●  ●
●  ●  ●
●  ●  ●
```

**Rules:**
1. Connect all 9 dots
2. Use four straight lines
3. Without lifting your pen
4. Without retracing

## The Termial (Triangular Number)

From the comments: **"Termial of 9 is 45"**

The **termial** (triangular number) of n is:

```
T(n) = 1 + 2 + 3 + ... + n = n(n+1)/2
```

For n = 9:
```
T(9) = 9 × 10 / 2 = 45
```

This is the sum of all integers from 1 to 9.

## The Solution (Thinking Outside the Box)

The classic solution requires extending lines **beyond the grid boundary**:

```
Start ──→──→──→──┐
                  │ (line extends past the dots)
    ┌──←──←──←──←┘
    │
    └──→──→──→──→──┐
                    │
         ←──←──←──←┘
```

This is the origin of the phrase **"thinking outside the box."**

## Connections

- Connects to [Paradoxes](../theoretical-cs/paradoxes.md) -- breaking assumed constraints
- The triangular number formula uses concepts from [Modular Arithmetic](../math/modular-arithmetic.md) (summation patterns)
