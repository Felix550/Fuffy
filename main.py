import subprocess
import sys
import difflib

i = 0
def go_enum(reset = False):
    global i
    if reset:
        i = 0
    result = i
    i += 1
    return result

OP_PUSH = go_enum(True)
OP_PUSHSTRING = go_enum()
OP_PLUS = go_enum()
OP_SUB = go_enum()
OP_MUL = go_enum()
OP_IDIV = go_enum()
OP_PRINT = go_enum()
OP_DUMP = go_enum()
OP_DUMPMEMORY = go_enum()
OP_DEBUGDUMP = go_enum()
OP_TRASH = go_enum()
OP_STACKLEN = go_enum()
OP_STACKCLEAR = go_enum()
OP_LOADTOMEMORY = go_enum()
OP_LOADFROMMEMORY = go_enum()
OP_DUP = go_enum()
OP_USAGE = go_enum()
OP_EXIT = go_enum()
OP_CALL = go_enum()
OP_CMP = go_enum()
OP_LOGIC = go_enum()

OP_IF = go_enum()
OP_ELSE = go_enum()
OP_ENDIF = go_enum()

OP_WHILE = go_enum()
OP_ENDWHILE = go_enum()

CMP_EQ = go_enum(True)
CMP_NE = go_enum()
CMP_GT = go_enum()
CMP_LT = go_enum()
CMP_GE = go_enum()
CMP_LE = go_enum()

LOGIC_NOT = go_enum(True)
LOGIC_AND = go_enum()
LOGIC_NAND = go_enum()
LOGIC_XAND = go_enum()
LOGIC_OR = go_enum()
LOGIC_NOR = go_enum()
LOGIC_XOR = go_enum()

H_PRINTF = go_enum(True)
H_TRASH = go_enum()
H_STACKLEN = go_enum()
H_EXIT = go_enum()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PC:
    def __init__(self, src, c_index=0):
        self.c_index = c_index
        self.src = src

    def peek(self) -> str:
        if self.c_index + 1 > len(self.src):
            return None
        else:
            return self.src[self.c_index]

    def consume(self):
        passer = self.src[self.c_index]
        self.c_index += 1
        return passer

    def get(self):
        return self.src[self.c_index]

    def index(self):
        return self.c_index
    
    def reset(self):
        self.c_index = 0
        self.src = None
        
def Error(msg, reason=None, fix=None, file=None, row=None, col=None):
    location = ""
    if file and row and col:
        location = f"{file}:{row}:{col} "

    print(f"{bcolors.FAIL}{location}{bcolors.UNDERLINE}Error: {msg}{bcolors.ENDC}{bcolors.FAIL}", end="")

    if reason and reason != "":
        print(f"\nReason: {reason}", end="")

    if fix and fix != "":
        print(f"\nPossible Fix: {fix}", end="")

    print(f"{bcolors.ENDC}")
    exit(1)
    
def Warn(msg, file=None, row=None, col=None):
    if file and row and col:
        print(f"{bcolors.WARNING}{file}:{row}:{col} Warning: {msg}{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Warning: {msg}{bcolors.ENDC}")
        
def Success(msg, file=None, row=None, col=None):
    if file and row and col:
        print(f"{bcolors.OKGREEN}{file}:{row}:{col} SUCCESS: {msg}{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}SUCCESS: {msg}{bcolors.ENDC}")
    
def Push(x):
    return (OP_PUSH, x)

def PushString(x):
    return (OP_PUSHSTRING, x)

def Plus():
    return (OP_PLUS, )

def Sub():
    return (OP_SUB, )

def Mul():
    return (OP_MUL, )

def IDiv():
    return (OP_IDIV, )

def Print():
    return (OP_PRINT, )

def Dump():
    return (OP_DUMP, )

def DebugDump():
    return (OP_DEBUGDUMP, )

def DumpMemory(x):
    return (OP_DUMPMEMORY, x)

def Trash():
    return (OP_TRASH, )

def StackLen():
    return (OP_STACKLEN, )

def StackClear():
    return (OP_STACKCLEAR, )

def LoadToMemory(x):
    return (OP_LOADTOMEMORY, x) #Pop Stack to Memory

def LoadFromMemory(x):
    return (OP_LOADFROMMEMORY, x) #Push Memory to Stack

def Dup():
    return (OP_DUP, ) #Push Memory to Stack

def Usage(tok,usage):
    return (OP_USAGE,(tok,usage)) #Error(f"Usage of \"{tok}\": {usage}")

def Exit():
    return (OP_EXIT,)

def Call(x):
    return (OP_CALL,x)

def IF():
    return (OP_IF,)

def ELSE():
    return (OP_ELSE,)

def ENDIF():
    return (OP_ENDIF,)

def WHILE():
    return (OP_WHILE,)

def ENDWHILE():
    return (OP_ENDWHILE,)

Memories = {
    "a": "rax",
    "b": "rbx",
    "1": "rcx",
    "2": "rdx",
    "3": "r8",
    "4": "r9",
}

