from math import isqrt

N = 400

# 前四个特点蕴含：恰一条奇数棱 + 至少两条被 4 整除
# => 两条偶棱必须都被 4 整除。于是只需枚举 (4的倍数, 4的倍数, 奇数)
E = list(range(4, N + 1, 4))
O = list(range(1, N + 1, 2))

def sq(n):
    r = isqrt(n)
    return r if r * r == n else None

cands = []
for i, e1 in enumerate(E):
    for e2 in E[i:]:
        for o in O:
            t = tuple(sorted((e1, e2, o)))
            if t[0] == t[1] or t[1] == t[2]:
                continue                      # 三条棱互不相同
            if sum(1 for x in t if x % 3 == 0) != 2:
                continue                      # 恰两条棱被 3 整除
            cands.append(t)

cands.sort()
print('棱 <= %d 时，满足前四个特点的三元组共 %d 个' % (N, len(cands)))
print('最小的 6 个:', cands[:6])

# 其中有多少真正构成前面四种情形
euler, facec, two = [], [], 0
for t in cands:
    a, b, c = t
    d, e, f = sq(a * a + b * b), sq(a * a + c * c), sq(b * b + c * c)
    g = sq(a * a + b * b + c * c)
    nface = sum(1 for x in (d, e, f) if x)
    if nface == 3 and not g:
        euler.append(t)
    elif nface == 2 and g:
        facec.append(t)
    elif nface <= 1:
        two += 1

print()
print('  其中构成 abcdef（三面对角线整数）  : %d 个  %s' % (len(euler), euler[:4]))
print('  其中构成 abcdeg/abcdfg/abcefg 之一 : %d 个  %s' % (len(facec), facec[:4]))
print('  什么都不是（最多一条面对角线）     : %d 个' % two)
print('  检验：%d + %d + %d = %d' % (len(euler), len(facec), two, len(cands)))

print()
print('最小的三个"符合前四个特点却不构成任何情形"的例子：')
shown = 0
for t in cands:
    a, b, c = t
    d, e, f = sq(a * a + b * b), sq(a * a + c * c), sq(b * b + c * c)
    g = sq(a * a + b * b + c * c)
    nface = sum(1 for x in (d, e, f) if x)
    if nface <= 1:
        print('   (%3d,%3d,%3d)  d=%-4s e=%-4s f=%-4s g=%-4s  7个距离中整数个数=%d'
              % (a, b, c, d or '---', e or '---', f or '---', g or '---',
                 nface + (1 if g else 0) + 3))
        shown += 1
        if shown == 3:
            break
