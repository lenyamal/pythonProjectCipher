class Alphabet:
    def __init__(self, size, first_big, first_small):
        self.size = size
        self.first_big = first_big
        self.first_small = first_small
        self.letters = [[self.match(i) for i in range(self.index(self.first_big),
                                                      self.index(self.first_big) + self.size)],
                        [self.match(i) for i in range(self.index(self.first_small),
                                                      self.index(self.first_small) + self.size)]]

    def index(self, char: chr) -> int:
        pass

    def match(self, index: int) -> chr:
        pass


class AlphabetRU(Alphabet):
    def __init__(self):
        super().__init__(33, 'А', 'а')

    def index(self, char: chr) -> int:
        if ord(self.first_big) <= ord(char) <= ord(self.first_big) + self.size - 1:
            if ord(char) > ord('Е'):
                return ord(char) + 1 - ord(self.first_big)
            return ord(char) - ord(self.first_big)
        if char == 'Ё':
            return ord('Е') + 1 - ord(self.first_big)
        if ord(self.first_small) <= ord(char) <= ord(self.first_small) + self.size - 1:
            if ord(char) > ord('е'):
                return ord(char) + 1 - ord(self.first_small) + self.size
            return ord(char) - ord(self.first_small) + self.size
        if char == 'ё':
            return ord('е') + 1 - ord(self.first_small) + self.size
        return -1

    def match(self, index: int) -> chr:
        if 0 <= index < self.index('Ё'):
            return chr(ord(self.first_big) + index % self.size)
        if index == self.index('Ё'):
            return 'Ё'
        if self.index('Ё') < index < self.size:
            return chr(ord(self.first_big) + index % self.size - 1)
        if index < self.index('ё'):
            return chr(ord(self.first_small) + index % self.size)
        if index == self.index('ё'):
            return 'ё'
        if self.index('ё') < index:
            return chr(ord(self.first_small) + index % self.size - 1)
        return '0'


class AlphabetEN(Alphabet):
    def __init__(self):
        super().__init__(26, 'A', 'a')

    def index(self, char: chr):
        if ord(self.first_big) <= ord(char) <= ord(self.first_big) + self.size:
            return ord(char) - ord(self.first_big)
        if ord(self.first_small) <= ord(char) <= ord(self.first_small) + self.size:
            return ord(char) + self.size - ord(self.first_small)
        return -1

    def match(self, index: int) -> chr:
        if index < self.size:
            return chr(ord(self.first_big) + index % self.size)
        return chr(ord(self.first_small) + index % self.size)


class Cipher:
    def __init__(self, alphabet: "Alphabet"):
        self.alphabet = alphabet


class Caesar(Cipher):

    def cipher(self, old_string: str, key: int) -> str:
        new_string = []
        for char in old_string:
            index = self.alphabet.index(char)
            if index != -1:
                new_string.append(self.alphabet.letters[index
                                                        // self.alphabet.size][(index + key)
                                                                               % self.alphabet.size])
            else:
                new_string.append(char)
        return ''.join(new_string)

    def decipher(self, string: str, key: int) -> str:
        return self.cipher(string, -key % self.alphabet.size)


class Vigenere(Cipher):

    def cipher(self, string: str, keyword: str) -> str:
        key = ''.join([keyword[i % len(keyword)] for i in
                       range(len(string))])
        new_string = []
        for i in range(len(string)):
            index = self.alphabet.index(string[i])
            if index != -1:
                new_string.append(self.alphabet.letters[index
                                                        // self.alphabet.size][(index
                                                                                + self.alphabet.index(key[i]))
                                                                               % self.alphabet.size])
            else:
                new_string.append(string[i])
        return ''.join(new_string)

    def decipher(self, string: str, keyword: str) -> str:
        new_keyword = []
        for char in keyword:
            index = self.alphabet.index(char)
            new_keyword.append(self.alphabet.letters[index
                                                     // self.alphabet.size][-index
                                                                            % self.alphabet.size])
        return self.cipher(string, ''.join(new_keyword))


class Hack(Cipher):
    def __init__(self, alphabet: "Alphabet"):
        super().__init__(alphabet)

    def hack(self, string: str) -> str:
        dictionary = {}
        for char in string:
            index = self.alphabet.index(char)
            if index != -1:
                dictionary[char.upper()] = dictionary.get(char.upper(), 0) + 1
        caesar = Caesar(self.alphabet)
        try:
            most_popular = max(dictionary.keys(), key=lambda x: dictionary[x])
            if self.alphabet.__class__.__name__ == "AlphabetEN":
                return caesar.decipher(string, ord(most_popular) - ord('E'))
            if self.alphabet.__class__.__name__ == "AlphabetRU":
                return caesar.decipher(string, ord(most_popular) - ord('О'))
        except:
            return caesar.decipher(string, 0)
