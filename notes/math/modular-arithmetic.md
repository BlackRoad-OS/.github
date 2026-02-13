# Modular Arithmetic

## Definition

If A and B are two integers, and A is divided by B, then the relationship:

```
A = B × Q + R
```

is written in modular arithmetic as:

```
A (mod B) = R
```

Where:
- **A** = Dividend
- **B** = Divisor (modulus)
- **Q** = Quotient
- **R** = Remainder

## Examples

### Basic Example

```
14 ÷ 3 = 4, remainder 2
→ 14 (mod 3) = 2
```

### Detailed Breakdown

```
In Math:        11 : 3 = 3 remaining 2

In Modular:     2 ≡ 11 mod 3
                11 = (3 × 3) + 2

In Alteryx:     Mod(11, 3)    → "Modulo of 11 divided by 3"
```

## Clock Arithmetic (mod 12)

The clock is the most intuitive example of modular arithmetic:

```
9 o'clock + 4 hours = 1 o'clock
Because: 9 + 4 = 13 ≡ 1 (mod 12)
```

**13 is the same as 1 when divided by 12.**

Other clock examples:
```
10 + 5 = 15 ≡ 3 (mod 12)
6 + 6 = 12 ≡ 0 (mod 12)
11 + 3 = 14 ≡ 2 (mod 12)
```

## Properties of Modular Arithmetic

If `a ≡ b (mod n)`, then:

### Addition
```
a + k ≡ b + k (mod n)
```

### Subtraction
```
a - k ≡ b - k (mod n)
```

### Scalar Multiplication
```
k·a ≡ k·b (mod n)
```

### Exponentiation
```
a^k ≡ b^k (mod n)
```

These properties mean you can **add, subtract, multiply, and exponentiate** both sides of a modular congruence and the relationship holds.

## Applications

- **Cryptography** (RSA, Diffie-Hellman)
- **Hash functions**
- **Clock arithmetic / cyclic systems**
- **Error-detecting codes** (ISBN, checksums)
- **Calendar calculations** (day of week)

## Connections

- Modular arithmetic underlies much of [IPv4 Subnetting](../networking/ipv4-subnetting.md) (binary math)
- Connects to [Linear Algebra](linear-algebra.md) through finite fields
