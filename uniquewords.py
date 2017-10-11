#!/usr/bin/env python3
# Copyright (c) 2017 Kandia Roman. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.


import collections
import string
import sys
import time
import optparse

class InvalidFileFormat(Exception): pass
class InvalidArguments(Exception): pass


time_start = time.time()


def main():
    opts, args = options()
    words = collections.defaultdict(int)
    strip = string.whitespace + string.punctuation + string.digits + "\"'"
    filename = opts.filename
    part_text = opts.parttext
    if part_text:
        line_start = define_type(opts.parttext[0])
        line_end = define_type(opts.parttext[1])
        base_on_line, base_on_phrase = define_base(line_start, line_end)
        process_start = False
    min_len_word = opts.lengthword[0]
    max_len_word = opts.lengthword[1] + 1
    exclude_words = opts.excludewords
    if exclude_words:
        exclude_words = load_uws(exclude_words)
    exclude_with_symbols = opts.excludewithsymbols
    for i, line in enumerate(open(filename), start=1):
        # This flag will turn on or turn off file processing
        # from line to line or from phrase to phrase.
        if part_text:
            if base_on_line:
                if i == line_start:
                    process_start = True
            elif base_on_phrase:
                if line.find(line_start) != -1:
                    process_start = True
            if not process_start:
                continue
        line = encoding_line(line, encoding_map)
        line = cut_tags(line)
        for word in line.lower().split():
            word = word.strip(strip)
            # Check if we need exclude some words.
            if exclude_words:
                if word in exclude_words:
                    continue
            # Check if we need exclude some words
            # with particular symbol.
            if exclude_with_symbols:
                found = False
                for symbol in exclude_with_symbols:
                    if symbol in word:
                        found = True
                        break
                if found:
                    continue
            if len(word) > min_len_word and len(word) < max_len_word:
                words[word] += 1
        if part_text:
            if base_on_line:
                if i == line_end:
                    break
            elif base_on_phrase:
                if line.find(line_end) != -1:
                    break

    output_words(words, opts)
    execution_time()
    terminate()


def define_base(start, end):
    """Defining base of the parttext processing.
    """
    base_on_line = base_on_phrase = False
    try:
        if isinstance(start, int) and isinstance(end, int):
            base_on_line = True
        elif isinstance(start, str) and isinstance(end, str):
            base_on_phrase = True
        else:
            raise InvalidArguments
    except InvalidArguments as err:
        if isinstance(err, InvalidArguments):
            error = "Error: given invalid arguments. Type of the argument {0} must be equivalent type to argument {1}".format(start, end)
        print(error)
        terminate()

    return base_on_line, base_on_phrase


def define_type(var):
    """Defining type of the variable.
    """
    try:
        var = int(var)
    except ValueError:
        var = str(var)
    return var


def load_uws(filename):
    """Loads unique words from the file previously saved with this program.

    For example to exclude some words in this program
    when another file to the scan will be executed.
    """
    WORD = 0
    words = []
    f = None
    try:
        if not filename.endswith(".uws"):
            raise InvalidFileFormat
        for line in open(filename):
            line = line.split()
            word = line[WORD]
            words.append(word)
    except InvalidFileFormat as err:
        if isinstance(err, InvalidFileFormat):
            error = "Error: invalid file format: " + filename + "."
        print(error)
        terminate()
    except EnvironmentError as err:
        print("Error: failed to load {0}: {1}!".format(filename, err))
        return []
    finally:
        if f is not None:
            f.close()
    return words


def format_float(value, length=3):
    """Returns a string formated from the float number with defined float number part length.

    >>> format_float(1.2351)
    '1.235'
    >>> format_float(1.23)
    '1.230'
    >>> format_float(1.2351, 4)
    '1.2351'
    """
    try:
        if isinstance(value, float):
            left_part, right_part = str(value).split(".")
            if len(right_part) > length:
                right_part = right_part[:length]
            elif len(right_part) < length:
                right_part = right_part + "0" * (length - len(right_part))
            formated_float = left_part + "." + right_part
            return formated_float
        else:
            raise TypeError
    except TypeError:
        error = "Error: {0} - is not a float number!".format(value)
        print(error)


def sort_d(d, key="words", reverse=False):
    """Returns sorted dictionary by key or value.
    """
    try:
        if isinstance(d, dict):
            if key == "words":
                def by_item(item):
                    return item[0]
            elif key == "occurs":
                def by_item(item):
                    return item[1]
            else:
                print("Invalid key for sorted. "
                      "Valid key is 'words' or 'occurs'.")
                return
            return sorted(d.items(), key=by_item, reverse=True if reverse else False)
        else:
            raise TypeError
    except TypeError:
        error = "Error: {0} - is not a dictionary!".format(d)
        print(error)


def cut_tags(line):
    """Function do cut tags from the line.

    >>> cut_tags("<i>Still, <a>things could</a> be a lot worse.</i>")
    'Still, things could be a lot worse.'
    """
    tag_start = tag_end = False
    tag = ""
    tags = []
    if "<" in line and ">" in line:
        for c in line:
            if c == "<":
                tag_start = True
            elif c == ">":
                tag_end = True
            if tag_start:
                tag += c
            if tag_end:
                tags.append(tag)
                tag_start = tag_end = False
                tag = ""

        def cut(tags, line):
            if tags:
                for tag in tags:
                    line = line.replace(tag, "")
            return line

    if tags:
        return cut(tags, line)
    else:
        return line


