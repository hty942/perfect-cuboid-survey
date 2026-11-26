from math import gcd, isqrt

LIM = 1500
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

bricks = []
for a in range(1, LIM + 1):
    for b in adj[a]:
        if b <= a:
            continue
        for c in adj[a] & adj[b]:
            if c > b:
                bricks.append((a, b, c))

# 按最大棱排序（尺寸意义上的从小到大）
bricks.sort(key=lambda t: (t[2], t[1], t[0]))
print('Euler brick (棱<=%d) 共 %d 个，按最大棱排序:' % (LIM, len(bricks)))
for (a, b, c) in bricks:
    d, e, f = isqrt(a*a+b*b), isqrt(a*a+c*c), isqrt(b*b+c*c)
    g2 = a*a+b*b+c*c
    g = isqrt(g2)
    tag = ' <-- 完美!' if g*g == g2 else ''
    kind = '原始' if gcd(gcd(a, b), c) == 1 else '非原始'
    print('  (%4d,%4d,%4d) 面角线 %4d %4d %4d  空间对角线 %.4f  %s%s'
          % (a, b, c, d, e, f, g2 ** 0.5, kind, tag))

prim = [t for t in bricks if gcd(gcd(t[0], t[1]), t[2]) == 1]
print()
print('原始 brick 共 %d 个，检验 Wikipedia 的三条断言:' % len(prim))
for (a, b, c) in prim:
    n3 = sum(1 for x in (a, b, c) if x % 3 == 0)
    n4 = sum(1 for x in (a, b, c) if x % 4 == 0)
    n11 = sum(1 for x in (a, b, c) if x % 11 == 0)
    print('  (%4d,%4d,%4d): 被3整除的棱数=%d  被4整除的棱数=%d  被11整除的棱数=%d'
          % (a, b, c, n3, n4, n11))

# 空间对角线若存在会有什么约束：用原始三元组斜边的性质
print()
print('完美长方体等价于四方组:')
print('  a^2+b^2+c^2 = g^2  且  g^2 = c^2+d^2 = b^2+e^2 = a^2+f^2')
print('  即 (c,d,g)、(b,e,g)、(a,f,g) 也都是勾股三元组')
