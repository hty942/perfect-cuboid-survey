from math import gcd, isqrt

LIM = 1500

# 邻接表: a -> {b : a^2 + b^2 是完全平方}
adj = {}
for a in range(1, LIM + 1):
    s = set()
    for b in range(1, LIM + 1):
        if a == b:
            continue
        t = a * a + b * b
        r = isqrt(t)
        if r * r == t:
            s.add(b)
    adj[a] = s

# Euler brick: 三对面角线都是整数
bricks = []
for a in range(1, LIM + 1):
    for b in adj[a]:
        if b <= a:
            continue
        for c in adj[a] & adj[b]:
            if c > b:
                bricks.append((a, b, c))

print('1) Euler brick (棱 <= %d): %d 个' % (LIM, len(bricks)))
print('   最小 8 个:', bricks[:8])

# 空间对角线
perfect = []
for (a, b, c) in bricks:
    t = a * a + b * b + c * c
    g = isqrt(t)
    if g * g == t:
        perfect.append((a, b, c, g))
print('2) 完美长方体:', perfect if perfect else '一个都没有')

# 结构检查
prim = [t for t in bricks if gcd(gcd(t[0], t[1]), t[2]) == 1]
print('3) 原始 Euler brick: %d 个' % len(prim))
print('   非"恰一条奇棱"的:', [t for t in bricks if sum(1 for x in t if x % 2) != 1][:4])
print('   原始 brick 中两条偶棱不都被 4 整除的:',
      [t for t in prim if sorted(x % 4 for x in t if x % 2 == 0) != [0, 0]][:4])
print('   原始 brick 中两条偶棱不都被 16 整除的例子:',
      [t for t in prim if sorted(x for x in t if x % 2 == 0)[0] % 16 != 0][:3])

# 奇棱的整除性
odd_vals = [x for t in prim for x in t if x % 2 == 1]
print('4) 原始 brick 的奇棱: 最小 %d, 前 12 个 %s' % (min(odd_vals), sorted(odd_vals)[:12]))

# 各素数是否至少整除一条棱
for p in (3, 5, 7, 11, 13, 17):
    n = sum(1 for t in prim if any(x % p == 0 for x in t))
    print('   素数 %2d 至少整除一条棱: %d/%d' % (p, n, len(prim)))

# 三对面角线的结构
print('5) 面角线示例:')
for (a, b, c) in bricks[:5]:
    d = isqrt(a * a + b * b)
    e = isqrt(a * a + c * c)
    f = isqrt(b * b + c * c)
    g = isqrt(a * a + b * b + c * c)
    print('   (%3d,%3d,%3d) 面角线 %3d %3d %3d  空间对角线 sqrt(%d) ≈ %.4f'
          % (a, b, c, d, e, f, a * a + b * b + c * c, (a * a + b * b + c * c) ** 0.5))
