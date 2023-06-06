import sys

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

def ee_execute(s):
    if s!="1101000000000000":
        opcode= s[:5]
        if opcode == "00000": #add
            rd=registers[s[7:10]]
            rs1=registers[s[10:13]]
            rs2 = registers[s[13:16]]
            result=rf[rs1]+rf[rs2]
            if result > 127:
                rf['FLAGS'][-4] = '1' #overflow flag
                rf[rd]=0
            else:
                rf['FLAGS'][-4] = '0'  # Clear flags
                rf[rd]=result


        elif opcode == "00001": #sub
            rd=registers[s[7:10]]
            rs1=registers[s[10:13]]
            rs2 = registers[s[13:16]]
            if rf[rs2]>rf[rs1]:
                rf['FLAGS'][-4] = '1' #overflow flag
                rf[rd]=0
            else:
                rf[rd]=rf[rs1]-rf[rs2]
                rf['FLAGS'][-4] = '0'  # Clear flags

            
        elif opcode == "00110":  # mul
            rd = registers[s[7:10]]
            rs1 = registers[s[10:13]]
            rs2 = registers[s[13:16]]
            result = rf[rs1] * rf[rs2]
            if result > 127:
                rf['FLAGS'][-4] = '1' #overflow flag
                rf[rd]=0
            else:
                rf['FLAGS'][-4] = '0'  # Clear flags
                rf[rd]=result


        elif opcode == "00111":  # div
            rs1 = registers[s[10:13]]
            rs2 = registers[s[13:16]]
            if rf[rs2] != 0:
                rf['R0'] = rf[rs1] // rf[rs2]
                rf['R1'] = rf[rs1] % rf[rs2]
                rf['FLAGS'][-4] = '0'  # Clear flags
            else:
                rf['FLAGS'][-4] = '1' #overflow flag
                rf['R0']=0
                rf['R1']=0
        
        elif opcode == "01110": #cmp
            rs1 = registers[s[10:13]]
            rs2 = registers[s[13:16]]
            if rf[rs1]>rf[rs2]:     #greater
                rf['FLAGS'][-2]='1' 
            elif rf[rs1]<rf[rs2]:   #less
                rf['FLAGS'][-3]='1'
            elif rf[rs1]==rf[rs2]:  #equal
                rf['FLAGS'][-1]='1'

        return False, pc+1
    else:
        return True, pc+1

opcodes = {
    "00000": "add", "00001": "sub", "00010": "movI", "00011": "movR",
    "00100": "ld" , "00101": "st" , "00110": "mul" , "00111": "div" ,
    "01000": "rs" , "01001": "ls" , "01010": "xor" , "01011": "or"  ,
    "01100": "and", "01101": "not", "01110": "cmp" , "01111": "jmp" ,
    "11100": "jlt", "11101": "jgt", "11111": "je"  , "11010": "hlt"
}

registers = {'000':'R0', '001':'R1', '010':'R2', '011':'R3', '100':'R4', '101':'R5', '110':'R6', '111':'FLAGS'}

rf = {'R0':0, 'R1':0, 'R2':0, 'R3':0, 'R4':0, 'R5':0, 'R6':0, 'FLAGS': '0000000000000000'}
erb = '000000000'

mem=[]
# f=open('i.txt')
# f1=open('o.txt','w')
for i in sys.stdin:
    mem.append(i.strip())
pc=0
halted=False

while(not halted):
    inst = mem[pc]
    halted, new_pc = ee_execute(inst)
    sys.stdout.write(decimal_to_binary(pc)+'        ')
    sys.stdout.write((f"{erb+decimal_to_binary(rf['R0'])} {erb+decimal_to_binary(rf['R1'])} {erb+decimal_to_binary(rf['R2'])} {erb+decimal_to_binary(rf['R3'])} {erb+decimal_to_binary(rf['R4'])} {erb+decimal_to_binary(rf['R5'])} {erb+decimal_to_binary(rf['R6'])} {rf['FLAGS']}\n"))
    pc = new_pc

for i in mem:
    sys.stdout.write(i+"\n")
if (len(mem)<128):
    sys.stdout.write("0000000000000000\n"*(128-len(mem)))
# print((f"{erb+decimal_to_binary(rf['R0'])} {erb+decimal_to_binary(rf['R1'])} {erb+decimal_to_binary(rf['R2'])} {erb+decimal_to_binary(rf['R3'])} {erb+decimal_to_binary(rf['R4'])} {erb+decimal_to_binary(rf['R5'])} {erb+decimal_to_binary(rf['R6'])} {rf['FLAGS']}"))
# f1.close()