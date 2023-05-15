global res
global karp
global line_count


#function to convert decimal number to binary number
def decimal_to_binary(n):
    global karp
    if n>127 or n<0:
        # print('illegal immediate value')
        f.write('error in line '+ str(line_count) +': illegal immediate value')
        karp = False
        return
    res = ''
    while (n!=0):
        res = str(n%2) + res
        n=n//2
    if len(res)<7:
        res = '0'*(7-len(res)) + res
    return res

#function to read and get data
def process_data(x):
    f = open(x)
    code = []
    for i in f.readlines():
        if not(i.isspace()):
            code.append(i.strip())
    return code

#function to store variables
def check_variables(code):
    variables = []
    for i in code:
        if 'var' not in i.split():
            break
        variables.append(i.strip().split()[1])
    return variables

#function to store labels
def check_labels(instructions):
    labels = {}
    for i in instructions:
        if ':' in i:
            labels[i.strip().split()[0][:-1]] = decimal_to_binary(instructions.index(i))
    return labels

#function to assign memory to variables
def assign_var_memory(variables, n):
    d=dict()
    for i in variables:
        d[i]=decimal_to_binary(n)
        n+=1
    return d

#function to handle halt exception
def check_halt(instructions):
    hlt = 0
    check = True if 'hlt' in instructions[-1].split() else False
    for i in instructions:
        if 'hlt' in i.split():
            hlt += 1
    return hlt, check


# function to perform type-A encoding
def do_1(x):
    global res, karp
    if len(x) != 4:
        f.write('error in line '+ str(line_count) +': invalid instruction format')
        karp = False
        return
    try:
        res += opcodes[x[0]] + '00' + registers[x[1]] + registers[x[2]] + registers[x[3]] + '\n'
    except KeyError:
        karp = False
        # print('typos in register')
        f.write('error in line '+ str(line_count) +': typos in register')

# function to perform type-B encoding
def do_2(x):
    global res, karp
    if len(x) != 3:
        f.write('error in line '+ str(line_count) +': invalid instruction format')
        karp = False
        return
    if x[0] == 'mov':
        res += opcodes["movI"]
    else:
        res += opcodes[x[0]]
    if x[1] not in registers:
        karp = False
        f.write('error in line '+ str(line_count) +': typos in register')
        return
    try:
        res += '0' + registers[x[1]] + decimal_to_binary(int(x[2][1:])) + '\n'
    except:
        karp = False
        f.write(' error in line '+ str(line_count) +': ' + str(x[2]) + ' is not defined')

# function to perform type-C encoding
def do_3(x):
    global res, karp
    if len(x) != 3:
        f.write('error in line '+ str(line_count) +': invalid instruction format')
        karp = False
        return
    if x[0] == 'mov':
        res += opcodes["movR"]
    else:
        res += opcodes[x[0]]
    try:
        res += '00000' + registers[x[1]] + registers[x[2]] + '\n'
    except KeyError:
        karp = False
        # print('typos in register')
        f.write('error in line '+ str(line_count) +': typos in register')

# function to perform type-D encoding
def do_4(x):
    global res, karp
    if len(x) != 3:
        f.write('error in line '+ str(line_count) +': invalid instruction format')
        karp = False
        return
    if x[1] not in registers:
        karp = False
        # print('typos in register')
        f.write('error in line '+ str(line_count) +': typos in register')
    if x[2] not in variables:
        karp = False
        if x[1] in labels:
            # print('misuse of label as variable')
            f.write('error in line '+ str(line_count) +': misuse of label as variable')
            return
        else:
            # print('undefined variable')
            f.write('error in line '+ str(line_count) +': undefined variable, no variable named '+ str(x[2]))
            return
    res += opcodes[x[0]] + '0' + registers[x[1]] + var_memory[x[2]] + '\n'

# function to perform type-E encoding
def do_5(x):
    global res, karp
    if len(x) != 2:
        f.write('error in line '+ str(line_count) +': invalid instruction format')
        karp = False
        return
    if x[1] not in labels:
        karp = False
        if x[1] in variables:
            # print('misuse of variable as label')
            f.write('error in line '+ str(line_count) +': misuse of variable as label')
            return
        else:
            # print('undefined label')
            f.write('error in line '+ str(line_count) +': undefined label, no label named '+ str(x[1]))
            return
    res += opcodes[x[0]] + '0000' + labels[x[1]] + '\n'

# function to perform type-F encoding
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
#checking variables
variables = check_variables(code)
#getting instructions
instructions = code[len(variables):]
#checking labels
labels = check_labels(instructions)
#assigning variables memory
var_memory = assign_var_memory(variables,len(instructions))

#handling hlt errors
halt,last_halt = check_halt(instructions)
if not(last_halt) and halt>0:
    karp = False
    # print("hlt is not the last instruction")
    f.write('error: hlt is not the last instruction')
if halt>1:
    karp = False
    # print("more than one hlt instruction is present")
    f.write('error: more than one hlt instruction is present')
if halt == 0:
    karp = False
    # print("hlt instruction is missing")
    f.write('error: hlt instruction is missing')


res, line_count = '', len(variables)
for i in instructions:
    line_count+=1
    if karp:
        x = i.split()
        if 'var' in x and len(x)==2:
            karp = False
            # print("variable not declared at beginning")
            f.write('error in line '+ str(line_count) +': variable not declared at beginning')
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
            # print("illegal use of flags register")
            f.write('error in line '+ str(line_count) +': illegal use of flags register')
            break
        if x[0] not in inst_type.keys():
            karp = False
            # print("typos in instruction")
            f.write('error in line '+ str(line_count) +': typos in instruction, no instruction named '+ str(x[0]))
            break
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
else:
    print("an error was encountered while generating output")
f.close()