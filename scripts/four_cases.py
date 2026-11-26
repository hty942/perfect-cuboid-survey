from math import isqrt
from collections import defaultdict, Counter

LIM = 2000

# P[x] = {y : x^2 + y^2 是完全平方}
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
print('LIM =', LIM, ' 邻接表建好')

cases = defaultdict(list)
euler = set()

for v in range(1, LIM + 1):
    L = sorted(P[v])
    for i, x in enumerate(L):
        for y in L[i + 1:]:
            xy = (y in P[x])            # b-c 是否勾股对
            g2 = v * v + x * x + y * y
            g = isqrt(g2)
            gsq = (g * g == g2)
            if xy:
                euler.add(tuple(sorted((v, x, y))))
            elif gsq:
                # 恰两对勾股 + 体对角线为整数。共享顶点放在哪个位置，就对应哪个情形
                cases['abcdeg'].append((v, x, y, g))   # 共享顶点在 a：ab、ac 勾股
                cases['abcdeg'].append((v, y, x, g))
                cases['abcdfg'].append((x, v, y, g))   # 共享顶点在 b：ab、bc 勾股
                cases['abcdfg'].append((y, v, x, g))
                cases['abcefg'].append((x, y, v, g))   # 共享顶点在 c：ac、bc 勾股
                cases['abcefg'].append((y, x, v, g))

print()
for name in ('abcdef', 'abcdeg', 'abcdfg', 'abcefg'):
    if name == 'abcdef':
        lst = [tuple(t) + (None,) for t in sorted(euler)]
    else:
        lst = cases[name]
    lst = sorted(lst, key=lambda t: (max(t[:3]), t[0], t[1], t[2]))
    print('%s: 共 %d 组' % (name, len(lst)))
    for t in lst[:4]:
        a, b, c, g = t
        d = isqrt(a * a + b * b)
        e = isqrt(a * a + c * c)
        f = isqrt(b * b + c * c)
        dd = d if d * d == a * a + b * b else None
        ee = e if e * e == a * a + c * c else None
        ff = f if f * f == b * b + c * c else None
        print('    (%4d,%4d,%4d)  d=%-5s e=%-5s f=%-5s g=%-5s'
              % (a, b, c, dd if dd else '---', ee if ee else '---',
                 ff if ff else '---', g if g else '---'))

print()
print('=== 逐位置统计（每个位置上是奇数/被4整除/被3整除/被11整除的比例）===')
for name in ('abcdef', 'abcdeg', 'abcdfg', 'abcefg'):
    if name == 'abcdef':
        lst = [tuple(t) + (None,) for t in sorted(euler)]
    else:
        lst = cases[name]
    n = len(lst)
    print('%s  (n=%d):' % (name, n))
    for pos, idx in (('a', 0), ('b', 1), ('c', 2)):
        odd = sum(1 for t in lst if t[idx] % 2 == 1)
        d4 = sum(1 for t in lst if t[idx] % 4 == 0)
        d3 = sum(1 for t in lst if t[idx] % 3 == 0)
        d11 = sum(1 for t in lst if t[idx] % 11 == 0)
        print('   %s: 奇数 %-8s 被4整除 %-8s 被3整除 %-8s 被11整除 %-8s'
              % (pos, '%d/%d' % (odd, n), '%d/%d' % (d4, n),
                 '%d/%d' % (d3, n), '%d/%d' % (d11, n)))
    for label, fn in (('恰一条奇数棱', lambda t: sum(1 for x in t[:3] if x % 2) == 1),
                      ('恰两条棱被3整除', lambda t: sum(1 for x in t[:3] if x % 3 == 0) == 2),
                      ('至少两条棱被4整除', lambda t: sum(1 for x in t[:3] if x % 4 == 0) >= 2),
                      ('有棱被11整除', lambda t: any(x % 11 == 0 for x in t[:3]))):
        print('   %s: %d/%d' % (label, sum(1 for t in lst if fn(t)), n))
