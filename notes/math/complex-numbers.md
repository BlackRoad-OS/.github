# Complex Numbers

## Multiplication of Complex Conjugates

```
a(a - aib + aib - ibib)
= a² - (ib)²
= a² + b²
```

**Key identity:**

```
(a + ib)(a - ib) = a² + b²
```

This is the **complex conjugate product** -- multiplying a complex number by its conjugate always yields a real number.

## Imaginary Numbers

```
(y + x)² y
```

- Imaginary unit: `i² = -1`
- Complex number form: `z = a + bi`

## Real Numbers

- `x` is real
- **Euler's identity:** `e^(iπ) + 1 = 0`
- Magnitude: `(y + x)²`

### Absolute Value

```
|x| = 1
|x - 1| = -1   (Note: absolute value is always >= 0; this explores when the inner expression is negative)
A = 1
```

## Euler's Formula Expansion

```
e^(ix) = 1 + ix - x²/2 - ix³/6 + x⁴/24 - ...
```

This is the **Taylor series expansion** of `e^(ix)`:

```
e^(ix) = cos(x) + i·sin(x)

cos(x) = 1 - x²/2! + x⁴/4! - ...
sin(x) = x - x³/3! + x⁵/5! - ...
```

## Connections

- Complex numbers connect to [Quantum Mechanics](../physics/quantum-mechanics.md) via the Schrodinger equation
- Euler's formula connects to [Modular Arithmetic](modular-arithmetic.md) through cyclic groups
