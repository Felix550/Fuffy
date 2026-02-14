# Fuffy — User Guide

Fuffy is a lazy stack-based programming language for Windows x64.

---

## Overview

Fuffy works with a stack: you can push numbers or strings, perform arithmetic, print values, remove items, and check the stack length. Special sequences like `\n`, `\t`, and escaped quotes are supported inside strings.

---

## Building
To Build the command is
```text
main.py [program.fuffy] [-r]
```

If you put ```-r``` the program will run after compiling

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

| Command            | Description                                                 | Example                                                                       |
| -------            | ----------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `dump`             | Dumps the top of the stack and remove it                    | `69 dump` prints `69` and removes it from stack                               |
| `dump.[register]`  | Dumps a specific register                                   | `dump.a` prints `rax` content                                                 |
| `ddump`            | Dumps the top of the stack without removing it              | `104 ddump dump` prints `104` without removing, then `dump` consumes it       |
| `sum`              | Add the top two numbers                                     | `34 35 sum dump` prints `69`                                                  |
| `sub`              | Subtract top number from second                             | `500 100 sub dump` prints `400`                                               |
| `mul`              | Multiply top two numbers                                    | `2 10 mul dump` prints `20`                                                   |
| `idiv`             | Integer division; produces quotient and remainder           | `20 6 idiv 1 rem dump` prints quotient, `20 6 idiv 2 rem prt` prints remainder|
| `rem`\*              | Remove an item from the stack by position                   | `34 35 36 2 rem` removes second from top (35)                                 |
| `sl`               | Get the current number of items in the stack                | `sl dump.a` prints the stack length                                           |
| `sclr`             | Clear the stack                                             | `sclr` removes all items from the stack                                       |
| `ltm.[register]`   | Loads from the top of the stack to the specified register   | `ltm.a` the top of the stack goes into rax                                    |
| `lfm.[register]`   | Loads from the specified register to the top of the stack   | `lfm.a` rax goes onto the stack                                               |

\* rem != remainder, rem is REMOVE

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
20 6 idiv 1 rem dump
"20 %% 6 = " dump
20 6 idiv 2 rem dump
"-----------------------------------------------\n" dump
34 35
"stack len: " dump
sl dump.a
sclr
"-----------------------------------------------\n" dump
35 34 sum ltm.1 dump.1
"-----------------------------------------------\n" dump
"104 - 4 = %d, %s, %s\n" ltm.1
104 4 sub ltm.2
":)" ltm.3
"ciao" ltm.4
print
"Hello\n" ltm.1
print
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
-----------------------------------------------
104 - 4 = 100, :), ciao
Hello
```