from math import isqrt
from itertools import permutations
from collections import Counter

LIM = 1000
P = {}
for x in range(1, LIM + 1):
    S = set()
    for y in range(1, LIM + 1):
        if x == y:
            continue
        t = x * x + y * y
        r = isqrt(t)
        if r * r == t:
            S.add(y)
    P[x] = S
print('LIM =', LIM)

# 所有"至少两对面角线为整数"的无序三元组
triples = set()
for v in range(1, LIM + 1):
    L = sorted(P[v])
    for i, x in enumerate(L):
        for y in L[i + 1:]:
            triples.add(tuple(sorted((v, x, y))))
print('至少两对面角线为整数的三元组:', len(triples))

def satisfied(a, b, c):
    d = isqrt(a * a + b * b); ds = d * d == a * a + b * b
    e = isqrt(a * a + c * c); es = e * e == a * a + c * c
    f = isqrt(b * b + c * c); fs = f * f == b * b + c * c
    g = isqrt(a * a + b * b + c * c); gs = g * g == a * a + b * b + c * c
    out = set()
    if ds and es and fs: out.add('abcdef')
    if ds and es and gs: out.add('abcdeg')
    if ds and fs and gs: out.add('abcdfg')
    if es and fs and gs: out.add('abcefg')
    return out

cnt = Counter()
sample = {}
for t in triples:
    s = set()
    for perm in permutations(t):
        s |= satisfied(*perm)
    cnt[len(s)] += 1
    sample.setdefault(len(s), (t, sorted(s)))

print()
print('同一个 abc（允许重新摆长宽高）能同时满足的情形个数：')
for k in sorted(cnt):
    t, names = sample[k]
    print('  满足 %d 种: %5d 组   例 %s -> %s' % (k, cnt[k], t, names))

print()
print('四种情形能被同一组数同时满足的组数:', cnt.get(4, 0))
print()
print('示范：一组数如何用三种摆法满足三种情形')
a, b, c = 104, 153, 672
for perm in sorted(set(permutations((104, 153, 672)))):
    s = satisfied(*perm)
    if s:
        x, y, z = perm
        d = isqrt(x * x + y * y); e = isqrt(x * x + z * z); f = isqrt(y * y + z * z)
        g = isqrt(x * x + y * y + z * z)
        print('   (a,b,c)=%-16s d=%-4s e=%-4s f=%-4s g=%-4s -> %s'
              % (str(perm), d if d * d == x * x + y * y else '---',
                 e if e * e == x * x + z * z else '---',
                 f if f * f == y * y + z * z else '---',
                 g if g * g == x * x + y * y + z * z else '---', sorted(s)))
