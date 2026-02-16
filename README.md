# Fuffy — User Guide

Fuffy is a lazy stack-based programming language for Windows x64.

---

## Overview

Fuffy works with a stack: you can push numbers or strings, perform arithmetic, print values, remove items and much more!

---

## Building
To Build the command is
```text
main.py [program.fuffy] [-r] [-mtc] 
```

If you put ```-r``` the program will run after compiling \
If you put ```-mtc``` the program will ignore all the others aarguments and only compile the temp.asm into an a.exe


---

## Writing Programs

* **Numbers**: Writing a number pushes it onto the stack.
* **Strings**: Enclose text in double quotes (`"`) to push it onto the stack. Escape sequences are handled automatically.
* **Comments**: Lines starting with `;` are ignored.

### Example

```text
; Load and print a number
69 dump

; Print a string with newline
"Hello, World!\n" dump
```

---

## Commands
    
| Command           | Description                                                  | Example                                                                            |
| ----------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `dump`            | Dumps the top of the stack and remove it                     | `69 dump` prints `69` and removes it from stack                                    |
| `dump.[register]` | Dumps a specific register                                    | `dump.a` prints `rax` content                                                      |
| `ddump`           | Dumps the top of the stack without removing it               | `104 ddump dump` prints `104` without removing, then `dump` consumes it            |
| `sum`             | Add the top two numbers                                      | `34 35 sum dump` prints `69`                                                       |
| `sub`             | Subtract top number from second                              | `500 100 sub dump` prints `400`                                                    |
| `mul`             | Multiply top two numbers                                     | `2 10 mul dump` prints `20`                                                        |
| `idiv`\*          | Integer division; produces quotient and remainder            | `20 6 idiv 1 trash dump` prints quotient, `20 6 idiv 2 trash prt` prints remainder |
| `trash`\*\*       | Remove an item from the stack by position on the stack       | `34 35 36 2 trash` removes second from top (35)                                    |
| `sl`              | Get the current number of items in the stack                 | `sl dump.a` prints the stack length                                                |
| `sclr`            | Clear the stack                                              | `sclr` removes all items from the stack                                            |
| `ltm.[register]`  | Moves the top stack value into the specified register.       | `ltm.a` Moves the top stack value into `rax`                                       |
| `lfm.[register]`  | Pushes the value from the specified register onto the stack. | `lfm.a` rax goes onto the stack                                                    |
| `exit`            | Exits with the return code found on top of the stack         | `69 exit` exits with code 69                                                       |

\* i stands for Integer \
\*\* Stack index is required, Top of stack is 1.

Note.
`dump` is just a 'faster' version of `print`

## Comparators and Logic Gates 
### All of these keywords consume two values from the stack and push one result. `not` consumes one value and pushes one result.
### Non-zero values are treated as true, 0 is treated as false.

| Keyword  | Description                                                                                                | Example                                                   |
| -------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `=`      | Push 1 on the stack if the 2 elements on the stack are equal otherwise push 0                              | `2 2 = dump` prints `1` and `1 2 = dump` prints `0`       |
| `!=`     | Push 1 on the stack if the 2 elements on the stack are NOT equal otherwise push 0                          | `1 2 != dump` prints `1` and `2 2 != dump` prints `0`     |
| `<`\*    | Push 1 on the stack if the second element on the stack is less than the first otherwise push 0             | `1 2 < dump` prints `1` and `3 2 < dump` prints `0`       |
| `>`\*    | Push 1 on the stack if the second element on the stack is greater than the first otherwise push 0          | `2 1 > dump` prints `1` and `1 2 > dump` prints `0`       |
| `<=`\*   | Push 1 on the stack if the second element on the stack is less than or equal the first otherwise push 0    | `2 2 <= dump` prints `1` and `3 2 <= dump` prints `0`     |
| `>=`\*   | Push 1 on the stack if the second element on the stack is greater than or equal the first otherwise push 0 | `1 1 >= dump` prints `1` and `1 2 >= dump` prints `0`     |
| `not`    | Push 1 on the stack if the first element on the stack is 0 otherwise push 0                                | `1 not dump` prints `0` and `0 not dump` prints `1`       |
| `and`\*  | Push 1 on the stack if both elements on the stack are non-zero otherwise push 0                            | `1 1 and dump` prints `1` and `1 0 and dump` prints `0`   |
| `nand`\* | Push 0 on the stack if both elements on the stack are non-zero otherwise push 1                            | `1 1 nand dump` prints `0` and `1 0 nand dump` prints `1` |
| `or`\*   | Push 1 on the stack if at least one element on the stack is non-zero otherwise push 0                      | `0 1 or dump` prints `1` and `0 0 or dump` prints `0`     |
| `nor`\*  | Push 1 on the stack if both elements on the stack are 0 otherwise push 0                                   | `0 0 nor dump` prints `1` and `1 0 nor dump` prints `0`   |
| `xor`\*  | Push 1 on the stack if the two elements on the stack are different otherwise push 0                        | `1 0 xor dump` prints `1` and `1 1 xor dump` prints `0`   |
| `xand`\* | Push 1 on the stack if the two elements on the stack are equal otherwise push 0                            | `1 1 xand dump` prints `1` and `1 0 xand dump` prints `0` |

