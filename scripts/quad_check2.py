from math import gcd, isqrt

# --- A) 勒贝格恒等式：允许参数为 0，看覆盖是否完整 ---
def lebesgue(Amax):
    out = set()
    rng = range(0, Amax + 1)
    for A in rng:
        for B in rng:
            for C in rng:
                for D in rng:
                    d = A * A + B * B + C * C + D * D
                    if d == 0:
                        continue
                    legs = sorted((abs(A * A + B * B - C * C - D * D),
                                   abs(2 * A * C - 2 * B * D),
                                   abs(2 * A * D + 2 * B * C)))
                    if legs[0] > 0 and sum(x * x for x in legs) == d * d:
                        out.add((legs[0], legs[1], legs[2], d))
    return out

LIM = 60
sols = []
for a in range(1, LIM + 1):
    for b in range(a, LIM + 1):
        s = a * a + b * b
        for c in range(b, LIM + 1):
            t = s + c * c
            d = isqrt(t)
            if d <= LIM and d * d == t:
                sols.append((a, b, c, d))
prim = {t for t in sols if gcd(gcd(t[0], t[1]), gcd(t[2], t[3])) == 1}

gen = lebesgue(8)
print('A) primitive d<=%d: brute=%d  Lebesgue(params>=0)=%d  missing=%s'
      % (LIM, len(prim), len(prim & gen), sorted(prim - gen)[:8]))

# --- B) 哪些 d 无解，范围拉大到 400 ---
LIM3 = 400
have = set()
for a in range(1, LIM3 + 1):
    for b in range(a, LIM3 + 1):
        s = a * a + b * b
        if s + b * b > LIM3 * LIM3:
            break
        for c in range(b, LIM3 + 1):
            t = s + c * c
            if t > LIM3 * LIM3:
                break
            d = isqrt(t)
            if d * d == t:
                have.add(d)

def is_forbidden(d):
    while d % 2 == 0:
        d //= 2
    return d == 1 or d == 5

missing = [d for d in range(1, LIM3 + 1) if not (d in have)]
pred = [d for d in range(1, LIM3 + 1) if is_forbidden(d)]
print('B) d<=%d 无解的 d: %s' % (LIM3, missing))
print('   与 {2^a} ∪ {5*2^a} 一致:', missing == pred)

# --- C) 三条腿同时是完全平方数：a^4+b^4+c^4 = d^2 ---
hits = []
for a in range(1, 151):
    for b in range(a, 151):
        for c in range(b, 151):
            t = a ** 4 + b ** 4 + c ** 4
            r = isqrt(t)
            if r * r == t:
                hits.append((a, b, c, r))
print('C) a^4+b^4+c^4=d^2 (a,b,c<=150):', hits[:6], '共', len(hits))
if hits:
    a, b, c, d = hits[0]
    print('   检验: %d^2 + %d^2 + %d^2 = %d^2 ?' % (a*a, b*b, c*c, d),
          a*a**0 == a*a**0 and (a*a)**2 + (b*b)**2 + (c*c)**2 == d*d)

# --- D) 腿含 1 的无穷族 ---
print('D) 1 + (2k)^2 + (2k^2)^2 = (2k^2+1)^2 验证 k=1..6:',
      all(1 + (2*k)**2 + (2*k*k)**2 == (2*k*k+1)**2 for k in range(1, 7)))

# --- E) 原始解中两偶腿 mod 4 同余：证明性检查已做，这里扩大到 d<=400 ---
bad = 0
for (a, b, c, d) in [(x, y, z, w) for x in range(1, 120) for y in range(x, 120)
                     for z in range(y, 120) for w in [isqrt(x*x+y*y+z*z)]
                     if w*w == x*x + y*y + z*z and w <= 400
                     and gcd(gcd(x, y), gcd(z, w)) == 1]:
    ev = [v % 4 for v in (a, b, c) if v % 2 == 0]
    if len(set(ev)) != 1 or sum(1 for v in (a, b, c) if v % 2) != 1 or d % 2 == 0:
        bad += 1
print('E) d<=400 原始解结构违例数:', bad)
