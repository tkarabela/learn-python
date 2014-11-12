#!/usr/bin/env python3

ENCODING_TABLE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--.."}

DECODING_TABLE = {code: letter for letter, code in ENCODING_TABLE.items()}


def latin_to_morse(text, ignore_other_characters=True):
    chunks = []

    for c in text.upper():
        if c in ENCODING_TABLE:
            chunks.append(ENCODING_TABLE[c])
        elif c.isspace():
            chunks.append("")
        else:
            if not ignore_other_characters:
                raise ValueError("Cannot encode character %r" % c)

    return "/".join(chunks)


def morse_to_latin(text):
    chunks = text.split("/")
    return "".join(DECODING_TABLE.get(chunk, " ") for chunk in chunks)


# -----------------------------------------------------------------------------
# tests
# -----------------------------------------------------------------------------

assert latin_to_morse("ALOHA") == ".-/.-../---/..../.-"
assert morse_to_latin(".-/.-../---/..../.-") == "ALOHA"

assert latin_to_morse("Oh, NO!") == "---/....//-./---"
assert morse_to_latin("---/....//-./---") == "OH NO"

try:
    latin_to_morse("!!!", ignore_other_characters=False)
    assert False
except ValueError:
    pass
