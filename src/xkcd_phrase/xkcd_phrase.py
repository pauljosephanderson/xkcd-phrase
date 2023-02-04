#!/usr/bin/env python
# encoding: utf-8
from argparse import ArgumentParser, Namespace
from argcomplete import autocomplete
import os
import sys
from io import open
from typing import List, Callable, Any, Union, Dict 

from xkcd_phrase.lib.xkcd_validate import (validate_options)

from xkcd_phrase.lib.xkcd_utilities import (
    locate_wordfile,
    choose_words,
    generate_wordlist,
    set_case,
    find_acrostic,
    special_char_sub,
    padding_digits_sub,
    generate_random_padding_numbers,
    generate_random_padding_chars,
    verbose_entropy
    )

from xkcd_phrase.lib.xkcd_default import (
    DEFAULT_WORDFILE,
    MIN_LENGTH, 
    MAX_LENGTH, 
    NUM_WORDS,
    ACROSTIC,
    NUMERIC_CHAR_NUM,
    NUMERIC_CHAR_APPEND,
    SPECIAL_CHAR_NUM, 
    SPECIAL_CHAR_APPEND,
    INTERACTIVE,
    VALID_CHARS,
    VERBOSE,
    COUNT,
    DELIM,
    SEP,
    CASE,
    SPECIAL_CHARS,
)

from xkcd_phrase.lib.case import (CASE_METHODS)

def try_input(
    prompt: str,
    validate: Callable[[str], Any],
    testing: bool = False,
    method: str = None,
) -> bool:
    """
    Suppress stack trace on user cancel and validate input with supplied
    validate callable.
    """
    if testing == False:
        try:
            answer = input(prompt)
        except (KeyboardInterrupt, EOFError):
            ''' user cancelled '''
            print("")
            sys.exit(0)

        """
        validate input
        """
        return validate(answer)
    else:
        if method == "NumWords":
            answer = "2"
        elif method == "NumWords0":
            answer = ""
        elif method == "NumWordsError":
            answer = "0"
        elif method == "Accept":
            answer = "y"
        print(validate(answer))
        return validate(answer)


def initialize_interactive_run(options: Namespace) -> None:
    def n_words_validator(answer: Union[str, int]) -> int:
        """
        Validate custom number of words input
        """

        if isinstance(answer, str) and len(answer) == 0:
            return options.num_words
        try:
            number = int(answer)
            if number < 1:
                raise ValueError
            return number
        except ValueError:
            sys.stderr.write("Please enter a positive integer\n")
            sys.exit(1)

    if not options.acrostic:
        n_words_prompt = "Enter number of words (default {0}):\n".format(options.num_words)
        options.num_words = try_input(
            n_words_prompt, n_words_validator, options.testing, options.testtype
        )
    else:
        options.num_words = len(options.acrostic)


def interactive_run_accept(
    wordlist: List[str],
    num_words: int = NUM_WORDS,
    acrostic: str = False,
    delimiter: str = DELIM,
    valid_delim: str = list(SPECIAL_CHARS.values()),
    case: str = CASE,
    numeric_char_num: int = NUMERIC_CHAR_NUM,
    numeric_char_append: bool = NUMERIC_CHAR_APPEND,
    special_char_num: int = SPECIAL_CHAR_NUM,
    special_char_append: bool = SPECIAL_CHAR_APPEND,
    testing: bool = False,
) -> str:
    ''' define input validators '''
    def accepted_validator(answer: str) -> bool:
        return answer.lower().strip() in ["y", "yes"]

    ''' generate passphrases until the user accepts '''
    accepted = False

    while not accepted:
        phrase = gen_phrase(
            wordlist, 
            num_words, 
            acrostic, 
            numeric_char_num, 
            numeric_char_append, 
            special_char_num, 
            special_char_append, 
            case, 
            delimiter,
            valid_delim
        )
        print("Generated: " + phrase)
        print(testing)
        accepted = try_input(
            prompt="Accept? [yN] ",
            validate=accepted_validator,
            testing=testing,
            method="Accept",
        )
        print("accepted", accepted)
    return phrase


