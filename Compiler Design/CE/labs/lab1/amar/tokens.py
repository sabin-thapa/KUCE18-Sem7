from typing import Union, Mapping

from enum import Enum, auto
import keyword

reserved = keyword.kwlist

operatorsMappings: Mapping[str, str] = {
    '+': "PLUS",
    '-': "MINUS",
    '*': "MULT",
    '/': "DIV",
    '%': "MOD",
    '**': 'POW'
}

relationsMappings: Mapping[str, str] = {
    '=': "EQ",
    "<": "GREATER",
    ">": "SMALLER",
    "!": 'NOTEQ'
}

specialCharMappings: Mapping[str, str] = {
    '"': "DOUBLE_QUOTE",
    "'": "SINGLE_QUOTE",
    '#': "HASH",
    '(': 'PARAM_OPEN',
    ')': 'PARAM_CLOSE',
    '[': 'BRACKET_OPEN',
    ']': 'BRACKET_CLOSE',
    ':': 'DELIMITER_COLON',
    ',': "COMMA"
}


class TokenTypes(Enum):
    INT = auto()
    FLOAT = auto()
    STR = auto()
    IDENT = auto()
    RESERVED = auto()
    RELATION = auto()
    OPERATOR = auto()


class Token:
    def __init__(self, token_type: str, value: Union[int, str, None] = None):
        self.token_type: str = token_type
        self.value: Union[int, str] = value

    def __str__(self):
        return f"<{self.token_type},{self.value}>"

    def __repr__(self):
        return f"<{self.token_type},{self.value}>"
