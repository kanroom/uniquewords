# uniquewords
Allows extract from the text file unique words, and calculate their occurrence.</br>
Supports several options which allows to do this process more functionality.

Options:
<ul>
  <li>
    -f, --file</br>
      file which will be processed
  </li>
  <li>
    -p, --part</br>
      processing entire or part of the file [default: entire],
      if part of the file, then define start and end of the process
      (allowed types is an integer - numbers of the start and end line
      and string - starting and ending part of the text)
  </li>
  <li>
    -l, --length</br>
      define minimal and maximal length of the unique word [default: (1, 30)]
  </li>
  <li>
    -e, --exclude</br>
      load unique words from the file (previously saved with this program)
      with extension - .uws,
      to exclude them in current process
  </li>
  <li>
    -s, --symbols</br>
      define the symbols in the string with which words should be excluded
  </li>
  <li>
    -o, --order</br>
      order the outputted unique words by words or occurs [default: words]
  </li>
  <li>
    -u, --output</br>
      output results on terminal or infile (or both) [default: infile]  </li>
  </li>
</ul>