def gen_phrase(
    wordlist: List[str],
    num_words: int,
    acrostic: str,
    numeric_char_num: int,
    numeric_char_append: bool,
    special_char_num: int, 
    special_char_append: bool,
    case: str,
    delimiter: str,
    valid_delim: str
) -> str:
    words = choose_words(wordlist, num_words, acrostic)
    case_words = set_case(words, method=case)

    if (special_char_num>0):
        if not special_char_append:
            special_char_sub(case_words, num_words, special_char_num, delimiter, valid_delim)
        else:
            temp_val = case_words[num_words-1]+ generate_random_padding_chars(special_char_num, delimiter)
            case_words.pop()
            case_words.append(temp_val)
    
    if  (numeric_char_num >0):
        if not numeric_char_append:
            padding_digits_sub(case_words, num_words, numeric_char_num)
        else:
            temp_val = case_words[num_words-1]+str(generate_random_padding_numbers(numeric_char_num))
            case_words.pop()
            case_words.append(temp_val)

    return delimiter.join(case_words)


def generate_xkphrase(
    wordlist: List[str],
    num_words: int = NUM_WORDS,
    interactive: bool = INTERACTIVE,
    delimiter: str = DELIM,
    valid_delim: str = list(SPECIAL_CHARS.values()),
    case: str = CASE,
    acrostic: str = ACROSTIC,
    numeric_char_num: int = NUMERIC_CHAR_NUM,
    numeric_char_append: bool = NUMERIC_CHAR_APPEND,
    special_char_num: int = SPECIAL_CHAR_NUM,
    special_char_append: bool = SPECIAL_CHAR_APPEND,
    testing: bool = False
) -> str:
    """
    Generate an XKCD-style phrase from the words in wordlist.
    """

    phrase = None

    ''' useful if driving the logic from other code '''
    if not interactive:
        return gen_phrase(
            wordlist, 
            num_words, 
            acrostic,
            numeric_char_num, 
            numeric_char_append,
            special_char_num, 
            special_char_append,
            case, 
            delimiter,
            valid_delim
        )

    else:
        ''' else, interactive session '''
        phrase = interactive_run_accept(
            wordlist,
            num_words,
            acrostic,
            delimiter,
            valid_delim,
            case,
            numeric_char_num,
            numeric_char_append,
            special_char_num, 
            special_char_append,
            testing,
        )
        return phrase


def emit_phrase(wordlist: List[str], options: Namespace) -> None:
    """Generate the specified number of phrases and output them."""
    count = options.count
    
    while count > 0:
        phrase = generate_xkphrase(
                wordlist,
                interactive=options.interactive,
                num_words=options.num_words,
                acrostic=options.acrostic,
                delimiter=options.delimiter,
                valid_delim=options.valid_delim,
                case=options.case,
                numeric_char_num=options.numeric_char_num,
                numeric_char_append=options.numeric_char_append,
                special_char_num=options.special_char_num,
                special_char_append=options.special_char_append,
                testing=options.testing,
            )
        if options.verbose:
            entropy = verbose_entropy(phrase, 
                                        options.case,
                                        options.valid_chars, 
                                        options.valid_delim, 
                                        options.delimiter,
                                        options.numeric_char_num,
                                        options.special_char_num
                                        )

            print("".join(entropy))
        else:
            print(phrase,end=options.separator)
        count -= 1


