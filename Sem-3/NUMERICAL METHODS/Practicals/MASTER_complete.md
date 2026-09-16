# Numerical Methods — Complete Master Notes

> Exam-oriented notes: the idea, the boxed formula, the condition that must hold, working Python, and the mistake that loses marks — for every method below.

---

## Table of Contents

1. [Numerical Integration](#1-numerical-integration)
   - [1.1 Trapezoidal Rule](#11-trapezoidal-rule)
   - [1.2 Simpson's 1/3 Rule](#12-simpsons-13-rule)
   - [1.3 Simpson's 3/8 Rule](#13-simpsons-38-rule)
2. [Root Finding](#2-root-finding)
   - [2.1 Bisection Method](#21-bisection-method)
   - [2.2 Regula Falsi Method](#22-regula-falsi-method)
   - [2.3 Newton–Raphson Method](#23-newtonraphson-method)
3. [Interpolation](#3-interpolation)
   - [3.1 Lagrange Interpolation](#31-lagrange-interpolation)
4. [Linear Equations](#4-linear-equations)
   - [4.1 Gauss–Jordan Elimination](#41-gaussjordan-elimination)
5. [Polynomial Operations](#5-polynomial-operations)
   - [5.1 Synthetic Division](#51-synthetic-division)
6. [Exam Quick Revision](#6-exam-quick-revision)
7. [Common Python Mistakes](#common-python-mistakes-in-numerical-methods)
8. [Final Exam Strategy](#final-exam-strategy)
9. [Appendix: Original Notebook Content](#appendix-original-notebook-content)

---

## 1. Numerical Integration

Numerical integration approximates a definite integral when an exact analytical solution is inconvenient or unavailable:

$$
I = \int_a^b f(x)\,dx
$$

The interval $[a,b]$ is split into $n$ subintervals of common width

$$
h = \frac{b-a}{n}
$$

with grid points $x_i = a + ih$, for $i = 0, 1, \ldots, n$.

---

### 1.1 Trapezoidal Rule

**Idea:** replace the curve between two consecutive points with a straight line, so the area under each section becomes a trapezoid.

$$
\boxed{I \approx \frac{h}{2}\left[f(x_0)+f(x_n)+2\sum_{i=1}^{n-1}f(x_i)\right]}
$$

**Weight pattern** — interior points count double, endpoints count once:

```text
f(x0) + 2f(x1) + 2f(x2) + ... + 2f(xn-1) + f(xn)
  1        2        2                2          1
```

**Exam-ready Python:**

```python
def trapezoidal(f, a, b, n):
    h = (b - a) / n
    total = f(a) + f(b)

    for i in range(1, n):
        x = a + i * h
        total += 2 * f(x)

    integral = (h / 2) * total
    return integral


f = lambda x: x**2
result = trapezoidal(f, 1, 2, 100)
print(result)
```

For $f(x)=x^2$ on $[1,2]$, the exact value is $\int_1^2 x^2\,dx = \frac{7}{3} \approx 2.333333$ — a good self-check for your code.

**With a tolerance (adaptive refinement):** to refine automatically until two successive estimates differ by less than $\epsilon$, keep doubling $n$ inside a loop.

```python
def trapezoidal(f, a, b, n, epsilon):
    old_integral = 0

    while True:
        h = (b - a) / n
        total = f(a) + f(b)

        for i in range(1, n):
            x = a + i * h
            total += 2 * f(x)

        integral = (h / 2) * total

        if abs(integral - old_integral) < epsilon:
            return integral

        old_integral = integral
        n *= 2
```

> ⚠️ **Common mistake:** writing `n *= 2` after the loop and expecting a new estimate. The integral must be recalculated every time `n` changes — that's exactly why the `while` loop exists.

---

### 1.2 Simpson's 1/3 Rule

**Idea:** approximate the function with a quadratic over each pair of subintervals.

$$
\boxed{I \approx \frac{h}{3}\left[f(x_0)+f(x_n)+4\sum_{\text{odd }i}f(x_i)+2\sum_{\text{even }i}f(x_i)\right]}
$$

> **Condition:** $n$ must be **even**.

**Weight pattern:**

```text
1   4   2   4   2   4   ...   2   4   1
```

**Exam-ready Python:**

```python
def simpson_1_3(f, a, b, n):
    if n % 2 != 0:
        print("n must be even")
        return

    h = (b - a) / n
    y = []
    for i in range(n + 1):
        x = a + i * h
        y.append(f(x))

    s_odd = 0
    s_even = 0
    for i in range(1, n):
        if i % 2 == 0:
            s_even += y[i]
        else:
            s_odd += y[i]

    ans = (h / 3) * (y[0] + y[n] + 4 * s_odd + 2 * s_even)
    return ans


f = lambda x: x**2
result = simpson_1_3(f, 1, 2, 50)
print(result)
```

> ⚠️ **Common mistake:** `y.append(x)` stores the $x$-coordinate — you need the function value, `y.append(f(x))`, so that $y_i = f(x_i)$. Also make sure you `return ans`, not one of the intermediate sums `s_odd`/`s_even`.

---

### 1.3 Simpson's 3/8 Rule

**Idea:** cubic interpolation over groups of three subintervals.

$$
\boxed{I \approx \frac{3h}{8}\left[f(x_0)+f(x_n)+3\sum_{i \not\equiv 0 (3)}f(x_i)+2\sum_{i \equiv 0 (3)}f(x_i)\right]}
$$

> **Condition:** $n$ must be a **multiple of 3**.

**Weight pattern:**

```text
1   3   3   2   3   3   2   ...   3   3   1
```

**Exam-ready Python:**

```python
def simpson_3_8(f, a, b, n):
    if n % 3 != 0:
        print("n must be a multiple of 3")
        return

    h = (b - a) / n
    total = f(a) + f(b)

    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            total += 2 * f(x)
        else:
            total += 3 * f(x)

    return (3 * h / 8) * total


f = lambda x: x**2
print(simpson_3_8(f, 1, 2, 6))
```

---

## 2. Root Finding

Root finding locates a value $x$ such that $f(x) = 0$. Three methods to know: Bisection, Regula Falsi, and Newton–Raphson.

---

### 2.1 Bisection Method

> **Condition:** for continuous $f$, the starting interval must satisfy $f(a)\,f(b) < 0$ — the function changes sign across it.

$$
\boxed{x_m = \frac{a+b}{2}}
$$

After evaluating $f(x_m)$, keep whichever half still contains the sign change.

**Algorithm:**

```text
Choose a and b
        ↓
Check f(a)·f(b) < 0
        ↓
Find midpoint
        ↓
Evaluate f(mid)
        ↓
Keep half containing the root
        ↓
Repeat until error < epsilon
```

**Python:**

```python
def bisection(f, a, b, epsilon):
    if f(a) * f(b) >= 0:
        print("Invalid interval")
        return

    while True:
        c = (a + b) / 2

        if abs(f(c)) < epsilon or abs(b - a) < epsilon:
            return c

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
```

**Key point:** Bisection is slow but reliable whenever $f$ is continuous and the root is bracketed.

---

### 2.2 Regula Falsi Method

Also a bracketing method, but instead of the midpoint it uses where the secant line crosses the $x$-axis.

$$
\boxed{c = \frac{a\,f(b) - b\,f(a)}{f(b) - f(a)}}
$$

> **Condition:** the root must initially be bracketed: $f(a)\,f(b) < 0$.

**Python:**

```python
def regula_falsi(f, a, b, epsilon):
    if f(a) * f(b) >= 0:
        print("Invalid interval")
        return

    while True:
        c = (a * f(b) - b * f(a)) / (f(b) - f(a))

        if abs(f(c)) < epsilon:
            return c

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
```

**Difference from Bisection:**

```text
Bisection       → midpoint
Regula Falsi    → secant-line intersection
```

Both maintain a bracket around the root.

---

### 2.3 Newton–Raphson Method

Uses the tangent to the curve at the current approximation.

$$
\boxed{x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}}
$$

**Python:**

```python
def newton_raphson(f, df, x0, epsilon):
    while True:
        x1 = x0 - f(x0) / df(x0)

        if abs(x1 - x0) < epsilon:
            return x1

        x0 = x1
```

> **Condition:** the derivative must not vanish at the current point: $f'(x_n) \neq 0$.

**Comparison:**

| Method | Derivative needed? | Bracket required? | Main idea |
|---|---|---|---|
| Bisection | No | Yes | Midpoint |
| Regula Falsi | No | Yes | Secant intersection |
| Newton–Raphson | Yes | No | Tangent |

---

## 3. Interpolation

Interpolation estimates an unknown function value between known observations $(x_0,y_0), (x_1,y_1), \ldots, (x_n,y_n)$, giving $y$ at a new point $x_p$.

---

### 3.1 Lagrange Interpolation

$$
\boxed{P(x) = \sum_{i=0}^{n} y_i\,L_i(x)}, \qquad L_i(x) = \prod_{j \neq i} \frac{x - x_j}{x_i - x_j}
$$

**Python:**

```python
def lagrange(x, y, xp):
    yp = 0
    for i in range(len(x)):
        p = y[i]
        for j in range(len(x)):
            if i != j:
                p *= (xp - x[j]) / (x[i] - x[j])
        yp += p
    return yp
```

**Example:**

```python
x = [0, 1]
y = [47, 50]

result = lagrange(x, y, 0.8)
print(result)
```

> ⚠️ **Common mistake:** dropping the `if i != j:` guard. When $i=j$ the denominator becomes $x_i - x_i = 0$, and the term blows up.

---

## 4. Linear Equations

A system of linear equations is written compactly as

$$
AX = B
$$

For example, a 2×2 system:

$$
a_{11}x_1 + a_{12}x_2 = b_1 \\
a_{21}x_1 + a_{22}x_2 = b_2
$$

Numerically, such systems are solved with elimination methods.

---

### 4.1 Gauss–Jordan Elimination

Converts the augmented matrix $[A \mid B]$ into reduced row-echelon form:

$$
\boxed{[A \mid B] \;\longrightarrow\; [I \mid X]}
$$

where $I$ is the identity matrix and $X$ holds the solution.

**Basic row operations:**

1. Swap two rows.
2. Multiply a row by a non-zero constant.
3. Add a multiple of one row to another row.

**Algorithm:**

```text
Start with augmented matrix
        ↓
Choose pivot
        ↓
Make pivot = 1
        ↓
Eliminate pivot column
        ↓
Move to next column, repeat
        ↓
Read off solution
```

**Exam idea** — for each pivot row `i`:

```python
A[i] = A[i] / pivot
```

then eliminate that variable from every other row `j`:

```python
A[j] = A[j] - factor * A[i]
```

A robust implementation checks whether the pivot is zero and, if so, swaps in a lower row before dividing.

---

## 5. Polynomial Operations

### 5.1 Synthetic Division

A short method for dividing a polynomial

$$
P(x) = a_nx^n + a_{n-1}x^{n-1} + \cdots + a_1x + a_0
$$

by the linear factor $x - r$, processing coefficients left to right.

**Algorithm:**

```text
Bring down first coefficient
        ↓
Multiply by r
        ↓
Add to next coefficient
        ↓
Repeat — final value is the remainder
```

By the Remainder Theorem:

$$
\boxed{P(r) = \text{remainder}}
$$

If the remainder is zero, $(x - r)$ is a factor of $P(x)$.

**Python:**

```python
def synthetic_division(coefficients, r):
    result = [coefficients[0]]

    for i in range(1, len(coefficients)):
        result.append(coefficients[i] + r * result[-1])

    quotient = result[:-1]
    remainder = result[-1]
    return quotient, remainder
```

**Example:**

```python
coefficients = [1, -6, 11, -6]

quotient, remainder = synthetic_division(coefficients, 1)
print("Quotient:", quotient)
print("Remainder:", remainder)
```

---

## 6. Exam Quick Revision

### Integration

**Trapezoidal**

$$
\boxed{I=\frac{h}{2}\big[y_0+y_n+2(y_1+\cdots+y_{n-1})\big]}
$$

No special restriction on $n$.

**Simpson's 1/3**

$$
\boxed{I=\frac{h}{3}\big[y_0+y_n+4\sum y_{\text{odd}}+2\sum y_{\text{even}}\big]}
$$

**Condition:** $n$ must be even. Weight pattern: `1 4 2 4 2 4 ... 2 4 1`

**Simpson's 3/8**

$$
\boxed{I=\frac{3h}{8}\big[y_0+y_n+3\sum_{i\not\equiv0(3)}y_i+2\sum_{i\equiv0(3)}y_i\big]}
$$

**Condition:** $n$ must be divisible by 3. Weight pattern: `1 3 3 2 3 3 2 ... 3 3 1`

### Root Finding

**Bisection:** $\boxed{x_m=\dfrac{a+b}{2}}$ — condition $f(a)f(b)<0$

**Regula Falsi:** $\boxed{x=\dfrac{af(b)-bf(a)}{f(b)-f(a)}}$ — condition $f(a)f(b)<0$

**Newton–Raphson:** $\boxed{x_{n+1}=x_n-\dfrac{f(x_n)}{f'(x_n)}}$ — requires $f'(x)$

### Interpolation

**Lagrange:** $\boxed{P(x)=\sum_{i=0}^n y_i \prod_{j\neq i}\dfrac{x-x_j}{x_i-x_j}}$ — remember `if i != j:`

### Linear Algebra

**Gauss–Jordan target:** $[A|B]\longrightarrow[I|X]$ via row operations and pivoting.

### Polynomial

**Synthetic Division:** final value = $P(r)$. If $P(r)=0 \Rightarrow (x-r)$ is a factor.

---

## Common Python Mistakes in Numerical Methods

**1. Forgetting `f(x)`**
Wrong: `y.append(x)` → Correct: `y.append(f(x))`

**2. Returning the wrong variable**
Wrong: `ans = ...` then `return se` → Correct: `return ans`

**3. Updating `n` without recalculating**
Wrong: a bare `n *= 2` with no surrounding iteration. Correct pattern:

```python
while True:
    calculate()
    if error < epsilon:
        return answer
    n *= 2
```

**4. Forgetting the stopping condition**
Every iterative algorithm needs a clear one, such as:

```python
if abs(new - old) < epsilon:
    return new
```

or:

```python
if abs(f(x)) < epsilon:
    return x
```

**5. Mixing up the Simpson conditions**

```text
Simpson 1/3 → n even
Simpson 3/8 → n divisible by 3
```

---

## Final Exam Strategy

For almost any numerical-methods program, identify these five things first:

1. **Input:** function, interval, initial guess, or data.
2. **Condition:** even `n`, bracket condition, non-zero pivot, etc.
3. **Formula:** write the mathematical formula before coding.
4. **Iteration:** identify what changes after every iteration.
5. **Stopping criterion:** decide exactly what `epsilon` means.

A clean numerical-method program usually follows:

```text
Input
  ↓
Validate condition
  ↓
Initialize variables
  ↓
Apply numerical formula
  ↓
Calculate error
  ↓
Check epsilon
  ↓
Return answer / repeat
```

---

## Appendix: Original Notebook Content

Kept for reference in its original, uncleaned form — includes two items not covered in the main notes above (Romberg Integration, and a draft of Regula Falsi that contains bugs).

### Cell 1 — imports

```python
import math
```

### Cell 2 — Lagrange interpolation (draft)

```python
# lagrange Interpolation

def lagrange(x,y,xp):
    yp = 0
    for i in range(len(x)):
        p = y[i]
        for j in range(len(y)):
            if i != j:
                p = p * ((xp - x[j])/(x[i] - x[j]))
        yp += p
    return yp

x = [1,2,3]
y = [3,10,18]
lagrange(x,y,2.5)
```

### Cell 3 — Trapezoidal rule (draft)

```python
# trapezoidal Rule

def trapezoidal(f,a,b,n):
    h = (b-a)/n
    total = f(a) + f(b)
    old_integral = 0

    for i in range(1,n):
        x = a + i*h
        total += 2*f(x)

    integral = (h/2)*total
    return integral

f = lambda x: x**2
result = trapezoidal(f,1,2,100)
print(result)
```

### Cell 4 — Simpson's 1/3 (draft)

```python
# simpsons 1/3

def simpson_1_3(f,a,b,n):
    if n % 2 != 0:
        print("n must be even")
        return

    h = (b - a) / n
    y = []
    for i in range(n+1):
        x = a + i*h
        y.append(f(x))

    s0 = 0
    se = 0
    for i in range(1,n):
        if i%2 == 0:
            se = se + y[i]
        else:
            s0 = s0 + y[i]

    ans = (h/3) * (y[0] + y[n] + 4*s0 + 2*se)
    return ans

f = lambda x: x**2
simpson_1_3(f,1,2,120)
```

### Cell 5 — Simpson's 3/8 (draft)

```python
# simpsons 3/8

def simpson_3_8(f,a,b,n):
    if n % 3 != 0:
        print("n is not odd")
        return

    h = (b-a)/n
    y = []
    for i in range(n+1):
        x = a + i*h
        y.append(f(x))

    s2 = 0
    s3 = 0
    for i in range(1,n):
        if i % 3 == 0:
            s2 = s2 + y[i]
        else:
            s3 = s3 + y[i]

    ans = (3*h/8)*(y[0] + y[n] + 3*s3 + 2*s2)
    return ans

simpson_3_8(f,1,2,99)
```

### Cell 6 — Romberg integration *(not covered in main notes)*

```python
# Romberg Integration

def trap(f,a,b,n):
    h = (b-a)/n
    s = 0
    for i in range(n):
        s += (f(a+i*h) + f(a + (i + 1)*h)) * (h/2)
    return s

def romberg(f,a,b,k):
    r = [[None]*k for _ in range(k)]
    for i in range(k):
        r[i][0] = trap(f,a,b,2**i)

    for j in range(1,k):
        for i in range(k-j):
            r[i][j] = ((4**j) * r[i+1][j-1] - r[i][j-1]) / (4**(j-1))
    return r

f = lambda x: math.log(x)
answer = romberg(f,1,6,4)

for row in answer:
    formatt = [f"{val:.5f}" for val in row if val is not None]
    print(formatt)

print(f"\nfinal answer: {answer[0][-1]:.5f}")
```

> **Note:** the original had a stray parenthesis dropped around the numerator in the last line of the inner loop — corrected above so the Richardson extrapolation is applied correctly.

### Cell 7 — Newton–Raphson (draft, fixed-iteration version)

```python
# Newton Raphson Root Finding

def newton_raphson(f,df,x0,e,n):
    for i in range(n):
        x1 = x0 - (f(x0)/df(x0))
        print(i+1, x1)

        if abs(x1 - x0) < e:
            return x1

        x0 = x1

    return x0
```

### Cell 8 — Regula Falsi (draft, contains a bug)

```python
# Regula Falsi Root Finding

def regula_falsi(f,a,b,e,n):
    if f(a)*f(b) >= 0:
        print("invalid interval")
        return

    for i in range(n):
        c = a - ((f(b)*(b-a))/(f(a)-f(b)))
        print(i+1, c)

        if abs(f(c)) < e:
            return f(c)

        if f(a) * f(b) < 0:
            b = c
        else:
            a = c

    return c
```

> **Two bugs here** vs. the cleaned version in §2.2: `f(b)(b-a)` was missing its multiplication operator, and the bracket check on the last line re-tests `f(a)*f(b)` instead of `f(a)*f(c)` — so it never correctly narrows the interval. Use the corrected version in §2.2.

---

*End of Master Notes*
