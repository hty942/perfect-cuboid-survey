# Perfect Cuboids: A Computationally Verified Survey, with a Note on the Meaning of Existence

> **Compiled by**: Huang Tianyi and DeepSeek V4.1 Flash
> **Note**: The literature review, computational verification and bilingual writing were produced in collaboration between Huang Tianyi and DeepSeek V4.1 Flash. The paper contains no new theorems. Every claim is tagged **【P】** (a complete proof is given), **【C】** (verified by computation, range stated), or **【L】** (quoted from the literature).
> **Date**: 2026-11-26

---

## Abstract

We follow the thread "a sum of perfect squares is again a perfect square" from two terms (Pythagorean triples) through three terms (Pythagorean quadruples) and four terms, and arrive at the perfect cuboid problem.

We present a **2×2 classification**: with coordinates $k$ (the number of edge-pairs whose squares sum to a square) and $\mathcal G$ (whether the space diagonal is an integer), Euler bricks, face cuboids and perfect cuboids all fit into one table. The four common "six-of-seven" configurations occupy only two cells; the perfect cuboid occupies a third cell—and satisfies **none** of the four configurations. This single picture explains why several plausible "proof" strategies are necessarily circular.

The incremental content of this paper:

1. the forbidden set $\{2^a\}\cup\{5\cdot2^a\}$ for three-square diagonals is extended from $d\le 400$ to $d\le 1000$;
2. an intersection theorem is formalised: the numbers that are simultaneously a Pythagorean hypotenuse and have a square that is a sum of three positive squares are exactly those with a prime factor $\equiv 1 \pmod 4$ that are not of the form $5\cdot 2^a$;
3. it is proved that a single unordered triple can satisfy at most 3 of the 4 configurations, with an exact structural classification;
4. it is proved that "every cuboid belongs to the four configurations" is equivalent to "no perfect cuboid exists", exposing the circularity;
5. a geometric observation: over $\mathbb R$ and $\mathbb C$ the solutions of the four equations project onto all of $\mathbb P^2$, so "is a perfect square" does not lower the dimension geometrically—the reduction cannot reach a curve by dimension count.

Every numerical assertion is covered by the **53 checks** in `scripts/verify_all.py`; all pass.

Section 11 discusses a non-mathematical question: if a perfect cuboid (assuming one exists) is too large to exhibit, does its existence still mean anything?

---

## 0. Conventions

| Tag | Meaning |
|---|---|
| **【P】** | complete proof given here |
| **【C】** | verified computationally, range in parentheses |
| **【L】** | quoted from the literature, not independently proved here |

Environment: Python 3.12, standard library only, integer square root via `math.isqrt`. All scripts are reproducible.

---

## 1. Perfect squares

### 1.1 Intrinsic criterion 【P】

Let $n=\prod p_i^{e_i}$. The following are equivalent:

1. $n$ is a perfect square;
2. every $e_i$ is even;
3. $n$ has an odd number of positive divisors.

For (3): divisors pair as $d\cdot(n/d)$, and only $\sqrt n$ pairs with itself.

Corollary: if $p\equiv 3\pmod 4$ and $p\mid n$ with $n$ a square, then $p^2\mid n$.

### 1.2 Fast sieving (necessary, not sufficient)

| Test | Possible values for a square |
|---|---|
| last digit | $0,1,4,5,6,9$ (never $2,3,7,8$) |
| last two digits | exactly 22 patterns |
| number of trailing zeros | must be even |
| $\bmod 4$ | $0$ or $1$ |
| $\bmod 8$ | $0,1,4$ (odd squares are $\equiv 1$) |
| $\bmod 16$ | $0,1,4,9$ |
| $\bmod 9$ / digital root | residue $\in\{0,1,4,7\}$; root $\in\{1,4,7,9\}$ |
| binary | even number of trailing zeros |

【C】exactly 22 last-two-digit patterns (check 1.3); squares mod 16 form $\{0,1,4,9\}$ (1.4).

### 1.3 Structural properties

