from math import gcd, isqrt

LIM = 200

# --- 1) 暴力枚举 a <= b <= c 的所有解 ---
sols = []
for a in range(1, LIM + 1):
    for b in range(a, LIM + 1):
        s = a * a + b * b
        for c in range(b, LIM + 1):
            t = s + c * c
            d = isqrt(t)
            if d <= LIM and d * d == t:
                sols.append((a, b, c, d))

print('solutions with d<=%d: %d' % (LIM, len(sols)))
print('  smallest 8:', sols[:8])
print('  three distinct legs, smallest:', [t for t in sols if len(set(t[:3])) == 3][:5])

# --- 2) 原始解的结构 ---
prim = [t for t in sols if gcd(gcd(t[0], t[1]), gcd(t[2], t[3])) == 1]
print('primitive solutions: %d' % len(prim))
print('  奇数腿个数不为1的:', [t for t in prim if sum(1 for x in t[:3] if x % 2) != 1][:5])
print('  d 为偶数的:', [t for t in prim if t[3] % 2 == 0][:5])
print('  两条偶腿 mod 4 不同的:', [t for t in prim
      if len({x % 4 for x in t[:3] if x % 2 == 0}) != 1][:5])
print('  三腿全为奇数的:', [t for t in sols if all(x % 2 for x in t[:3])][:5])
print('  三腿全为偶数的:', [t for t in sols if all(x % 2 == 0 for x in t[:3])][:3])

# --- 3) 哪些 d 能当斜边(三条腿均正) ---
have = {t[3] for t in sols}
missing = [d for d in range(1, 121) if d not in have]
print('d<=120 中无解的 d:', missing)

# --- 4) 勒贝格恒等式是否覆盖全部原始解 ---
def lebesgue(Amax):
    out = set()
    for A in range(1, Amax + 1):
        for B in range(1, Amax + 1):
            for C in range(1, Amax + 1):
                for D in range(1, Amax + 1):
                    d = A * A + B * B + C * C + D * D
                    legs = sorted((abs(A * A + B * B - C * C - D * D),
                                   abs(2 * A * C - 2 * B * D),
                                   abs(2 * A * D + 2 * B * C)))
                    if legs[0] > 0 and legs[0] ** 2 + legs[1] ** 2 + legs[2] ** 2 == d * d:
                        out.add((legs[0], legs[1], legs[2], d))
    return out

LIM2 = 60
gen = lebesgue(9)
brute = {t for t in prim if t[3] <= LIM2}
print('primitive d<=%d: brute=%d  covered-by-Lebesgue=%d  missing=%s'
      % (LIM2, len(brute), len(brute & gen), sorted(brute - gen)[:6]))

# --- 5) 三条腿能否同时是完全平方数 (a^4+b^4+c^4 = d^2) ---
hits = []
for a in range(1, 61):
    for b in range(a, 61):
        for c in range(b, 61):
            t = a ** 4 + b ** 4 + c ** 4
            r = isqrt(t)
            if r * r == t:
                hits.append((a, b, c, r))
print('a^4+b^4+c^4 = d^2 的小解 (a,b,c<=60):', hits)

# --- 6) 三腿相等不可能 ---
print('3a^2 = d^2 有解吗:', [d for d in range(1, 500) if (3 * d * d) % 1 == 0 and isqrt(3 * d * d) ** 2 == 3 * d * d and False] or '无 (sqrt(3) 无理)')
