# for floating point numbers it is assumed that they are normalised numbers, i.e. (1+m)
# we calculated the range of floating point numbers, with 3 as bias for exponent and exponent ranges in [-2,3], to be [0.01, 15.75]
# and since we have only 5 bits for mantissa, we are limited to very few values for floating point numbers
# and we are not approximating the floating point number to the nearest one rather considering only exact value
import sys
global res
global karp
global line_count


#function to convert decimal number to binary number
def decimal_to_binary(n):
    global karp
    if n>127 or n<0:
        # print('illegal immediate value')
        sys.stdout.write('error in line '+ str(line_count) +': illegal immediate value\n')
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
def process_data():
    # f = open(x)
    code = []
    for i in sys.stdin:
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
        sys.stdout.write('error in line '+ str(line_count) +': invalid instruction format\n')
        karp = False
        return
    try:
        res += opcodes[x[0]] + '00' + registers[x[1]] + registers[x[2]] + registers[x[3]] + '\n'
    except KeyError:
        karp = False
        # print('typos in register')
        sys.stdout.write('error in line '+ str(line_count) +': typos in register\n')

# function to perform type-B encoding
def do_2(x):
    global res, karp
    if len(x) != 3:
        sys.stdout.write('error in line '+ str(line_count) +': invalid instruction format\n')
        karp = False
        return
    if x[0] == 'mov':
        res += opcodes["movI"]
    else:
        res += opcodes[x[0]]
    if x[1] not in registers:
        karp = False
        sys.stdout.write('error in line '+ str(line_count) +': typos in register\n')
        return
    try:
        res += '0' + registers[x[1]] + decimal_to_binary(int(x[2][1:])) + '\n'
    except:
        karp = False
        sys.stdout.write(' error in line '+ str(line_count) +': ' + str(x[2]) + ' is not defined\n')

# function to perform type-C encoding
def do_3(x):
    global res, karp
    if len(x) != 3:
        sys.stdout.write('error in line '+ str(line_count) +': invalid instruction format\n')
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
        sys.stdout.write('error in line '+ str(line_count) +': typos in register\n')

# function to perform type-D encoding
def do_4(x):
    global res, karp
    if len(x) != 3:
        sys.stdout.write('error in line '+ str(line_count) +': invalid instruction format\n')
        karp = False
        return
    if x[1] not in registers:
        karp = False
        # print('typos in register')
        sys.stdout.write('error in line '+ str(line_count) +': typos in register\n')
    if x[2] not in variables:
        karp = False
        if x[1] in labels:
            # print('misuse of label as variable')
            sys.stdout.write('error in line '+ str(line_count) +': misuse of label as variable\n')
            return
        else:
            # print('undefined variable')
            sys.stdout.write('error in line '+ str(line_count) +': undefined variable, no variable named '+ str(x[2])+'\n')
            return
    res += opcodes[x[0]] + '0' + registers[x[1]] + var_memory[x[2]] + '\n'

# function to perform type-E encoding
def do_5(x):
    global res, karp
    if len(x) != 2:
        sys.stdout.write('error in line '+ str(line_count) +': invalid instruction format\n')
        karp = False
        return
    if x[1] not in labels:
        karp = False
        if x[1] in variables:
            # print('misuse of variable as label')
            sys.stdout.write('error in line '+ str(line_count) +': misuse of variable as label\n')
            return
        else:
            # print('undefined label')
            sys.stdout.write('error in line '+ str(line_count) +': undefined label, no label named '+ str(x[1])+'\n')
            return
    res += opcodes[x[0]] + '0000' + labels[x[1]] + '\n'

# function to perform type-F encoding
def do_6(x):
    global res
    res += opcodes[x[0]] + '00000000000'

