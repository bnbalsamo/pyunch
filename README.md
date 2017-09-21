# pyunch

v0.0.1

[![Build Status](https://travis-ci.org/bnbalsamo/pyunch.svg?branch=master)](https://travis-ci.org/bnbalsamo/pyunch) [![Coverage Status](https://coveralls.io/repos/github/bnbalsamo/pyunch/badge.svg?branch=master)](https://coveralls.io/github/bnbalsamo/pyunch?branch=master)

A process launcher

# Quickstart

```$ pyunch-index```

```$ pyunch```

# Explanation

pyunch, by default, reads $HOME/.config/pyunch/indices, collected JSON documents in reverse sort order, and updates  dictionary with their contents. The JSON keys become the values displayed by pyunch, while the list values are then supplied to ```subprocess.Popen()```.

```pyunch-index``` is a command line utility for generating indices of executables from file system paths. By default it will scan all the paths in $PATH, gathering executables and generating an index that will be written to $HOME/.config/pyunch/indices/0-path_index.json.

# Help

```
$ pyunch --help
usage: pyunch [-h] [-i INDEX_DIR] [-x WIDTH] [-y HEIGHT]
              [--yposition YPOSITION] [--xposition XPOSITION]
              [--xoffset XOFFSET] [--yoffset YOFFSET]
              [--background BACKGROUND] [--foreground FOREGROUND]
              [--activeBackground ACTIVEBACKGROUND]
              [--activeForeground ACTIVEFOREGROUND]
              [--disabledForeground DISABLEDFOREGROUND]
              [--highlightBackground HIGHLIGHTBACKGROUND]
              [--highlightColor HIGHLIGHTCOLOR]
              [--insertBackground INSERTBACKGROUND]
              [--selectColor SELECTCOLOR]
              [--selectBackground SELECTBACKGROUND]
              [--selectForeground SELECTFOREGROUND]
              [--troughColor TROUGHCOLOR]

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX_DIR, --index-dir INDEX_DIR
                        The directory containing the json indices
  -x WIDTH, --width WIDTH
                        The width of the window
  -y HEIGHT, --height HEIGHT
                        The height of the window
  --yposition YPOSITION
                        The y position (top, bottom, or center) of the window
  --xposition XPOSITION
                        The x position (left, right, or center) of the window
  --xoffset XOFFSET     The offset to apply to the x position
  --yoffset YOFFSET     The offset to apply to the y position
  --background BACKGROUND
  --foreground FOREGROUND
  --activeBackground ACTIVEBACKGROUND
  --activeForeground ACTIVEFOREGROUND
  --disabledForeground DISABLEDFOREGROUND
  --highlightBackground HIGHLIGHTBACKGROUND
  --highlightColor HIGHLIGHTCOLOR
  --insertBackground INSERTBACKGROUND
  --selectColor SELECTCOLOR
  --selectBackground SELECTBACKGROUND
  --selectForeground SELECTFOREGROUND
  --troughColor TROUGHCOLOR
```

```
$ pyunch-index --help
usage: pyunch-index [-h] [--no-environmental] [--recurse] [-p PATH]
                    [-d OUT_DIR] [-f OUT_FILE] [--update]

optional arguments:
  -h, --help            show this help message and exit
  --no-environmental    Don't grab the $PATH environmental variable
                        automatically
  --recurse             Recursively scan provided paths. WARNING: THIS CAN
                        MAKE THINGS RUN SLOWLY IN DEEP DIRECTORY STRUCTURES.
  -p PATH, --path PATH  Manually specify paths to parse looking for
                        executables.
  -d OUT_DIR, --out-dir OUT_DIR
                        The directory to save the index to
  -f OUT_FILE, --out-file OUT_FILE
                        The file name to save the index to
  --update              Update a file which is already in place
```


# Author
Brian Balsamo <brian@brianbalsamo.com>
