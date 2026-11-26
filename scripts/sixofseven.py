from math import gcd, isqrt
from collections import defaultdict

LIM = 1000

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

# 枚举"至少两对面角线为整数"的 (a,b,c)，a<b<c
cand = set()
for a in range(1, LIM + 1):
    L = sorted(P[a])
    for i, b in enumerate(L):
        for c in L[i + 1:]:
            cand.add(tuple(sorted((a, b, c))))

def classify(a, b, c):
    d2 = a * a + b * b
    e2 = a * a + c * c
    f2 = b * b + c * c
    g2 = d2 + c * c
    def sq(n):
        r = isqrt(n)
        return r if r * r == n else None
    return sq(d2), sq(e2), sq(f2), sq(g2)

groups = defaultdict(list)
for (a, b, c) in sorted(cand):
    d, e, f, g = classify(a, b, c)
    key = (d is not None, e is not None, f is not None, g is not None)
    groups[key].append((a, b, c, d, e, f, g))

print('棱 <= %d 的分类 (d,e,f,g 是否整数):' % LIM)
for key in sorted(groups, key=lambda k: (-sum(k), k)):
    nm = ''.join(n for n, ok in zip('defg', key) if ok)
    print('  d/e/f/g 中为整数的: %-4s  共 %5d 组   最小: %s'
          % (nm, len(groups[key]), groups[key][0][:3]))

print()
print('=== 四种目标情形的实例 ===')
names = {'abcdef': (True, True, True, False),
         'abcefg': (False, True, True, True),
         'abcdfg': (True, False, True, True),
         'abcdeg': (True, True, False, True)}
for nm, key in names.items():
    lst = sorted(groups.get(key, []), key=lambda t: (max(t[0], t[1], t[2]), t[0] * t[1] * t[2]))
    print('%s: 共 %d 组' % (nm, len(lst)))
    for row in lst[:5]:
        a, b, c, d, e, f, g = row
        print('   (%3d,%3d,%3d)  d=%-5s e=%-5s f=%-5s g=%-5s'
              % (a, b, c, d if d else '---', e if e else '---', f if f else '---', g if g else '---'))

print()
print('=== 各类型的 abc 结构特点 ===')
for nm, key in names.items():
    lst = groups.get(key, [])
    if not lst:
        continue
    prim = [t for t in lst if gcd(gcd(t[0], t[1]), t[2]) == 1]
    odd = [t for t in lst if sum(1 for x in t[:3] if x % 2) == 1]
    n3 = [t for t in lst if sum(1 for x in t[:3] if x % 3 == 0) == 2]
    n4 = [t for t in lst if sum(1 for x in t[:3] if x % 4 == 0) >= 2]
    n11 = [t for t in lst if any(x % 11 == 0 for x in t[:3])]
    print('%s: 共 %d，原始 %d，恰一奇棱 %d/%d，恰两棱被3整除 %d/%d，'
          '至少两棱被4整除 %d/%d，有棱被11整除 %d/%d'
          % (nm, len(lst), len(prim), len(odd), len(lst), len(n3), len(lst),
             len(n4), len(lst), len(n11), len(lst)))
