from math import gcd, isqrt

# ============ 读法一：同一组平方数，a^2+b^2=s^2 且 s^2+c^2=d^2 ============
LIM = 60
triples = []
for a in range(1, LIM + 1):
    for b in range(a, LIM + 1):
        s = isqrt(a * a + b * b)
        if s <= LIM and s * s == a * a + b * b and a < b:
            triples.append((a, b, s))

chains = set()
for (a, b, s) in triples:
    for (x, y, t) in triples:
        if x == s and y != s:
            chains.add((a, b, y, t))
        elif y == s and x != s:
            chains.add((a, b, x, t))
print('1) 勾股链 (a,b,c,d) 满足 a^2+b^2=s^2 且 s^2+c^2=d^2')
print('   最小 6 组:', sorted(chains)[:6])
print('   总数 (s<=%d): %d' % (LIM, len(chains)))

# 万能延伸公式
print('2) 万能延伸: 任意斜边 s 都能当腿')
for s in (5, 10, 13, 17, 25):
    if s % 2 == 1:
        c, d = (s * s - 1) // 2, (s * s + 1) // 2
    else:
        c, d = s * s // 4 - 1, s * s // 4 + 1
    ok = s * s + c * c == d * d
    print('   s=%-3d -> c=%-5d d=%-5d  校验 %s' % (s, c, d, ok))

# ============ 读法二：同一个数 N=c^2 兼作两种"斜边" ============
def is_hypot_triple(c):
    for a in range(1, c):
        b2 = c * c - a * a
        b = isqrt(b2)
        if b * b == b2 and b > 0 and a < b:
            return True
    return False

def is_hypot_quad(c):
    for x in range(1, c):
        for y in range(x, c):
            z2 = c * c - x * x - y * y
            if z2 <= 0:
                break
            z = isqrt(z2)
            if z * z == z2 and z >= y:
                return True
    return False

def has_p1mod4(n):
    x, p = n, 2
    while p * p <= x:
        if x % p == 0:
            if p % 4 == 1:
                return True
            while x % p == 0:
                x //= p
        p += 1
    return x > 1 and x % 4 == 1

def is_5pow2(n):
    while n % 2 == 0:
        n //= 2
    return n == 5

CLIM = 200
both, only2, only3, neither = [], [], [], []
for c in range(2, CLIM + 1):
    t2, t3 = is_hypot_triple(c), is_hypot_quad(c)
    if t2 and t3:
        both.append(c)
    elif t2:
        only2.append(c)
    elif t3:
        only3.append(c)
    else:
        neither.append(c)

print('3) c<=%d 同时是三元组斜边和四元组斜边的 c:' % CLIM)
print('   ', both)
print('   只有三元组有解但四元组无解的 c:', only2)
print('   预测(有 1 mod 4 素因子 且 不是 5*2^k):',
      [c for c in range(2, CLIM + 1) if has_p1mod4(c) and not is_5pow2(c)] == both)
print('   其中 5*2^k 家族的成员:', [c for c in range(2, CLIM + 1) if is_5pow2(c)])