- consecutive squares differ by consecutive odd numbers: $(k+1)^2-k^2=2k+1$;
- $1+3+5+\cdots+(2k-1)=k^2$;
- $k^2=T_k+T_{k-1}$;
- $1^3+2^3+\cdots+k^3=(1+2+\cdots+k)^2$;
- multiplicatively closed: square × square = square. Not closed under addition.

### 1.4 A computational trap 【C】

A double has 53 bits of precision. For $n=10^{32}-1$:

```
isqrt(n)          = 9999999999999999    <- correct
int(math.sqrt(n)) = 10000000000000000    <- wrong by 1
```

Use `r = isqrt(n); r*r == n`.

---

## 2. Two terms: $a^2+b^2=c^2$

### 2.1 Complete description (Euclid) 【P】

All positive solutions are

$$a=k(m^2-n^2),\quad b=2kmn,\quad c=k(m^2+n^2),$$

with $m>n\ge 1$, $\gcd(m,n)=1$, $m-n$ odd, $k\ge 1$ (swap $a,b$ if needed).

【C】brute force for $c\le 2000$ yields 1981 triples, **matching the formula exactly**; 319 of them are primitive.

### 2.2 Structure of primitive triples 【P】【C】

For a primitive triple $(a,b,c)$:

- one leg is even, one is odd;
- the even leg is divisible by 4;
- exactly one leg is divisible by 3;
- exactly one of $a,b,c$ is divisible by 5.

【C】verified on all 319 primitive triples with $c\le 2000$, zero exceptions.

### 2.3 The two sharpest restrictions

**(i) The two summands cannot both be fourth powers 【L】**

If $a,b$ are both perfect squares, then $a^2+b^2=c^2$ gives $x^4+y^4=z^2$. Fermat proved this has no positive integer solution, by infinite descent.

【C】no triple with $c\le 2000$ has two square legs.

**(ii) A hypotenuse must have a prime factor $\equiv 1\pmod 4$ 【P】**

If $p\equiv 3\pmod 4$ divides $m^2+n^2$, then $-1$ is a quadratic residue mod $p$, a contradiction; so $p$ divides both $m$ and $n$, contradicting $\gcd(m,n)=1$.

【C】for $n\le 2000$, "$n$ is a hypotenuse" coincides exactly with "$n$ has a prime factor $\equiv 1\pmod 4$".

### 2.4 Number of representations 【P】【C】

The number of triples with hypotenuse $c$ (including non-primitive) is

$$\frac{\prod_{p_i\equiv 1(4)}(2e_i+1)-1}{2},\qquad c=\prod p_i^{e_i}.$$

【C】exact for all $c\le 2000$. Examples: $5\to1$, $25\to2$, $65\to4$, $325\to7$, $1105=5\cdot13\cdot17\to13$.

---

## 3. Three terms: $a^2+b^2+c^2=d^2$

### 3.1 Complete parametrisation (four-square identity) 【P】

$$(A^2+B^2+C^2+D^2)^2=(A^2+B^2-C^2-D^2)^2+(2AC-2BD)^2+(2AD+2BC)^2.$$

With $d=A^2+B^2+C^2+D^2$, the three terms on the right are the legs. **Parameters may be zero**—for instance $(1,2,2,3)$ requires $A=B=C=1,\ D=0$.

【C】all 126 primitive quadruples with $d\le 60$ are generated, none missing.

### 3.2 Structural theorem 【P】【C】

In a primitive quadruple:

- **exactly one leg is odd**;
- $d$ is odd;
- **the two even legs are congruent mod 4** (both divisible by 4, or both $\equiv 2\pmod 4$).

Proof: an even leg $\equiv 0\pmod 4$ has square $\equiv 0\pmod 8$; one $\equiv 2\pmod 4$ has square $\equiv 4\pmod 8$. An odd leg has square $\equiv 1\pmod 8$. Of the three combinations $1+0+0=1$, $1+0+4=5$, $1+4+4=9\equiv1$, only the second is not a square residue and is excluded; the rest are $\equiv 1\pmod 8$, so $d$ is odd.

