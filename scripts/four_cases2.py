from math import gcd, isqrt

LIM = 2000
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

euler = set()      # 三对面角线均整数
facec = set()      # 恰两对面角线整数 + 体对角线整数

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

def diag(a, b):
    t = a * a + b * b
    r = isqrt(t)
    return r if r * r == t else None

def isprim(t):
    return gcd(gcd(t[0], t[1]), t[2]) == 1

print()
print('【abcDef 情形】Euler brick（d,e,f 整数，g 不是整数）')
print('  总计 %d 个无序三元组，其中原始 %d 个'
      % (len(euler), sum(1 for t in euler if isprim(t))))
print('  最小的 8 个：')
for t in sorted(euler, key=lambda u: (max(u), u)):
    a, b, c = t
    print('    (%4d,%4d,%4d)  d=%-5d e=%-5d f=%-5d  原始=%s'
          % (a, b, c, diag(a, b), diag(a, c), diag(b, c), isprim(t)))

print()
print('【abcdeg / abcdfg / abcefg 三情形】共享同一批无序三元组')
print('  总计 %d 个无序三元组，其中原始 %d 个'
      % (len(facec), sum(1 for t in facec if isprim(t))))
print('  全部 11 个（标出哪一对是"非平方"的面）：')
for t in sorted(facec, key=lambda u: (max(u), u)):
    a, b, c = t
    pairs = [('ab', a, b), ('ac', a, c), ('bc', b, c)]
    bad = [nm for nm, x, y in pairs if diag(x, y) is None]
    g = isqrt(a * a + b * b + c * c)
    print('    (%4d,%4d,%4d)  d=%-5s e=%-5s f=%-5s g=%-5d  非平方面=%s  原始=%s'
          % (a, b, c, diag(a, b) or '---', diag(a, c) or '---', diag(b, c) or '---',
             g, bad[0], isprim(t)))

print()
print('=== 只统计原始解的结构特点 ===')
def stats(name, lst):
    pr = [t for t in lst if isprim(t)]
    n = len(pr)
    if n == 0:
        return
    print('%s (原始解 n=%d):' % (name, n))
    print('   恰一条奇数棱      : %d/%d' % (sum(1 for t in pr if sum(1 for x in t if x % 2) == 1), n))
    print('   恰两条棱被3整除   : %d/%d' % (sum(1 for t in pr if sum(1 for x in t if x % 3 == 0) == 2), n))
    print('   至少两条棱被4整除 : %d/%d' % (sum(1 for t in pr if sum(1 for x in t if x % 4 == 0) >= 2), n))
    print('   有棱被11整除      : %d/%d' % (sum(1 for t in pr if any(x % 11 == 0 for x in t)), n))
    print('   有棱被5整除       : %d/%d' % (sum(1 for t in pr if any(x % 5 == 0 for x in t)), n))
    print('   三条棱全不同      : %d/%d' % (sum(1 for t in pr if len(set(t)) == 3), n))

stats('abcdef', euler)
stats('abcdeg/abcdfg/abcefg（同一批）', facec)
