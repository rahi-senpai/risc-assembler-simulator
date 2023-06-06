import sys
global flag

def decimal_to_binary(n):
    res = ''
    while (n!=0):
        res = str(n%2) + res
        n=n//2
    if len(res)<7:
        res = '0'*(7-len(res)) + res
    return res

def binary_to_decimal(s):
    res=0
    for i in range((len(s))):
        res += int(s[i])*(2**(len(s)-i-1))
    return res

def ee_execute(s,pc):
    opcode= s[:5]
    if opcode == "00000": #add
        rd=registers[s[7:10]]
        rs1=registers[s[10:13]]
        rs2 = registers[s[13:16]]
        result=rf[rs1]+rf[rs2]
        if result > 127:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]=0
        else:
            rf[rd]=result
        return False, pc+1

    elif opcode == "00001": #sub
        rd=registers[s[7:10]]
        rs1=registers[s[10:13]]
        rs2 = registers[s[13:16]]
        if rf[rs2]>rf[rs1]:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]=0
        else:
            rf[rd]=rf[rs1]-rf[rs2]
        return False, pc+1

    elif opcode == "00110":  # mul
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        result = rf[rs1] * rf[rs2]
        if result > 127:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf[rd]=0
        else:
            rf[rd]=result
        return False, pc+1

    elif opcode == "00111":  # div
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        if rf[rs2] != 0:
            rf['R0'] = rf[rs1] // rf[rs2]
            rf['R1'] = rf[rs1] % rf[rs2]
        else:
            rf['FLAGS'] = '0000000000001000' #overflow flag
            rf['R0']=0
            rf['R1']=0
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
        rf[rd]=binary_to_decimal(s[9:16])
        return False, pc+1

    elif opcode == "00011": #movR
        rd = registers[s[10:13]]
        rs = registers[s[13:16]]
        if rs == 'FLAGS':
            rf[rd] = binary_to_decimal(rf[rs])
            rf['FLAGS'] = '0000000000000000'
        else:
            rf[rd] = rf[rs]
        return False, pc+1

    elif opcode == "01000": #rs
        imm = binary_to_decimal(s[9:16])
        rd = registers[s[6:9]]
        rf[rd] = rd>>imm
        return False, pc+1

    elif opcode == "01001": #ls
        imm = binary_to_decimal(s[9:16])
        rd = registers[s[6:9]]
        rf[rd] = rd<<imm
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
        rf[rd]=rf[rs1]^rf[rs2]
        return False, pc+1

    elif opcode == "01011": #or
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        rf[rd]=rf[rs1]|rf[rs2]
        return False, pc+1

    elif opcode == "01100": #and
        rd = registers[s[7:10]]
        rs1 = registers[s[10:13]]
        rs2 = registers[s[13:16]]
        rf[rd]=rf[rs1]&rf[rs2]
        return False, pc+1

    elif opcode == "01101": #not
        rd = registers[s[10:13]]
        rs = registers[s[13:16]]
        rf[rd] = ~rf[rs]
        return False, pc+1

    elif opcode == "00100": #ld
        addr = binary_to_decimal(s[9:16])
        r = registers[s[6:9]]
        if addr in variables:
            rf[r] = variables[addr]
        return False, pc+1

    elif opcode == "00101": #st
        addr = binary_to_decimal(s[9:16])
        r = registers[s[6:9]]
        variables[addr] = rf[r]
        return False, pc+1

    elif opcode == "11010": #hlt
        return True, pc+1


registers = {'000':'R0', '001':'R1', '010':'R2', '011':'R3', '100':'R4', '101':'R5', '110':'R6', '111':'FLAGS'}

variables = dict()

rf = {'R0':0, 'R1':0, 'R2':0, 'R3':0, 'R4':0, 'R5':0, 'R6':0, 'FLAGS': '0000000000000000'}
erb = '000000000'

mem=[]
for i in sys.stdin:
    mem.append(i.strip())
pc=0
halted=False

while(not halted):
    inst = mem[pc]
    halted, new_pc = ee_execute(inst,pc)
    sys.stdout.write(decimal_to_binary(pc)+'        ')
    sys.stdout.write((f"{erb+decimal_to_binary(rf['R0'])} {erb+decimal_to_binary(rf['R1'])} {erb+decimal_to_binary(rf['R2'])} {erb+decimal_to_binary(rf['R3'])} {erb+decimal_to_binary(rf['R4'])} {erb+decimal_to_binary(rf['R5'])} {erb+decimal_to_binary(rf['R6'])} {rf['FLAGS']}\n"))
    pc = new_pc

for i in variables.keys():
    mem.insert(i,erb+decimal_to_binary(variables[i]))
for i in mem:
    sys.stdout.write(i+"\n")
if (len(mem)<128):
    sys.stdout.write("0000000000000000\n"*(128-len(mem)))