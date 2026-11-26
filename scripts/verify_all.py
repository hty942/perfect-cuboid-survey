#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py — re-derive every numeric claim in the accompanying article.

Run:  python verify_all.py
Every line prints PASS / FAIL.  Exit code is 0 iff all checks pass.

Requires only the Python standard library (3.8+).
"""

from math import gcd, isqrt
from collections import Counter

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond)))
    tag = "PASS " if cond else "FAIL "
    print(tag + name + (("   [" + detail + "]") if detail else ""))


def sq(n):
    if n < 0:
        return None
    r = isqrt(n)
    return r if r * r == n else None


# ---------------------------------------------------------------- section 1
print("=" * 78)
print("SECTION 1  perfect squares")
print("=" * 78)

# 1.1 count of squares in [1,N] is floor(sqrt(N))
ok = True
for N in range(1, 20001):
    cnt = sum(1 for k in range(1, isqrt(N) + 1) if k * k <= N)
    if cnt != isqrt(N):
        ok = False
        break
check("1.1  count of positive squares <= N equals floor(sqrt(N)), N<=20000", ok)

# 1.2 float sqrt fails for large n
N = 10 ** 32 - 1
check("1.2  isqrt(10^32-1) == 10^16-1", isqrt(N) == 10 ** 16 - 1, str(isqrt(N)))
try:
    import math
    bad = int(math.sqrt(N)) != isqrt(N)
    check("1.2b float sqrt gives the wrong floor for 10^32-1", bad,
          "int(sqrt)=%d" % int(math.sqrt(N)))
except Exception as e:
    print("      (float check skipped: %s)" % e)

# 1.3 last-two-digit set has exactly 22 members
last2 = {k * k % 100 for k in range(100)}
check("1.3  exactly 22 possible last-two-digit patterns", len(last2) == 22, str(len(last2)))

# 1.4 squares mod 16 in {0,1,4,9}
check("1.4  squares mod 16 in {0,1,4,9}", {k * k % 16 for k in range(16)} == {0, 1, 4, 9})


# ---------------------------------------------------------------- build P
print()
print("=" * 78)
print("SECTION 2  two squares (Pythagorean triples), c <= 2000")
print("=" * 78)

LIM = 2000
P = {}
for x in range(1, LIM + 1):
    S = set()
    for y in range(1, LIM + 1):
        if x != y:
            t = x * x + y * y
            r = isqrt(t)
            if r * r == t:
                S.add(y)
    P[x] = S
print("      (adjacency table built, %d vertices)" % LIM)

# 2.1 brute force count vs Euclid parametrisation
brute = set()
for a in range(1, LIM):
    for b in range(a + 1, LIM):
        s = a * a + b * b
        c = isqrt(s)
        if c <= LIM and c * c == s:
            brute.add((a, b, c))

gen = set()
for m in range(2, isqrt(LIM) + 2):
    for n in range(1, m):
        if (m - n) % 2 == 0 or gcd(m, n) != 1:
            continue
        base = (m * m - n * n, 2 * m * n, m * m + n * n)
        k = 1
        while k * base[2] <= LIM:
            a, b, c = base[0] * k, base[1] * k, base[2] * k
            gen.add((min(a, b), max(a, b), c))
            k += 1
check("2.1  Euclid formula reproduces all triples with c<=2000", brute == gen,
      "brute=%d formula=%d" % (len(brute), len(gen)))

prim_triples = sorted(t for t in gen if gcd(gcd(t[0], t[1]), t[2]) == 1)
check("2.1b number of primitives with c<=2000", len(prim_triples) == 319, str(len(prim_triples)))

# 2.2 parity / divisibility structure of primitive triples
bad_even4 = bad3 = bad5 = badpar = 0
for (a, b, c) in prim_triples:
    ev = b if a % 2 else a
    if ev % 4 != 0:
        bad_even4 += 1
    if sum(1 for x in (a, b) if x % 3 == 0) != 1:
        bad3 += 1
    if sum(1 for x in (a, b, c) if x % 5 == 0) != 1:
        bad5 += 1
    if (a % 2) == (b % 2):
        badpar += 1
check("2.2  even leg of a primitive triple is divisible by 4", bad_even4 == 0)
check("2.3  exactly one leg divisible by 3", bad3 == 0)
check("2.4  exactly one of a,b,c divisible by 5", bad5 == 0)
check("2.5  the two legs have different parity", badpar == 0)

# 2.6 no triple with both legs perfect squares
both = [t for t in brute if sq(t[0]) and sq(t[1])]
check("2.6  no triple has two square legs, c<=2000", both == [])

# 2.7 hypotenuse criterion
def has_p1mod4(n):
    x, p = n, 2
    while p * p <= x:
        if x % p == 0:
            if p % 4 == 1:
                return True
            while x % p == 0:
                x //= p
        p += 1
    return x > 1 and x % 4 == 1

hyp = {c for (_, _, c) in brute}
mismatch = [n for n in range(1, LIM + 1) if (n in hyp) != has_p1mod4(n)]
check("2.7  n is a hypotenuse iff n has a prime factor = 1 mod 4, n<=2000", mismatch == [],
      "mismatches=%d" % len(mismatch))

# 2.8 number of representations of c
def reps_formula(n):
    x, prod, p = n, 1, 2
    while p * p <= x:
        if x % p == 0:
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            if p % 4 == 1:
                prod *= 2 * e + 1
        p += 1
    if x > 1 and x % 4 == 1:
        prod *= 3
    return (prod - 1) // 2

cnt = Counter(c for (_, _, c) in brute)
bad = [n for n in range(1, LIM + 1) if cnt.get(n, 0) != reps_formula(n)]
check("2.8  number of triples with hypotenuse c matches the divisor formula", bad == [],
      "counterexamples=%d" % len(bad))


# ---------------------------------------------------------------- section 3
print()
print("=" * 78)
print("SECTION 3  three squares (Pythagorean quadruples)")
print("=" * 78)

# 3.1 enumerate a<=b<=c with a^2+b^2+c^2=d^2, d<=200
D = 200
quads = []
for a in range(1, D + 1):
    for b in range(a, D + 1):
        s2 = a * a + b * b
        # c >= b, so the smallest possible total is a^2 + 2*b^2
        if s2 + b * b > D * D:
            break
        for c in range(b, D + 1):
            t = s2 + c * c
            if t > D * D:
                break
            r = isqrt(t)
            if r * r == t:
                quads.append((a, b, c, r))
print("      (enumeration done, %d solutions with d<=%d)" % (len(quads), D))

prim_q = [t for t in quads if gcd(gcd(t[0], t[1]), gcd(t[2], t[3])) == 1]
check("3.1  quadruple solutions with d<=200", len(quads) == 2255, str(len(quads)))
check("3.2  primitive quadruples with d<=200", len(prim_q) == 1364, str(len(prim_q)))
check("3.3  in a primitive quadruple exactly one leg is odd",
      all(sum(1 for x in t[:3] if x % 2) == 1 for t in prim_q))
check("3.4  in a primitive quadruple d is odd",
      all(t[3] % 2 == 1 for t in prim_q))
check("3.5  the two even legs are congruent mod 4",
      all(len({x % 4 for x in t[:3] if x % 2 == 0}) == 1 for t in prim_q))

# 3.6 Lebesgue identity covers all primitive quadruples with d<=60
def lebesgue(Amax):
    out = set()
    rng = range(0, Amax + 1)
    for A in rng:
        for B in rng:
            for C in rng:
                for E in rng:
                    d = A * A + B * B + C * C + E * E
                    if d == 0:
                        continue
                    legs = sorted((abs(A * A + B * B - C * C - E * E),
                                   abs(2 * A * C - 2 * B * E),
                                   abs(2 * A * E + 2 * B * C)))
                    if legs[0] > 0 and sum(x * x for x in legs) == d * d:
                        out.add((legs[0], legs[1], legs[2], d))
    return out

gen_q = lebesgue(8)
prim_q60 = {t for t in prim_q if t[3] <= 60}
check("3.6  Lebesgue identity covers every primitive quadruple with d<=60",
      prim_q60 <= gen_q, "primitive=%d covered=%d" % (len(prim_q60), len(prim_q60 & gen_q)))

# 3.7 12^4+15^4+20^4 = 481^2
check("3.7  12^4+15^4+20^4 = 481^2", 12**4 + 15**4 + 20**4 == 481**2)

# 3.8 the family 1+(2k)^2+(2k^2)^2 = (2k^2+1)^2
check("3.8  1+(2k)^2+(2k^2)^2=(2k^2+1)^2 for k=1..50",
      all(1 + (2*k)**2 + (2*k*k)**2 == (2*k*k+1)**2 for k in range(1, 51)))

# 3.9 three-term forbidden set, d <= 1000
# fast version: d^2 = a^2+b^2+c^2  <=>  d^2 - c^2 is a sum of two positive squares
DT = 1000
two_sq = bytearray(DT * DT + 1)
for a in range(1, DT + 1):
    a2 = a * a
    if a2 + 1 > DT * DT:
        break
    for b in range(a, DT + 1):
        t = a2 + b * b
        if t > DT * DT:
            break
        two_sq[t] = 1

have = set()
for d in range(1, DT + 1):
    d2 = d * d
    for c in range(1, d):
        rem = d2 - c * c
        if rem < 2:
            break
        if two_sq[rem]:
            have.add(d)
            break

def forbidden3(d):
    while d % 2 == 0:
        d //= 2
    return d == 1 or d == 5

missing = [d for d in range(1, DT + 1) if d not in have]
pred = [d for d in range(1, DT + 1) if forbidden3(d)]
check("3.9  for d<=1000, d^2 is a sum of three positive squares iff d not in {2^a} U {5*2^a}",
      missing == pred, "missing=%d predicted=%d" % (len(missing), len(pred)))
check("3.9b the forbidden list up to 1000 is exactly 1,2,4,5,8,10,16,20,32,40,64,80,128,160,256,320,512,640",
      missing == [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 64, 80, 128, 160, 256, 320, 512, 640])


# ---------------------------------------------------------------- section 4
print()
print("=" * 78)
print("SECTION 4  four squares")
print("=" * 78)

# 4.1 which d are NOT sums of four positive squares, d <= 120
# fast version: d^2 = a^2+b^2+c^2+e^2  <=>  d^2 - a^2 is a sum of three positive squares
D4 = 120
three_sq = bytearray(D4 * D4 + 1)
for a in range(1, D4 + 1):
    a2 = a * a
    if a2 + 2 > D4 * D4:
        break
    for b in range(a, D4 + 1):
        s = a2 + b * b
        if s + 1 > D4 * D4:
            break
        for c in range(b, D4 + 1):
            t = s + c * c
            if t > D4 * D4:
                break
            three_sq[t] = 1

have4 = set()
for d in range(1, D4 + 1):
    d2 = d * d
    for a in range(1, d):
        rem = d2 - a * a
        if rem < 3:
            break
        if three_sq[rem]:
            have4.add(d)
            break
miss4 = [d for d in range(1, D4 + 1) if d not in have4]
check("4.1  for d<=120 only d=1 and d=3 fail to be a sum of four positive squares",
      miss4 == [1, 3], str(miss4))

# 4.2 Jacobi four-square theorem
MAXD = 30
r2 = Counter()
for z in range(-MAXD, MAXD + 1):
    for w in range(-MAXD, MAXD + 1):
        r2[z * z + w * w] += 1

def jacobi(n):
    return 8 * sum(k for k in range(1, n + 1) if n % k == 0 and k % 4 != 0)

bad = []
for d in range(1, MAXD + 1):
    brute_n = 0
    for x in range(-d, d + 1):
        for y in range(-d, d + 1):
            brute_n += r2.get(d * d - x * x - y * y, 0)
    if brute_n != jacobi(d * d):
        bad.append(d)
check("4.2  r4(d^2) = 8*sum{m | d^2, 4 does not divide m}, d<=30", bad == [], str(bad))

# 4.3 four equal squares
check("4.3  4a^2=(2a)^2 for a=1..20", all(4 * a * a == (2 * a) ** 2 for a in range(1, 21)))
check("4.4  k equal squares sum to a square iff k is a perfect square, k<=20",
      [k for k in range(1, 21) if sq(k)] == [1, 4, 9, 16])

# 4.5 four legs all perfect squares: 1^4+2^4+2^4+2^4 = 7^2
check("4.5  1^4+2^4+2^4+2^4 = 7^2", 1 + 16 + 16 + 16 == 49)


# ---------------------------------------------------------------- section 5
print()
print("=" * 78)
print("SECTION 5  the intersection of the two- and three-square conditions")
print("=" * 78)

def is_5pow2(n):
    while n % 2 == 0:
        n //= 2
    return n == 5

CLIM = 500
both_ok = True
exceptions = []
for c in range(2, CLIM + 1):
    t2 = c in hyp
    t3 = (c in have) if c <= DT else None   # c <= 500 < 1000, so 'have' is valid
    if t3 is None:
        continue
    pred2 = has_p1mod4(c) and not is_5pow2(c)
    if (t2 and t3) != pred2:
        both_ok = False
        exceptions.append(c)
check("5.1  c<=500: (hypotenuse and sum of three positive squares) iff "
      "(prime 1 mod 4 and c not of the form 5*2^a)", both_ok, str(exceptions[:8]))
only2 = [c for c in range(2, CLIM + 1) if c in hyp and c not in have]
check("5.2  the only c<=500 that is a hypotenuse but not a three-square sum are 5*2^a",
      all(c in (5, 10, 20, 40, 80, 160, 320) for c in only2), str(only2))


# ---------------------------------------------------------------- section 6
print()
print("=" * 78)
print("SECTION 6  Euler bricks and the four 6-of-7 cases, edges <= 2000")
print("=" * 78)

euler = set()
facec = set()
for v in range(1, LIM + 1):
    L = sorted(P[v])
    for i, x in enumerate(L):
        for y in L[i + 1:]:
            xy = (y in P[x])
            g2 = v * v + x * x + y * y
            g = isqrt(g2)
            gsq = (g * g == g2)
            if xy:
                euler.add(tuple(sorted((v, x, y))))
            elif gsq:
                facec.add(tuple(sorted((v, x, y))))

check("6.1  Euler bricks with edges <= 2000", len(euler) == 23, str(len(euler)))
check("6.2  primitive Euler bricks with edges <= 2000",
      sum(1 for t in euler if gcd(gcd(t[0], t[1]), t[2]) == 1) == 7)
check("6.3  face cuboids (exactly two face diagonals + space diagonal), edges <= 2000",
      len(facec) == 11, str(len(facec)))
check("6.4  primitive face cuboids", sum(1 for t in facec if gcd(gcd(t[0], t[1]), t[2]) == 1) == 6)
check("6.5  no perfect cuboid among them",
      not any(sq(t[0] * t[0] + t[1] * t[1] + t[2] * t[2]) for t in euler))

# 6.6 the four characteristics on primitive Euler bricks
prim_e = [t for t in euler if gcd(gcd(t[0], t[1]), t[2]) == 1]
check("6.6  every primitive Euler brick has exactly one odd edge",
      all(sum(1 for x in t if x % 2) == 1 for t in prim_e))
check("6.7  every primitive Euler brick has exactly two edges divisible by 3",
      all(sum(1 for x in t if x % 3 == 0) == 2 for t in prim_e))
check("6.8  every primitive Euler brick has at least two edges divisible by 4",
      all(sum(1 for x in t if x % 4 == 0) >= 2 for t in prim_e))
check("6.9  every primitive Euler brick has three distinct edges",
      all(len(set(t)) == 3 for t in prim_e))
check("6.19 every primitive Euler brick has an edge divisible by 9",
      all(any(x % 9 == 0 for x in t) for t in prim_e))
check("6.20 every primitive Euler brick has an edge divisible by 16",
      all(any(x % 16 == 0 for x in t) for t in prim_e))
check("6.10 every primitive Euler brick has an edge divisible by 11",
      all(any(x % 11 == 0 for x in t) for t in prim_e))
check("6.11 every primitive Euler brick has an edge divisible by 5",
      all(any(x % 5 == 0 for x in t) for t in prim_e))

# 6.12 primitive face cuboids: 11-divisibility is NOT universal
prim_f = [t for t in facec if gcd(gcd(t[0], t[1]), t[2]) == 1]
n11 = sum(1 for t in prim_f if any(x % 11 == 0 for x in t))
n5 = sum(1 for t in prim_f if any(x % 5 == 0 for x in t))
check("6.12 primitive face cuboids with an edge divisible by 11 is 4 of 6", (n11, len(prim_f)) == (4, 6),
      "%d/%d" % (n11, len(prim_f)))
check("6.13 primitive face cuboids with an edge divisible by 5 is 5 of 6", (n5, len(prim_f)) == (5, 6),
      "%d/%d" % (n5, len(prim_f)))

# 6.14 at most 3 of the four cases per unordered triple
LIM1000 = 1000
P1000 = {}
for x in range(1, LIM1000 + 1):
    S = set()
    for y in range(1, LIM1000 + 1):
        if x != y:
            t = x * x + y * y
            r = isqrt(t)
            if r * r == t:
                S.add(y)
    P1000[x] = S

triples2 = set()
for v in range(1, LIM1000 + 1):
    L = sorted(P1000[v])
    for i, x in enumerate(L):
        for y in L[i + 1:]:
            triples2.add(tuple(sorted((v, x, y))))

def satisfied(a, b, c):
    D_ = sq(a * a + b * b)
    E_ = sq(a * a + c * c)
    F_ = sq(b * b + c * c)
    G_ = sq(a * a + b * b + c * c)
    out = set()
    if D_ and E_ and F_:
        out.add("abcdef")
    if D_ and E_ and G_:
        out.add("abcdeg")
    if D_ and F_ and G_:
        out.add("abcdfg")
    if E_ and F_ and G_:
        out.add("abcefg")
    return out

from itertools import permutations as _perm
dist = Counter()
for t in triples2:
    s = set()
    for p in _perm(t):
        s |= satisfied(*p)
    dist[len(s)] += 1
check("6.14 at least two face diagonals integer, edges<=1000: total 5775", len(triples2) == 5775,
      str(len(triples2)))
check("6.15 distribution of how many of the four cases a triple can satisfy",
      dict(dist) == {0: 5760, 1: 10, 3: 5}, str(dict(dist)))
check("6.16 no triple satisfies all four cases", dist.get(4, 0) == 0)

# 6.17 necessary conditions are weak: edges <= 400
N400 = 400
cnt4 = 0
cands = []
E4 = list(range(4, N400 + 1, 4))
O4 = list(range(1, N400 + 1, 2))
for i, e1 in enumerate(E4):
    for e2 in E4[i:]:
        for o in O4:
            t = tuple(sorted((e1, e2, o)))
            if len(set(t)) < 3:
                continue
            if sum(1 for x in t if x % 3 == 0) != 2:
                continue
            cnt4 += 1
            cands.append(t)
check("6.17 triples with edges <= 400 satisfying the four characteristics", cnt4 == 218361, str(cnt4))

euler400 = [t for t in cands
            if all(sq(x * x + y * y) for x, y in ((t[0], t[1]), (t[0], t[2]), (t[1], t[2])))
            and not sq(t[0]**2 + t[1]**2 + t[2]**2)]
check("6.18 of those, only 2 are Euler bricks", len(euler400) == 2, str(sorted(euler400)))


# ---------------------------------------------------------------- section 7
print()
print("=" * 78)
print("SECTION 7  perfect cuboid search, edges <= 2000")
print("=" * 78)

perfect = [t for t in euler
           if sq(t[0]**2 + t[1]**2 + t[2]**2)]
check("7.1  no perfect cuboid with all edges <= 2000", perfect == [], str(perfect))
check("7.2  smallest Euler brick is (44,117,240)", sorted(euler, key=lambda t: (t[2], t[1], t[0]))[0] == (44, 117, 240))


# ---------------------------------------------------------------- summary
print()
print("=" * 78)
fails = [n for (n, ok) in RESULTS if not ok]
print("TOTAL %d checks, %d passed, %d failed" % (len(RESULTS), len(RESULTS) - len(fails), len(fails)))
if fails:
    print("FAILED:")
    for f in fails:
        print("  - " + f)
print("=" * 78)
raise SystemExit(1 if fails else 0)