【C】zero violations on the 1364 primitive quadruples with $d\le 200$.

### 3.3 All three legs can be fourth powers

$$144^2+225^2+400^2=481^2\qquad\text{i.e.}\qquad 12^4+15^4+20^4=481^2.$$

This is the **opposite** of the two-term case: $x^4+y^4=z^2$ has no solution, but $x^4+y^4+z^4=w^2$ does. The displayed line is the smallest primitive solution (exhaustive for $a,b,c\le 150$).

### 3.4 Forbidden diagonals 【P】【C】

**【P】Necessity.** If $d=2^a$, then $d^2=4^a$. If $4^a=x^2+y^2+z^2$, reducing mod 4 forces $x,y,z$ all even; descending repeatedly reduces to $1=x'^2+y'^2+z'^2$, which requires two zeros. If $d=5\cdot2^a$, the same descent reaches $25$; the only ways to write $25$ as a sum of three squares are $25+0+0$ and $9+16+0$, both with a zero.

**【C】Sufficiency.** For $d\le 1000$, "$d^2$ is a sum of three positive squares" coincides exactly with $d\notin\{2^a\}\cup\{5\cdot2^a\}$. The forbidden values up to 1000 are exactly 18:

$$1,2,4,5,8,10,16,20,32,40,64,80,128,160,256,320,512,640.$$

> The sufficiency direction is not proved in general here; it is only verified to 1000. This is the most carefully hedged point in the paper.

### 3.5 An infinite family 【P】

$$1+(2k)^2+(2k^2)^2=(2k^2+1)^2,\qquad k=1,2,3,\dots$$

giving $(1,2,2,3)$, $(1,4,8,9)$, $(1,6,18,19)$, $(1,8,32,33)$, …

### 3.6 Smallest solutions

- smallest: $1^2+2^2+2^2=3^2$;
- smallest with three distinct legs: $2^2+3^2+6^2=7^2$;
- smallest with all three legs squares: $144^2+225^2+400^2=481^2$.

---

## 4. Four terms: $a^2+b^2+c^2+e^2=d^2$

### 4.1 The constraints collapse 【L】【C】

Lagrange's four-square theorem: **every positive integer is a sum of four squares.**

【C】for $d\le 120$, only $d=1$ and $d=3$ fail to be a sum of four positive squares; every $d\ge 4$ works.

Shrinkage of the forbidden set:

| Terms | Forbidden |
|---|---|
| two | must contain a prime $\equiv 1\pmod 4$—infinitely many exceptions |
| three | $2^a$ or $5\cdot2^a$—infinitely many exceptions |
| four | **only $d=1,3$** |

### 4.2 Parity of four legs 【C】

In a primitive solution the number of odd legs is 1 or 4 (2 or 3 odd legs give a sum $\equiv 2,3,6,7\pmod 8$, never a square).

- exactly 1 odd leg: of the three even legs, the number divisible by 4 is 1 or 3;
- 4 odd legs: $d\equiv 2\pmod 4$.

Note: a primitive four-term solution may have **even** $d$—impossible in the three-term case.

### 4.3 Jacobi's four-square theorem 【L】【C】

The number of lattice points on the sphere of radius $d$ has an elementary closed form:

$$r_4(d^2)=8\sum_{m\mid d^2,\ 4\nmid m}m.$$

【C】exact for $d\le 30$. Example:

$$r_4(5^2)=248=8+48+192,$$

namely 8 points $(\pm5,0,0,0)$, 48 points $(\pm3,\pm4,0,0)$, 192 points $(\pm1,\pm2,\pm2,\pm4)$.

### 4.4 Four equal legs

$$4a^2=(2a)^2.$$

More generally: **a sum of $k$ equal squares is a square iff $k$ is a perfect square.** 【C】verified for $k\le 20$ ($1,4,9,16$).

### 4.5 All four legs can be perfect squares

$$1^4+2^4+2^4+2^4=49=7^2.$$

---

## 5. The intersection of the two- and three-term conditions

**Theorem** 【P + C】. For $c\ge 2$, the following hold simultaneously:

