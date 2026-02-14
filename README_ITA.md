# Fuffy — Guida per l'utente

Fuffy è un linguaggio di programmazione lazy basato su stack per Windows x64.

---

## Panoramica

Fuffy lavora con uno stack: puoi pushare numeri o stringhe, eseguire operazioni aritmetiche, stampare valori, rimuovere elementi e controllare la lunghezza dello stack. Sequenze speciali come `\n`, `\t` e virgolette escape sono supportate all'interno delle stringhe.

---

## Compilazione

Per compilare il comando è

```text
main.py [program.fuffy] [-r]
```

Se passi `-r` il programma verrà eseguito dopo la compilazione.
Se passi `-mtc` il programma ignorerà tutti gli altri argomenti e compilerà solo `temp.asm` in `a.exe`.

---

## Scrivere programmi

* **Numeri**: Scrivere un numero lo inserisce nello stack.
* **Stringhe**: Racchiudi il testo tra virgolette doppie (`"`) per inserirlo nello stack. Le sequenze di escape sono gestite automaticamente.
* **Commenti**: Le righe che iniziano con `;` sono ignorate.

### Esempio

```text
; Carica e stampa un numero
69 dump

; Stampa una stringa con newline
"Hello, World!\n" dump
```

---

## Comandi

| Command           | Descrizione                                         | Esempio                                                                               |
| ----------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `dump`            | Stampa il top dello stack e lo rimuove              | `69 dump` stampa `69` e lo rimuove dallo stack                                        |
| `dump.[register]` | Stampa un registro specifico                        | `dump.a` stampa il contenuto di `rax`                                                 |
| `ddump`           | Stampa il top dello stack senza rimuoverlo          | `104 ddump dump` stampa `104` senza rimuoverlo, poi `dump` lo consuma                 |
| `sum`             | Somma i due numeri in cima allo stack               | `34 35 sum dump` stampa `69`                                                          |
| `sub`             | Sottrae il numero in cima dal secondo               | `500 100 sub dump` stampa `400`                                                       |
| `mul`             | Moltiplica i due numeri in cima                     | `2 10 mul dump` stampa `20`                                                           |
| `idiv`*           | Divisione intera; produce quoziente e resto         | `20 6 idiv 1 trash dump` stampa il quoziente, `20 6 idiv 2 trash prt` stampa il resto |
| `trash`**         | Rimuove un elemento dallo stack per posizione       | `34 35 36 2 trash` rimuove il secondo elemento (35)                                   |
| `sl`              | Ottiene il numero corrente di elementi nello stack  | `sl dump.a` stampa la lunghezza dello stack                                           |
| `sclr`            | Pulisce lo stack                                    | `sclr` rimuove tutti gli elementi dallo stack                                         |
| `ltm.[register]`  | Carica dal top dello stack nel registro specificato | `ltm.a` il top dello stack va in `rax`                                                |
| `lfm.[register]`  | Carica dal registro specificato nel top dello stack | `lfm.a` `rax` viene pushato nello stack                                               |

* `i` sta per Integer.
** Richiede l'indice nello stack; il top dello stack è 1.

Nota.
`dump` è solo una versione "più veloce" di `print`.

---

## Stringhe ed escape

Fuffy interpreta automaticamente le sequenze di escape comuni all'interno delle stringhe:

* `\n` → nuova linea
* `\t` → tab
* `\\` → backslash
* `\"` → virgolette doppie
* `\'` → apostrofo
* `%%` → percentuale

### Esempio

```text
"Hello\n\tMy name is 'Felix'\n" dump
```

Stampa:

```
Hello
	My name is 'Felix'
```

## Registri

Fuffy usa un insieme di REGISTRI che POSSONO essere usati per memorizzare valori TEMPORANEI come ARG o per mostrare i valori di quei REGISTRI

* `a` → `rax`
* `b` → `rbx`
* `1` → `rcx`
* `2` → `rdx`
* `3` → `r8`
* `4` → `r9`

### Esempio

```text
69 ltm.1 dump.1
104 ltm.2 lfm.2 dump
```

Stampa:

```
69
104
```

---

## Funzioni

### print

È equivalente a `printf()` in C, accetta i seguenti argomenti:

* `rcx` → La stringa base o valore da stampare, l'unico richiesto; usa `ltm.1`
* `rbx` → Primo parametro di formato, usa `ltm.2`
* `r8` → Secondo parametro di formato, usa `ltm.3`
* `r9` → Terzo parametro di formato, usa `ltm.4`

#### Esempio

```text
"104 - 4 = %d, %s, %s\n" ltm.1
104 4 sub ltm.2
":)" ltm.3
"Hello" ltm.4
print ;chiama la funzione
```

Stampa:

```
104 - 4 = 100, :), Hello
```

---

## Esempio completo

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
```

Stampa:

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
