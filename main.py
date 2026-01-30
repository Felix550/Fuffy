from enum import Enum
import subprocess
import sys

i = 0
def ilda(reset = False):
    global i
    if reset:
        i = 0
    result = i
    i += 1
    return result

OP_PUSH = ilda(True)
OP_PUSHSTRING = ilda()
OP_PLUS = ilda()
OP_SUB = ilda()
OP_MUL = ilda()
OP_IDIV = ilda()
OP_PRINT = ilda()
OP_DUMP = ilda()
OP_DUMPMEMORY = ilda()
OP_DEBUGDUMP = ilda()
OP_REMOVE = ilda()
OP_STACKLEN = ilda()
OP_STACKCLEAR = ilda()
OP_LOADTOMEMORY = ilda()
OP_LOADMEMORY = ilda()
OP_USAGE = ilda()

H_PRINTF = ilda(True)
H_REMOVE = ilda()
H_STACKLEN = ilda()

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
        
def Error(msg, file=None, row=None, col=None):
    if file and row and col:
        print(f"{bcolors.FAIL}{file}:{row}:{col}: Error: {msg}{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}Error: {msg}{bcolors.ENDC}")
    exit(1)
    
def Warn(msg, file=None, row=None, col=None):
    if file and row and col:
        print(f"{bcolors.WARNING}{file}:{row}:{col}: Warning: {msg}{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Warning: {msg}{bcolors.ENDC}")
    
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

def Remove():
    return (OP_REMOVE, )

def StackLen():
    return (OP_STACKLEN, )

def StackClear():
    return (OP_STACKCLEAR, )

def LoadToMemory(x):
    return (OP_LOADTOMEMORY, x) #Pop Stack to Memory

def LoadMemory(x):
    return (OP_LOADMEMORY, x) #Push Memory to Stack

def Usage(tok,usage):
    return (OP_USAGE,(tok,usage)) #Error(f"Usage of \"{tok}\": {usage}")

Memories = {
    "a": "rax",
    "b": "rbx",
    "1": "rcx",
    "2": "rdx",
    "3": "r8",
    "4": "r9",
}

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
    "rem": {
        "function": Remove(),
        "helpers": [H_REMOVE]
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
    "ldm": {
        "function": Usage("ldm",f"ldm.[register]\nRegisters:\n\t{"\n\t".join([f".{k} : \"{v}\"" for k, v in Memories.items()])}"),
        "helpers": None
    }
}

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
                    while pc.peek() is not None and (pc.peek().isalpha() or pc.peek().isdigit() or pc.peek() == "."):
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
                else:
                    pc.consume()
                    continue
    return result

helpers_needed = []

def check_helper(helper):
    if not any(h in helpers_needed for h in helper):
        helpers_needed.extend(helper)

strings = []

def parse_program_from_tokens(tokens,program_path):
    result = []

    for tok, (r, c) in tokens:
        tok: str
        # number
        if tok.isdigit():
            result.append(Push(int(tok)))
            continue

        # string
        if tok.startswith('"') and tok.endswith('"'):
            id = 0 if len(strings) == 0 else strings[-1][0] + 1
            strings.append((id, tok))
            result.append(PushString((id, tok)))
            continue

        # comment
        if tok.startswith(";"):
            continue
        
        if tok.startswith("ltm."):
            _,rhs = tok.split(".")
            if rhs == "a" or rhs == "b":
                Warn(f"Direct manipulation of internal memory locations like \"{Memories[rhs]}\" with \"{tok}\" is strongly discouraged, since these addresses are reserved for the compiler’s internal operations.",program_path,r,c)
            result.append(LoadToMemory(rhs))
            continue
        
        if tok.startswith("ldm."):
            _,rhs = tok.split(".")
            result.append(LoadMemory(rhs))
            continue
        
        if tok.startswith("dump."):
            helpers = [H_PRINTF]
            
            _,rhs = tok.split(".")
            result.append(DumpMemory(rhs))
            check_helper(helpers)
            continue

        # keyword
        if tok in Keywords:
            kw = Keywords[tok]

            # function
            result.append(kw["function"])

            # helpers
            helpers = kw.get("helpers")
            if helpers:
                check_helper(helpers)

            continue

        # invalid token
        Error(f"\"{tok}\" is not a valid keyword",program_path,r,c)

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
    
def remove_helpers(f):
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
    f.write("    xor r12, r12         ; j = 0  (usiamo r12 ma non lo preserviamo; se preferisci usa r11/r10 alternativi)\n")
    f.write(".recon_loop:\n")
    f.write("    cmp r10, rcx\n")
    f.write("    jae .done\n")
    f.write("    cmp r10, rdx\n")
    f.write("    je .skip_i\n")
    f.write("    mov rax, [rsp + r10*8]\n")
    f.write("    mov [r11 + r12*8], rax\n")
    f.write("    inc r12\n")
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

def general_print(stack, f, debug = False):
    if debug:
        f.write("    ;Debug Dump\n")
        f.write("    mov rdx, [rsp]\n")
        f.write("    call print_number\n")
    else:
        f.write("    ;Dump\n")
        f.write("    pop rdx\n")
        f.write("    call print_number\n")
        stack.pop()
        
def memory_general_print(f,m):
    f.write("    ;Dump Rax\n")
    f.write("    mov rdx, %s\n" % m)
    f.write("    call print_number\n")
    
def string_print(stack, f, debug = False):
    if debug:
        f.write("    ;Debug Dump\n")
        f.write("    mov rcx, [rsp]\n")
        f.write("    xor rax, rax\n")
        f.write("    call printf\n")
    else:
        f.write("    ;Dump\n")
        f.write("    pop rcx\n")
        f.write("    xor rax, rax\n")
        f.write("    call printf\n")
        stack.pop()
        
