#!/usr/bin/env python
# encoding: utf-8

import sys
from argparse import Namespace

from xkcd_phrase.lib.xkcd_utilities import (
    locate_wordfile,
    generate_wordlist
    )

from xkcd_phrase.lib.xkcd_default import (
    DEFAULT_WORDFILE,
    MIN_LENGTH,
    MIN_NUM_WORDS,
    ACROSTIC,
    VALID_CHARS,
    MIN_CHAR_SET,
    MIN_COUNT,
    SPECIAL_CHARS
)

def validate_options(options: Namespace, testing: bool = False) -> None:
    """
    Given a parsed collection of options, performs various validation checks.
    """

    """ Validate wordfile """    
    return_val=validate_wordfile(options.wordfile)
    options.wordfile = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')
    if (return_val[2] == 1):
        sys.exit(1)
            
    if testing == True:
        sys.stdout.write(return_val[0])
    

    """
    Validate min_length
    
    Possibly a bit sloppy but min_length validation MUST occur before max_length
    """    
    return_val=validate_min_length(options.min_length)
    options.min_length = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')
        
    """ Validate max_length """    
    return_val=validate_max_length(options.max_length, options.min_length)
    options.max_length = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')

    """ Validate num_words """    
    return_val=validate_num_words(options.num_words)
    options.num_words = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')

    """ Validate acrostic """    
    if(options.acrostic!=False):
        return_val=validate_acrostic(options.acrostic)
        options.acrostic = return_val[0]
        if (return_val[1] != ""):
            print(return_val[1],'\n')

    """ Validate numeric-char-num """    
    if(not options.numeric_char_append):
        return_val=validate_numeric_char_num(options.numeric_char_num, options.num_words)
        options.numeric_char_num = return_val[0]
        if (return_val[1] != ""):
            print(return_val[1],'\n')

    """ Validate --numeric-char-append assumed not required """    

    """ Validate special-char-num """    
    if(not options.special_char_append):
        return_val=validate_special_char_num(options.special_char_num, options.num_words)
        options.special_char_num = return_val[0]
        if (return_val[1] != ""):
            print(return_val[1],'\n')

    """ Validate --special-char-append assumed not required """    

    """ Validate --interactive assumed not required """    

    """ Validate Valid_char """    
    return_val=validate_valid_char(options.valid_chars)
    options.valid_chars = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')

    """ Validate --verbose assumed not required """    

    """ Validate count """    
    return_val=validate_count(options.count)
    options.count = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')

    """ Validate delimiter """    
    return_val=validate_delim(options.delimiter)
    options.delimiter = return_val[0]
    if (return_val[1] != ""):
        print(return_val[1],'\n')
    
    """ Validate --sep assumed not required """    

    """ Validate --case assumed not required """    

def validate_wordfile(wordfile: str) -> tuple:
 
    """
    Return Message along with the result
    """
    message=""
    exit=0

    wordfile = locate_wordfile(wordfile)
    if not wordfile:
        message=(
            "Could not find word file, or word file does not exist.\n"
            "Resetting to the default wordfile {0}"
            ).format(DEFAULT_WORDFILE)
        wordfile=locate_wordfile(DEFAULT_WORDFILE)
        if not wordfile:
            message=(
            "Could not find word file, or word file does not exist.\n"
            )
            exit=1
        
    if (len(generate_wordlist(wordfile))==0):
        message=(
            "Not a good word file. Resetting to the default wordfile {0}"
            ).format(DEFAULT_WORDFILE)
        wordfile=locate_wordfile(DEFAULT_WORDFILE)
        
            
    return(wordfile,message,exit)

def validate_min_length(min_length: int)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Validate that min_length is a reasonable value, 
    ie, equal or more than MIN_LENGTH
    """
    if min_length < MIN_LENGTH:
        message =(
            "Warning: minimum word length {0} is not a reasonable value.\n"
            "Setting minimum equal to {1}.".format(min_length, MIN_LENGTH)
        )
        min_length = MIN_LENGTH
    return(min_length, message)

def validate_max_length(max_length: int, min_length: int)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Validate that the max_length is larger than the min 
    """
    if max_length < min_length:
        message =(
            "Warning: maximum word length {0} is less than minimum of {1}.\n"
            "Setting maximum equal to minimum.".format(max_length, min_length)
        )
        max_length = min_length
    return(max_length, message)

