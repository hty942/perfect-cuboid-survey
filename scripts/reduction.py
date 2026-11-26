from math import isqrt, gcd

def sq(n):
    if n < 0:
        return None
    r = isqrt(n)
    return r if r * r == n else None

print('=== 第 1 步：等价改写 ===')
print('原始:  d^2=a^2+b^2, e^2=a^2+c^2, f^2=b^2+c^2, g^2=a^2+b^2+c^2')
print('改写:  由 f^2=b^2+c^2 得  g^2 = a^2 + f^2')
print('       即 (a,f,g) 也是勾股三元组 —— 三条腿 a,b,c 各自与另两条组成三元组\n')

for (a, b, c) in [(44, 117, 240), (104, 153, 672), (240, 252, 275)]:
    d, e, f, g = sq(a*a+b*b), sq(a*a+c*c), sq(b*b+c*c), sq(a*a+b*b+c*c)
    rhs = a*a + (f*f if f else b*b+c*c)
    print('  (%3d,%3d,%3d):' % (a, b, c))
    print('     a^2+f^2 = %d + %s = %d' % (a*a, f*f if f else b*b+c*c, rhs))
    print('     g^2     = %d   ->  恒等式 %s' % (a*a+b*b+c*c, rhs == a*a+b*b+c*c))

print()
print('=== 第 2 步：归一化 (g=1) —— 把"平方"条件写成"1+平方=平方" ===')
print('令 X=b/a, Y=c/a, Z=f/a。要证的是:')
print('  (i)  X^2 + Y^2 = Z^2')
print('  (ii) 1+X^2, 1+Y^2, 1+Z^2 全是有理数平方\n')

from fractions import Fraction as F
for (a, b, c) in [(44, 117, 240), (104, 153, 672), (240, 252, 275)]:
    print('  (%3d,%3d,%3d):' % (a, b, c))
    bc = sq(b * b + c * c)
    print('     条件(i)  X^2+Y^2 = Z^2   <=>  b^2+c^2 是平方: %s'
          % (('是 %d，Z = %d/%d = %s' % (bc, bc, a, F(bc, a))) if bc else '不是，Z 无定义(无理)'))
    for nm, val in (('1+X^2', a * a + b * b), ('1+Y^2', a * a + c * c), ('1+Z^2', a * a + b * b + c * c)):
        r = sq(val)
        print('     条件(ii) %-6s = (%d)/a^2  -> %s'
              % (nm, val, ('平方，等于 %d/%d' % (r, a)) if r else '不是平方'))

print()
print('=== 第 3 步：为什么归约到不了"曲线" ===')
print('对任意实数 (a,b,c)，d=sqrt(a^2+b^2) 等总是实数 —— 几何上零障碍。')
import random
random.seed(1)
print('  随机抽查 5 组实数 (a,b,c)，四个平方根全部存在:')
for _ in range(5):
    a, b, c = (round(random.uniform(1, 100) * 7) / 7 for _ in range(3))
    vals = [a*a+b*b, a*a+c*c, b*b+c*c, a*a+b*b+c*c]
    print('     (%.3f,%.3f,%.3f) -> sqrt 分别 = %.4f %.4f %.4f %.4f'
          % (a, b, c, vals[0] ** .5, vals[1] ** .5, vals[2] ** .5, vals[3] ** .5))
print('  实解簇 = 整个 (a,b,c) 空间，维数 3（射影 2）—— 与"条件"的个数无关。')
print('  => "是完全平方"这一条件在几何上不降维，解簇永远是曲面，降不到曲线。')

print()
print('=== 第 4 步：Euler brick 上 h=a^2+b^2+c^2 离平方有多远 ===')
LIM = 1500
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
bricks = set()
for v in range(1, LIM + 1):
    L = sorted(P[v])
    for i, x in enumerate(L):
        for y in L[i + 1:]:
            if y in P[x]:
                bricks.add(tuple(sorted((v, x, y))))
bricks = sorted(bricks, key=lambda t: (t[2], t[0]))
print('  Euler brick (棱<=%d) 共 %d 个，h 与最近平方的距离:' % (LIM, len(bricks)))
best = []
for (a, b, c) in bricks:
    h = a*a + b*b + c*c
    r = isqrt(h)
    best.append((min(h - r*r, (r+1)*(r+1) - h), a, b, c, h))
best.sort()
for gap, a, b, c, h in best[:6]:
    print('     (%4d,%4d,%4d) h=%d  sqrt=%.6f  距最近平方 %d' % (a, b, c, h, h ** .5, gap))
print('  最小距离 = %d （=0 就是完美长方体）' % best[0][0])
