# Chinese Reading and Writing Practice

Two Python programs are provided:

# writing-page.py

The writing-page.py program will generate a set of pages to practice your handwriting. 
The default page is US Letter (8.5"x11"), allowing for 10 rows of characters at 0.7" tall, 
and 0.25" pinyin and English defintions.

Basic usage:

Read the sample.json file, and create the output file as writing.pdf:

```
python3 writing-page.py sample.json writing.pdf
```

Advanced usage, found by running python3 writing-page.py --help:
```
usage: writing-page.py [-h] [-c CONFIG] [-s SAVE] [--page-size WIDTH HEIGHT]
                       [--margins VERTICALMARGIN HORIZONTALMARGIN]
                       [--square-size SQUARE_SIZE]
                       [--pinyin-height PINYIN_HEIGHT] [--vspace VSPACE]
                       [--hspace HSPACE] [--font FONT]
                       [--pinyinfont PINYINFONT] [--englishfont ENGLISHFONT]
                       [-v]
                       wordlist output

positional arguments:
  wordlist              List of words to use for the page, in JSON format
  output                Name of PDF file to output

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify configration file to use. Command line options
                        override the config file. Defaults to writing-page.ini
                        in the current directory.
  -s SAVE, --save SAVE  Save configuration file to specified name. Use it
                        later with the --config option.
  --page-size WIDTH HEIGHT
                        Specify page width and height. All size units are in
                        inches.
  --margins VERTICALMARGIN HORIZONTALMARGIN
                        Page Vertical (top/bottom) and Horizional (left/right)
                        margins.
  --square-size SQUARE_SIZE
                        Size of squares for Chinese characters. Font is
                        autoscaled to 8/9 of the box size.
  --pinyin-height PINYIN_HEIGHT
                        Height of pinyin text.
  --vspace VSPACE       Vertical space between bottom of square and top of
                        pinyin.
  --hspace HSPACE       Horizontal space between columns.
  --font FONT           Font to use for Chinese characters. This font must
                        include the Chinese characters to work.
  --pinyinfont PINYINFONT
                        Font to use for pinyin characters. This font must
                        include accented latin characters (macron, grave,
                        caron, and acute) to work properly. Uses Chinese font
                        if not specified.
  --englishfont ENGLISHFONT
                        Font to use for English definitions. Uses Pinyin font
                        if not specified.
  -v, --verbose

Args that start with '--' (eg. --page-size) can also be set in a config file
(./writing-page.ini or specified via -c). Config file syntax allows:
key=value, flag=true, stuff=[a,b,c] (for details, see syntax at
https://goo.gl/R74nmi). If an arg is specified in more than one place, then
commandline values override config file values which override defaults.
```


# flashcards.py

The flashcards.py program will generate a set of flashcards to help with your memory. 
The default settings are for 3"x5" index cards, with 0.5" Pinyin and English text, 
and 2" Chinese characters. You can change this as appropriate.

Basic usage:

python3 flashcards.py sample.json cards.pdf

Advanced usage, found by running python3 flashcards.py --help:
```
usage: flashcards.py [-h] [-c CONFIG] [-s SAVE] [--page-size WIDTH HEIGHT]
                     [--margins VERTICALMARGIN HORIZONTALMARGIN]
                     [--square-size SQUARE_SIZE]
                     [--pinyin-height PINYIN_HEIGHT]
                     [--english-height ENGLISH_HEIGHT] [--font FONT]
                     [--pinyinfont PINYINFONT] [--englishfont ENGLISHFONT]
                     [-v]
                     wordlist output

positional arguments:
  wordlist              List of words to use for the page, in JSON format
  output                Name of PDF file to output

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify configration file to use. Command line options
                        override the config file. Defaults to writing-page.ini
                        in the current directory.
  -s SAVE, --save SAVE  Save configuration file to specified name. Use it
                        later with the --config option.
  --page-size WIDTH HEIGHT
                        Specify page width and height. All size units are in
                        inches.
  --margins VERTICALMARGIN HORIZONTALMARGIN
                        Page Vertical (top/bottom) and Horizional (left/right)
                        margins. Text will be horizontally centered between
                        the margins.
  --square-size SQUARE_SIZE
                        Size of squares for Chinese characters. Font is
                        autoscaled to 8/9 of the box size.
  --pinyin-height PINYIN_HEIGHT
                        Height of pinyin text.
  --english-height ENGLISH_HEIGHT
                        Height of english text, uses pinyin-height if
                        unspecified
  --font FONT           Font to use for Chinese characters. The file
                        fireflysung.ttf should have been included with this
                        script. This font must include the Chinese characters
                        to work.
  --pinyinfont PINYINFONT
                        Font to use for pinyin characters. This font must
                        include accented latin characters (macron, grave,
                        caron, and acute) to work properly. Uses Chinese font
                        if not specified. The fireflysung.ttf file includes
                        the required characters.
  --englishfont ENGLISHFONT
                        Font to use for English definitions. Uses Pinyin font
                        if not specified.
  -v, --verbose         Verbose output, increasing the number of v's increases
                        verbosity.

Args that start with '--' (eg. --page-size) can also be set in a config file
(./flashcards.ini or specified via -c). Config file syntax allows: key=value,
flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi).
If an arg is specified in more than one place, then commandline values
override config file values which override defaults.
```

