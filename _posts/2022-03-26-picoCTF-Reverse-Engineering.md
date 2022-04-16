---
title: picoCTF writeup for RE
category: [writeup, OJ] 
tags: [revserse]
---

> 前段时间花了3-4天打了CMU举办的picoCTF 2022，发现这个比赛相比于国内的CTF比赛来说题目阶梯性更好，范围更广，也更加让人感兴趣（可能是因为题目简单容易拿flag）。于是打算刷一下picoCTF的其他题目，也都是往期picoCTF的题目合集，希望能提高自己的逆向能力。之后也可以考虑考虑刷刷其他的入门级CTF题库，比如Reversing.Kr和一些国内的平台。

## picoCTF 2022

先附上结果，Pwn和Re的最后两道题不会做，之后好好看看；Misc和Crypto通过Google以后都能做出来；Web就图一乐好了。

![picoCTF2022.png](https://s2.loli.net/2022/03/26/InVg3qtfeyNJMLT.jpg)

言归正传，开始picoCTF的刷题之旅吧～

## Wizard Like

首先是一道没做出来的Re：

<https://github.com/elemental-unicorn/picoctf-2022/tree/master/reverse_eng/wizard-like>

## Transformation

将原ASCII字符串，两个字符一组，通过移位方式组成一个新的unicode字符并写入文件。反向上述操作即可，需要熟悉python的字符操作。

```python
with open('enc','r') as f:
    enc = f.read()
    flag = ''
    for c in enc:
        flag += chr(ord(c) >> 8)
        flag += chr(ord(c) - ((ord(c) >> 8) << 8))
```

一个有趣的地方在于，原文件是按字符而不是字节写入的。如果使用`'rb'`方式读取后直接`chr()`字符值会报错，是因为unicode的字符范围为0-0x10ffff。但Unicode超过ASCII的部分不是直接和二进制数值对应的，会有[二次编码](https://en.wikipedia.org/wiki/UTF-8)，实际的二进制值是超过0x10ffff的。比如，'灩'.encode() != ord('灩')。

## keygenme-py

看起来比较复杂的一个python菜单程序，如果顺序分析会比较麻烦（而且很多单词都看不懂）。其实大致逻辑就是需要crack这个用fernet加密的python程序，通过逆向分析jump_into_full这个标志变量的调用关系，可以得到破解的流程为：menu_trial->enter_license->check_key。正确的key即为flag，至于这个破解后的python程序怎么运行其实和题目关系不大，可以用作本地验证flag。

重点分析check_key，其首先检查了flag长度是否为程序头部定义的三个部分之和，随后检查固定的第一部分`"picoCTF{1n_7h3_|<3y_of_"`。随后检查第二部分，将其与用户名的sha256值按照打乱的顺序比较，通过即可。

```python
from hashlib import sha256
username_trial = "ANDERSON"
order = [4,5,3,6,2,7,1,8]
flag = ""
# python3中需要先encode
username_trial_hash = sha256(username_trial.encode()).hexdigest()
for i in order:
    flag += username_trial_hash[i]
flag = "picoCTF{1n_7h3_|<3y_of_{}}".format(flag)
```

## crackme-py

提供了两个函数，choose_greastest只是简单地返回用户输入两个数的最大值，似乎没用到decode_secret。然而程序头部的提示它将一个重要的数值加密并隐藏在了程序里面。其实只需要对bezos_cc_secret调用解密函数即可，是一个ROT47的解密函数。

```python
decode_secret(bezos_cc_secret)
```

## shop

题目是Go语言写的，函数表很丰富，但Ghidra的逆向效果不太好，插件都只适合老版本的Ghidra。
分析menu函数的关键逻辑，没有对购买数量的符号做检查，或者说没有在重新计算coins时使用绝对值，导致可以通过购买负数个商品来获得coins，达到购买flag需要的coins。

```python
from pwn import *

context(arch="i386", os="linux", log_level="debug")
host = "mercury.picoctf.net"
port = 24851

p = remote(host, port)

p.recvuntil(b"Choose an option: \n")
p.sendline(b"0")
p.recvline()
# not check sign, cause under flow
p.sendline(b"-6")

# get flag
p.recvuntil(b"Choose an option: \n")
p.sendline(b"2")
p.recvline()
p.sendline(b"1")

recv = p.recv().decode()
flag = recv[recv.find("[") + 1 : recv.find("]")].split(" ")
flag = "".join([chr(int(c)) for c in flag])
```

## Hurry up! Wait

* 初步动态分析：一开始以为是一个PE文件，结果是ELF。先跑一下程序（需要按照libgnat-7.so.1），输入后没有反应。
* 静态分析：
  * 分析程序类型：在Ghidra里面查看，函数表很丰富。按照函数名称排序，发现有一系列`ada`开头的函数。使用strings分析，也可以发现`GNAT Version: 7.5.0`这样的字符串。通过Google发现这是一个叫做[Ada](https://zh.wikipedia.org/zh-hans/Ada)的语言，采用[GNAT](https://www.adacore.com)进行编译。可以自己编译一个[简单的Hello-world程序](https://riptutorial.com/ada)，发现其入口点为entry。
  * 分析程序功能：定位到entry函数，并进入`0x00101fcc`。发现在`__gnat_initialize`和`gnat_finalize`之间有三个功能函数。通过查看call trees，可以简单看出第一个函数是负责初始化的。而第二个函数`0x0010298a`比较特别，只调用了`ada__calendar__delays__delay_for`这一个库函数，这个库函数实现了sleep的效果。还有其他27个自定义的函数。这27个自定义的函数功能几乎一样，都调用了`Ada.Text_IO.put`，且第二个参数都一样，为0x1。查看APi发现，第一个参数为要打印的字符，第二个参数即stdout。而去第一个参数的位置查看，出现了"picoCTF{}"等字符。
  * 可以直接手动查看27个函数的调用位置，恢复出flag。
* 动态调试：可以直接通过gdb的jump命令绕过`ada__calendar__delays__delay_for`函数。不过函数的实际执行地址是不确定的，而且由于被stripped了，只能先断在这个函数，然后绕过更加底层的`system.os_primitives.timed_delay`，即可打印出flag。

![](https://s2.loli.net/2022/03/30/gkjvwCWnUi1NHP4.png){: width="90%" height="90%" .mx-auto.d-block :}

```shell
(gdb) b ada__calendar__delays__delay_for
(gdb) r
(gdb) jump *0x7ffff796c360
```

## gogo

* 初步动态分析：需要验证输入的password。
* 静态分析：
  * Go语言写的，第一个检查逻辑在checkPassword。可以看到有32bytes的可打印字符写在了栈上。首先对输入长度做检查，随后将输入逐位与栈上`$esp-0x40`处长为0x20的字符串异或，再将结果与栈上`$esp-0x20`处长为0x20的字符串比较。
  * 随后需要经过ambush的检查，main提示需要输入hash前的数值，并将用户输入传递给ambush。ambush首先将输入转化为bytes数组，经过md5后与栈上的字符串比较。
* 动态分析：
  * 程序在运行的时候开了5个轻量级进程LWP（Go并发编程的特点），会影响调试的顺序，最好使用`ni`和`si`来调试。
  * 在checkPassword里比较的代码`0x080d4b21`处下断点，通过`x /8x $esp-0x20`拿到栈上的值，利用异或的性质解出原输入。
  * 提取出ambush中的md5sum值，通过破解网站得到unhash value。

```python
# get checkPassword's input
from Crypto.Util.number import long_to_bytes

bsrc = [
    0x38313638,
    0x31663633,
    0x64336533,
    0x64373236,
    0x37336166,
    0x62646235,
    0x39383338,
    0x65343132,
]
bdst = [
    0x5D47534A,
    0x54034541,
    0x0A5A025D,
    0x0D455753,
    0x555D0005,
    0x0E011054,
    0x4B575541,
    0x01465045,
]
bsrc = b"".join[[long_to_bytes(b](::-1) for b in bsrc])
bdst = b"".join[[long_to_bytes(b](::-1) for b in bdst])
password = b"".join([(bsrc[i] ^ bdst[i]).to_bytes(1, "big") for i in range(len(bsrc))])

# get ambush's input
# look up bsrc on <https://crackstation.net> or just google it to get the unhashed value
print(bsrc)

# get_flag
from pwn import *

context(arch="i386", os="linux", log_level="debug")
host = "mercury.picoctf.net"
port = 4052

p = remote(host, port)
p.recvuntil(b"Enter Password: ")
p.sendline(password)
p.recvuntil(b"What is the unhashed key?\n")
p.sendline(b"goldfish")
p.recv()
```

## Let's get dynamic

需要分析出这段汇编代码读取的内容，提示在调试器里面运行。看起来.LC0存储了一些8进制的unicode字符，所以动态分析比较好。需要在x86_64的机器里面将汇编编译成可执行文件。

```bash
gcc -c chall.s -o chall.o
gcc chall.o -o chall
```

先进行静态分析，main函数首先把.LC0段的数据借助rax和rdx存放到栈上，每次8字节。随后再将一部分硬编码的数据存放到栈上。此时，`rbp-0x90`到`rbp-0x20`都是已经填入的数据。随后通过fgets读入0x31字节的变量，经过循环之后，调用memcmp函数。

动态调试后，随意输入都会显示flag正确，有点奇怪。在memcpy前下断点，查看参数发现一部分flag，但长度只有0x12。之前调用的strlen，发现其返回结果为0x12，所以猜测strlen决定了memcmp第二个参数的长度。所以需要hook`strlen`的返回值，即可打印完整的flag。

有几种hook的方法，包括修改strlen返回值，或者直接在汇编代码中修改。考虑到这里strlen在循环中被调用了多次，所以直接修改汇编代码更加方便。进行如下修改，再查看memcmp的参数即可。

```bash
# call strlen@PLT
movq $49, %rax # AT&T format
```

ps：可以使用ltrace来追踪运行时调用的库函数

## not crypto

给了二进制文件，提示虽然它虽然是包括密码学操作的，但不是一个密码学的题目，所以题目的关键应该不是分析加密逻辑。
随机输入，发现密码错误，猜测需要输入正确的flag。发现有memcmp函数，直接下断点去找参数即可。用Ubuntu-18.04会有问题，不知道为啥。

```bash
b memcmp
run
x /s $rdi
```

## Easy as GDB

提示需要爆破，可以使用gdb-python。需要输入正确的flag才能通过检测。最后的检测是逐位与数据段的字符数组比较，考虑爆破。
需要在`000108c4`函数内部爆破，所以需要定位到爆破的位置，逐位爆破。通过继承gdb.Breakpoint类，来统计一次运行中比较的次数，在爆破某一位时，如果某个输入的比较次数比其他输入都多1，则说明当前字符爆破成功。

```python
import gdb
import string
from queue import Queue, Empty

MAX_FLAG_LEN = 200
COMPARE_LOC = "*0x5655598e"
PASS_LOC = "*0x56555a72"
ALPHABET = string.ascii_letters + string.digits + '{}_'


class ComparePoint(gdb.Breakpoint):
    def __init__(self, req_hit, queue, *args) -> None:
        super().__init__(*args)
        self.silent = True
        self.hit = 0
        self.req_hit = req_hit
        self.queue = queue

    def stop(self):
        self.hit += 1
        if self.hit == self.req_hit:
            al = gdb.parse_and_eval("$al")
            bl = gdb.parse_and_eval("$dl")
            self.queue.put(al == bl)
        return False


class PassPoint(gdb.Breakpoint):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.silent = True
        self.hit = 0

    def stop(self):
        self.hit += 1
        return False


queue = Queue()
gdb.execute("set disable-randomization on")
gdb.execute("delete")
pp = PassPoint(PASS_LOC)
flag = ""

for i in range(1, MAX_FLAG_LEN):
    for c in ALPHABET:
        cp = ComparePoint(i, queue, COMPARE_LOC)
        print("bruting with " + flag + c)
        gdb.execute("run <<< " + flag + c)
        try:
            res = queue.get(timeout=1)
            cp.delete()
            if res:
                flag += c
                print("\ncurrent flag is {}\n".format(flag))
                break
        except Empty:
            gdb.execute("q")

    if pp.hit:
        print("flag found: {}".format(flag))
        gdb.execute("q")
```

* 用python扩展gdb：<https://segmentfault.com/a/1190000005718889>
* 官方文档：<https://sourceware.org/gdb/current/onlinedocs/gdb/Python-API.html>

## reverse_cipher

在main函数里打开两个文件，从flag.txt中读取0x18字节的数据，并在"picoCTF{xxx}"的中间部分进行编码操作，将结果写入到rev_this。
根据rev_this的值逆向出flag.txt即可。

```python
rev_flag = open('rev_this','r').read()
for i in range(8,23):
    if i & 0x1:
            flag += chr(ord(rev_flag[i])+2)
    else:
            flag += chr(ord(rev_flag[i])-5)
```

## OTP Implementation

## asm

x86系列逆向题目

### asm1

给定asm1函数参数，需要获取输出。人工分析跳转即可，或者也可以采用unicorn来执行。

```python
arg = 0x2e0
flag = arg - 0xa
```

### asm2

分析给定asm2函数两个参数，获取输出。需要分析好参数位置。

```python
arg1,arg2 = 0x4,0x2d
while arg1 < 0x5fa1:
    arg2 += 1
    arg1 +=0xd1
```

### asm3

分析给定asm2函数三个参数，获取输入。主要考察eax，ax，al，ah的区别。使用bytearray来处理位运算，或者使用unicorn或者其他[在线模拟器](https://carlosrafaelgn.com.br/Asm86/)模拟执行，需要自己手动把参数压栈，并调用asm3。
用python模拟有点麻烦，处理溢出以及寄存器分片不方便，其实可以直接[编译执行](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/asm3.md)，注意需要标注intel格式的汇编代码。

```python
arg1,arg2,arg3 = 0xd73346ed,0xd48672ae,0xd3c8b139
arg1 = arg1.to_bytes(4, "little")
arg2 = arg2.to_bytes(4, "little")
eax = arg1[2] << 0x8
eax = eax << 0x10 # 溢出了
eax = eax - arg2[0] # 位数不确定
eax = eax + (arg2[1] << 0x8)
ax = eax & 0xffff
ax = ax ^ (arg3 & 0xffff)
eax = ((eax >> 0x10) << 0x10) + ax
print(hex(eax))
```

编译执行的Makefile如下：

```bash
all:
    gcc -m32 -masm=intel -c asm3.s -o asm3.1.o
    gcc -m32 -c asm3.c -o asm3.2.o
    gcc -m32 asm3.1.o asm3.2.o -o asm3.o
clean:
    rm asm3.1.o asm3.2.o asm3.o
```

使用unicorn模拟的脚本如下，和模拟器原理类似，相对复杂的是需要自己布局，但获取信息更加灵活。

```python
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EAX
from pwn import asm, p32

# code to be emulated
X86_CODE32 = asm('''start:
    mov    ah,BYTE PTR [ebp+0x9]
    shl    ax,0x10
    sub    al,BYTE PTR [ebp+0xd]
    add    ah,BYTE PTR [ebp+0xe]
    xor    ax,WORD PTR [ebp+0x12]
    ''')

# memory address to start emulation
ADDRESS = 0x1000000
STACK = 0x2000000

print("Emulate i386 code")


def hook_code(mu, address, size, user_data):
    print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %
          (address, size))


try:
    # Initialize emulator
    mu = Uc(UC_ARCH_X86, UC_MODE_32)

    # map memory
    mu.mem_map(ADDRESS, 2*1024*1024)
    mu.mem_map(STACK, 2*1024*1024)

    # write machine code
    mu.mem_write(ADDRESS, X86_CODE32)

    # set stack frame
    frame = b'A'*8 + p32(0xd73346ed) + p32(0xd48672ae) + p32(0xd3c8b139)
    mu.mem_write(STACK, frame)

    # initialize machine registers
    mu.reg_write(UC_X86_REG_EBP, STACK)

    # use hook to debug
    mu.hook_add(UC_HOOK_CODE, hook_code)

    # start emulation in infinite time and unlimited instructions
    mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE32))

    print("EMulation done. Below is the CPU context")

    r_eax = mu.reg_read(UC_X86_REG_EAX)
    print(">>> EAX = 0x%x" % r_eax)

except UcError as e:
    print("ERROR: %s" % e)
```

## asm4

采用asm3的方法编译出二进制程序，直接运行出结果。需要修改`jne  0x514 <asm4+23>`为`jne  asm4+23`才能正确地找到相对地址，也可以使用内联汇编来嵌入汇编代码到目标文件中。
程序逻辑如下：

```python
s = 'picoCTF_a3112'
res = 0x246
for i in range(1,len(s)-1):
    res += (ord(s[i+1])-ord(s[i-1]))
print(hex(res))
```

## driods

Android 系列逆向题目
入门教程：<https://nusgreyhats.org/posts/writeups/introduction-to-android-app-reversing/>

### droids0

通过android virtual device运行，显示没有输出到终端。最后在bug report中找到flag。
通过jadx解出apk中的java代码，分析逻辑，MainActivity.java的按钮调用了FlagstaffHill.java中的getFlag方法，其将flag以INFO等级输出到log。可以通过Android Studio的logcat或者adb的logcat来获取flag。

### droids1

通过AVD运行，显示需要输入password。通过jadx反汇编出java代码，关键逻辑在FlagstaffHill.java中的getFlag方法。其将输入与`ctx.getString(R.string.password)`比较，如果通过则输出flag。搜索字符串找到R.string.password即可。也可以选择逆向`fenugreek(input)`方法，这样麻烦一点。

### droids2

类似的程序逻辑，提示应该和smali代码有关。将getFlag的代码直接提取到exp.java中运行的道password，再在模拟器中获得flag。

```java
import java.io.Console;

public class exp {
    public static String getFlag() {
        String[] witches = { "weatherwax", "ogg", "garlick", "nitt", "aching", "dismass" };
        int second = 3 - 3;
        int third = (3 / 3) + second;
        int fourth = (third + third) - second;
        int fifth = 3 + fourth;
        int sixth = (fifth + second) - third;
        String password = "".concat(witches[fifth]).concat(".").concat(witches[third]).concat(".")
                .concat(witches[second]).concat(".").concat(witches[sixth]).concat(".").concat(witches[3]).concat(".")
                .concat(witches[fourth]);
        return password;
    }

    public static void main(String[] args) {
        System.out.println(getFlag());
    }
}
```

### droids3

类似的程序逻辑，但点击输入后没用。查看反汇编后的java代码发现getFlag调用了none函数，返回了固定的明文。yep函数则调用了cilantro，看起来可以获得flag。
使用apktool解包，直接修改`smali/com/hellocmu/picoctf/FlagstaffHill.smali`的代码，将getFlag中的none改为yep。然后重新打包，并签名即可，再放入AVD运行即可。

```bash
apktool decode three.apk --no-res
apktool build three -o recompile/three.apk
java -jar ~/Tools/uber-apk-signer-1.2.1.jar -a recompile
```

### droids4

类似的程序逻辑，将getFlag中的逻辑提取出来，得到字符串"alphabetsoup"，然后返回"call it"。结合提示，在getFlag中调用应该是能够获取flag的cardamom函数即可。
如果直接在getFlag的最开始调用这个函数，直接绕过password的检查，运行的时候会闪退，不知道为啥。

## ARMssembly

ARM系列逆向题目

### ARMssembly 0

提供了一段ARM汇编，需要分析出给定两个输入后的输出结果。之前对于ARM汇编不太熟悉，使用了在线汇编器<https://godbolt.org>进行辅助学习。
首先将两个参数（分别存储在`x0+8`和`x0+16`）经过`atoi`变成int类型的值，再将两个值作为参数调用func1。func1首先是交换了两个参数的位置（w0和w1），并返回较大的值。

```python
flag = 4112417903
flag = hex(flag)[2:].rjust(8,'0')
flag = "picoCTF{" + flag + "}" 
```

### ARMssembly 1

需要在给定变量（写死在了func里面）的情况下，提供什么参数打印出win。分析win的调用点，推出`cmp x0, 0`成立，即func需要返回0。
分析func的功能，首先将81，0（通过wzr寄存器），3依次写入`sp+16,20,24`。随后以`sp+28`为临时变量，使用`lsl`来进行逻辑左移，`sdiv`进行带符号除法，最后与输入进行减法，得到返回值。根据之前的分析，sdiv后的结果即为需要输入的变量值。

```python
a,b,c = 81,0,3
d = a << b
d = a // c
flag = hex(d)[2:].rjust(8,'0')
flag = "picoCTF{" + flag + "}" 
```

### ARMssembly 2

需要分析给定输入下的输出。分析printf的第一个字符串，可知输出格式为`%ld`。func1中是一个循环结构，首先给`sp+24,+28`置零，随后进入.L2。.L2为循环条件，.L3为循环体。每次循环，`sp+24 += 3`，`sp+28 += 1`，当`sp+28`等于输入值时循环结束，并返回`sp+24`的值，相当于进行了乘法。

```python
flag = 2610164910
flag *= 3
flag = hex(flag)[-8:].rjust(8,'0') # 注意只取低4字节
flag = "picoCTF{" + flag + "}"
```

### ARMssembly 3

和ARMssembly2类似，需要分析给定输入下的输出。func1是一个循环，在循环体内部为条件语句，并调用了func2。每次循环将输入参数左移一位，并判断其LSB，如果为1，则将结果加3，即实际上是在二进制表示下统计1的个数。

```python
from pwn import p32
arg = 469937816
flag = 0
while arg > 0:
    if arg & 0x1:
        flag += 3
    arg = arg >> 1
flag = "{:0>8x}".format(flag) # 使用python的格式化字符串
flag = "picoCTF{" + flag + "}"
```

### ARMssembly 4

通过asm系列题目学到了，可以直接编译后运行，得到flag。
代码逻辑有点长，编译成二进制后通过ghidra写出逆向脚本。
好吧其实很简单，弄清楚跳转就行。

```python
arg = 3434881889
arg += 100
arg += 0xd
arg += 2
print('picoCTF{'+hex(arg)[2:]+'}')
```

## vault-door

Java系列逆向题目，picoCTF想出了一个类似于科幻闯关的故事，还挺有意思。

### vault-door-training

虽然不太懂Java语法，但能看懂程序逻辑就行。flag写在程序里面了，直接匹配字符串。

### vault-door-1

在checkPassword里面，按照打乱的顺序逐字节地判断flag正确性。按照顺序赋值给新的字符串即可。可以使用正则表达式（VS Code自带）来提取出重复的赋值操作，exp太长就不放了。

### vault-door-3

在checkPassword里面，分段对字符串进行操作，逆向上述操作的功能和顺序即可。

```python
buffer = list("jU5t_a_sna_3lpm18g947_u_4_m9r54f")
flag = ["A" for i in range(32)]
for i in range(17, 32, 2):
    flag[i] = buffer[i]
for i in range(16, 32, 2):
    flag[46 - i] = buffer[i]
for i in range(8, 16):
    flag[23 - i] = buffer[i]
for i in range(8):
    flag[i] = buffer[i]
flag = "".join(flag)
flag = "picoCTF{" + flag + "}"
```

### vault-door-4

在checkPassword里面，将字符串与ASCII值（decimal,hexdecimal,octal）比较，对应ASCII表恢复即可，需要注意python里面octal的前缀为`0o`。

```python
flag = ""
for i in range(32):
    if i < 24:
        flag += chr(bytes[i])
    else:
        flag += bytes[i]

flag = "picoCTF{" + flag + "}"
print(flag)
```

### vault-door-5

在checkPassword里面，先后经过url编码和base64编码，逆向上述操作即可。

```python
from base64 import b64decode
from urllib.parse import unquote_plus

enc_flag = (
    "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"
    + "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"
    + "JTM0JTVmJTY1JTMzJTMxJTM1JTMyJTYyJTY2JTM0"
)

flag = b64decode(enc_flag).decode()
flag = unquote_plus(flag)
flag = "picoCTF{" + flag + "}"
print(flag)
```

### vault-door-6

在checkPassword里面，逐位与0x55异或。由于两次异或后结果相同，重复该操作即可。

```python
flag = [0x3b,...,0x6d]
flag = [chr(b ^ 0x55) for b in flag]
flag = "".join(flag)
flag = "picoCTF{" + flag + "}"
print(flag)
```

### vault-door-7

在passwordToIntArray里面，将4个byte一组转化为1个int，逆向该操作即可。

```python
from Crypto.Util.number import long_to_bytes

ints = [
    1096770097,
    1952395366,
    1600270708,
    1601398833,
    1716808014,
    1734304867,
    942695730,
    942748212,
]

flag = b"".join([long_to_bytes(i) for i in ints]).decode()
flag = "picoCTF{" + flag + "}"
print(flag)
```

### vault-door-8

在scramable中，对于每个char，按照一定的顺序调用switchBits。创建rescramable，复用switchBits方法，按照相反的顺序恢复。

```java
public void rescramble(char[] password) {
    for (int b = 0; b < password.length; b++) {
        char c = password[b];
        c = switchBits(c, 6, 7);
        c = switchBits(c, 2, 5);
        /* d = switchBits(d, 4, 5); e = switchBits(e, 5, 6); */ c = switchBits(c, 3, 4);
        c = switchBits(c, 0, 1);
        c = switchBits(c, 4, 7);
        /* c = switchBits(c,14,3); c = switchBits(c, 2, 0); */ c = switchBits(c, 5, 6);
        c = switchBits(c, 0, 3);
        c = switchBits(c, 1, 2);
        password[b] = c;
    }
    String flag = String.valueOf(password);
    flag = "picoCTF{" + flag + "}";
    System.out.println(flag);
}

public boolean checkPassword(String password) {
    // ...
    rescramble(expected);
    return Arrays.equals(scrambled, expected);
}
```

## speeds and feeds

模拟了工业场景中CNC车床的输出数据。使用了一种叫做[G-Code](https://zh.wikipedia.org/wiki/G代码)的语言，需要将其[可视化](https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiF0LH5sOv2AhV0NKYKHeGmCuMQFnoECAkQAQ&url=https%3A%2F%2Fncviewer.com%2F&usg=AOvVaw0aN-HCIWixmN87qclUeHGP)。

```bash
nc mercury.picoctf.net 33596 > chall.nc
```

## 参考链接

* 题目地址：<https://play.picoctf.org/practice?category=3>
* picoCTF writeup from 2018 to 2021：<https://github.com/Dvd848/CTFs>
