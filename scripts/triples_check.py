from math import gcd, isqrt

LIM = 2000

prim = []
for m in range(2, isqrt(LIM) + 2):
    for n in range(1, m):
        if (m - n) % 2 == 1 and gcd(m, n) == 1:
            prim.append((m * m - n * n, 2 * m * n, m * m + n * n))

allt = set()
for a in range(1, LIM):
    for b in range(a + 1, LIM):
        s = a * a + b * b
        c = isqrt(s)
        if c <= LIM and c * c == s:
            allt.add((a, b, c))

gen = set()
for (a, b, c) in prim:
    k = 1
    while k * c <= LIM:
        x, y = a * k, b * k
        gen.add((min(x, y), max(x, y), c * k))
        k += 1

print("c<=%d: brute=%d formula=%d identical=%s" % (LIM, len(allt), len(gen), allt == gen))

primset = {(min(a, b), max(a, b), c) for (a, b, c) in prim if c <= LIM}
print("primitive triples with c<=%d: %d" % (LIM, len(primset)))

# 修正：先挑出偶数腿，再判断它 mod 4
bad4 = [t for t in primset if (t[0] if t[0] % 2 == 0 else t[1]) % 4 != 0]
print("  偶数腿不被4整除的:", bad4[:5])

# 奇数腿平方 mod 8，偶数腿平方 mod 16，斜边平方 mod 8
print("  奇数腿^2 % 8 的取值:", sorted({(t[0] if t[0] % 2 else t[1]) ** 2 % 8 for t in primset}))
print("  偶数腿^2 % 16 的取值:", sorted({(t[0] if t[0] % 2 == 0 else t[1]) ** 2 % 16 for t in primset}))
print("  c^2 % 8 的取值:", sorted({t[2] ** 2 % 8 for t in primset}))
print("  c % 4 的取值:", sorted({t[2] % 4 for t in primset}))

# 两腿同时为完全平方数？
both = [t for t in allt if isqrt(t[0]) ** 2 == t[0] and isqrt(t[1]) ** 2 == t[1]]
print("两腿同时为平方数的三元组 (c<=%d): %s" % (LIM, both))

# 斜边判定：n 是某三元组斜边  <=>  n 有素因子 ≡ 1 (mod 4)
def smallest_prime_factor_1mod4(n):
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            if p % 4 == 1:
                return True
            while x % p == 0:
                x //= p
        p += 1
    return x > 1 and x % 4 == 1

hyp = {c for (_, _, c) in allt}
mismatch = [n for n in range(1, LIM + 1) if (n in hyp) != smallest_prime_factor_1mod4(n)]
print("斜边判定不符的 n (<= %d): %s" % (LIM, mismatch[:10]), "共", len(mismatch))
