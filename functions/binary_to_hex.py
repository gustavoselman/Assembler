def binary_to_hex(binario):
    # Calculate the necessary length for the hexadecimal representation to have 10 characters
    longitud_hexadecimal = (len(binario) + 3) // 4

    # Add zeros to the left so that the hexadecimal representation has the desired length
    binario = binario.zfill(longitud_hexadecimal * 4)

    # Convert the binary to hexadecimal
    # [2:] se utiliza para quitar el prefijo "0x" de la representación hexadecimal
    hexadecimal = hex(int(binario, 2))[2:]

    # Fill with zeros to the left so that the hexadecimal representation always has 10 characters
    hexadecimal = hexadecimal.zfill(10)

    return hexadecimal
