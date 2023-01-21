def char_to_binary(a):
    char_ascii = ord(a)
    div = []
    result = ''
    for i in range(8):
        temp = char_ascii % 2
        div.append(temp)
        char_ascii = int(char_ascii / 2)
    for i in div[::-1]:
        result += str(i)
    return result


def binary_to_char(a):
    i = 7
    char_ascii = 0
    while i >= 0:
        char_ascii += int(a[7-i]) * (2**i)
        i -= 1
    return chr(char_ascii)

