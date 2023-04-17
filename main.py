#!/usr/bin/env python3

import parse as inp
import library as lib

args = inp.parser.parse_args()

if args.type.lower() == "caesar":
    executor = lib.Caesar
    key = int(args.key)
elif args.type.lower() == "vigenere":
    executor = lib.Vigenere
    key = args.key

if args.mode == "c":
    execute = executor.cipher
elif args.mode == "d":
    execute = executor.decipher

with open(args.input) as file:
    output = None if not args.output else open(args.output, "w")
    for string in file.readlines():
        if args.mode == "hack":
            print(lib.hack(string.rstrip()), file=output)
        else:
            print(execute(string.rstrip(), key), file=output)
