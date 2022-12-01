---
# the default layout is 'page'
icon: fas fa-info-circle
order: 5
---

<!-- > Add Markdown syntax content to file `_tabs/about.md`{: .filepath } and it will show up on this page.
{: .prompt-tip } -->

## Brief intro

* I've obtained bachelor degree in information security from [Shanghai Jiao Tong University](https://www.sjtu.edu.cn)
* I'm studying for a [cyber security](https://infosec.sjtu.edu.cn/index.aspx) master degree at [Shanghai Jiao Tong University](https://www.sjtu.edu.cn)
* I'm a novice CTF player at [Ph0t1n1a](https://ctftime.org/team/55197/), which is the junior team of [0ops](https://ctftime.org/team/4419)
* I'm interseted in [Software Reverse Engineering](https://en.wikipedia.org/wiki/Reverse_engineering#Software) and [Static Program Analysis](https://en.wikipedia.org/wiki/Program_analysis#Static_program_analysis)
* I have a poor computer science foundation, and want to **PUSH** myself

## Resume

I host my resume on [Reactive Resume](https://rxresu.me/cascades/resume-en), which supports continuous update & publish.

## Blog

I write blogs about scientific research and computer security skills, which is hosted on [GitHub Pages](https://github.com/cascades-sjtu/cascades-sjtu.github.io).

## Want more info

Just solve a simple RSA[^1] problem and you will get my qq number!

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