class xkcd_phraseArgumentParser(ArgumentParser):
    """Command-line argument parser for this program."""

    def __init__(self: Any, *args: Any, **kwargs: Any):
        super(xkcd_phraseArgumentParser, self).__init__(*args, **kwargs)

        self._add_arguments()

    def _add_arguments(self) -> None:
        """Add the arguments needed for this program."""
        exclusive_group = self.add_mutually_exclusive_group()
        self.add_argument(
            "-w",
            "--wordfile",
            dest="wordfile",
            default=DEFAULT_WORDFILE,
            metavar="WORDFILE",
            help=
            (
                "Specify that the file WORDFILE contains the list"
                " of valid words from which to generate passphrases."
                " Provided wordfiles: eff-long (default), eff-short,"
                " eff-special"
            ),
        )
        self.add_argument(
            "--min",
            dest="min_length",
            type=int,
            default=MIN_LENGTH,
            metavar="MIN_LENGTH",
            help=
            (
                "Generate passphrases containing words of at least MIN_LENGTH characters."
            ),
        )
        self.add_argument(
            "--max",
            dest="max_length",
            type=int,
            default=MAX_LENGTH,
            metavar="MAX_LENGTH",
            help=
            (
                "Generate passphrases containing words of at most MAX_LENGTH characters."
            ),
        )
        exclusive_group.add_argument(
            "-n",
            "--num-words",
            dest="num_words",
            type=int,
            default=NUM_WORDS,
            metavar="NUM_WORDS",
            help=
            (
                "Generate passphrases containing exactly NUM_WORDS words."
            ),
        )
        exclusive_group.add_argument(
            "-a",
            "--acrostic",
            dest="acrostic",
            type=str,
            default=ACROSTIC,
            metavar="ACROSTIC",
            help=
            (
                "Generate passphrases with an acrostic matching ACROSTIC. "
                "This will over ride -n/--num-words"
            ),
        )
        self.add_argument(
            "--numeric-char-num",
            dest="numeric_char_num",
            type=int,
            default=NUMERIC_CHAR_NUM,
            metavar="NUMERIC_CHAR_NUM",
            help=
            (
                "Number of numerical digits to include in passphrase."
            ),
        )
        self.add_argument(
            "--numeric-char-append",
            action="store_true",
            dest="numeric_char_append",
            default=NUMERIC_CHAR_APPEND,
            help=
            (
                "Append the numeric characters at the end of the word"
                "Don't substitute numeric characters for any of the letters"
            ),
        )
        self.add_argument(
            "--special-char-num",
            dest="special_char_num",
            type=int,
            default=SPECIAL_CHAR_NUM,
            metavar="SPECIAL_CHAR_NUM",
            help=
            (
                "Number of special characters to swap with letters within the passphrase."
            ),
        )
        self.add_argument(
            "--special-char-append",
            action="store_true",
            dest="special_char_append",
            default=SPECIAL_CHAR_APPEND,
            help=
            """(
                    "Append the special characters at the end of the word"
                    "Don't substitute special characters for any of the letters"
                ),"""
        )
        self.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            dest="interactive",
            default=INTERACTIVE,
            help=
            (
                "Generate and output a passphrase, query the user to"
                " accept it, and loop until one is accepted."
            ),
        )
        self.add_argument(
            "-v",
            "--valid-chars",
            dest="valid_chars",
            default=VALID_CHARS,
            metavar="VALID_CHARS",
            help=
            (
                "Limit passphrases to only include words matching the regex"
                " pattern VALID_CHARS (e.g. 'a-z')."
            ),
        )
        self.add_argument(
            "-V",
            "--verbose",
            action="store_true",
            dest="verbose",
            default=VERBOSE,
            help=
            (
                "Report various metrics for given options."
            ),
        )
        self.add_argument(
            "-c",
            "--count",
            dest="count",
            type=int,
            default=COUNT,
            metavar="COUNT",
            help=
            (
                "Generate COUNT passphrases."
            ),
        )
        self.add_argument(
            "-d",
            "--delimiter",
            dest="delimiter",
            default=DELIM,
            metavar="DELIM",
            help=
            (
                "Separate words within a passphrase with DELIM."
            ),
        )
        self.add_argument(
            "-s",
            "--separator",
            dest="separator",
            default=SEP,
            metavar="SEP",
            help=
            (
                "Separate generated passphrases with SEP."
            ),
        ),
        self.add_argument(
            "-x",
            "--valid-delim",
            dest="valid_delim",
            type=str,
            metavar="DEFAULT_DELIMITERS",
            choices=list(SPECIAL_CHARS.values()),
            default=list(SPECIAL_CHARS.values()),
            help=
            (
                "Limit passphrases to only include words matching the regex pattern DEFAULT_DELIMITERS "
                "Choices: {special_chars} (defualt: ' ')."
                .format(special_chars=list(SPECIAL_CHARS.values()))
            ),
        )
        self.add_argument(
            "-C",
            "--case",
            dest="case",
            type=str,
            metavar="CASE",
            choices=list(CASE_METHODS.keys()),
            default=CASE,
            help=
            (
                "Choose the method for setting the case of each word in the passphrase. "
                "Choices: {cap_meths} (default: 'first')."
                .format(cap_meths=list(CASE_METHODS.keys())
            )
        ),
    )


def main() -> int:
    """Mainline code for this program."""

    exit_status = 0

    try:
        parser = xkcd_phraseArgumentParser()

        autocomplete(parser)
        options = parser.parse_args()
        options.testing = False
        validate_options(options)

        my_wordlist = generate_wordlist(
            wordfile=options.wordfile,
            min_length=options.min_length,
            max_length=options.max_length,
            valid_chars=options.valid_chars,
        )

        if options.interactive:
            options.testtype = "NumWords"
            initialize_interactive_run(options)

        emit_phrase(my_wordlist, options)

    except SystemExit as exc:
        exit_status = exc.code

    return exit_status


def init() -> None:
    if __name__ == "__main__":
        exit_status = main()
        sys.exit(exit_status)

init()
