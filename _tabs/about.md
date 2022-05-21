---
title: About
icon: fas fa-info-circle
order: 4
---

<!-- > Add Markdown syntax content to file `_tabs/about.md`{: .filepath } and it will show up on this page.
{: .prompt-tip } -->

## Why I made this website

I made this website as the following reasons:

* I'm studying for a [**cyber security**](https://infosec.sjtu.edu.cn/index.aspx) master degree at **Shanghai Jiao Tong University**.
* I'm a novice CTF player at [**Ph0t1n1a**](https://ctftime.org/team/55197/).
* I'm interseted at **Reverse Engineering** and **Program Analysis**.
* I have a poor computer science foundation, and want to **PUSH** myself.

## Resume

I host my resume on [**Reactive Resume**](https://rxresu.me/cascades/resume-en).

## Want more info

Just solve a simple RSA[^1] problem and you will get my qq number.

```python
from Crypto.Util.number import *
from myself import qq

p, q = getPrime(32), getPrime(32)
n, phi = p*q, (p-1)*(q-1)
e = 0x10001
d = pow(e, -1, phi)
enc = pow(qq, e, n)
assert n == 6303039709899593443
assert enc == 2865907171382757979
```

[^1]: https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/
