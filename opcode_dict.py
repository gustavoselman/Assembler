opcode_dict = {
    'MOV': {
        'A_B': ['00000000010000100000'],
        'B_A': ['00000000001100000000'],
        'A_LIT': ['00000000010001100000'],
        'B_LIT': ['00000000001001100000'],
        'A_(DIR)': ['00000110010001000000'],
        'B_(DIR)': ['00000110001001000000'],
        '(DIR)_A': ['00000110000100000001'],
        '(DIR)_B': ['00000110000000100001'],
        'A_(B)': ['00000010010001000000'],
        'B_(B)': ['00000010001001000000'],
        '(B)_A': ['00000010000100000001'],
        '(B)_LIT': ['00000010000001100001']
    },
    'ADD': {
        'A_B': ['00000000010100100000'],
        'B_A': ['00000000001100100000'],
        'A_LIT': ['00000000010101100000'],
        'B_LIT': ['00000000001101100000'],
        'A_(DIR)': ['00000110010101000000'],
        'B_(DIR)': ['00000110001101000000'],
        '(DIR)': ['00000110000100100001'],
        'A_(B)': ['00000010010101000000'],
        'B_(B)': ['00000010001101000000'],
    },
    'SUB': {
        'A_B': ['00000000010100100100'],
        'B_A': ['00000000001100100100'],
        'A_LIT': ['00000000010101100100'],
        'B_LIT': ['00000000001101100100'],
        'A_(DIR)': ['00000110010101000100'],
        'B_(DIR)': ['00000110001101000100'],
        '(DIR)': ['00000110000100100101'],
        'A_(B)': ['00000010010101000100'],
        'B_(B)': ['00000010001101000100'],
    },
    'AND': {
        'A_B': ['00000000010100101000'],
        'B_A': ['00000000001100101000'],
        'A_LIT': ['00000000010101101000'],
        'B_LIT': ['00000000001101101000'],
        'A_(DIR)': ['00000110010101001000'],
        'B_(DIR)': ['00000110001101001000'],
        '(DIR)': ['00000110000100101001'],
        'A_(B)': ['00000010010101001000'],
        'B_(B)': ['00000010001101001000'],
    },
    'OR': {
        'A_B': ['00000000010100101100'],
        'B_A': ['00000000001100101100'],
        'A_LIT': ['00000000010101101100'],
        'B_LIT': ['00000000001101101100'],
        'A_(DIR)': ['00000110010101001100'],
        'B_(DIR)': ['00000110001101001100'],
        '(DIR)': ['00000110000100101101'],
        'A_(B)': ['00000010010101001100'],
        'B_(B)': ['00000010001101001100'],
    },
    'XOR': {
        'A_B': ['00000000010100110000'],
        'B_A': ['00000000001100110000'],
        'A_LIT': ['00000000010101110000'],
        'B_LIT': ['00000000001101110000'],
        'A_(DIR)': ['00000110010101010000'],
        'B_(DIR)': ['00000110001101010000'],
        '(DIR)': ['00000110000100110001'],
        'A_(B)': ['00000010010101010000'],
        'B_(B)': ['00000010001101010000'],
    },
    'NOT': {
        'A': ['00000000010100010100'],
        'B_A': ['00000000001100010100'],
        '(DIR)_A': ['00000110000100010101'],
        '(B)_A': ['00000010000100110101']
    },
    'SHL': {
        'A': ['00000000010100011100'],
        'B_A': ['00000000001100011100'],
        '(DIR)_A': ['00000110000100011101'],
        '(B)_A': ['00000010000100111101']
    },
    'SHR': {
        'A': ['00000000010100011000'],
        'B_A': ['00000000001100011000'],
        '(DIR)_A': ['00000110000100011001'],
        '(B)_A': ['00000010000100111001']
    },
    'INC': {
        'A': ['00000000110101100000'],
        'B': ['00000000001010100000'],
        '(DIR)': ['00000110000011000001'],
        '(B)': ['00000010000011000001']
    },
    'DEC': {
        'A': ['00000000110101100100']
    },
    'CMP': {
        'A_B': ['00000000000100100100'],
        'A_LIT': ['00000000000101100100'],
        'A_(DIR)': ['00000110000101000100'],
        'A_(B)': ['00000010000101000100']
    },
    'JMP': {
        'Ins': ['00100000000000000010']
    },
    'JEQ': {
        'Ins': ['00100000100000000010']
    },
    'JNE': {
        'Ins': ['00100001000000000010']
    },
    'JGT': {
        'Ins': ['00100001100000000010']
    },
    'JGE': {
        'Ins': ['10100000000000000010']
    },
    'JLT': {
        'Ins': ['10100000100000000010']
    },
    'JLE': {
        'Ins': ['10100001000000000010']
    },
    'JCR': {
        'Ins': ['10100001100000000010']
    },
    'NOP': {
        None: ['00000000000000000000']
    },
    'PUSH': {
        'A': ['00010100000100000001'],
        'B': ['00010100000000100001']
    },
    'POP': {
        'A': ['00001000100000000000', '00000100010001000000'],
        'B': ['00001001000000000000', '00000100001001000000']
    },
    'CALL': {
        'Ins': ['01110100000000000011']
    },
    'RET': {
        None: ['00001000000000000000', '00000100000000000011']
    }
}
