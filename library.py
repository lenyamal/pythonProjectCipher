class Alphabet:

    def index(char: chr) -> int:
        if ord('A') <= ord(char) <= ord('Z'):
            return ord(char) - ord('A')
        if ord('a') <= ord(char) <= ord('z'):
            return ord(char) + Alphabet.size - ord('a')
        return -1

    letters = [[chr(i) for i in range(ord('A'), ord('Z') + 1)], [chr(i)
               for i in range(ord('a'), ord('z') + 1)]]
    size = 26


class Caesar:

    def cipher(old_string: str, key: int) -> str:
        new_string = []
        for char in old_string:
            index = Alphabet.index(char)
            if index != -1:
                new_string.append(Alphabet.letters[index
                                  // Alphabet.size][(index + key)
                                  % Alphabet.size])
            else:
                new_string.append(char)
        return ''.join(new_string)

    def decipher(string: str, key: int) -> str:
        return Caesar.cipher(string, -key % Alphabet.size)


class Vigenere:

    def cipher(string: str, keyword: str) -> str:
        key = ''.join([keyword[i % len(keyword)] for i in
                      range(len(string))])
        new_string = []
        for i in range(len(string)):
            index = Alphabet.index(string[i])
            if index != -1:
                new_string.append(Alphabet.letters[index
                                  // Alphabet.size][(index
                                  + Alphabet.index(key[i]))
                                  % Alphabet.size])
            else:
                new_string.append(string[i])
        return ''.join(new_string)

    def decipher(string: str, keyword: str) -> str:
        new_keyword = []
        for char in keyword:
            index = Alphabet.index(char)
            new_keyword.append(Alphabet.letters[index
                               // Alphabet.size][-index
                               % Alphabet.size])
        return vigenere.cipher(string, ''.join(new_keyword))


def hack(string: str) -> str:
    dictionary = {}
    for char in string:
        index = Alphabet.index(char)
        if index != -1:
            dictionary[char.upper()] = dictionary.get(char.upper(), 0) \
                + 1
    try:
        most_popular = max(dictionary.keys(), key=lambda x: \
                           dictionary[x])
        return caesar.decipher(string, ord(most_popular) - ord('E'))
    except:
        return caesar.decipher(string, 0)
