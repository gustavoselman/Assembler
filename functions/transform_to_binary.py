def transform_to_binary(number: str) -> str:

    last_character = number[-1]
    number = number[:-1] if last_character.isalpha() else number

    if last_character.lower() == 'h':
        # hexadecimal
        decimal_value = int(number, 16)

    elif last_character.lower() == 'd':
        # decimal
        decimal_value = int(number)

    elif last_character.lower() == 'b':
        # binary
        return number.zfill(16)
    else:
        # decimal
        decimal_value = int(number)

    binary_representation = bin(decimal_value)[2:]
    return binary_representation.zfill(16)


if __name__ == '__main__':
    print(transform_to_binary('B3h'))
    print(transform_to_binary('B3H'))
    print(transform_to_binary('12d'))
    print(transform_to_binary('10'))
    print(transform_to_binary('101b'))
    print(transform_to_binary('9'))