encoding_map = {"\u201d": "\"",
                "\u201c": "\"",
                "\u2018": "'",
                "\u2019": "'",
                "\xa9": "(c)"}


def encoding_line(line, encoding_map):
    """A simple replacing undefined unicode character with defined replacer in encoding_map.
    """
    for k in encoding_map.keys():
        if line.find(k) != -1:
            line = line.replace(k, encoding_map[k])
    return line


def terminate():
    """Terminate current program.
    """
    input("Press Enter to exit...")
    exit()


def seconds_to_minutes(seconds):
    """Converts seconds into minutes and seconds.

    >>> seconds_to_minutes(59)
    [0, 59]
    >>> seconds_to_minutes(60)
    [1, 0]
    >>> seconds_to_minutes(69)
    [1, 9]
    """
    MINUTES, SECONDS = range(2)
    output = []
    seconds = int(seconds)
    if seconds >= 60:
        s = 0
        while seconds % 60 != 0:
            seconds -= 1
            s += 1
        minutes = seconds / 60
        output.insert(MINUTES, int(minutes))
        output.insert(SECONDS, s)
    elif 0 <= seconds < 60:
        output.insert(MINUTES, 0)
        output.insert(SECONDS, seconds)
    elif seconds < 0:
        print("Error: seconds value must be positive!")

    if output:
        return output
    else:
        return None


def execution_time():
    """Prints how much time was spent, to the moment when this function was called.
    """
    global time_start
    time_end = time.time()
    execution_time = time_end - time_start
    directive = ""
    if execution_time > 60:
        # Converting seconds in to minutes and seconds.
        m, s = seconds_to_minutes(execution_time)
        execution_time = "{0} m. {1} s.".format(m, s)
    else:
        directive = " s."
        execution_time = format_float(execution_time)
    print("Execution time: ", execution_time, directive)


def clock(end=False):
    """Represents a simple clock.
    """
    while not end:
        print(time.strftime("%H:%M:%S"), end="\r")
        time.sleep(1)


def max_len_key(dict):
    """Returns maximal length key of the represented dictionary.

    >>> dict = {"first": 5, "second": 6}
    >>> max_len_key(dict)
    6
    """
    max_len_key = 0
    for k in dict.keys():
        if len(k) > max_len_key:
            max_len_key = len(k)
    return max_len_key


def output_words(words, opts):
    """Outputting words on the terminal or in the file (or both).
    """
    if words:
        output = opts.outputwords
        order = opts.orderwords
        len_occur = len(str(max(words.values())))
        len_index = len(str(len(words)))
        len_word = max_len_key(words)
        if output == "both" or output == "terminal":
            index = 1
            for word, count in sort_d(words, key=order):
                try:
                    print("{0:{li}} {1:{lw}} occurs {2:{lo}} times".format(
                            index, word, count, li=len_index, lw=len_word, lo=len_occur))
                except UnicodeEncodeError as err:
                    print("UnicodeEncodeError: {0} with index: {1}".format(err, index))
                index += 1
        if output == "both" or output == "infile":
            filename = opts.filename
            if not filename.endswith(".uws"):
                filename += ".uws"
            f = None
            try:
                f = open(filename, "w", encoding="utf8")
                for word, count in sort_d(words, key=order):
                    f.write("{0:{lw}} occurs {1:{lo}} times".format(
                            word, count, lw=len_word, lo=len_occur) + "\n")
            except TypeError as err:
                print("Type error:", err)
            except EnvironmentError as err:
                print("Error: failed to save {0}: {1}!".format(filename, err))
                return True
            else:
                print("Saved {0} word{1} to {2}".format(len(words),
                      ("s" if len(words) != 1 else ""), filename))
            finally:
                if f is not None:
                    f.close()
    else:
        print("There are no words at all!")
        terminate()


def options():
    usage = """
%prog [options]

Allows extract from the text file unique words,
and calculate their occurrence.
Supports several options which allows
to do this process more functionality."""

    output_list = "terminal infile both".split()
    order_list = "words occurs".split()
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename",
                      action="store",
                      help=("file which will be processed"))
    parser.add_option("-p", "--part", dest="parttext",
                      action="store", nargs=2,
                      help=("processing entire or part of the file [default: entire], "
                            "if part of the file, then define start and end of the process "
                            "(allowed types is an integer - numbers of the start and end line "
                            "and string - starting and ending part of the text)"))
    parser.add_option("-l", "--length", dest="lengthword",
                      action="store", type="int", nargs=2, default=(1, 30),
                      help=("define minimal and maximal length of the unique word [default: %default]"))
    parser.add_option("-e", "--exclude", dest="excludewords",
                      action="store", type="string",
                      help=("load unique words from the file (previously saved with this program) "
                            "with extension - .uws, "
                            "to exclude them in current process"))
    parser.add_option("-s", "--symbols", dest="excludewithsymbols",
                      action="store", type="string",
                      help=("define the symbols in the string with which words should be excluded"))
    parser.add_option("-o", "--order", dest="orderwords",
                      action="store", choices=order_list, default="words",
                      help=("order the outputted unique words by words or occurs [default: %default]"))
    parser.add_option("-u", "--output", dest="outputwords",
                      action="store", choices=output_list, default="infile",
                      help=("output results on terminal or infile (or both) [default: %default]"))

    opts, args = parser.parse_args()
    if not opts.filename:
        parser.error("define file which will be processed")

    return opts, args


main()