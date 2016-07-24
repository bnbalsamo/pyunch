# pyunch

pyunch is a minimal process launcher inspired by dmenu.

Invoke it, start typing, hit enter when the entry you want to run is highlighted.


usage: pyunch [-h] [--no-environmental NO_ENVIRONMENTAL] [--recurse RECURSE]
              [-p PATH] [-x WIDTH] [-y HEIGHT] [--yposition YPOSITION]
              [--xposition XPOSITION] [--xoffset XOFFSET] [--yoffset YOFFSET]

```
optional arguments:
  -h, --help            show this help message and exit
  --no-environmental NO_ENVIRONMENTAL
                        Don't grab the $PATH environmental variable
                        automatically
  --recurse RECURSE     Recursively scan provided paths. WARNING: THIS CAN
                        MAKE THINGS RUN SLOWLY IN DEEP DIRECTORY STRUCTURES.
  -p PATH, --path PATH  Manually specify paths to parse looking for
                        executables.
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
```
