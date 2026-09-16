# Numerical Methods — Complete Master Notes

> **Purpose:** Exam-oriented notes combining the original notebook content with cleaned code, explanations, formulas, conditions, common mistakes, and quick revision points.

---

## Table of Contents

1. [Numerical Integration](#1-numerical-integration)
   - [Trapezoidal Rule](#11-trapezoidal-rule)
   - [Simpson's 1/3 Rule](#12-simpsons-13-rule)
   - [Simpson's 3/8 Rule](#13-simpsons-38-rule)
2. [Root Finding](#2-root-finding)
   - [Bisection Method](#21-bisection-method)
   - [Regula Falsi Method](#22-regula-falsi-method)
   - [Newton–Raphson Method](#23-newtonraphson-method)
3. [Interpolation](#3-interpolation)
   - [Lagrange Interpolation](#31-lagrange-interpolation)
4. [Linear Equations](#4-linear-equations)
   - [Gauss–Jordan Elimination](#41-gaussjordan-elimination)
5. [Polynomial Operations](#5-polynomial-operations)
   - [Synthetic Division](#51-synthetic-division)
6. [Exam Quick Revision](#6-exam-quick-revision)

---

# 1. Numerical Integration

Numerical integration is used to approximate a definite integral when an exact analytical solution is inconvenient or unavailable.

For

$$
I = \int_a^b f(x)\,dx
$$

we divide the interval $[a,b]$ into $n$ subintervals.

The common step size is

$$
h = rac{b-a}{n}.
$$

The grid points are

$$
x_i = a+ih,\qquad i=0,1,\ldots,n.
$$

---

## 1.1 Trapezoidal Rule

### Idea

The Trapezoidal Rule replaces the curve between two consecutive points with a straight line. The area under each small section is therefore approximated by a trapezoid.

The composite Trapezoidal Rule is

$$
oxed{
I pprox
rac{h}{2}
\left[
f(x_0)+f(x_n)
+2\sum_{i=1}^{n-1}f(x_i)
ight]
}
$$

where

$$
h=rac{b-a}{n}.
$$

### Weight pattern

```text
f(x0) + 2f(x1) + 2f(x2) + ... + 2f(xn-1) + f(xn)
  1        2        2                2          1
```

### Exam-ready Python

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

For

$$
f(x)=x^2,\quad a=1,\quad b=2
$$

the exact integral is

$$
\int_1^2x^2dx=rac73pprox2.333333.
$$

### With tolerance / epsilon

If an approximation must be refined until the difference between two successive estimates is below $\epsilon$, repeatedly increase $n$.

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

### Important correction

Do **not** write only:

```python
n *= 2
```

after the loop and expect a new approximation. The integral must be recalculated after changing `n`, which is why a `while` loop is required.

---

## 1.2 Simpson's 1/3 Rule

### Idea

Simpson's 1/3 Rule approximates the function using quadratic interpolation over pairs of subintervals.

The composite formula is

$$
oxed{
Ipprox
rac{h}{3}
\left[
f(x_0)+f(x_n)
+4\sum_{	ext{odd }i}f(x_i)
+2\sum_{	ext{even }i}f(x_i)
ight]
}
$$

### Condition

**$n$ must be even.**

### Weight pattern

```text
1   4   2   4   2   4   ...   2   4   1
```

### Exam-ready Python

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

    ans = (h / 3) * (
        y[0] + y[n] + 4 * s_odd + 2 * s_even
    )

    return ans


f = lambda x: x**2

result = simpson_1_3(f, 1, 2, 50)

print(result)
```

### Important mistake to avoid

This:

```python
y.append(x)
```

stores the $x$-coordinate.

For numerical integration, we need the function value:

```python
y.append(f(x))
```

So

$$
y_i=f(x_i).
$$

Also, if the calculated answer is stored in `ans`, return:

```python
return ans
```

not one of the intermediate sums.

---

## 1.3 Simpson's 3/8 Rule

### Idea

Simpson's 3/8 Rule uses cubic interpolation over groups of three subintervals.

The composite formula is

$$
oxed{
Ipprox
rac{3h}{8}
\left[
f(x_0)+f(x_n)
+3\sum f(x_i)
+2\sum f(x_i)
ight]
}
$$

More explicitly, the interior weights follow:

```text
1   3   3   2   3   3   2   ...   3   3   1
```

### Condition

**$n$ must be a multiple of 3.**

### Exam-ready Python

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

# 2. Root Finding

Root finding means finding a value $x$ such that

$$
f(x)=0.
$$

Common numerical methods include:

- Bisection
- Regula Falsi
- Newton–Raphson

---

## 2.1 Bisection Method

### Condition

For a continuous function, the initial interval $[a,b]$ should satisfy

$$
f(a)f(b)<0.
$$

This means the function changes sign across the interval.

### Formula

The midpoint is

$$
oxed{x_m=rac{a+b}{2}}
$$

After evaluating $f(x_m)$, retain the half-interval containing the sign change.

### Algorithm

```text
Choose a and b
Check f(a)f(b) < 0
        ↓
Find midpoint
        ↓
Evaluate f(mid)
        ↓
Select half containing root
        ↓
Repeat until error < epsilon
```

### Python

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

### Key point

Bisection is slow but reliable when the function is continuous and the root is bracketed.

---

## 2.2 Regula Falsi Method

Regula Falsi is also a bracketing method, but instead of taking the midpoint, it uses the intersection of a secant line with the $x$-axis.

### Formula

$$
oxed{
c=
rac{af(b)-bf(a)}
{f(b)-f(a)}
}
$$

The root must initially be bracketed:

$$
f(a)f(b)<0.
$$

### Python

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

### Difference from Bisection

```text
Bisection       → midpoint
Regula Falsi    → secant-line intersection
```

Both maintain a bracket around the root.

---

## 2.3 Newton–Raphson Method

Newton–Raphson uses the tangent to the curve at the current approximation.

### Formula

$$
oxed{
x_{n+1}
=
x_n-rac{f(x_n)}{f'(x_n)}
}
$$

### Python

```python
def newton_raphson(f, df, x0, epsilon):

    while True:

        x1 = x0 - f(x0) / df(x0)

        if abs(x1 - x0) < epsilon:
            return x1

        x0 = x1
```

### Important condition

The derivative should not be zero:

$$
f'(x_n)
eq0.
$$

### Comparison

| Method | Derivative needed? | Bracket required? | Main idea |
|---|---|---|---|
| Bisection | No | Yes | Midpoint |
| Regula Falsi | No | Yes | Secant intersection |
| Newton–Raphson | Yes | No | Tangent |

---

# 3. Interpolation

Interpolation estimates an unknown function value between known observations.

Given points

$$
(x_0,y_0),(x_1,y_1),\ldots,(x_n,y_n),
$$

we estimate $y$ at a new point $x_p$.

---

## 3.1 Lagrange Interpolation

The Lagrange interpolation polynomial is

$$
oxed{
P(x)=
\sum_{i=0}^{n}
y_iL_i(x)
}
$$

where

$$
L_i(x)=
\prod_{\substack{j=0\j
e i}}^n
rac{x-x_j}{x_i-x_j}.
$$

### Python

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

### Example

```python
x = [0, 1]
y = [47, 50]

result = lagrange(x, y, 0.8)

print(result)
```

### Important mistake

The condition

```python
if i != j:
```

is essential because the denominator

$$
x_i-x_i=0
$$

when $i=j$.

---

# 4. Linear Equations

A system of linear equations can be represented as

$$
AX=B.
$$

For example,

$$
egin{aligned}
a_{11}x_1+a_{12}x_2 &= b_1\
a_{21}x_1+a_{22}x_2 &= b_2.
\end{aligned}
$$

Numerically, the system can be solved using elimination methods.

---

## 4.1 Gauss–Jordan Elimination

Gauss–Jordan elimination converts the augmented matrix

$$
[A|B]
$$

into reduced row-echelon form.

The desired final structure is

$$
[I|X]
$$

where $I$ is the identity matrix and $X$ contains the solution.

### Basic row operations

1. Swap two rows.
2. Multiply a row by a non-zero constant.
3. Add a multiple of one row to another row.

### Algorithm

```text
Start with augmented matrix
        ↓
Choose pivot
        ↓
Make pivot = 1
        ↓
Eliminate pivot column
        ↓
Move to next column
        ↓
Repeat
        ↓
Read solution
```

### Exam idea

For each pivot:

```python
A[i] = A[i] / pivot
```

then eliminate that variable from every other row:

```python
A[j] = A[j] - factor * A[i]
```

A robust implementation should check whether the pivot is zero and, if necessary, swap with a lower row.

---

# 5. Polynomial Operations

## 5.1 Synthetic Division

Synthetic division provides a short method for dividing a polynomial by a linear factor

$$
x-r.
$$

Suppose

$$
P(x)=a_nx^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0.
$$

The coefficients are processed from left to right.

### Algorithm

For divisor $x-r$:

```text
Bring down first coefficient
        ↓
Multiply by r
        ↓
Add to next coefficient
        ↓
Repeat
```

The final value is the remainder.

By the Remainder Theorem,

$$
oxed{P(r)=	ext{remainder}}.
$$

If the remainder is zero, then

$$
x-r
$$

is a factor of $P(x)$.

### Python

```python
def synthetic_division(coefficients, r):

    result = [coefficients[0]]

    for i in range(1, len(coefficients)):
        result.append(
            coefficients[i] + r * result[-1]
        )

    quotient = result[:-1]
    remainder = result[-1]

    return quotient, remainder
```

Example:

```python
coefficients = [1, -6, 11, -6]

quotient, remainder = synthetic_division(coefficients, 1)

print("Quotient:", quotient)
print("Remainder:", remainder)
```

---

# 6. Exam Quick Revision

## Integration

### Trapezoidal

$$
oxed{
I=
rac{h}{2}
[y_0+y_n+2(y_1+\cdots+y_{n-1})]
}
$$

No special restriction on $n$.

---

### Simpson's 1/3

$$
oxed{
I=
rac{h}{3}
[y_0+y_n+4\sum y_{	ext{odd}}+2\sum y_{	ext{even}}]
}
$$

**Condition:** $n$ must be even.

Weight pattern:

```text
1  4  2  4  2  4 ... 2  4  1
```

---

### Simpson's 3/8

$$
oxed{
I=
rac{3h}{8}
[y_0+y_n+3\sum y_{i
ot\equiv0(3)}
+2\sum y_{i\equiv0(3)}]
}
$$

**Condition:** $n$ must be divisible by 3.

Weight pattern:

```text
1  3  3  2  3  3  2 ... 3  3  1
```

---

## Root Finding

### Bisection

$$
oxed{x_m=rac{a+b}{2}}
$$

Condition:

$$
f(a)f(b)<0.
$$

---

### Regula Falsi

$$
oxed{
x=
rac{af(b)-bf(a)}
{f(b)-f(a)}
}
$$

Condition:

$$
f(a)f(b)<0.
$$

---

### Newton–Raphson

$$
oxed{
x_{n+1}
=
x_n-rac{f(x_n)}{f'(x_n)}
}
$$

Requires $f'(x)$.

---

## Interpolation

### Lagrange

$$
oxed{
P(x)=\sum_{i=0}^n y_i
\prod_{j
e i}
rac{x-x_j}{x_i-x_j}
}
$$

Remember:

```python
if i != j:
```

---

## Linear Algebra

### Gauss–Jordan

Target:

$$
[A|B]\longrightarrow[I|X]
$$

Use row operations and pivoting.

---

## Polynomial

### Synthetic Division

For divisor:

$$
x-r
$$

the final synthetic-division value is:

$$
P(r).
$$

If it equals zero:

$$
P(r)=0
\Rightarrow x-r	ext{ is a factor}.
$$

---

# Common Python Mistakes in Numerical Methods

### 1. Forgetting `f(x)`

Wrong:

```python
y.append(x)
```

Correct:

```python
y.append(f(x))
```

---

### 2. Returning the wrong variable

Wrong:

```python
ans = ...
return se
```

Correct:

```python
ans = ...
return ans
```

---

### 3. Updating `n` without recalculating

Wrong:

```python
n *= 2
```

with no surrounding iteration.

Correct:

```python
while True:
    calculate()
    if error < epsilon:
        return answer
    n *= 2
```

---

### 4. Forgetting the stopping condition

Iterative algorithms should have a clear condition such as:

```python
if abs(new - old) < epsilon:
    return new
```

or:

```python
if abs(f(x)) < epsilon:
    return x
```

---

### 5. Incorrect Simpson conditions

```text
Simpson 1/3 → n even
Simpson 3/8 → n divisible by 3
```

---

# Final Exam Strategy

For almost every numerical-method program, identify these five things first:

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

## End of Master Notes


---

# Original Notebook Content (Preserved)


### Original Code Cell 1

```python
import math
```


### Original Code Cell 2

```python
# lagrange Interpolation

def lagrange(x,y,xp):
    yp = 0

    for i in range(len(x)):
        p = y[i]
        for j in range(len(y)):
            if i != j:
                p = p * (( xp - x[j])/(x[i] - x[j]))

        yp += p

    return yp

x = [1,2,3]
y = [3,10,18]

lagrange(x,y,2.5)
```


### Original Code Cell 3

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


### Original Code Cell 4

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


### Original Code Cell 5

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

    ans = (3*h/8)*(y[0] + y[n] + 3* s3 + 2* s2)

    return ans

simpson_3_8(f,1,2,99)
```


### Original Code Cell 6

```python
# Romberg Integration

def trap(f,a,b,n):
    h = (b-a)/n
    s = 0

    for i in range(n):
        s += (f(a+i*h) + f(a + (i + 1)* h)) * (h/2)

    return s 

def romberg(f,a,b,k):
    r = [[None]*k for _ in range(k)]

    for i in range(k):
        r[i][0] = trap(f,a,b,2**i)

    for j in range(1,k):
        for i in range(k-j):
            r[i][j] = ((4 ** j) * r[i+1][j-1] - r[i][j-1] / (4**(j-1) ))

    return r 

f = lambda x: math.log(x)

answer = romberg(f,1,6,4)

for row in answer:
    formatt = [f"{val : .5f}" for val in row if val is not None]

    print(formatt)

print(f"\n final answer: {answer[0][-1]: .5f}")
```


### Original Code Cell 7

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


### Original Code Cell 8

```python
# Regula Falsi Root Finding

def regula_falsi(f,a,b,e,n):
    
    if f(a)*f(b) >= 0:
        print(" invalid interval")
        return

    for i in range(n):
        c = a - ((f(b)(b-a))/(f(a)-f(b)))

        print(i+1, c)

        if abs(f(c)) < e:
            return f(c)

        if f(a) * f(b) < 0:
            b = c

        else:
            a = c

    return c
```