Comparators = {
    "=":  CMP_EQ,
    "!=":  CMP_NE,
    ">":  CMP_GT,
    "<":  CMP_LT,
    ">=":  CMP_GE,
    "<=":  CMP_LE,
}

Comparators_rev = {v: k for k, v in Comparators.items()}

Logic_Gates = {
    "not":  (LOGIC_NOT,1),
    "and":  (LOGIC_AND,2),
    "nand":  (LOGIC_NAND,2),
    "xand":  (LOGIC_XAND,2),
    "or":  (LOGIC_OR,2),
    "nor":  (LOGIC_NOR,2),
    "xor":  (LOGIC_XOR,2),
}

Logic_Gates_rev = {v[0]: k for k, v in Logic_Gates.items()}

Keywords = {
    "sum": {
        "function": Plus(),
        "helpers": None
    },
    "sub": {
        "function": Sub(),
        "helpers": None
    },
    "mul": {
        "function": Mul(),
        "helpers": None
    },
    "idiv": {
        "function": IDiv(),
        "helpers": None
    },
    "print": {
        "function": Print(),
        "helpers": [H_PRINTF]
    },
    "dump": {
        "function": Dump(),
        "helpers": [H_PRINTF]
    },
    "ddump": {
        "function": DebugDump(),
        "helpers": [H_PRINTF]
    },
    "trash": {
        "function": Trash(),
        "helpers": [H_TRASH]
    },
    "sl": {
        "function": StackLen(),
        "helpers": [H_STACKLEN]
    },
    "sclr": {
        "function": StackClear(),
        "helpers": None
    },
    "ltm": {
        "function": Usage("ltm",f"ltm.[register]\nRegisters:\n\t{"\n\t".join([f".{k} : \"{v}\"" for k, v in Memories.items()])}"),
        "helpers": None
    },
    "lfm": {
        "function": Usage("lfm",f"lfm.[register]\nRegisters:\n\t{"\n\t".join([f".{k} : \"{v}\"" for k, v in Memories.items()])}"),
        "helpers": None
    },    
    "dup": {
        "function": Dup(),
        "helpers": None
    },
    "exit": {
        "function": Exit(),
        "helpers": [H_EXIT]
    },
    "if": {
        "function": IF(),
        "helpers": None
    },    
    "else": {
        "function": ELSE(),
        "helpers": None
    },    
    "endif": {
        "function": ENDIF(),
        "helpers": None
    },
    "while": {
        "function": WHILE(),
        "helpers": None
    },
    "endwhile": {
        "function": ENDWHILE(),
        "helpers": None
    },
}

global virtual_stack
virtual_stack = []

# stack / asm helpers (usare sempre queste per mantenere sync)
def push_imm(f, value):
    """Push immediato (numero) su stack a runtime e modello."""
    f.write(f"    push {value}\n")
    virtual_stack.append(("int", value))

def push_reg(f, reg, typ="int", value=None):
    """Push del valore contenuto in reg (es. rax) sullo stack."""
    f.write(f"    push {reg}\n")
    virtual_stack.append((typ, value))

def push_rax(f, typ="int", value=None):
    f.write("    push rax\n")
    virtual_stack.append((typ, value))

def push_string_pointer(f, sid, token):
    """Carica l'indirizzo della stringa in rax, poi push rax e aggiorna il modello."""
    f.write(f"    lea rax, [rel S_{sid}]\n")
    push_rax(f, "string", token)

def pop_value(f, register):
    """
    Emette 'pop <register>' e aggiorna il modello rimuovendo l'elemento top.
    Restituisce la tupla (type, value) dell'elemento rimosso.
    """
    if not virtual_stack:
        Error("stack underflow (pop)")
    f.write(f"    pop {register}\n")
    return virtual_stack.pop()

def discard_top(f):
    """Rimuove top senza scrivere in registro (equivalente a pop + drop)."""
    if not virtual_stack:
        Error("stack underflow (discard)")
    f.write("    add rsp, 8\n")
    virtual_stack.pop()

def peek_type():
    return virtual_stack[-1][0] if virtual_stack else None

def stack_size():
    return len(virtual_stack)
    
def peek_top_to_reg(f, reg):
    f.write(f"    mov {reg}, [rsp]\n")


