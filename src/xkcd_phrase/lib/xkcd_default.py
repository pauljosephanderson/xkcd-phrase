"""Default Settings file for xkcd_pass modules."""
from typing import List, Callable, Dict

""" Set Default values """
DEFAULT_WORDFILE = "eff-long"
MIN_LENGTH = 4
MAX_LENGTH = 9
NUM_WORDS = 4
ACROSTIC = False
NUMERIC_CHAR_NUM = 0
NUMERIC_CHAR_APPEND = False
SPECIAL_CHAR_NUM = 0 
SPECIAL_CHAR_APPEND = False
INTERACTIVE = False
VALID_CHARS  = ["a-z"]
VERBOSE = False
COUNT = 1
DELIM = " "
SEP = "\n"
CASE = "first"


SPECIAL_CHARS: Dict[str, Callable[[List[str]], List[str]]] = {
    "space": " ",
    "full stop": ".",
    "exclamation": "!",
    "ampersand": "@",
    "hash": "#",
    "dollar": "$",
    "carrat": "^",
    "and": "&",
    "asterix": "*",
    "left bracket": "(",
    "right bracket": ")",
    "colon": ":",
    "equal": "=",
    "percentage": "%%",
    "under score": "_"
}

""" Set Minimum / floor values.  Default values will be higher """
MIN_CHAR_SET = 10
MIN_NUM_WORDS = 3
MIN_COUNT = 1