def validate_num_words(num_words: int)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Validate that num_words is a reasonable value, 
    ie, equal or more than MIN_NUM_WORDS
    """
    if num_words < MIN_NUM_WORDS:
        message =(
            "Warning: the number of words selected for the passphrase, {0}\n"
            "is not a reasonable value.  Setting the word number to {1}.".format(num_words, MIN_NUM_WORDS)
        )
        num_words = MIN_NUM_WORDS
    return(num_words, message)

def validate_acrostic(acrostic: str)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Validate that acrostic is either False or a valid word, 
    """
    if (acrostic.isalpha()==False):
        message =(
            "Warning: {0} is not a valid word. Setting Acrosic to {1}.".format(acrostic, ACROSTIC)
        )
        acrostic = ACROSTIC
    return(acrostic, message)

def validate_numeric_char_num(numeric_char_num: int, num_words: int)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Validate that numeric_char_num is less than or equal to num_words 
    """
    if numeric_char_num > num_words:
        message =(
            "Warning: numeric-char-num {0} is more than the {1} words in the phrase.\n"
            "Setting numeric-char-num  to the number of words.".format(numeric_char_num, num_words)
        )
        numeric_char_num = num_words
        
    return(numeric_char_num, message)

def validate_special_char_num(special_char_num: int, num_words: int)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Validate that special_char_num is less than or equal to num_words 
    """
    if special_char_num > num_words:
        message =(
            "Warning: special-char-num {0} is more than the {1} words in the phrase.\n"
            "Setting special-char-num  to the number of words.".format(special_char_num, num_words)
        )
        special_char_num = num_words
 
    return(special_char_num, message)

def validate_valid_char(valid_chars: str)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """
    Identify from valid_chars the number of possible characters that could be used 
    """
    if isinstance(valid_chars, str):
        valid_chars = list(valid_chars)
        char_a = ''
        i=0
        valid_set = []
        check_char = valid_chars[len(valid_chars)-1]
        while (char_a != check_char):
            char_b = valid_chars[i]
            if not char_b.isalpha():
                if(char_b == '-'):
                    char_b = valid_chars[i+1]
                    """
                    Create a list of the characters between char_a and char_b
                    eg if a-g is fed in, a list of b,c,d,e,f is created and itterated through
                    """
                    missing_char = list(map(chr, range(ord(char_a)+1, ord(char_b))))
                    for j in range(len(missing_char)):
                        valid_set.append(missing_char[j].lower())
                    valid_set.append(char_b.lower())
                elif(char_b != ','):
                    """
                    A character st could be expressed as a-m,p for example
                    , is a valid seperator so pass over it and don't throw a warning
                    Any other special char will thorw a warning and be removed
                    """
                    message =("Warning: The Character set has an anomolous char {0} which is being removed.\n"
                     "A valid character set is {1}".format(valid_chars[i], VALID_CHARS)
                     )
            else:
                valid_set.append(char_b)
            char_a = char_b
            i+=1
        if (len(valid_set) >= MIN_CHAR_SET):
            valid_chars = valid_set
        else:
            """
            Incase anything else goes wrong, just set back to [a-z] and expand the regex to a list
            """
            message=("Warning: The Character set provided in not recognised as a valid set.\n"
             "Resetting the character set back to {0}".format(VALID_CHARS)
             )
            valid_chars = list(map(chr, range(ord(VALID_CHARS[0][0]), ord(VALID_CHARS[0][-1])+1)))
            
    elif isinstance(valid_chars, list):
        """
        Most likely to get here by accepting the default
        Ensure the list is lowercase as case is handled by method_case
        """
        valid_chars = list(map(chr, range(ord(valid_chars[0][0]), ord(valid_chars[0][-1])+1)))
        valid_chars=list(map(str.lower, valid_chars))

    else:
        """
        You would need to be doing something weird to get here so it's a catchall
        """
        message=("Warning: The Character set provided in not recognised as a valid set.\n"
         "Resetting the character set back to {0}".format(VALID_CHARS)
        )
        valid_chars = list(map(chr, range(ord(VALID_CHARS[0][0]), ord(VALID_CHARS[0][-1])+1)))
    """
    finally sort and dedup the list - just in case ...
    """
    return(sorted(set(valid_chars)), message)

def validate_count(count: int)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
   
    """ Validate that count is > 0 """
    if (count < MIN_COUNT):
        message =(
            "Warning: the number of phrases selected for the passphrase, {0}\n"
            "is not a reasonable value.  Setting the phrase number to {1}.".format(count, MIN_COUNT)
        )
        count = MIN_COUNT
    return(count, message)

def validate_delim(delimiter: str)-> tuple:
 
    """
    Return Message along with the result
    """
    message=""
    if delimiter not in list(SPECIAL_CHARS.values()):
        message=(
            "Warning: delimiter chosen {0} is not in valid delimiter list \n"
            "{1}. Removing the delimiter".format(delimiter,list(SPECIAL_CHARS.values()))
        )
        delimiter = ""
    return(delimiter, message)


