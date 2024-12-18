with open("../inputs/day17.txt") as f:
    lines = [line.strip() for line in f.readlines()]

a_value = int(lines[0].split(":")[1].strip())
b_value = int(lines[1].split(":")[1].strip())
c_value = int(lines[2].split(":")[1].strip())
instruction_pointer = 0
program = [int(i) for i in lines[4].split(":")[1].strip().split(",")]
print(a_value)
print(b_value)
print(c_value)
print(program)
p_len = len(program)
output = ""


def get_combo_operand(operand_in):
    match operand_in:
        case 0:
            return 0
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return a_value
        case 5:
            return b_value
        case 6:
            return c_value
        case 7:
            raise ValueError("7 is not a valid combo operand")


def adv(operand_in):
    global a_value
    a_value = a_value // (2 ** get_combo_operand(operand_in))


def bxl(operand_in):
    global b_value
    b_value = b_value ^ operand_in


def bst(operand_in):
    global b_value
    b_value = get_combo_operand(operand_in) % 8


def jnz(operand_in):
    global instruction_pointer
    if a_value == 0:
        return
    instruction_pointer = operand_in


def bxc(operand_in):
    global b_value
    b_value = b_value ^ c_value


def out(operand_in):
    global output
    output += str(get_combo_operand(operand_in) % 8) + ","


def bdv(operand_in):
    global b_value
    b_value = a_value // (2 ** get_combo_operand(operand_in))


def cdv(operand_in):
    global c_value
    c_value = a_value // (2 ** get_combo_operand(operand_in))


while instruction_pointer < p_len - 1:
    operator = program[instruction_pointer]
    operand = program[instruction_pointer + 1]
    match operator:
        case 0:
            adv(operand)
        case 1:
            bxl(operand)
        case 2:
            bst(operand)
        case 3:
            jnz(operand)
        case 4:
            bxc(operand)
        case 5:
            out(operand)
        case 6:
            bdv(operand)
        case 7:
            cdv(operand)
    if operator != 3 or a_value == 0:
        instruction_pointer += 2

print(f"A: {a_value}")
print(f"B: {b_value}")
print(f"C: {c_value}")
print(f"output: {output.strip(',')}")
