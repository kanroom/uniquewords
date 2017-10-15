# uniquewords
Allows extract from the text file unique words, and calculate their occurrence.
Supports several options which allows to do this process more functionality.

Options:
  -f, --file
    file which will be processed
  -p, --part
    processing entire or part of the file [default: entire],
    if part of the file, then define start and end of the process
    (allowed types is an integer - numbers of the start and end line
    and string - starting and ending part of the text)
  -l, --length
    define minimal and maximal length of the unique word [default: (1, 30)]
  -e, --exclude
    load unique words from the file (previously saved with this program)
    with extension - .uws,
    to exclude them in current process
  -s, --symbols
    define the symbols in the string with which words should be excluded
  -o, --order
    order the outputted unique words by words or occurs [default: words]
  -u, --output
    output results on terminal or infile (or both) [default: infile]
