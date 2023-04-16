import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="path to input file", required=True)
parser.add_argument("-o", "--output", help="path to output file, default - console")
parser.add_argument(
    "-m",
    "--mode",
    help="'c' - to cipher, 'd' - to decipher, 'hack' - automatically hack Caesar cipher",
    required=True,
)
parser.add_argument(
    "-t",
    "--type",
    help="'caesar' - to use Caesar cipher, 'vigenere' - to use Vigenere cipher, required if not hack-mode",
)
parser.add_argument(
    "-k", "--key", help="keyword for cipher: required type 'int' for Caesar cipher and 'str' for Vigenere"
)
