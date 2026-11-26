from math import gcd, isqrt
from collections import Counter

D = 80
sols = []
for a in range(1, D + 1):
    for b in range(a, D + 1):
        s2 = a * a + b * b
        if s2 + 2 * b * b > D * D:
            break
        for c in range(b, D + 1):
            s3 = s2 + c * c
            if s3 + c * c > D * D:
                break
            for e in range(c, D + 1):
                t = s3 + e * e
                if t > D * D:
                    break
                r = isqrt(t)
                if r * r == t:
                    sols.append((a, b, c, e, r))

prim = [t for t in sols if gcd(gcd(t[0], t[1]), gcd(t[2], t[3])) == 1]

# 预测 A: 恰 1 条奇腿时，三条偶腿中 ≡2 (mod 4) 的个数只能是 0,2,3 —— 不能是 1
cnt = Counter()
for t in prim:
    odd = [x for x in t[:4] if x % 2]
    even = [x for x in t[:4] if x % 2 == 0]
    if len(odd) == 1:
        cnt[sum(1 for x in even if x % 4 == 2)] += 1
print('A) 1 奇腿原始解中，偶腿里 ≡2 (mod 4) 的个数分布:', dict(sorted(cnt.items())))

# 预测 B: 4 条奇腿时，d ≡ 2 (mod 4)
four_odd = [t for t in prim if all(x % 2 for x in t[:4])]
print('B) 4 奇腿原始解 %d 组，d mod 4 的取值: %s'
      % (len(four_odd), sorted({t[4] % 4 for t in four_odd})))
print('   例:', four_odd[:4])

# 预测 C: 四条腿全为平方数的最小非平凡例
print('C) 1^4+2^4+2^4+2^4 =', 1 + 16 + 16 + 16, '= 7^2 ?', 1 + 16 + 16 + 16 == 49)

# 预测 D: 四条腿全等恒成立; k 个相等的平方数之和是平方数  <=>  k 是完全平方数
print('D) k 个 a^2 之和 = k*a^2 是平方数 <=> k 是完全平方数:',
      [k for k in range(1, 17) if isqrt(k) ** 2 == k])
