# Python Mutability & References

## The Puzzle (from r/PythonLearnersHub)

```python
# Output of this Python program?
a = [[1], [2]]
b = a
b[0].append(11)
b += [[3]]
b[1].append(22)
b[2].append(33)

print(a)
```

### Possible Answers
```
A) [[1], [2]]
B) [[1, 11], [2]]
C) [[1, 11], [2, 22]]
D) [[1, 11], [2, 22], [3, 33]]
```

### Correct Answer: **C) [[1, 11], [2, 22]]**

## Why?

### Step-by-step trace:

```python
a = [[1], [2]]          # a points to a list of two lists
b = a                    # b points to the SAME object as a (no copy!)

b[0].append(11)          # Mutates the first inner list
                         # a is now [[1, 11], [2]] (same object!)

b += [[3]]               # THIS IS THE KEY LINE
                         # b += [[3]] is equivalent to b = b + [[3]]
                         # This creates a NEW list and reassigns b
                         # Now b = [[1, 11], [2], [3]]
                         # But a still points to the ORIGINAL list!
                         # a = [[1, 11], [2]]

b[1].append(22)          # Mutates b's second element
                         # But b[1] is still the SAME object as a[1]
                         # So a[1] also becomes [2, 22]
                         # a = [[1, 11], [2, 22]]

b[2].append(33)          # Mutates b's third element [3] → [3, 33]
                         # a has no third element, unaffected
```

### Final state:
```python
a = [[1, 11], [2, 22]]           # Answer C
b = [[1, 11], [2, 22], [3, 33]]
```

## Key Concepts

### Assignment creates references, not copies
```python
b = a    # b and a point to the SAME object
```

### `+=` on lists can rebind
```python
b += [[3]]   # Creates new list, rebinds b
             # Different from b.extend([[3]]) which mutates in-place
```

### Inner lists are shared objects
Even after `b` is reassigned, `b[0]` and `a[0]` still point to the same inner list, so mutations to one affect the other.

## Mental Model

```
Before b += [[3]]:
a ──→ [ ref0, ref1 ]
b ──→ ↑ (same object)
       ref0 → [1, 11]
       ref1 → [2]

After b += [[3]]:
a ──→ [ ref0, ref1 ]          (original list)
b ──→ [ ref0, ref1, ref2 ]    (NEW list, but shares ref0 and ref1)
       ref0 → [1, 11]
       ref1 → [2, 22]
       ref2 → [3, 33]
```

## Connections

- Memory models relate to [Agentic Architecture](../ai-architecture/agentic-patterns.md) (shared memory vs. isolated agents)
- Binary representation relates to [IPv4 Subnetting](../networking/ipv4-subnetting.md)