1. $c$ is the hypotenuse of some Pythagorean triple;
2. $c^2$ is a sum of three positive squares;

if and only if

$$c\ \text{has a prime factor}\ \equiv 1\pmod 4\ \text{and}\ c\ \text{is not of the form}\ 5\cdot2^a.$$

**Proof.**
($\Rightarrow$) By 2.3(ii), $c$ has a prime factor $\equiv 1\pmod 4$; by the necessity in 3.4, $c\notin\{2^a\}\cup\{5\cdot2^a\}$. Since $c$ has such a prime factor it cannot be $2^a$; hence $c\notin\{5\cdot2^a\}$.

($\Leftarrow$) By 2.3(ii), $c$ is a hypotenuse; and since $c\notin\{2^a\}\cup\{5\cdot2^a\}$, the sufficiency in 3.4 (verified to 1000) gives that $c^2$ is a sum of three positive squares. $\blacksquare$

**The sole culprit is the prime 5**: $5\equiv 1\pmod 4$, so it is a legitimate hypotenuse ($3^2+4^2=5^2$), but $25=5^2$ is not a sum of three positive squares, so $5$ and all its doublings $5,10,20,40,\dots$ drop out.

【C】exact for $c\le 500$; the failures are precisely $5,10,20,40,80,160,320$.

---

## 6. Perfect cuboids

### 6.1 Definition

A cuboid with edges $a,b,c$ is a perfect cuboid when all four of the following are integers:

$$d^2=a^2+b^2,\quad e^2=a^2+c^2,\quad f^2=b^2+c^2,\quad g^2=a^2+b^2+c^2.$$

Satisfying only the first three is an **Euler brick**.

### 6.2 Equivalent form 【P】

From $f^2=b^2+c^2$,

$$g^2=a^2+b^2+c^2=a^2+f^2.$$

So **$(a,f,g)$ is also a Pythagorean triple**. A perfect cuboid is equivalently a common leg $a$ of the triples $(a,b,d)$, $(a,c,e)$, $(a,f,g)$ with $b^2+c^2=f^2$.

### 6.3 Known Euler bricks

The smallest, found by Paul Halcke in 1719:

$$(44,117,240),\qquad (d,e,f)=(125,244,267).$$

【C】23 Euler bricks with edges $\le 2000$, 7 of them primitive.

### 6.4 Necessary divisibility conditions

If a perfect cuboid exists, then:

| Condition | Status |
|---|---|
| exactly one odd edge | 【P】mod 4 |
| both even edges divisible by 4 | 【P】even leg of a primitive triple |
| two edges divisible by 3, one of them by 9 | 【L】+【C】 |
| two edges divisible by 4, one of them by 16 | 【L】+【C】 |
| one edge divisible by 5, 7, 11, 19 | 【L】 |

Caveat: **the divisibility by 7 and 19 is not satisfied by Euler bricks.** For example $(44,117,240)$ has no edge divisible by 7. These are constraints specific to perfect cuboids.

### 6.5 Search status 【L】

| Bound | Value | Source |
|---|---|---|
| smallest edge | $>5\times10^{11}$ | Matson, 2015 |
| odd edge | $>2.5\times10^{13}$ | Matson, 2015 |
| bounded fibres | all 2040 fibres with $m\le100$ excluded | Peschmann 2026 + Cipollini 2026 |

【C】no perfect cuboid with edges $\le 2000$.

### 6.6 Recent preprints (not peer-reviewed)

| Date | arXiv | Author | Content |
|---|---|---|---|
| 2026-09-29 | 2609.38650 | Asiryan | finiteness in square classes, weighted zero density |
| 2026-10-07 | 2610.10643 | Asiryan | rank condition (correcting Paulsen–West) |
| 2026-10-18 | 2610.25319 | Asiryan | irreducibility of the degree-10 cuboid polynomial |
| 2026-11-04 | 2611.10012 | Asiryan | excludes 54 of 76 factorisation patterns of the degree-12 polynomial |
| 2026-09-13 | 2609.14526 | Cipollini | eliminates Peschmann's remaining 968 fibres |

