global res
global karp

def decimal_to_binary(n):
    global karp
    if n>127:
        print('illegal immediate value')
        karp = False
    res = ''
    while (n!=0):
        res = str(n%2) + res
        n=n//2
    if len(res)<7:
        res = '0'*(7-len(res)) + res
    return res

def process_data(x):
    f = open(x)
    code = []
    for i in f.readlines():
        if not(i.isspace()):
            code.append(i.strip())
    return code

def check_variables(code):
    variables = []
    for i in code:
        if 'var' not in i.split():
            break
        variables.append(i.strip().split()[1])
    return variables

def check_labels(instructions):
    labels = {}
    for i in instructions:
        if ':' in i:
            labels[i.strip().split()[0][:-1]] = decimal_to_binary(instructions.index(i))
    return labels

def assign_var_memory(variables, n):
    d=dict()
    for i in variables:
        d[i]=decimal_to_binary(n)
        n+=1
    return d

def check_halt(instructions):
    hlt = 0
    check = True if 'hlt' in instructions[-1].split() else False
    for i in instructions:
        if 'hlt' in i.split():
            hlt += 1
    return hlt, check

def do_1(x):
    global res, karp
    try:
        res += opcodes[x[0]] + '00' + registers[x[1]] + registers[x[2]] + registers[x[3]] + '\n'
    except KeyError:
        karp = False
        print('typos in register')

def do_2(x):
    global res, karp
    if x[0] == 'mov':
        res += opcodes["movI"]
    else:
        res += opcodes[x[0]]
    try:
        res += '0' + registers[x[1]] + decimal_to_binary(int(x[2][1:])) + '\n'
    except KeyError:
        karp = False
        print('typos in register')

def do_3(x):
    global res, karp
    if x[0] == 'mov':
        res += opcodes["movR"]
    else:
        res += opcodes[x[0]]
    try:
        res += '00000' + registers[x[1]] + registers[x[2]] + '\n'
    except KeyError:
        karp = False
        print('typos in register')

def do_4(x):
    global res, karp
    if x[1] not in registers:
        karp = False
        print('typos in register')
    if x[2] not in variables:
        karp = False
        if x[1] in labels:
            print('misuse of label as variable')
            return
        else:
            print('undefined variable')
            return
    res += opcodes[x[0]] + '0' + registers[x[1]] + var_memory[x[2]] + '\n'

def do_5(x):
    global res, karp
    if x[1] not in labels:
        karp = False
        if x[1] in variables:
            print('misuse of variable as label')
            return
        else:
            print('undefined label')
            return
    res += opcodes[x[0]] + '0000' + labels[x[1]] + '\n'

def do_6(x):
    global res
    res += opcodes[x[0]] + '00000000000'


opcodes = {
    "add"  :"00000", "sub"  :"00001", "movI" :"00010", "movR" :"00011",
    "ld"   :"00100", "st"   :"00101", "mul"  :"00110", "div"  :"00111",
    "rs"   :"01000", "ls"   :"01001", "xor"  :"01010", "or"   :"01011",
    "and"  :"01100", "not"  :"01101", "cmp"  :"01110", "jmp"  :"01111",
    "jlt"  :"11100", "jgt"  :"11101", "je"   :"11111", "hlt"  :"11010"
}

inst_type = {
    "add"  :1, "sub"  :1, "movI" :2, "movR" :3,
    "ld"   :4, "st"   :4, "mul"  :1, "div"  :3,
    "rs"   :2, "ls"   :2, "xor"  :1, "or"   :1,
    "and"  :1, "not"  :3, "cmp"  :3, "jmp"  :5,
    "jlt"  :5, "jgt"  :5, "je"   :5, "hlt"  :6
}

registers = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}

karp = True
input_file = 'input.txt'
code = process_data(input_file)
f=open('output.txt','w')
variables = check_variables(code)
instructions = code[len(variables):]
labels = check_labels(instructions)
var_memory = assign_var_memory(variables,len(instructions))

halt,last_halt = check_halt(instructions)
if not(last_halt) and halt>0:
    karp = False
    print("hlt is not the last instruction")
if halt>1:
    karp = False
    print("more than one hlt instruction is present")
if halt == 0:
    karp = False
    print("hlt instruction is missing")

res=''
for i in instructions:
    if karp:
        x = i.split()
        if 'var' in x and len(x)==2:
            karp = False
            print("variable not declared at beginning")
            break
        if ':' in i:
            x = x[1:]
        if 'mov' in x:
            if '$' in x[2]:
                do_2(x)
            else:
                do_3(x)
            continue
        if 'FLAGS' in x:
            karp = False
            print("illegal use of flags register")
        if x[0] not in inst_type.keys():
            karp = False
            print("typos in instruction")
        y = inst_type[x[0]]
        if y == 1:
            do_1(x)
        if y == 2:
            do_2(x)
        if y == 3:
            do_3(x)
        if y == 4:
            do_4(x)
        if y == 5:
            do_5(x)
        if y == 6:
            do_6(x)

if karp:
    f.write(res)
    print("output generated successfully in output.txt")
f.close()