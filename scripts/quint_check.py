from math import gcd, isqrt
from collections import Counter

D = 80

# --- 1) 枚举 a <= b <= c <= e, 四平方和 = d^2 ---
sols = []
for a in range(1, D + 1):
    for b in range(a, D + 1):
        s2 = a * a + b * b
        if s2 + 2 * b * b > D * D:
            break
        for c in range(b, D + 1):
            s3 = s2 + c * c
            if s3 + c * c > D * D:
                break
            for e in range(c, D + 1):
                t = s3 + e * e
                if t > D * D:
                    break
                r = isqrt(t)
                if r * r == t:
                    sols.append((a, b, c, e, r))

print('1) 解的总数 (d<=%d): %d' % (D, len(sols)))
print('   最小 6 组:', sols[:6])

prim = [t for t in sols if gcd(gcd(t[0], t[1]), gcd(t[2], t[3])) == 1 and t[4] > 0]
print('   原始解: %d 组' % len(prim))

# --- 2) 原始解中奇数腿的个数分布 / d 的奇偶 ---
print('2) 原始解中奇数腿个数分布:', Counter(sum(1 for x in t[:4] if x % 2) for t in prim))
print('   d 的奇偶分布:', Counter(t[4] % 2 for t in prim))
print('   四腿全奇的例子:', [t for t in prim if all(x % 2 for x in t[:4])][:4])
print('   四腿全偶的例子:', [t for t in sols if all(x % 2 == 0 for x in t[:4])][:3])

# --- 3) 哪些 d 无解(要求四条腿均为正) ---
have = {t[4] for t in sols}
print('3) d<=%d 中无解的 d:' % D, [d for d in range(1, D + 1) if d not in have])

# --- 4) 四条腿能否同时是完全平方数: x^4+y^4+z^4+w^4 = d^2 ---
hits = []
for x in range(1, 46):
    for y in range(x, 46):
        for z in range(y, 46):
            s = x ** 4 + y ** 4 + z ** 4
            for w in range(z, 46):
                t = s + w ** 4
                r = isqrt(t)
                if r * r == t:
                    hits.append((x, y, z, w, r))
print('4) x^4+y^4+z^4+w^4=d^2 (各<=45):', hits[:5], '共', len(hits))

# --- 5) 四腿全相等 ---
print('5) 4a^2 = (2a)^2 恒成立 ->', [(a, 2 * a) for a in (1, 2, 3)])

# --- 6) 雅可比四平方定理: r4(n) = 8 * sum{d | n, 4∤d} d ---
MAXD = 30
r2 = Counter()
for z in range(-MAXD, MAXD + 1):
    for w in range(-MAXD, MAXD + 1):
        r2[z * z + w * w] += 1

def jacobi(n):
    return 8 * sum(k for k in range(1, n + 1) if n % k == 0 and k % 4 != 0)

bad = []
for d in range(1, MAXD + 1):
    brute = 0
    for x in range(-d, d + 1):
        for y in range(-d, d + 1):
            brute += r2.get(d * d - x * x - y * y, 0)
    if brute != jacobi(d * d):
        bad.append((d, brute, jacobi(d * d)))
print('6) r4(d^2) 与雅可比公式不符的 d:', bad)
print('   例: r4(5^2) =', jacobi(25), ' r4(13^2) =', jacobi(169), ' r4(25^2) =', jacobi(625))

# --- 7) 三腿互不相同的最小解 ---
print('7) 四腿互不相同的最小解:', [t for t in sols if len(set(t[:4])) == 4][:4])