def tokenize_file(file_path):
    result = []
    with open(file_path,"r") as f:
        content = f.readlines()
        for i,line in enumerate(content):
            row = i + 1
            column = 0
            pc = PC(line)
            buff = ""
            while pc.peek() is not None:
                ch: str = pc.peek()
                column = pc.index() + 1
                if ch.isdigit():
                    buff += pc.consume()
                    while pc.peek() is not None and pc.peek().isdigit():
                        buff += pc.consume()
                    result.append((buff,(row,column)))
                    buff = ""
                    continue
                elif ch == "\"":
                    pc.consume()  # consuma la quote iniziale
                    buff = "\""
                    escape_next = False

                    while pc.peek() is not None:
                        cons = pc.consume()

                        if escape_next:
                            # carattere preceduto da backslash, trattalo come letterale
                            buff += cons
                            escape_next = False
                        elif cons == "\\":
                            escape_next = True
                            buff += cons
                        elif cons == "\"":
                            buff += cons
                            break  # chiude la stringa
                        else:
                            buff += cons

                    result.append((buff,(row,column)))
                    buff = ""
                    continue
                elif ch.isalpha():
                    buff += pc.consume()
                    while pc.peek() is not None and (pc.peek().isalpha() or pc.peek().isdigit() or pc.peek() == "." or (pc.peek().isprintable() and not pc.peek().isspace() and not pc.peek() == ";")):
                        buff += pc.consume()
                    result.append((buff,(row,column)))
                    buff = ""
                    continue
                elif ch == ";":
                    buff += pc.consume()
                    while pc.peek() is not None and pc.peek().isprintable():
                        buff += pc.consume()
                    result.append((buff,(row,column)))
                    buff = ""
                    continue
                elif ch.isprintable() and not ch.isspace():
                    buff += pc.consume()
                    while pc.peek() is not None and (pc.peek().isprintable() and not pc.peek().isspace() and not pc.peek().isdigit()):
                        buff += pc.consume()
                    result.append((buff,(row,column)))
                    buff = ""
                    continue
                else:
                    pc.consume()
                    continue
    return result

helpers_needed = []

def check_helper(helper):
    if not any(h in helpers_needed for h in helper):
        helpers_needed.extend(helper)

strings = []

"""
    "foo": {
        "tokens": [],
        "id": 0
    },
"""

functions = {}
functions_context = []

def parse_program_from_tokens(tokens,program_path):
    functions_counter = 0
    result = []

    def append_to_result(function,position):
        if functions_context:
            f_name = functions_context[-1]["name"]
            functions[f_name]["tokens"].append((function, position))
            return
        result.append((function,position))

    pc = PC(tokens)
    while pc.peek() is not None:
        tok , (r,c) = pc.consume()
        
        # number
        if tok.isdigit():
            append_to_result(Push(int(tok)),(r,c))
            continue

        # string
        if tok.startswith('"') and tok.endswith('"'):
            id = 0 if len(strings) == 0 else strings[-1][0] + 1
            strings.append((id, tok))
            append_to_result(PushString((id, tok)),(r,c))
            continue

        # comment
        if tok.startswith(";"):
            continue
        
        if tok.startswith("ltm."):
            _,rhs = tok.split(".")
            if rhs == "a" or rhs == "b":
                Warn(f"direct manipulation of internal memory locations like \"{Memories[rhs]}\" with \"{tok}\" is strongly discouraged, since these addresses are reserved for the compiler’s internal operations",file=program_path,row=r,col=c)
            append_to_result(LoadToMemory(rhs),(r,c))
            continue
        
        if tok.startswith("lfm."):
            _,rhs = tok.split(".")
            append_to_result(LoadFromMemory(rhs),(r,c))
            continue
        
        if tok.startswith("dump."):
            helpers = [H_PRINTF]
            
            _,rhs = tok.split(".")
            append_to_result(DumpMemory(rhs),(r,c))
            check_helper(helpers)
            continue
        
        if tok == "func":
            rhs = ""
            if pc.peek() is not None:
                rhs, _ = pc.consume()

            if rhs == "" or rhs == "endfunc":
                Error("function name can't be empty",row=r,col=c,file=program_path)
            if rhs in functions:
                Error(f"function with name '{rhs}' arleady exists",row=r,col=c,file=program_path)

            functions_counter += 1
            functions[rhs] = {"tokens":[],
                              "id":functions_counter,
                              "start_pos":(r,c),
                              "end_pos":None}
            functions_context.append({"id":functions_counter,
                                      "name":rhs})
            continue
        
        if tok == "endfunc":
            if not functions_context:
                Error("unexpected 'endfunc'",
                      reason="there is no active FUNC to close",
                      fix="remove 'endfunc' or add a matching 'func.<name>'",
                      file=program_path, row=r, col=c)
            f_ctx = functions_context.pop()
            functions[f_ctx["name"]]["end_pos"] = (r, c)
            continue
        
        """
        if tok.startswith("call."):
            _,rhs = tok.split(".")
            if rhs == "":
                Error("function name can't be empty",row=r,col=c,file=program_path)
            if not rhs in functions:
                Error(f"a function with named '{rhs}' doesn't exists",row=r,col=c,file=program_path)

            append_to_result(Call(rhs),(r,c))
            continue
        """

        # keyword
        if tok in Keywords:
            kw = Keywords[tok]

            # function
            append_to_result(kw["function"],(r,c))

            # helpers
            helpers = kw.get("helpers")
            if helpers:
                check_helper(helpers)

            continue
        
        if tok in Comparators:
            append_to_result((OP_CMP, Comparators[tok]),(r,c))
            continue
        
        if tok in Logic_Gates:
            append_to_result((OP_LOGIC, Logic_Gates[tok]),(r,c))
            continue
        
        if tok in functions:
            append_to_result(Call(tok),(r,c))
            continue

        # invalid token
        threshold = 0.6  # soglia di similarità

        # trova la prima chiave simile
        similar = Keywords | functions
        similar_key = next(
            (k for k in similar.keys() if difflib.SequenceMatcher(None, k, tok).ratio() >= threshold),
            False
        )
        Error(f"\"{tok}\" is not a valid keyword or a valid function name",fix=f"maybe you meant: \"{similar_key}\"" if similar_key else "",file=program_path,row=r,col=c)

    return result