# function to perform movf(8bit immediate)
def do_22(x):
    global res, karp
    di = {0.5: '1', 0.75: '11', 0.625: '101', 0.875: '111', 0.5625: '1001', 0.6875: '1011', 0.8125: '1101', 0.9375: '1111',
          0.53125: '10001', 0.59375: '10011', 0.65625: '10101', 0.71875: '10111', 0.78125: '11001', 0.84375: '11011', 
          0.90625: '11101', 0.96875: '11111', 0.25: '01', 0.125: '001', 0.375: '011', 0.0625: '0001', 0.1875: '0011', 
          0.3125: '0101', 0.4375: '0111', 0.03125: '00001', 0.09375: '00011', 0.15625: '00101', 0.21875: '00111', 
          0.28125: '01001', 0.34375: '01011', 0.40625: '01101', 0.46875: '01111'}
    if float(x[2][1:])>=0.01 and float(x[2][1:])<=15.75:
        f = bin(int(float(x[2][1:])))[2:]
        if (float(x[2][1:]) - int(float(x[2][1:]))) not in di.keys():
            karp = False
            sys.stdout.write('error in line '+ str(line_count) +': the floating number cant be represented in given system\n')
            return
        d = di[float(x[2][1:]) - int(float(x[2][1:]))]
        if len(f)>=1 and len(d)+len(f)-1<=5:
            cat = f[1:]+d
            if len(cat)<5:
                cat += '0'*(5-len(cat))
            res += opcodes[x[0]] + registers[x[1]] + format((len(f)-1+3),'03b') + cat + '\n'
        else:
            karp = False
            sys.stdout.write('error in line '+ str(line_count) +': the floating number cant be represented in given system\n')
    else:
        karp = False
        sys.stdout.write('error in line '+ str(line_count) +': the floating number is out of range\n')


opcodes = {
    "add"  :"00000", "sub"  :"00001", "movI" :"00010", "movR" :"00011",
    "ld"   :"00100", "st"   :"00101", "mul"  :"00110", "div"  :"00111",
    "rs"   :"01000", "ls"   :"01001", "xor"  :"01010", "or"   :"01011",
    "and"  :"01100", "not"  :"01101", "cmp"  :"01110", "jmp"  :"01111",
    "jlt"  :"11100", "jgt"  :"11101", "je"   :"11111", "hlt"  :"11010",
    "addf" :"10000", "subf" :"11001", "movf" :"11010"
}

inst_type = {
    "add"  :1, "sub"  :1, "movI" :2, "movR" :3,
    "ld"   :4, "st"   :4, "mul"  :1, "div"  :3,
    "rs"   :2, "ls"   :2, "xor"  :1, "or"   :1,
    "and"  :1, "not"  :3, "cmp"  :3, "jmp"  :5,
    "jlt"  :5, "jgt"  :5, "je"   :5, "hlt"  :6,
    "addf" :1, "subf" :1, "movf" :22
}

registers = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}

karp = True
input_file = 'input.txt'
code = process_data()

# f=open('output.txt','w')
#checking variables
variables = check_variables(code)
#getting instructions
instructions = code[len(variables):]
#checking labels
labels = check_labels(instructions)
#assigning variables memory
var_memory = assign_var_memory(variables,len(instructions))

if len(code)>128:
    karp = False
    sys.stdout.write('error: number of instructions are more than 128\n')

#handling hlt errors
halt,last_halt = check_halt(instructions)
if not(last_halt) and halt>0:
    karp = False
    # print("hlt is not the last instruction")
    sys.stdout.write('error: hlt is not the last instruction\n')
if halt>1:
    karp = False
    # print("more than one hlt instruction is present")
    sys.stdout.write('error: more than one hlt instruction is present\n')
if halt == 0:
    karp = False
    # print("hlt instruction is missing")
    sys.stdout.write('error: hlt instruction is missing\n')

res, line_count = '', len(variables)
for i in instructions:
    line_count+=1
    if karp:
        x = i.split()
        if 'var' in x and len(x)==2:
            karp = False
            # print("variable not declared at beginning")
            sys.stdout.write('error in line '+ str(line_count) +': variable not declared at beginning\n')
            break
        if ':' in i:
            x = x[1:]
        if 'mov' in x:
            if x[1] == 'FLAGS':
                karp = False
                sys.stdout.write('error '+ str(line_count) +': illegal use of flags register\n')
            if '$' in x[2]:
                do_2(x)
            else:
                do_3(x)
            continue
        if 'FLAGS' in x:
            karp = False
            # print("illegal use of flags register")
            sys.stdout.write('error in line '+ str(line_count) +': illegal use of flags register\n')
            break
        if x[0] not in inst_type.keys():
            karp = False
            # print("typos in instruction")
            sys.stdout.write('error in line '+ str(line_count) +': typos in instruction, no instruction named '+ str(x[0])+'\n')
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
        if y == 22:
            do_22(x)


if karp:
    sys.stdout.write(res)
    # print("output generated successfully in output.txt")
# else:
    # print("an error was encountered while generating output")
# f.close()