from functions.transform_to_binary import transform_to_binary
from opcode_dict import opcode_dict


def get_instructions(operation: str, mode: str, literal: str) -> (str, str):
    ''' Return a tuple with the instructions in binary format '''

    if mode == 'Label':
        return None, None

    instruction_1 = None
    instruction_2 = None
    if operation in opcode_dict:
        if mode in opcode_dict[operation]:
            opcodes = opcode_dict[operation][mode]

            # Ej: ['NOP'] or ['ADD', 'A', 'B'] or ['RET']
            if literal == None:
                literal = '0'

            opcode_1 = opcode_dict[operation][mode][0]
            instruction_1 = transform_to_binary(literal) + opcode_1

            if len(opcodes) == 2:
                opcode_2 = opcode_dict[operation][mode][1]
                instruction_2 = transform_to_binary(literal) + opcode_2

            return instruction_1, instruction_2

        else:
            print(f"\t- Mode {mode} not found in opcode_dict")
            return None, None
    else:
        print(f"\t- Operation {operation} not found in opcode_dict")
        return None, None


def get_operation(line: list) -> str:
    return line[0]


def get_mode_and_literal(line: list, data_dict: dict, labels_dict: dict) -> (str, str):
    mode = None
    literal = None

    operation = get_operation(line)
    # Verifica si la línea contiene operación válida en el diccionario de opcodes
    if operation in opcode_dict:
        modes = opcode_dict[operation]

        # Si la operacion no tiene argumentos para el modo - Ej: ['NOP']
        if len(line) == 1:
            mode = None
            literal = None

        # Si la operacion tiene un solo argumento para el modo
        elif len(line) == 2:
            # JMP or JEQ or JNE or JGT or JGE or JLT or JLE or JCR - Ej: ['JNE', '<label>']
            if operation[0] == 'J':
                arg_1 = line[1]
                if arg_1 in labels_dict:
                    mode = 'Ins'
                    literal = labels_dict[arg_1]

            # CALL - Ej: ['CALL', '<label>']
            elif operation == 'CALL':
                arg_1 = line[1]
                if arg_1 in labels_dict:
                    mode = 'Ins'
                    literal = labels_dict[arg_1]

            # PUSH A / PUSH B
            elif operation == 'PUSH':
                arg_1 = line[1]
                processed_arg_1, literal_1 = processed_argument(
                    arg_1, data_dict)
                mode = processed_arg_1
                literal = None

            # POP A / POP B
            elif operation == 'POP':
                arg_1 = line[1]
                processed_arg_1, literal_1 = processed_argument(
                    arg_1, data_dict)
                mode = processed_arg_1
                literal = None

            # SHR A / SHL A
            elif operation == 'SHR' or operation == 'SHL':
                arg_1 = line[1]
                mode = 'A'
                literal = None

            elif operation == 'ADD' or operation == 'SUB' or operation == 'AND' or operation == 'OR' or operation == 'XOR':
                arg_1 = line[1]
                processed_arg_1, literal_1 = processed_argument(
                    arg_1, data_dict)
                mode = processed_arg_1
                literal = literal_1

            # INC A / INC B / INC (Dir) / DEC A / DEC B / DEC (Dir)
            elif operation == 'INC' or operation == 'DEC':
                arg_1 = line[1]
                processed_arg_1, literal_1 = processed_argument(
                    arg_1, data_dict)
                mode = processed_arg_1
                literal = literal_1 if literal_1 != None else '1'

            elif operation == 'NOT':
                arg_1 = line[1]
                processed_arg_1, literal_1 = processed_argument(
                    arg_1, data_dict)
                mode = processed_arg_1
                literal = None

        # Si la operacion tiene dos argumentos para el modo - Ej: ['MOV', 'A', '(varA)']
        elif len(line) == 3:
            arg_1 = line[1]
            arg_2 = line[2]

            processed_arg_1, literal_1 = processed_argument(arg_1, data_dict)
            processed_arg_2, literal_2 = processed_argument(arg_2, data_dict)

            mode = "_".join([processed_arg_1, processed_arg_2])
            literal = literal_1 if literal_1 != None else literal_2

        else:
            mode = "Invalid operation"
            literal = ""

    else:
        if operation[-1] == ":":
            mode = "Label"
            literal = None
        else:
            mode = "Invalid operation"
            literal = None

    return mode, literal


def processed_argument(argument: str, data_dict: dict) -> (str, str):
    ''' Return a tuple with the processed argument and the literal if it exists '''

    if argument == '(A)' or argument == '(B)':
        processed_argument = argument
        literal = None

    elif argument[0] == '(' and argument[-1] == ')':
        processed_argument = '(DIR)'
        if argument[1:-1] in data_dict:             # (varA)
            literal = data_dict[argument[1:-1]]
        else:                                       # (10b)
            literal = argument[1:-1]

    elif argument == 'A' or argument == 'B':
        processed_argument = argument
        literal = None

    elif argument in data_dict:
        processed_argument = 'LIT'
        literal = data_dict[argument]

    else:
        processed_argument = 'LIT'
        literal = argument

    return processed_argument, literal


def get_data_lines(lines: list[list[str]]) -> list[list[str]]:
    index_data_line = lines.index(['DATA:'])
    index_code_line = lines.index(['CODE:'])

    data_lines = lines[index_data_line + 1:index_code_line]

    return data_lines


def get_code_lines(lines: list[list[str]]) -> list[list[str]]:
    index_code_line = lines.index(['CODE:'])

    code_lines = lines[index_code_line + 1:]

    return code_lines


def get_labels_dict(lines: list[list[str]]) -> dict[str, str]:
    ''' Return a dictionary with the labels and their memory direction '''

    labels_dict = dict()

    data_lines = get_data_lines(lines)
    code_lines = get_code_lines(lines)

    # se ocupan 2 instrucciones por cada variable guardada en DATA
    current_direction = len(data_lines) * 2

    for line in code_lines:
        if line[0][-1] == ':':
            labels_dict[line[0][:-1]] = str(current_direction)
        else:
            # POP y RET ocupan 2 instrucciones
            if get_operation(line) == 'POP' or get_operation(line) == 'RET':
                current_direction += 2
            else:
                current_direction += 1

    return labels_dict


if __name__ == "__main__":
    print(get_mode_and_literal(['NOT', 'A'], {
          'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    # print(get_mode_and_literal(['SUB', '(varC)'], {'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    # print(get_mode_and_literal(['AND', '(varC)'], {'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    # print(get_mode_and_literal(['OR', '(varC)'], {'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    # print(get_mode_and_literal(['XOR', '(varC)'], {'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    print(get_mode_and_literal(['NOT', 'B', 'A'], {
          'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    print(get_mode_and_literal(['NOT', '(Dir)', 'A'], {
          'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
    print(get_mode_and_literal(['NOT', '(B)', 'A'], {
          'varA': 0, 'varB': 1, 'varC': 2}, {'labelA': 0, 'labelB': 1}))