def print_helpers(f):
    f.write("print_number: ; RDX\n")
    f.write("    sub rsp, 40                 ; shadow space per call a printf\n")
    f.write("\n")
    f.write("    lea rcx, [rel fmt]          ; RCX = stringa di formato\n")
    f.write("    call printf\n")
    f.write("\n")
    f.write("    add rsp, 40                 ; ripristina stack\n")
    f.write("    ret\n")
    f.write("\n")
    
def trash_helpers(f):
    f.write("global remove_nth\n")
    f.write("; RCX = M, RDX = N\n")
    f.write("; clobbers: RAX,R8,R9,R10,R11\n")
    f.write("remove_nth:\n")
    f.write("    ; validate inputs\n")
    f.write("    test rcx, rcx        ; if M==0 return\n")
    f.write("    jz .ret\n")
    f.write("    test rdx, rdx        ; if N==0 return\n")
    f.write("    jz .ret\n")
    f.write("    cmp rdx, rcx\n")
    f.write("    ja .ret              ; if N > M return\n")
    f.write("\n")
    f.write("    mov r8, rsp          ; r8 = original rsp (base of block)\n")
    f.write("    mov r9, rcx\n")
    f.write("    imul r9, 8           ; r9 = M*8\n")
    f.write("    sub rsp, r9          ; allocate buffer of M qwords at new rsp\n")
    f.write("\n")
    f.write("    xor r10, r10         ; i = 0\n")
    f.write(".copy_loop:\n")
    f.write("    cmp r10, rcx\n")
    f.write("    jae .reconstruct\n")
    f.write("    mov rax, [r8 + r10*8]\n")
    f.write("    mov [rsp + r10*8], rax\n")
    f.write("    inc r10\n")
    f.write("    jmp .copy_loop\n")
    f.write("\n")
    f.write(".reconstruct:\n")
    f.write("    lea r11, [r8 + 8]    ; r11 = destination base (new stack start after removal)\n")
    f.write("    xor r10, r10         ; i = 0\n")
    f.write("    xor r9, r9         ; j = 0  (usiamo r12 ma non lo preserviamo; se preferisci usa r11/r10 alternativi)\n")
    f.write(".recon_loop:\n")
    f.write("    cmp r10, rcx\n")
    f.write("    jae .done\n")
    f.write("    cmp r10, rdx\n")
    f.write("    je .skip_i\n")
    f.write("    mov rax, [rsp + r10*8]\n")
    f.write("    mov [r11 + r9*8], rax\n")
    f.write("    inc r9\n")
    f.write(".skip_i:\n")
    f.write("    inc r10\n")
    f.write("    jmp .recon_loop\n")
    f.write("\n")
    f.write(".done:\n")
    f.write("    ; ora puntiamo rsp al nuovo top (original_rsp + 8) — stack ora contiene M-1 elementi\n")
    f.write("    lea rax, [r8 + 8]\n")
    f.write("    mov rsp, rax\n")
    f.write("\n")
    f.write(".ret:\n")
    f.write("    ret\n")
    
def stack_len_helpers(f):
    f.write("get_stack_len:\n")
    f.write("    mov rax, [rel StackBase]  ; rax = stack base salvato all'entry\n")
    f.write("    sub rax, rsp              ; rax = bytes usati\n")
    f.write("    cmp rax, 8\n")
    f.write("    jb .zero\n")
    f.write("    sub rax, 8                ; escludi il return address della CALL\n")
    f.write("    shr rax, 3                ; divide per 8 -> numero di qword\n")
    f.write("    ret\n")
    f.write(".zero:\n")
    f.write("    xor rax, rax\n")
    f.write("    ret\n")
    
def exit_helpers(f):
    f.write("exit_with_code:\n")
    f.write("    mov rax, [rsp + 8]    ; leggi il qword sotto il return address\n")
    f.write("    mov ecx, eax          ; primo argomento = codice di uscita (lower 32 bit)\n")
    f.write("    sub rsp, 32           ; shadow space per Windows x64\n")
    f.write("    call ExitProcess\n")
    f.write("    add rsp, 32\n")

def general_print(stack, f, debug = False):
    f.write("    ;Debug Dump\n" if debug else "    ;Dump\n")
    if debug:
        peek_top_to_reg(f, "rdx")
    else:
        pop_value(f, "rdx")
        
    f.write("    call print_number\n")
        

        
def memory_general_print(f, m):
    f.write("    ;Dump Rax\n")
    f.write("    mov rdx, %s\n" % m)
    f.write("    call print_number\n")
    
