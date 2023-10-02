import sys

def pc_conversion(n):
    res = ''
    while (n!=0):
        res = str(n%2) + res
        n=n//2
    if len(res)<7:
        res = '0'*(7-len(res)) + res
    return res

def decimal_to_binary(n):
    res = ''
    while (n!=0):
        res = str(n%2) + res
        n=n//2
    if len(res)<16:
        res = '0'*(16-len(res)) + res
    return res

def binary_to_decimal(s):
    res=0
    for i in range((len(s))):
        res += int(s[i])*(2**(len(s)-i-1))
    return res

def binary_to_float(s):
    res=0
    exp = s[8:11]
    return res

def ee_execute(s,pc):
    opcode= s[:5]
    if opcode == "00000": #add
        rd=registers[s[7:10]]
        rs1=registers[s[10:13]]
        rs2 = registers[s[13:16]]
        result=decimal_to_binary(binary_to_decimal(rf[rs1])+binary_to_decimal(rf[rs2]))
        if result > '1111111111111111':
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]='0000000000000000'
        else:
            rf[rd]=result
            rf['FLAGS'] = '0000000000000000'
        return False, pc+1

    elif opcode == "00001": #sub
        rd=registers[s[7:10]]
        rs1=registers[s[10:13]]
        rs2 = registers[s[13:16]]
        if rf[rs2]>rf[rs1]:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]='0000000000000000'
        else:
            rf[rd]=decimal_to_binary(binary_to_decimal(rf[rs1])-binary_to_decimal(rf[rs2]))
            rf['FLAGS'] = '0000000000000000'
        return False, pc+1

    elif opcode == "00110":  # mul
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        result = decimal_to_binary(binary_to_decimal(rf[rs1]) * binary_to_decimal(rf[rs2]))
        if result > '1111111111111111':
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]='0000000000000000'
        else:
            rf[rd]=result
            rf['FLAGS'] = '0000000000000000'
        return False, pc+1

    elif opcode == "00111":  # div
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        if rf[rs2] != 0:
            rf['R0'] = decimal_to_binary(binary_to_decimal(rf[rs1]) // binary_to_decimal(rf[rs2]))
            rf['R1'] = decimal_to_binary(binary_to_decimal(rf[rs1]) % binary_to_decimal(rf[rs2]))
            rf['FLAGS'] = '0000000000000000'
        else:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf['R0']='0000000000000000'
            rf['R1']='0000000000000000'
        return False, pc+1

    elif opcode == "01110": #cmp
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        if rf[rs1]>rf[rs2]:     #greater
            rf['FLAGS']='0000000000000010' 
        elif rf[rs1]<rf[rs2]:   #less
            rf['FLAGS']='0000000000000100'
        elif rf[rs1]==rf[rs2]:  #equal
            rf['FLAGS']='0000000000000001'
        return False, pc+1

    elif opcode == "00010": #movI
        rd=registers[s[6:9]]
        rf[rd]=decimal_to_binary(binary_to_decimal(s[9:16]))
        return False, pc+1

    elif opcode == "00011": #movR
        rd = registers[s[10:13]]
        rs = registers[s[13:16]]
        if rs == 'FLAGS':
            rf[rd] = rf[rs]
            # rf['FLAGS'] = '0000000000000000'
        else:
            rf[rd] = rf[rs]
        return False, pc+1

    elif opcode == "01000": #rs
        imm = binary_to_decimal(s[9:16])
        rd = registers[s[6:9]]
        rf[rd] = decimal_to_binary(binary_to_decimal(rf[rd])>>imm)
        return False, pc+1

    elif opcode == "01001": #ls
        imm = binary_to_decimal(s[9:16])
        rd = registers[s[6:9]]
        rf[rd] = decimal_to_binary(binary_to_decimal(rf[rd])<<imm)
        return False, pc+1

    elif opcode == "01111": #jmp
        pc = binary_to_decimal(s[9:16])
        return False, pc

    elif opcode == "11100": #jlt
        if rf['FLAGS'][-3]=='1':
            rf['FLAGS'] = '0000000000000000'
            pc = binary_to_decimal(s[9:16])
            return False, pc
        rf['FLAGS'] = '0000000000000000'
        return False, pc+1

    elif opcode == "11101": #jgt
        if rf['FLAGS'][-2]=='1':
            rf['FLAGS'] = '0000000000000000'
            pc = binary_to_decimal(s[9:16])
            return False, pc
        rf['FLAGS'] = '0000000000000000'
        return False, pc+1

    elif opcode == "11111": #je
        if rf['FLAGS'][-1]=='1':
            rf['FLAGS'] = '0000000000000000'
            pc = binary_to_decimal(s[9:16])
            return False, pc
        rf['FLAGS'] = '0000000000000000'
        return False, pc+1

    elif opcode == "01010": #xor
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        rf[rd]=decimal_to_binary(binary_to_decimal(rf[rs1]) ^ binary_to_decimal(rf[rs2]))
        return False, pc+1

    elif opcode == "01011": #or
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        rf[rd]=decimal_to_binary(binary_to_decimal(rf[rs1]) | binary_to_decimal(rf[rs2]))
        return False, pc+1

    elif opcode == "01100": #and
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        rf[rd]=decimal_to_binary(binary_to_decimal(rf[rs1]) & binary_to_decimal(rf[rs2]))
        return False, pc+1

    elif opcode == "01101": #not
        rd = registers[s[10:13]]
        rs = registers[s[13:16]]
        abc = rf[rs]
        rez = ''
        for m in abc:
            if m=='0':
                rez+='1'
            else:
                rez+='0'
        rf[rd] = rez
        return False, pc+1

    elif opcode == "00100": #ld
        addr = binary_to_decimal(s[9:16])
        r = registers[s[6:9]]
        if addr in variables:
            rf[r] = variables[addr]
        else:
            rf[r] = '0000000000000000'
            vars.append(addr)
            variables[addr] = '0000000000000000'
        return False, pc+1

    elif opcode == "00101": #st
        addr = binary_to_decimal(s[9:16])
        r = registers[s[6:9]]
        if addr not in vars:
            vars.append(addr)
        variables[addr] = rf[r]
        return False, pc+1

    elif opcode == "11010": #hlt
        rf['FLAGS'] = '0000000000000000'
        return True, pc+1

    elif opcode == "10000": #addf
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        result=rf[rs1]+rf[rs2]
        if result > 127:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]=0
        else:
            rf[rd]=result
            rf['FLAGS'] = '0000000000000000'
        return True, pc+1

    elif opcode == "11001": #subf
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        if rf[rs2]>rf[rs1]:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]=0
        else:
            rf[rd]=rf[rs1]-rf[rs2]
            rf['FLAGS'] = '0000000000000000'
        return True, pc+1

    elif opcode == "11010": #movf
        rd = registers[s[5:8]]
        rf[rd]=binary_to_float(s[8:16])
        return True, pc+1