\* Remember: [Stack](https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29) is a LIFO structure, so \
* first value → the most recently pushed (top of stack)
* second value → the value beneath it

---

## Strings and Escapes

Fuffy automatically interprets common escape sequences inside strings:

* `\n` → newline
* `\t` → tab
* `\\` → backslash
* `\"` → double quote
* `\'` → apostrophe
* `%%` → percent

### Example

```text
"Hello\n\tMy name is 'Felix'\n" dump
```

Prints:

```
Hello
	My name is 'Felix'
```
  
## Registers

Fuffy uses a set of REGISTERS that CAN be used to store TEMPORANY values such as ARGS, etc. or to show the values of those REGISTERS
* `a` → `rax`
* `b` → `rbx`
* `1` → `rcx`
* `2` → `rdx`
* `3` → `r8`
* `4` → `r9`

### Example

```text
69 ltm.1 dump.1
104 ltm.2 lfm.2 dump
```

Prints:

```
69
104
```

---

## Flow Controls

### `if`

Executes a block only if the value on the stack is **non-zero**.

**Behavior**

1. Pops the first value from the stack.
2. If the value is **0**, execution jumps to the matching `else` (if present) or `endif`.
3. If the value is **non-zero**, execution continues inside the `if` block.

Non-zero values are treated as **true**.

#### Syntax

```
<condition> ;on the stack
if
    ... true block ...
endif
```

#### With `else`

```
<condition> ;on the stack
if
    ... true block ...
else
    ... false block ...
endif
```

### Examples

**Basic condition**

```
1 if
    "true" dump
endif
```

Prints:

```
true
```

**False condition**

```
0 if
    "true" dump
endif
```

Prints nothing.

**If / else**

```
0 if
    "true" dump
else
    "false" dump
endif
```

Prints:

```
false
```

**Using a comparator and logic gate**

```
5 3 > 2 3 < or if
    "greater and less" dump
else
    "not greater and less" dump
endif
```

Prints:

```
greater and less
```

#### Notes

* `if` blocks can be nested.
* The condition value is always removed from the stack.
* Empty `if` or `else` blocks are allowed but may produce warnings.

---

## Functions
### print

Is the same as `printf()` in C, it accepts the following arguments:
* `rcx` → The base string or value to print, the only required one, use `ltm.1`
* `rbx` → The first format parameter, use `ltm.2`
* `r8` → The second format parameter, use `ltm.3`
* `r9` → The third format parameter, use `ltm.4`

#### Example

```text
"104 - 4 = %d, %s, %s\n" ltm.1
104 4 sub ltm.2
":)" ltm.3
"Hello" ltm.4
print ;call the function
```

Prints:

```
104 - 4 = 100, :), Hello
```

---

## Complete Example

```text
; By Felix_550
"34 + 35 = " dump
34 35 sum dump
"-----------------------------------------------\n" dump
"20 // 6 = " dump
20 6 idiv 1 trash dump
"20 %% 6 = " dump
20 6 idiv 2 trash dump
"-----------------------------------------------\n" dump
34 35
"stack len: " dump
sl dump.a
sclr
"-----------------------------------------------\n" dump
35 34 sum ltm.1 dump.1
200 100 sub ltm.1 lfm.1 dump
"-----------------------------------------------\n" dump
"104 - 4 = %d, %s, %s\n" ltm.1
104 4 sub ltm.2
":)" ltm.3
"ciao" ltm.4
print
"Hello\n" ltm.1
print
34 35 sum 69 = if
    100 4 sum 104 != if
        "then1" dump
    else
        "else1" dump
    endif
else
    0 if
        "then2" dump
    else
        "else2" dump
    endif
endif

69 exit
```

Prints:

```text
34 + 35 = 69
-----------------------------------------------
20 // 6 = 3
20 % 6 = 2
-----------------------------------------------
stack len: 2
-----------------------------------------------
69
100
-----------------------------------------------
104 - 4 = 100, :), ciao
Hello
else1
```

Exit Code:
```text
69
```