Cipollini's abstract states: *"the result is still a bounded-fiber theorem rather than a proof of the full perfect-cuboid conjecture."*

---

## 7. The 2×2 classification

### 7.1 Two coordinates

For an unordered triple $\{a,b,c\}$ let

- $k$ = the number of edge-pairs whose squares sum to a square ($k=0,1,2,3$);
- $\mathcal G$ = whether $a^2+b^2+c^2$ is a perfect square ($0$ or $1$).

| | $\mathcal G=0$ ($g$ not an integer) | $\mathcal G=1$ ($g$ an integer) |
|---|---|---|
| $k=3$ | **Euler brick** ✓ exists, infinitely many | **perfect cuboid** ✗ unknown |
| $k=2$ | belongs to no configuration (the vast majority) | **face cuboid** ✓ exists |
| $k\le1$ | none | none |

### 7.2 The four "six-of-seven" configurations

Expanding the cells $k=3,\mathcal G=0$ and $k=2,\mathcal G=1$ by labels gives four configurations:

| Configuration | Meaning | Count (edges $\le 2000$) | Primitive |
|---|---|---|---|
| `abcdef` | $d,e,f$ integers, $g$ not | 23 | 7 |
| `abcdeg` | $d,e,g$ integers, $f$ not | 11 | 6 |
| `abcdfg` | $d,f,g$ integers, $e$ not | 11 | 6 |
| `abcefg` | $e,f,g$ integers, $d$ not | 11 | 6 |

**The last three are the same set of numbers.** Each unordered triple has exactly one pair whose sum of squares is not a square; placing that pair on a given face determines the configuration. For $\{104,153,672\}$:

```
(a,b,c)=(104,153,672) -> f missing -> abcdeg   d=185 e=680 g=697
(a,b,c)=(153,104,672) -> e missing -> abcdfg   d=185 f=680 g=697
(a,b,c)=(153,672,104) -> d missing -> abcefg   e=185 f=680 g=697
```

【C】11 unordered face cuboids with edges $\le 2000$, giving $11\times2=22$ ordered solutions per configuration.

### 7.3 At most 3 of the 4 【P】【C】

**Theorem.** An unordered triple can satisfy at most 3 of the four configurations, never 4.

**Proof.** `abcdef` requires all three pairs to be Pythagorean, i.e. $k=3$; while `abcdeg`/`abcdfg`/`abcefg` each require exactly two, i.e. $k=2$. Since $k$ is label-independent, it cannot be both 3 and 2. $\blacksquare$

【C】among the 5775 triples with at least two integer face diagonals and edges $\le 1000$:

```
satisfy 0 configurations: 5760
satisfy 1 configuration :   10   <- Euler brick
satisfy 2 configurations:    0
satisfy 3 configurations:    5   <- face cuboid
satisfy 4 configurations:    0
```

**Both zeros are informative**: "2" can never occur (the three "one-face-missing" configurations hold or fail together, depending on $g$); "4" is exactly the perfect cuboid.

---

## 8. Why several "proof" strategies must fail

### 8.1 All four characteristics are consequences of a perfect cuboid 【P】

Assume a primitive perfect cuboid exists.

1. **Exactly one odd edge**: two odd edges give a sum $\equiv2\pmod4$, not a square; three even edges are not primitive.
2. **Exactly two edges divisible by 3**: squares mod 3 are $0,1$; two edges not divisible by 3 give a sum $\equiv2\pmod3$, a contradiction.
3. **At least two edges divisible by 4**: let $a$ be the unique odd edge and $b,c$ even. Put $h=\gcd(a,b)$, write $a=ha_0,\ b=hb_0,\ d=hd_0$; then $(a_0,b_0,d_0)$ is primitive. Euclid's formula gives $b_0=2mn$ with $m,n$ of opposite parity, so $4\mid b_0$, hence $4\mid b$. Likewise $4\mid c$.
4. **Three distinct edges**: if $a=b$ then $d=a\sqrt2\notin\mathbb Z$, a contradiction.

