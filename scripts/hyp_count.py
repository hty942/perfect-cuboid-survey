from math import isqrt
from collections import Counter

LIM = 3000
cnt = Counter()
for a in range(1, LIM):
    for b in range(a + 1, LIM):
        s = a * a + b * b
        c = isqrt(s)
        if c <= LIM and c * c == s:
            cnt[c] += 1


def formula(n):
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


bad = [n for n in range(1, LIM + 1) if cnt.get(n, 0) != formula(n)]
print('count-formula counterexamples (n<=%d): %s  total=%d' % (LIM, bad[:10], len(bad)))
print('hottest hypotenuses:', cnt.most_common(4))
for n in (5, 15, 25, 65, 325, 1105, 5525):
    print('  n=%-5d brute=%-3d formula=%d' % (n, cnt.get(n, 0), formula(n)))
