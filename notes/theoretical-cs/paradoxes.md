# Paradoxes & Self-Reference

## The Liar Paradox

```
"This sentence is false"
```

- If the sentence is **true**, then it must be false (because it says so)
- If the sentence is **false**, then it must be true (because "this sentence is false" would be wrong)
- **It refers to its own truth value** -- creating an unresolvable loop

## Levels of Abstraction

The key insight: paradoxes arise when a system tries to **talk about itself**.

| Level | Example |
|-------|---------|
| Object level | A program running |
| Meta level | A program analyzing another program |
| Self-referential | A program analyzing itself |

When the meta level and object level collapse into each other, paradoxes emerge.

## Cantor Diagonalization

**Georg Cantor's proof that the real numbers are uncountable:**

1. Assume you can list ALL real numbers between 0 and 1
2. Construct a new number by changing each diagonal digit
3. This new number differs from every number on the list
4. Contradiction: the list was supposed to be complete

**Applied to computation** → [The Halting Problem](halting-problem.md)

1. Assume a program `h` can decide halting for ALL programs
2. Construct `h+` that does the opposite of what `h` predicts
3. Feed `h+` its own source code
4. Contradiction: `h` gives the wrong answer

## The Monty Hall Trolley Problem

A creative fusion of two classic problems (from r/trolleyproblem):

> You are forced to blindly choose a path for a trolley to travel down, knowing one has only 1 person tied to it and the other two have 5. As the trolley approaches, one pathway (which you did not choose) is revealed to have 5 people. Is it in your moral best interest to switch to the unknown path?

This combines:
- **Monty Hall Problem** (probability -- you should switch, 2/3 chance of saving more people)
- **Trolley Problem** (ethics -- is it moral to actively switch and potentially cause harm?)

### The Math

If you initially pick randomly among 3 tracks:
- P(picked the 1-person track) = 1/3
- P(picked a 5-person track) = 2/3
- After reveal: switching gives 2/3 chance of the 1-person track

**Switching is both probabilistically and ethically optimal.**

## Connections

- Self-reference is the core of the [Halting Problem](halting-problem.md)
- Abstract reasoning connects to [Linear Algebra function spaces](../math/linear-algebra.md)
- Godel's Incompleteness Theorems (related to Golden Braid / GEB)