**Consequence: these four characteristics cannot exclude a perfect cuboid**—they are its own consequences.

### 8.2 Two forms of circularity

**Form 1**: "prove that the four characteristics plus the four configurations are impossible". Under the strict reading this is a tautology (`abcdef` contains $g\notin\mathbb Z$, `abcdeg` contains $g\in\mathbb Z$), and the four characteristics are never used. A perfect cuboid is a $7/7$ object, not one of the four $6/7$ objects.

**Form 2**: "prove that every cuboid has the four characteristics and is one of the four configurations". Let

- $C$ = cuboids with integer edges and integer face diagonals, $C=E\sqcup P$ ($E$ Euler bricks, $P$ perfect cuboids);
- $S$ = the set satisfying at least one of the four configurations.

Then $E\subseteq S$ and $P\cap S=\varnothing$, so

$$C\subseteq S\iff E\cup P\subseteq S\iff P\subseteq S\iff P=\varnothing.$$

**"Every cuboid belongs to the four configurations" is equivalent to "no perfect cuboid exists".** That is a circle.

### 8.3 How weak the necessary conditions are

【C】with edges $\le 400$, exactly **218,361** triples satisfy all four characteristics; only **2** of them are genuine Euler bricks:

$$(44,117,240),\qquad(240,252,275).$$

A ratio of about $9\times10^{-6}$. The four characteristics are a coarse sieve: they remove 98%, but one still has to remove 99.999% of what remains.

---

## 9. Reduction: from examples to equations

### 9.1 Equivalent form

$$g^2=a^2+f^2.$$

【C】$(44,117,240)$: $44^2+267^2=73225=g^2$; $(104,153,672)$: $104^2+f^2=485809=697^2$.

### 9.2 Normalisation: a clean four-condition form

Put $X=b/a,\ Y=c/a,\ Z=f/a$. The four conditions correspond one-to-one with four geometric quantities:

| Condition | Quantity |
|---|---|
| $\mathrm{(i)}\ X^2+Y^2=Z^2$ | face diagonal $f$ (face $bc$) |
| $\mathrm{(ii)_1}\ 1+X^2\in\mathbb Q^2$ | face diagonal $d$ (face $ab$) |
| $\mathrm{(ii)_2}\ 1+Y^2\in\mathbb Q^2$ | face diagonal $e$ (face $ac$) |
| $\mathrm{(ii)_3}\ 1+Z^2\in\mathbb Q^2$ | space diagonal $g$ |

```
( 44,117,240):  (i) yes  1+X^2=125/44 yes  1+Y^2=244/44 yes  1+Z^2 no          -> Euler brick
(104,153,672):  (i) no   1+X^2=185/104 yes 1+Y^2=680/104 yes 1+Z^2=697/104 yes -> face cuboid
(240,252,275):  (i) yes  1+X^2=348/240 yes 1+Y^2=365/240 yes 1+Z^2 no          -> Euler brick
```

Each row satisfies 3 of the 4 conditions—but a different 3.

### 9.3 Why the reduction cannot reach a curve 【P】

**Key observation**: "$1+X^2$ **has a square root**" holds automatically over $\mathbb R$ and $\mathbb C$—real and complex numbers always have square roots. What is hard is "$1+X^2$ is the square of a **rational** number".

Hence, if one only asks that $d,e,f,g$ be real (or complex), the solution set is the whole $(a,b,c)$ space (dimension 3, projectively 2), independent of the number of conditions. **"Is a perfect square" does not lower the dimension as a geometric condition**; everything hard sits in "the square root must be rational", which is not an algebraic condition.

And surfaces have no general tool for rational points—curves have Faltings (finiteness for genus $\ge2$), Chabauty–Coleman, elliptic-curve descent; surfaces have no counterpart.

### 9.4 Curves appear only after fixing a parameter

- Fix $a$: $b,c$ must satisfy $a^2+b^2=\square$, $a^2+c^2=\square$, $a^2+b^2+c^2=\square$—three conditions on two unknowns, reducing to finitely many candidates;
- Eliminating on those candidates yields elliptic curves, whose rational points **can** be decided;
- But $a$ has infinitely many values, and a slice handles one at a time. This is the shape of the bounded-fibre method in the literature, and the reason it cannot yield a universal statement.

