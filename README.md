# xkcd-phrase

A flexible and scriptable password generator which generates strong passphrases, inspired by [XKCD 936][xkcd].

```
$ xkcd-phrase
Move Barbed Unplug Huskiness 
```

This password generator is inspired by [XKCD 936][xkcd] and the version provided by [Adam Birds](https://github.com/adambirds/xkcd-pass-python) With the original code from [redacted/xkcd-password-generator](https://github.com/redacted/XKCD-password-generator).. The defaults have been configured in a way to give this tool the most compatibility out of the box with passphrase requirements and the flexibility to adjust for site specific requirements. The defaults provide:
* A phrase containing 4 words between 4 and 9 characters (The default wordfile `eff-long` only contains words between 4 and 9 characters).
* The first letter of each word is capitalized.
* A seperator for human readability.

This allows the phrase generator to provide phrases by default which will be strong, easy to remember, difficult to brute-force and still pass the usual requirements of at least one upper-case letter, one lower-case letter and a special character.

[xkcd]: https://xkcd.com/936/
![](https://imgs.xkcd.com/comics/password_strength.png)


## Install
`xkcd-phrase` can easily be installed with the following command:

```
pip install xkcd-phrase
```

or manually by:

```
python -m pip install <path><package>
```

## Source
The source code can be found [here](https://github.com/pauljosephanderson/xkcd-phrase).

## Requirements
Python 3 (Version 3.8 or later).

## Running `xkcd_phrase`
`xkcd-phrase` can be called with no arguments with an output using the default wordfile and settings.
```
$ xkcd-phrase
> Spiffy Deceit Unease Pushover
```
The default settings return a single phrase made up of 4 words each having: its first letter capitalized and spaces between the words for readability.

It can also be called with a mixture of multiple arguments for example:

```
$ xkcd-phrase -d _ -c 5 --min 5 --max 7 --numeric-char-num 4 --numeric-char-append
Cause_Resale_Moody_Arise6814
Suggest_Bundle_Cruelly_Suggest4674
Sleeve_Resort_Plastic_Drool5351
Hazily_Skimmed_Islamic_Gigolo6475
Salvage_Sphinx_Tightly_Banter9381
```

This will return:
* `-d _` words joined by `_`.
* `-c 5` 5 passwords to choose from.
* `--min 5 --max 7` words between 5 and 7 characters long.
* `--numeric-char-num 4` Include 4 numerical characters in the passphrase.
* `--numeric-char-append` Include the numerics on the end of the passphrase.

```
$ xkcd-phrase -V -n 6 --numeric-char-num 2 --special-char-num 2
The total possible number of symbol choices in the phrase is
77 possible symbols comprising:
        52 alphabetic characters
        10 numeric characters
        15 special characters

The phrase length is 53 with the entropy of the phrase is calculated as:
        log2(possible_symb (77) ^ phrase_len (53)) = 332.14

The phrase is: I)licit0y Dugout Reproduce Overfed De:al Sque3ze
```

This will return:
* `-V` verbose output explaining the entropy of the passphrase.
* `-n 6` Use 6 words in the phrase.
* `--numeric-char-num 2` Include 2 numerical characters in the passphrase.
* `--special-char-num 2` Include 2 special characters in the passphrase..
* Note the default behaviour to substitute the numeric and special characters randonly into words.

As an aide memoire, you can choose an acrostic for example:
```
$ xkcd-phrase -a queen
> Quadrant Uncover Enforced Excretion Nacho
```


A full overview of the available options can be accessed by running following command:

```
xkcd-phrase --help
```

## Bash-Completion
`xkcd-phrase` also supports bash-completion. To set this up you need to add the below to your `.bashrc` file:

```
eval "$(register-python-argcomplete xkcd-phrase)"
```

This will then take effect the next time you login. To enable bash-completion immediately, you can run:

```
source .bashrc
```

## Word Lists

Several word lists are provided with the package. The default, eff-long, was specifically designed by the EFF for [passphrase generation](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) and is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/us/). As it was originally intended for use with Diceware ensure that the number of words in your passphrase is at least six when using it. Two shorter variants of that list, eff-short and eff-special, are also included. Please refer to the EFF documentation linked above for more information.

Note that `xkcd-phrase` can be used with any word file of the correct format: a file containing one word per line.

## Changelog

* **Version 1.0.0**
    * Initial Release

## License

This project is released under the [GNU GENERAL PUBLIC LICENSE v3](https://github.com/pauljosephanderson/xkcd-phrase/blob/main/LICENSE). However the original code from [redacted/xkcd-password-generator](https://github.com/redacted/XKCD-password-generator) is licensed under the [BSD 3-Clause license](https://github.com/pauljosephanderson/xkcd-phrase/blob/main/LICENSE.BSD).

## Contributing

Contributions welcome and gratefully appreciated!