def string_print(stack, f, debug = False):
    if debug:
        f.write("    ;Debug Dump\n")
        peek_top_to_reg(f, "rcx")     # non-pop, solo peek
        f.write("    xor rax, rax\n")
        f.write("    sub rsp, 32\n")
        f.write("    call printf\n")
        f.write("    add rsp, 32\n")
    else:
        f.write("    ;Dump\n")
        pop_value(f, "rcx")           # pop -> aggiorna virtual_stack
        f.write("    xor rax, rax\n")
        f.write("    sub rsp, 32\n")
        f.write("    call printf\n")
        f.write("    add rsp, 32\n")
        
def printf(f):
    f.write("    ;Printf\n")
    f.write("    xor rax, rax\n")
    f.write("    sub rsp, 32\n")
    f.write("    call printf\n")
    f.write("    add rsp, 32\n")


def parse_string_var(s):
    # s is the full quoted string, e.g. '"foo\n"'
    specialchars = {
        "n": "10",
        "t": "9",
        "\\": str(ord("\\")),
        "\"": str(ord("\"")),
        "\'": str(ord("\'")),
    }

    pc = PC(s)
    result = []

    # expect starting quote
    if pc.peek() != '"':
        # fallback: parse as plain (no quotes)
        buff = ""
        while pc.peek() is not None:
            buff += pc.consume()
        if buff:
            result.append(buff)
        return result

    # consume opening quote and start quoted buffer including the opening quote
    pc.consume()
    buff = '"'

    while pc.peek() is not None:
        ch = pc.peek()
        if ch == '\\':
            # escape sequence
            pc.consume()            # consume '\'
            if pc.peek() is None:
                # trailing backslash: treat literally
                buff += '\\'
                break
            esc = pc.consume()
            if esc in specialchars:
                # close and append the quoted chunk
                buff += '"'           # append closing quote
                result.append(buff)
                buff = ""
                # append the escape as integer (e.g. 10)
                result.append(specialchars[esc])
                # if next char is closing quote, consume it (do NOT append it separately)
                if pc.peek() == '"':
                    pc.consume()
                # otherwise continue: if there are more characters they will form a new quoted chunk
                # so if next is not quote, start a new quoted chunk if next char exists
                if pc.peek() == '"':
                    # handled above
                    pass
                elif pc.peek() is not None:
                    # if there's more text (not starting with quote), start a new quoted chunk only if there is another opening quote
                    # but if it's more characters directly after escape (rare), start a new quoted chunk:
                    buff = '"'
            else:
                # unknown escape: treat literally as backslash + char
                buff += '\\' + esc
        elif ch == '"':
            # closing quote, consume and finish buffer
            pc.consume()
            buff += '"'
            result.append(buff)
            buff = ""
            break
        else:
            # normal character
            buff += pc.consume()

    # any remaining buffer (unclosed quote) — append as-is
    if buff:
        result.append(buff)

    return result
    
    