registers = {'000':'R0', '001':'R1', '010':'R2', '011':'R3', '100':'R4', '101':'R5', '110':'R6', '111':'FLAGS'}

di = {0.5: '1', 0.75: '11', 0.625: '101', 0.875: '111', 0.5625: '1001', 0.6875: '1011', 0.8125: '1101', 0.9375: '1111',
        0.53125: '10001', 0.59375: '10011', 0.65625: '10101', 0.71875: '10111', 0.78125: '11001', 0.84375: '11011', 
        0.90625: '11101', 0.96875: '11111', 0.25: '01', 0.125: '001', 0.375: '011', 0.0625: '0001', 0.1875: '0011', 
        0.3125: '0101', 0.4375: '0111', 0.03125: '00001', 0.09375: '00011', 0.15625: '00101', 0.21875: '00111', 
        0.28125: '01001', 0.34375: '01011', 0.40625: '01101', 0.46875: '01111'}

vars = []
variables = dict()

rf = {'R0':'0000000000000000', 'R1':'0000000000000000', 'R2':'0000000000000000', 'R3':'0000000000000000', 'R4':'0000000000000000', 'R5':'0000000000000000', 'R6':'0000000000000000', 'FLAGS': '0000000000000000'}

mem=[]
# f=open('i.txt')
for i in sys.stdin:
    mem.append(i.strip())
pc=0
halted=False

while(not halted):
    inst = mem[pc]
    halted, new_pc = ee_execute(inst,pc)
    sys.stdout.write(pc_conversion(pc)+'        ')
    sys.stdout.write((f"{rf['R0']} {rf['R1']} {rf['R2']} {rf['R3']} {rf['R4']} {rf['R5']} {rf['R6']} {rf['FLAGS']}\n"))
    pc = new_pc

vars.sort()
for i in vars:
    mem.insert(i,variables[i])
for i in mem:
    sys.stdout.write(i+"\n")
if (len(mem)<128):
    sys.stdout.write("0000000000000000\n"*(128-len(mem)))