def printf(f):
    f.write("    ;Printf\n")
    f.write("    xor rax, rax\n")
    f.write("    call printf\n")

def check_math(stack):
    assert str(stack[-1]).isdigit(), "Can't Do Math Operations with a String"

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

def generate_code(program, temp_path):
    stack = []
    with open(temp_path,"w") as f:
        f.write("global main\n")
        if H_PRINTF in helpers_needed:
            f.write("extern printf\n") 
        f.write("extern ExitProcess\n")
        f.write("\n")
        f.write("section .data\n")
        f.write("StackBase dq 0\n")
            
        f.write("fmt db \"%d\",10,0\n")
        for i in strings:
            f.write("S_%d db %s,0\n" % (i[0],','.join(parse_string_var(i[1]))))
        f.write("\n")
        f.write("section .text\n")
        
        if H_PRINTF in helpers_needed:
            print_helpers(f)
        if H_REMOVE in helpers_needed:
            remove_helpers(f)
        if H_STACKLEN in helpers_needed:
            stack_len_helpers(f)
            
        f.write("main:\n")
        f.write("    mov [rel StackBase], rsp\n")
            
        for i in program:
            if i[0] == OP_PUSH:
                f.write("    push %d\n" % i[1])
                stack.append(i[1])
            elif i[0] == OP_PUSHSTRING:
                f.write("    ;%s\n" % i[1][1])
                f.write("    lea rax, [rel S_%d]\n" % i[1][0])
                f.write("    push rax\n")
                stack.append(i[1][1])
            elif i[0] == OP_PLUS:
                assert len(stack) >= 2, "Stack must contain atleast 2 values to perform a sum"
                check_math(stack)
                f.write("    ;Add\n")
                f.write("    pop rax\n")
                f.write("    pop rbx\n")
                f.write("    add rax, rbx\n")
                f.write("    push rax\n")
                a, b = stack.pop(), stack.pop()
                stack.append(a + b)
            elif i[0] == OP_SUB:
                assert len(stack) >= 2, "Stack must contain atleast 2 values to perform a sub"
                check_math(stack)
                f.write("    ;Sub\n")
                f.write("    pop rbx\n")
                f.write("    pop rax\n")
                f.write("    sub rax, rbx\n")
                f.write("    push rax\n")
                a, b = stack.pop(), stack.pop()
                stack.append(b - a)
            elif i[0] == OP_MUL:
                assert len(stack) >= 2, "Stack must contain atleast 2 values to perform a sub"
                check_math(stack)
                f.write("    ;Sub\n")
                f.write("    pop rax\n")
                f.write("    pop rbx\n")
                f.write("    imul rax, rbx\n")
                f.write("    push rax\n")
                a, b = stack.pop(), stack.pop()
                stack.append(a * b)
            elif i[0] == OP_IDIV:
                assert len(stack) >= 2, "Stack must contain atleast 2 values to perform a sub"
                check_math(stack)
                f.write("    ;IDiv\n")
                f.write("    pop rbx\n")
                f.write("    pop rax\n")
                f.write("    cqo\n")
                f.write("    idiv rbx\n")
                f.write("    push rax\n")
                f.write("    push rdx\n")
                a, b = stack.pop(), stack.pop()
                stack.append(b // a)
                stack.append(b % a)
            elif i[0] == OP_PRINT:
                printf(f)
            elif i[0] == OP_DUMP:
                assert len(stack) >= 1, "Stack must contain atleast 1 value to perform a prt"
                if str(stack[-1]).startswith("\""):
                    string_print(stack,f)
                else:
                    general_print(stack,f)
            elif i[0] == OP_DEBUGDUMP:
                assert len(stack) >= 1, "Stack must contain atleast 1 value to perform a dprt"
                if str(stack[-1]).startswith("\""):
                    string_print(stack,f, True)
                else:
                    general_print(stack,f,True)
            elif i[0] == OP_DUMPMEMORY:
                mem = Memories[i[1]]
                memory_general_print(f,mem)
            elif i[0] == OP_REMOVE:
                assert len(stack) >= stack[-1], "Stack must contain atleast %d value to perform a rem" % stack[-1]
                f.write("    ;Remove\n")
                f.write("    mov rcx, %d ;stack element count\n" % len(stack))
                f.write("    pop rax\n")
                f.write("    mov rdx, rax ;index\n")
                f.write("    call remove_nth\n")
                a = -stack.pop()
                stack.pop(a)
            elif i[0] == OP_STACKLEN:
                f.write("    ;Stack Len\n")
                f.write("    call get_stack_len ; put in rax\n")
            elif i[0] == OP_STACKCLEAR:
                f.write("    ;Stack Clear\n")
                f.write("    mov rsp, [rel StackBase]\n")
                stack.clear()
            elif i[0] == OP_LOADTOMEMORY:
                mem = Memories[i[1]]
                f.write("    ;Load To Memory\n")
                f.write("    pop %s\n" % mem)
                stack.pop()
            elif i[0] == OP_LOADMEMORY:
                mem = Memories[i[1]]
                f.write("    ;Load Memory\n")
                f.write("    push %s\n" % mem)
                stack.append(None)
            elif i[0] == OP_USAGE:
                tok,usage = i[1]
                Error(f"Usage of \"{tok}\": {usage}")
            else:
                Error("Can Generate the following Operation Index: %s" % i[0])
        f.write("    xor ecx, ecx\n")
        f.write("    call ExitProcess\n")

def compile_program(program, temp_path, out_name, run):
    generate_code(program, temp_path)
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
    if len(arguments) >= 1:
        if arguments.pop(0) == "-r":
            run = True
    compile_program(program,"temp.asm", "a", run)