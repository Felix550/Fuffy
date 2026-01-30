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
69 prt

; Print a string with newline
"Hello, World!\n" prt
```

---

## Commands

| Command | Description                                                 | Example                                                                       |
| ------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `dump`  | Dumps the top of the stack and remove it                    | `69 dump` prints `69` and removes it from stack                               |
| `ddump` | Dumps the top of the stack without removing it              | `104 ddump dump` prints `104` without removing, then `dump` consumes it       |
| `sum`   | Add the top two numbers                                     | `34 35 sum dump` prints `69`                                                  |
| `sub`   | Subtract top number from second                             | `500 100 sub dump` prints `400`                                               |
| `mul`   | Multiply top two numbers                                    | `2 10 mul dump` prints `20`                                                   |
| `idiv`  | Integer division; produces quotient and remainder           | `20 6 idiv 1 rem dump` prints quotient, `20 6 idiv 2 rem prt` prints remainder|
| `rem`   | Remove an item from the stack by position                   | `34 35 36 2 rem` removes second from top (35)                                 |
| `sl`    | Get the current number of items in the stack                | `sl rdump` prints the stack length                                            |
| `rdump` | Dumps the value of the last computed result like sl         | `rdump` prints `RAX` or last result                                           |
| `sclr`  | Clear the stack                                             | `sclr` removes all items from the stack                                       |

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

---

## Complete Example

```text
; Strings
"Hello and Welcome to Fuffy!\n" dump

; Numbers and arithmetic
69 dump
34 35 sum dump
500 100 sub dump
2 10 mul dump

; Removing elements
34 35 36 2 rem
dump
dump

; Integer division
20 6 idiv 1 rem dump
20 6 idiv 2 rem dump

; Debug printing
104 ddump dump

; Stack utilities
sl
rdump
sclr
```