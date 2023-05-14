global res

def decimal_to_binary(n):
    if n>127:
        pass
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

def check_variables(instructions):
    variables = []
    for i in instructions:
        if 'var' not in i:
            break
        variables.append(i.strip().split()[1])
    return variables

def check_labels(instructions):
    labels = []
    for i in instructions:
        if ':' in i:
            labels.append((i.strip().split()[0]),instructions.index(i))
    return labels

def assign_var_memory(variables, n):
    d=dict()
    for i in variables:
        n+=1
        d[i]=decimal_to_binary(n)
    return d

def do_1(x):
    global res
    res += opcodes[x[0]] + '00' + registers[x[1]] + registers[x[2]] + registers[x[3]] + '\n'

def do_2(x):
    global res
    if x[0] == 'mov':
        res += opcodes["movI"]
    else:
        res += opcodes[x[0]]
    res += '0' + registers[x[1]] + decimal_to_binary(int(x[2][1:])) + '\n'

def do_3(x):
    global res
    if x[0] == 'mov':
        res += opcodes["movR"]
    else:
        res += opcodes[x[0]]
    res += '00000' + registers[x[1]] + registers[x[2]] + '\n'

def do_4(x):
    global res
    res += opcodes[x[0]] + '0' + registers[x[1]] + var_memory[x[2]] + '\n'

def do_5(x):
    global res
    res = opcodes[x[0]] + '0000' + labels[x[1]] + '\n'

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

input_file = 'input.txt'
code = process_data(input_file)
variables = check_variables(code)
instructions = code[len(variables):]
labels = check_labels(instructions)
var_memory = assign_var_memory(variables,len(instructions))

res=''
for i in instructions:
    x = i.split()
    if x[0] == 'mov':
        if '$' in x[2]:
            do_2(x)
        else:
            do_3(x)
        continue
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

f=open('output.txt','w')
f.write(res)
f.close()
print("output generated successfully in output.txt")