def generate_code_from_tokens(program, f, program_path,
                              stack=None,
                              if_context=None,
                              while_context=None,
                              counters=None):

    def check_math(stack_local, op):
        if len(stack_local) < 2 or stack_local[-1][0] != "int" or stack_local[-2][0] != "int":
            Error(f"'{op}' expects two ints.",
                  reason=f"Got {stack_local[-2][1] if len(stack_local) >= 2 else 'N/A'} as {stack_local[-2][0] if len(stack_local) >= 2 else 'N/A'} and {stack_local[-1][1] if len(stack_local) >= 1 else 'N/A'} as {stack_local[-1][0] if len(stack_local) >= 1 else 'N/A'}.",
                  file=program_path)

    def lbl_else_or_end(i): return f".L_ELSE_OR_END_{i}"
    def lbl_end(i): return f".L_END_{i}"
    def lbl_while_start(i): return f".L_WHILE_START_{i}"
    def lbl_while_end(i): return f".L_WHILE_END_{i}"

    # init mutable state if not provided (use virtual_stack as single source of truth)
    global virtual_stack
    if stack is None:
        stack = virtual_stack
    else:
        # synchronize virtual_stack with passed stack (caller may pass prefilled stack)
        virtual_stack[:] = stack
        stack = virtual_stack

    if if_context is None:
        if_context = []
    if while_context is None:
        while_context = []
    if counters is None:
        counters = {"if": 0, "while": 0}

    for i, (instr, (r, c)) in enumerate(program):
        op = instr[0]

        # PUSH
        if op == OP_PUSH:
            val = instr[1]
            push_imm(f, val)

        # PUSHSTRING
        elif op == OP_PUSHSTRING:
            sid, token = instr[1]
            f.write(f"    ;{token}\n")
            push_string_pointer(f, sid, token)

        # PLUS
        elif op == OP_PLUS:
            if len(stack) < 2:
                Error("stack must contain at least 2 values to perform 'sum'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            check_math(stack, "sum")
            f.write("    ;Add\n")
            a = pop_value(f, "rax")[1]
            b = pop_value(f, "rbx")[1]
            f.write("    add rax, rbx\n")
            push_rax(f, "int", a + b if (isinstance(a, int) and isinstance(b, int)) else None)

        # SUB
        elif op == OP_SUB:
            if len(stack) < 2:
                Error("stack must contain at least 2 values to perform 'sub'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            check_math(stack, "sub")
            f.write("    ;Sub\n")
            # pop order: top -> rbx, next -> rax ; then rax = rax - rbx
            a = pop_value(f, "rbx")[1]
            b = pop_value(f, "rax")[1]
            f.write("    sub rax, rbx\n")
            push_rax(f, "int", (b - a) if (isinstance(a, int) and isinstance(b, int)) else None)

        # MUL
        elif op == OP_MUL:
            if len(stack) < 2:
                Error("stack must contain at least 2 values to perform 'mul'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            check_math(stack, "mul")
            f.write("    ;Mul\n")
            a = pop_value(f, "rax")[1]
            b = pop_value(f, "rbx")[1]
            f.write("    imul rax, rbx\n")
            push_rax(f, "int", (a * b) if (isinstance(a, int) and isinstance(b, int)) else None)

        # IDIV
        elif op == OP_IDIV:
            if len(stack) < 2:
                Error("stack must contain at least 2 values to perform 'idiv'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            check_math(stack, "idiv")
            if isinstance(stack[-1][1], int) and stack[-1][1] == 0:
                Error("can't IDivide by 0", reason="division by zero", file=program_path, row=r, col=c)
            f.write("    ;IDiv\n")
            # pop divisor -> rbx, dividend -> rax
            a = pop_value(f, "rbx")[1]
            b = pop_value(f, "rax")[1]
            f.write("    cqo\n")
            f.write("    idiv rbx\n")
            push_reg(f, "rax", "int", (b // a) if (isinstance(a, int) and isinstance(b, int) and a != 0) else None)
            push_reg(f, "rdx", "int", (b % a) if (isinstance(a, int) and isinstance(b, int) and a != 0) else None)

        # PRINT (printf helper call)
        elif op == OP_PRINT:
            printf(f)

        # DUMP
        elif op == OP_DUMP:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform 'dump'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            top_type = stack[-1][0]
            if top_type == "string":
                string_print(stack, f)
            else:
                general_print(stack, f)

        # DEBUG DUMP
        elif op == OP_DEBUGDUMP:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform 'ddump'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            top_type = stack[-1][0]
            if top_type == "string":
                string_print(stack, f, True)
            else:
                general_print(stack, f, True)

        # DUMP MEMORY
        elif op == OP_DUMPMEMORY:
            mem = Memories[instr[1]]
            memory_general_print(f, mem)

        # TRASH
        elif op == OP_TRASH:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform 'trash'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            m = len(stack)
            idx_item = pop_value(f, "rax")
            if idx_item[0] != "int":
                Error("'trash' expects int index on top of stack",
                      reason=f"got {idx_item[0]}", file=program_path, row=r, col=c)
            idx = idx_item[1]
            if not isinstance(idx, int) or idx < 1 or idx > m:
                Error("'trash' index out of range.",
                      reason=f"index: {idx} / Stack Size: {m}", file=program_path, row=r, col=c)
            f.write("    ;Remove\n")
            f.write(f"    mov rcx, {m} ;stack element count\n")
            # pop index already done by pop_value above, so now remove nth
            f.write("    mov rdx, rax ;index\n")
            f.write("    call remove_nth\n")
            # update model: remove nth from virtual_stack (counting from top)
            del virtual_stack[-idx]

        # STACKLEN
        elif op == OP_STACKLEN:
            f.write("    ;Stack Len\n")
            f.write("    call get_stack_len ; put in rax\n")
            # not pushing model value automatically (caller may call push if needed)

        # STACKCLEAR
        elif op == OP_STACKCLEAR:
            f.write("    ;Stack Clear\n")
            f.write("    mov rsp, [rel StackBase]\n")
            virtual_stack.clear()

        # LOAD TO MEMORY (ltm.x)
        elif op == OP_LOADTOMEMORY:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform 'ltm'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            mem = Memories[instr[1]]
            f.write("    ;Load To Memory\n")
            popped = pop_value(f, mem)  # pop into register mem
            # already handled model pop

        # LOAD FROM MEMORY (lfm.x)
        elif op == OP_LOADFROMMEMORY:
            mem = Memories[instr[1]]
            f.write("    ;Load From Memory\n")
            push_reg(f, mem, "int", None)

        # DUP
        elif op == OP_DUP:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform 'dup'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            f.write("    ;Duplicate\n")
            f.write("    mov rax, [rsp]\n")
            push_rax(f, stack[-1][0], stack[-1][1])

        # USAGE (parser helper)
        elif op == OP_USAGE:
            tok, usage = instr[1]
            Error(f"wrong Usage of \"{tok}\"", fix=usage, file=program_path, row=r, col=c)

        # CALL
        elif op == OP_CALL:
            name = instr[1]
            f.write("    call %s\n" % name)
            # if function has sim_stack recorded, extend model accordingly (caller may have prepared args)
            if name in functions and "sim_stack" in functions[name]:
                for el in functions[name]["sim_stack"]:
                    virtual_stack.append(el)

        # EXIT (call helper)
        elif op == OP_EXIT:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform 'exit'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            code = pop_value(f, "rax")
            if code[0] != "int":
                Error("'exit' expects int err code", reason=f"got {code[0]}", file=program_path, row=r, col=c)
            f.write("    call exit_with_code\n")

        # CMP
        elif op == OP_CMP:
            cmp_type = instr[1]
            if len(stack) < 2:
                Error(f"stack must contain at least 2 values to perform a comparation: '{Comparators_rev.get(cmp_type, cmp_type)}'.",
                      reason=f"current stack size is: {len(stack)}.", file=program_path, row=r, col=c)
            f.write(f"    ;Comparator {Comparators_rev.get(cmp_type, cmp_type)}\n")
            # pop order: top -> rbx, next -> rax
            _rbx = pop_value(f, "rbx")[1]
            _rax = pop_value(f, "rax")[1]
            f.write("    cmp rax, rbx\n")
            if cmp_type == CMP_GT:
                f.write("    setg al\n")
            elif cmp_type == CMP_LT:
                f.write("    setl al\n")
            elif cmp_type == CMP_EQ:
                f.write("    sete al\n")
            elif cmp_type == CMP_NE:
                f.write("    setne al\n")
            elif cmp_type == CMP_GE:
                f.write("    setge al\n")
            elif cmp_type == CMP_LE:
                f.write("    setle al\n")
            else:
                Error(f"cannot generate code for comparation: {cmp_type}", file=program_path, row=r, col=c)
            f.write("    movzx rax, al\n")
            push_rax(f, "int", None)

        # LOGIC
        elif op == OP_LOGIC:
            logic_type, required_stack = instr[1]
            name = Logic_Gates_rev.get((logic_type, required_stack), str((logic_type, required_stack)))
            if len(stack) < required_stack:
                Error(f"stack must contain at least {required_stack} values to perform '{name}'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            f.write(f"    ;Logic Gate {name}\n")
            if required_stack > 1:
                _rbx = pop_value(f, "rbx")[1]
            _rax = pop_value(f, "rax")[1]
            if logic_type == LOGIC_NOT:
                f.write("    xor rax, 1\n")
            elif logic_type == LOGIC_AND:
                f.write("    and rax, rbx\n")
            elif logic_type == LOGIC_NAND:
                f.write("    and rax, rbx\n")
                f.write("    xor rax, 1\n")
            elif logic_type == LOGIC_XAND:
                f.write("    cmp rax, rbx\n")
                f.write("    sete al\n")
                f.write("    movzx rax, al\n")
            elif logic_type == LOGIC_OR:
                f.write("    or rax, rbx\n")
            elif logic_type == LOGIC_NOR:
                f.write("    or rax, rbx\n")
                f.write("    xor rax, 1\n")
            elif logic_type == LOGIC_XOR:
                f.write("    cmp rax, rbx\n")
                f.write("    setne al\n")
                f.write("    movzx rax, al\n")
            else:
                Error(f"cannot generate code for logic gate: {logic_type}", file=program_path, row=r, col=c)
            push_rax(f, "int", None)

        # IF
        elif op == OP_IF:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform: 'if'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            counters["if"] += 1
            if_context.append({"id": counters["if"], "has_else": False, "pos": (r, c), "else_pos": None, "last_i": i})
            pop_value(f, "rax")
            f.write("    test rax, rax\n")
            f.write(f"    jz {lbl_else_or_end(counters['if'])}\n")

        # ELSE
        elif op == OP_ELSE:
            if not if_context:
                Error("unexpected 'else'",
                      reason="there is no active IF block to negate.",
                      fix="remove 'else' or add a matching 'if' and 'endif'",
                      file=program_path, row=r, col=c)
            block = if_context[-1]
            block["has_else"] = True
            block["else_pos"] = (r, c)
            f.write(f"    jmp {lbl_end(block['id'])}\n")
            f.write(f"    {lbl_else_or_end(block['id'])}:\n")
            if block["last_i"] == i - 1:
                Warn("unused then block.", file=program_path, row=block["pos"][0], col=block["pos"][1])
            block["last_i"] = i

        # ENDIF
        elif op == OP_ENDIF:
            if not if_context:
                Error("unexpected 'endif'",
                      reason="there is no active IF block to close",
                      fix="remove 'endif' or add a matching 'if'",
                      file=program_path, row=r, col=c)
            block = if_context.pop()
            label = lbl_end(block["id"]) if block["has_else"] else lbl_else_or_end(block["id"])
            f.write(f"    {label}:\n")
            if block["last_i"] == i - 1:
                warn_pos = block["else_pos"] if block["has_else"] else block["pos"]
                Warn(f"unused {'else' if block['has_else'] else 'if'} block.",
                     file=program_path, row=warn_pos[0], col=warn_pos[1])

        # WHILE
        elif op == OP_WHILE:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform: 'while'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            counters["while"] += 1
            while_context.append({"id": counters["while"], "pos": (r, c), "last_i": i})
            pop_value(f, "rax")
            f.write(f"    {lbl_while_start(counters['while'])}:\n")
            f.write("    test rax, rax\n")
            f.write(f"    jz {lbl_while_end(counters['while'])}\n")

        # ENDWHILE
        elif op == OP_ENDWHILE:
            if len(stack) < 1:
                Error("stack must contain at least 1 value to perform: 'endwhile'",
                      reason=f"current stack size is: {len(stack)}", file=program_path, row=r, col=c)
            if not while_context:
                Error("unexpected 'endwhile'",
                      reason="there is no active WHILE block to close",
                      fix="remove 'endwhile' or add a matching 'while'",
                      file=program_path, row=r, col=c)
            block = while_context.pop()
            # At this point the body should have pushed the next condition; pop it into rax and jump
            pop_value(f, "rax")
            f.write(f"    jmp {lbl_while_start(block['id'])}\n")
            f.write(f"    {lbl_while_end(block['id'])}:\n")
            if block["last_i"] == i - 2:
                Warn("unused while block.", file=program_path, row=block["pos"][0], col=block["pos"][1])

        # Unknown operation
        else:
            Error(f"cannot generate code for operation index: {op}", file=program_path, row=r, col=c)

    # validation of unclosed blocks
    if len(if_context) > 0:
        r_opened, c_opened = if_context[-1]["pos"]
        Error(f"unclosed 'if' block", reason="the IF block was never terminated", fix="insert 'endif' at the end of the IF block", file=program_path, row=r_opened, col=c_opened)

    if len(while_context) > 0:
        r_opened, c_opened = while_context[-1]["pos"]
        Error(f"unclosed 'while' block", reason="the WHILE block was never terminated", fix="insert 'endwhile' at the end of the WHILE block", file=program_path, row=r_opened, col=c_opened)

    if len(functions_context) > 0:
        name = functions_context[-1]["name"]
        r_opened, c_opened = functions[name]["start_pos"]
        Error(f"unclosed 'func' block", reason="the FUNC block was never terminated", fix="insert 'endfunc' at the end of the FUNC block", file=program_path, row=r_opened, col=c_opened)

    # ritorna lo stato globale (ma è lo stesso virtual_stack)
    return virtual_stack, if_context, while_context, counters


def generate_code(program, temp_path, program_path):
    with open(temp_path, "w") as f:
        f.write("global main\n")
        for name in functions:
            f.write(f"global {name}\n")
            
        if H_PRINTF in helpers_needed:
            f.write("extern printf\n")
        f.write("extern ExitProcess\n")
        f.write("\n")
        f.write("section .data\n")
        f.write("StackBase dq 0\n")

        f.write("fmt db \"%d\",10,0\n")
        for i in strings:
            f.write("S_%d db %s,0\n" % (i[0], ','.join(parse_string_var(i[1]))))
        f.write("\n")
        f.write("section .text\n")

        if H_PRINTF in helpers_needed:
            print_helpers(f)
        if H_TRASH in helpers_needed:
            trash_helpers(f)
        if H_STACKLEN in helpers_needed:
            stack_len_helpers(f)
        if H_EXIT in helpers_needed:
            exit_helpers(f)

        f.write("main:\n")
        f.write("    sub rsp, 40\n")
        f.write("    mov [rel StackBase], rsp\n")

        stack, _, _, _ = generate_code_from_tokens(program, f, program_path)
                
        f.write("    xor ecx, ecx\n")
        f.write("    sub rsp, 32\n")
        f.write("    call ExitProcess\n")
        
        for name, func in functions.items():
            f.write(f"\n{name}:\n")
            virtual_stack[:] = stack
            generate_code_from_tokens(func["tokens"],f,program_path,stack)
            f.write(f"    ret\n")

def compile_program(program, temp_path, out_name, run):
    generate_code(program, temp_path, program_path)
    subprocess.call(["nasm","-f","win64",temp_path,"-o","%s.o" % out_name])
    subprocess.call(["gcc","%s.o" % out_name, "-o", "%s.exe" % out_name])
    if run:
        subprocess.call(["%s.exe" % out_name])

if __name__ == "__main__":
    arguments = sys.argv
    
    filename = arguments.pop(0)
    
    assert len(arguments) >= 1, "Atleast 1 argument"
    
    program_path = arguments.pop(0)
    tokens = tokenize_file(program_path)
    program = parse_program_from_tokens(tokens, program_path)
    run = False
    
    out_name = "a"
    temp_path = "temp.asm"
    if len(arguments) >= 1:
        if "-mtc" in arguments:
            Warn("/!\\ Manual Compilation STARTED /!\\")
            if subprocess.call(["nasm","-f","win64",temp_path,"-o","%s.o" % out_name]) == 0:
                Success("Created %s.o correctly!" % out_name)
            if subprocess.call(["gcc","%s.o" % out_name, "-o", "%s.exe" % out_name]) == 0: 
                Success("Created %s.exe correctly!" % out_name)
            exit(0)
        elif "-r" in arguments:
            run = True
    compile_program(program,temp_path, out_name, run)