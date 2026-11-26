# Perfect Cuboids — a verified survey / 完美长方体：一个经计算验证的综述

> A roadmap from "a sum of perfect squares is again a perfect square" to the perfect cuboid problem, with every numerical claim backed by a runnable check.
>
> 从「若干完全平方数之和仍是完全平方数」到完美长方体问题的一条线索，所有数值断言都有可运行的验证。

**Languages / 语言**: [中文](paper-zh.md) · [English](paper-en.md)
**Verification / 验证**: [`scripts/verify_all.py`](scripts/verify_all.py) — 53 checks, exit code 0 on success

---

## What is here / 内容

| File | Description |
|---|---|
| [`paper-zh.md`](paper-zh.md) | 中文正文（含哲学注记） |
| [`paper-en.md`](paper-en.md) | English full text (with the note on meaning) |
| [`scripts/verify_all.py`](scripts/verify_all.py) | 53 checks re-deriving every number in both papers |
| [`scripts/`](scripts/) | the individual experiments, kept for reference |
| [`data/verify_output.txt`](data/verify_output.txt) | recorded output of the full run |

## The one picture / 一张图

Let $k$ be the number of edge-pairs whose squares sum to a square, and $\mathcal G$ whether $a^2+b^2+c^2$ is a perfect square.

| | $\mathcal G=0$ | $\mathcal G=1$ |
|---|---|---|
| $k=3$ | **Euler brick** — exists, infinitely many | **perfect cuboid** — unknown |
| $k=2$ | belongs to no configuration | **face cuboid** — exists |

The four "six-of-seven" configurations (`abcdef`, `abcdeg`, `abcdfg`, `abcefg`) occupy only the top-left and bottom-right cells. **A perfect cuboid satisfies none of them.** This is why "prove that the four configurations are impossible" cannot say anything about perfect cuboids.

令 $k$ 为「平方和为完全平方」的棱对数，$\mathcal G$ 为 $a^2+b^2+c^2$ 是否为完全平方。四种「六缺一」情形只占左上和右下两个格子；完美长方体落在右上角，**不属于其中任何一种**。

## Headline results / 主要结论

- **Two terms**: Euclid's formula; a hypotenuse must have a prime factor $\equiv 1 \pmod 4$; two summands can never both be fourth powers (Fermat).
  - 两项：欧几里得公式；斜边须含 $\equiv 1 \pmod 4$ 素因子；两加数不可能同时是四次方。
- **Three terms**: the four-square identity; a primitive quadruple has exactly one odd leg, odd hypotenuse, and two even legs congruent mod 4. Forbidden diagonals: $\{2^a\}\cup\{5\cdot2^a\}$ — proved necessary, verified sufficient to $d\le 1000$.
  - 三项：四平方恒等式；原始解恰一奇腿、斜边为奇、两偶腿模 4 同余；斜边禁区 $\{2^a\}\cup\{5\cdot2^a\}$。
- **All three legs can be fourth powers**: $12^4+15^4+20^4=481^2$ — the opposite of the two-term case.
  - 三条腿可以同时是四次方，与两项情形相反。
- **Four terms**: Lagrange collapses the constraints; only $d=1,3$ fail.
  - 四项：拉格朗日让约束崩塌，只剩 $d=1,3$。
- **Intersection**: a number is both a hypotenuse and has a square that is a sum of three positive squares **iff** it has a prime factor $\equiv 1 \pmod 4$ and is not of the form $5\cdot 2^a$.
  - 交集：唯一的分歧族是 $5\cdot 2^a$，祸首是素数 5。
- **Four characteristics are consequences**: every primitive perfect cuboid must satisfy them, so they cannot exclude one.
  - 四个特点全部是完美长方体的推论，因此排除不了它。
- **No dimension reduction**: over $\mathbb R$ the four conditions are vacuous, so the solution set is a surface, not a curve.
  - 「是完全平方」在几何上不降维，解簇永远是曲面。

## Reproduce / 复现

```bash
python scripts/verify_all.py
```

Python 3.8+, standard library only. Runtime: a couple of minutes.

## Scope and honesty / 范围与诚实

This is a **survey**, not new research. Nothing here resolves the perfect cuboid problem. Every claim is tagged:

- **【P】** complete proof given
- **【C】** verified by computation, with the range stated
- **【L】** quoted from the literature

本文是综述，不解决完美长方体问题。所有结论按【证】【检】【献】标注。

## License

Text: CC BY 4.0 · Code: MIT