---

## 10. Verification checklist

`scripts/verify_all.py` performs **53 checks**, all passing:

| Section | Checks | Coverage |
|---|---|---|
| 1 | 5 | $\lfloor\sqrt N\rfloor$ count, float trap, last two digits, mod 16 |
| 2 | 9 | Euclid's formula, parity/divisibility, no square legs, hypotenuse criterion, representation count |
| 3 | 10 | quadruple enumeration and structure, Lebesgue coverage, $12^4+15^4+20^4$, forbidden set to 1000 |
| 4 | 5 | only $\{1,3\}$ fail for four squares, Jacobi's formula, equal and square legs |
| 5 | 2 | the intersection theorem |
| 6 | 20 | Euler brick and face cuboid counts, the four characteristics, configuration distribution, strength of necessary conditions, divisibility by 9 and 16 |
| 7 | 2 | perfect cuboid search to 2000 |

Run:

```bash
python scripts/verify_all.py
# exit code 0 means every check passes
```

---

## 11. A note on meaning: what if it is too large to exhibit?

> This section is not mathematics; it is a reflection with a stated position. It is kept separate from the open problems in Section 12.

### 11.1 The shape of the question

If a perfect cuboid exists, then by the current searches its **odd edge** exceeds $2.5\times10^{13}$ (dimensionless; the bound on the smallest edge is $5\times10^{11}$). Such a tuple cannot be exhibited in the physical world, nor listed by any human.

So one may ask: **does "it exists" still mean anything?**

### 11.2 Three questions must be separated

| Question | Content |
|---|---|
| (a) existence | is there a positive integer solution? |
| (b) constructivity | can one write down a solution explicitly? |
| (c) meaningfulness | if the solution is too large to exhibit, for whom does "existence" mean anything? |

### 11.3 The argument "too large, therefore meaningless" does not stand

**Reason 1: largeness is not intrinsic.**

The same perfect cuboid has, in Planck lengths, a size of order $10^{13}$; in light-years, of order $10^{-3}$. Since "large" varies arbitrarily with the unit, it cannot serve as a mathematical argument. **Largeness is a property of the representation, not of the object.**

**Reason 2: mathematical meaning does not depend on physical realizability.**

There are primes larger than $10^{100}$; we cannot list them, yet "there are infinitely many primes" is a theorem. The cardinality of the continuum, non-measurable sets, non-constructive existence proofs—none can be exhibited, all are mathematically meaningful.

### 11.4 But there is a genuine version

If the issue is not merely "large" but "too large for any physical process to write down", then the statement is **epistemically** empty. That is not a mathematical problem but a problem in the theory of knowledge.

Perfect cuboids have a special structure: the problem is a $\Sigma^0_1$ statement (an existential quantifier over integers). Hence:

- if **true**, it is in principle verifiable by exhibiting a solution—"yes" is always finitely confirmable;
- if **false**, it may require a proof we do not have, and may even be independent of ZFC.

**This asymmetry is real**: "yes" has a finite witness, "no" may not.

### 11.5 A sharper observation: the value of the answer depends on its direction

If a perfect cuboid exists, heuristics suggest there may be **finitely many** (not an infinite family)—an isolated exception. Then:

- if "exists", it is a curiosity: it overturns a long-standing intuition but produces no theory;
- if "does not exist", the proof would likely require new mathematics (as FLT produced algebraic number theory).

**The two answers have asymmetric value**, and this asymmetry has nothing to do with size. This, I think, is what is genuinely interesting about the problem.

### 11.6 Three positions

| Position | Answer to (c) |
|---|---|
| Platonism | truth is independent of cognition; the problem has a definite answer, we may simply never know it. |
| Formalism | truth is relative to a formal system; "existence" is derivability of a string. |
| Intuitionism | one cannot assert existence without construction—under this view "exists but unconstructible" is itself contradictory. |

### 11.7 The position of this paper

