from math import gcd, isqrt

def qr(M):
    return {(x * x) % M for x in range(M)}

def solve_mod(M, p=None, want_nontrivial=False, limit=1):
    """求 a^2+b^2=d^2, a^2+c^2=e^2, b^2+c^2=f^2, a^2+b^2+c^2=g^2 (mod M)"""
    Q = qr(M)
    out = []
    for a in range(M):
        aa = a * a % M
        for b in range(M):
            if (aa + b * b) % M not in Q:
                continue
            bb = b * b % M
            for c in range(M):
                cc = c * c % M
                if (aa + cc) % M not in Q:
                    continue
                if (bb + cc) % M not in Q:
                    continue
                if (aa + bb + cc) % M not in Q:
                    continue
                if want_nontrivial and p and a % p == 0 and b % p == 0 and c % p == 0:
                    continue
                out.append((a, b, c))
                if len(out) >= limit:
                    return out
    return out

print('=== 1) 小模数下解的结构 ===')
for M in (3, 4, 5, 8):
    sols = solve_mod(M, limit=10 ** 9)
    print('mod %d: 共 %d 组 (a,b,c)' % (M, len(sols)))
    if M == 3:
        from collections import Counter
        print('   (a,b,c) 中 ≡0 的个数分布:', Counter(sum(1 for x in t if x % 3 == 0) for t in sols))
        print('   全部解:', sols)
    if M == 4:
        from collections import Counter
        print('   奇数的个数分布:', Counter(sum(1 for x in t if x % 2) for t in sols))

print()
print('=== 2) 素数幂 p^k 上是否总有"非退化"解（即 gcd(a,b,c) 不被 p 整除）===')
bad = []
for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 128, 125, 169, 121):
    M = p
    pp = p
    k = 1
    while M * p <= 200:
        M *= p
        k += 1
        pp = p
    res = solve_mod(M, p=p, want_nontrivial=True, limit=1)
    ok = len(res) > 0
    if not ok:
        bad.append((p, M))
    print('  p=%3d  M=%-4d  %s' % (p, M, ('解 ' + str(res[0])) if ok else '无解 !!'))
print()
print('在所有检验过的素数幂上都有非退化解的例外:', bad if bad else '无（一个都没有）')

print()
print('=== 3) 已知的模约束（用真实 Euler brick 核对）===')
for (a, b, c) in [(44, 117, 240), (240, 252, 275), (85, 132, 720), (140, 480, 693)]:
    print('  (%4d,%4d,%4d): 被3整除棱数=%d 被4整除棱数=%d mod 3 余 (%d,%d,%d)'
          % (a, b, c, sum(1 for x in (a, b, c) if x % 3 == 0),
             sum(1 for x in (a, b, c) if x % 4 == 0), a % 3, b % 3, c % 3))