Stated explicitly as subjective:

1. **"Too large, therefore meaningless" does not stand**—largeness is not intrinsic (11.3, Reason 1), and mathematical meaning does not depend on physical realizability (Reason 2).
2. **"Existence without knowability" is a real problem**, but it belongs to epistemology, not to mathematics. The two can coexist: mathematically there is a definite answer; epistemically we may never know it.
3. **The interesting distinction is not "large or small" but "which way the answer goes"** (11.5). An isolated example is a curiosity; a non-existence theorem might be a new discipline.

---

## 12. Open problems

1. **The essential problem**: do positive integers $a,b,c,d,e,f,g$ satisfy the four equations? (open for three centuries)
2. **The bounded problem**: the 2040 fibres with $m\le100$ are excluded; what is the next range, and can a uniform exclusion mechanism replace fibre-by-fibre work?
3. **The reduction problem**: can one find a curve that is "closed" for perfect cuboids, so that Faltings/Chabauty apply without fixing a parameter?
4. **A small question left by this paper**: the **sufficiency** direction of 3.4 ($d\notin\{2^a\}\cup\{5\cdot2^a\}$ $\Rightarrow$ $d^2$ is a sum of three positive squares) is only verified to 1000 here. Does it have a clean elementary proof?
5. **Generalising the intersection theorem**: Section 5 gives the exact intersection of the hypotenuse condition and the three-square condition. Do four terms and five terms admit analogous exact intersections?

---

## Appendix A: Reproducing

```bash
git clone <this-repo>
cd perfect-cuboid-survey
python scripts/verify_all.py      # 53 checks, exit code 0 means all pass
```

Environment: Python 3.8+, standard library only. All computations finish within minutes on an ordinary laptop.

## Appendix B: References

**Classical**

1. L. E. Dickson, *History of the Theory of Numbers*, Vol. II, Ch. IV (Euler bricks).
2. W. Sierpiński, *Pythagorean Triangles*, Dover, 2003.
3. P. Halcke (1719), discoverer of the smallest Euler brick $(44,117,240)$.

**Surveys and searches**

4. A. de Grey, P. Gibbs, L. Helm, *Novel required properties of, and efficient algorithms to seek, perfect cuboids*, arXiv:2401.06784 (2024).
5. R. D. Matson, *Results of computer search for a perfect cuboid*, unsolvedproblems.org/S58 (2015).
6. B. Butler, odd-edge search to $3\times10^{12}$ (cited in Matson).

**Recent preprints (none peer-reviewed)**

7. R. Peschmann, *A torsion-intersection proof of perfect-cuboid nonexistence on 1,072 explicit master-tuple fibers*, arXiv:2604.28072.
8. R. Peschmann, *Exponent-one blockers and a Mordell-Weil construction of Euler bricks*, arXiv:2605.00573.
9. R. Cipollini, *Elimination of René Peschmann's 968 Remaining Hard Fibers for the Perfect Cuboid Problem*, arXiv:2609.14526.
10. V. Asiryan, *Finiteness in Square Classes and Weighted Zero Density of Perfect Cuboids*, arXiv:2609.38650.
11. V. Asiryan, *On the Rank Condition for Perfect Cuboids*, arXiv:2610.10643.
12. V. Asiryan, *Irreducibility of the Cuboid Polynomial $Q_{p,q}(t)$ via the Rank-One Chabauty–Coleman Method*, arXiv:2610.25319.
13. V. Asiryan, *Excluding 54 of the 76 Nontrivial Factorization Patterns of the Cuboid Polynomial $P_{a,b,u}(t)$*, arXiv:2611.10012.

**Classical theorems**

14. J. L. Lagrange, four-square theorem (1770).
15. C. G. J. Jacobi, formula for the number of four-square representations.
16. P. Fermat, $x^4+y^4=z^2$ has no solution (infinite descent).
17. G. Faltings, Mordell conjecture (1983).
18. C. Chabauty, R. Coleman, methods for rational points on curves.

---

*This document is released under CC BY 4.0; the accompanying code under MIT.*
