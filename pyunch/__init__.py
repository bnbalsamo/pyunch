"""
pyunch
"""
try:
    from os import scandir
except ImportError:
    from scandir import scandir
from os import access, X_OK, environ
from os.path import expandvars, join
from tkinter import *
from tkinter import ttk
from subprocess import Popen
from argparse import ArgumentParser
from os import system, makedirs
from platform import system as platform
from json import load, dump


__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"


CONF_DIR = join(expandvars("$HOME"), '.config', 'pyunch')


class App:
    def __init__(self, d,
                 width=225, height=100,
                 yposition="center", xposition="center",
                 yoffset=0, xoffset=0,
                 colors={}):

        self.d = d
        root = Tk(className="pyunch")
        if colors:
            root.tk_setPalette(**colors)
        root.title("pyunch")
        # Force the window to the front on macs
        # (I think?)
        if platform() == 'Darwin':
            system('''/usr/bin/osascript -e 'tell app "Finder" ''' +
                   '''to set frontmost of process "Python" to true' ''')
        # Force the window to the top on Linux
        root.wm_attributes("-topmost", 1)
        root.focus_force()
        self.in_text = StringVar()
        self.in_entry = ttk.Entry(root, textvariable=self.in_text)
        self.lbox = Listbox(
            root,
            listvariable=StringVar(value=sorted([k for k in self.d])),
            height=height,
            width=width,
            selectmode="SINGLE"
        )
        self.lbox.select_set(0)
        self.in_entry.focus()

        root.bind('<Escape>', self.exit)
        root.bind('<Up>', self.sel_up)
        root.bind('<Down>', self.sel_down)
        root.bind('<Key>', self.box_update)
        self.in_entry.bind('<Return>', self.run)

        self.in_entry.pack(fill=X, expand=True)
        self.lbox.pack(fill=BOTH, expand=True)

        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        if xposition == "right":
            x = ws - width
        elif xposition == "left":
            x = 0
        else:
            x = (ws / 2) - (width / 2)

        if yposition == "top":
            y = 0
        elif yposition == "bottom":
            y = hs - height
        else:
            y = (hs / 2) - (height / 2)

        x += xoffset
        y += yoffset

        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

        root.mainloop()

    def run(self, *args):
        sel = self.lbox.curselection()
        if not sel:
            # The selection doesn't match anything in self.d
            # Maybe just run it? For now, exit
            self.exit()
        k = self.lbox.get(sel)
        Popen(self.d[k])
        self.exit()

    def sel_up(self, *args):
        if self.lbox.curselection():
            cur_index = int(self.lbox.curselection()[0])
            if cur_index == 0:
                return
            new_index = cur_index - 1
            self.lbox.select_clear(cur_index)
            self.lbox.select_set(new_index)
            self.lbox.see(new_index)
        self.in_entry.focus()

    def sel_down(self, *args):
        if self.lbox.curselection():
            cur_index = int(self.lbox.curselection()[0])
            if cur_index == self.lbox.size() - 1:
                return
            new_index = cur_index + 1
            self.lbox.select_clear(cur_index)
            self.lbox.select_set(new_index)
            self.lbox.see(new_index)
        self.in_entry.focus()

    def box_update(self, *args):
        if self.in_text.get() == "":
            o_list = [x for x in self.d]
        else:
            listvar = [x for x in self.d
                       if self.in_text.get() in x]
            first = []
            second = []
            third = []
            for x in listvar:
                if x == self.in_text.get():
                    first.append(x)
                elif x.startswith(self.in_text.get()):
                    second.append(x)
                else:
                    third.append(x)

            o_list = first + second + sorted(third)

        self.lbox.config(listvariable=StringVar(value=o_list))
        self.lbox.selection_set(0)
        self.in_entry.focus()

    def exit(self, *args):
        exit()


def index_paths():

    def find_execs(path, recurse=False):
        d = {}
        for x in scandir(path):
            if x.is_file(follow_symlinks=True) and access(x.path, X_OK):
                d[x.name] = x.path
            if recurse is True:
                if x.is_dir(follow_symlinks=True):
                    d.update(find_execs(x.path))
        return d

    parser = ArgumentParser()
    parser.add_argument(
        "--no-environmental",
        help="Don't grab the $PATH environmental variable " +
        "automatically",
        action="store_true"
    )
    parser.add_argument(
        "--recurse",
        help="Recursively scan provided paths. WARNING: " +
        "THIS CAN MAKE THINGS RUN SLOWLY IN DEEP DIRECTORY " +
        "STRUCTURES.",
        action="store_true"
    )
    parser.add_argument(
        "-p", "--path", help="Manually specify paths to " +
        "parse looking for executables.",
        action="append"
    )
    parser.add_argument(
        "-d", "--out-dir", help="The directory to save the index to",
        type=str, default=join(CONF_DIR, 'indices')
    )
    parser.add_argument(
        "-f", "--out-file", help="The file name to save the index to",
        type=str, default="0-path_index.json"
    )
    parser.add_argument(
        "--update", help="Update a file which is already in place",
        action="store_true"
    )

    args = parser.parse_args()

    paths = []
    if not args.no_environmental:
        paths = paths + [x for x in environ['PATH'].split(":") if
                         x != '']
    if args.path:
        paths = paths + args.path

    target_path = join(args.out_dir, args.out_file)

    d = {}
    if args.update:
        with open(target_path) as f:
            d.update(load(f))

    while paths:
        p = paths.pop()
        d.update(find_execs(p), recurse=args.recurse)

    makedirs(args.out_dir, exist_ok=True)
    with open(target_path, 'w') as f:
        dump(d, f)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-i", "--index-dir",
        type=str, default=join(CONF_DIR, 'indices'),
        help="The directory containing the json indices"
    )
    parser.add_argument(
        "-x", "--width",
        type=int, default=225,
        help="The width of the window"
    )
    parser.add_argument(
        "-y", "--height",
        type=int, default=95,
        help="The height of the window"
    )
    parser.add_argument(
        "--yposition", type=str,
        default="center",
        help="The y position (top, bottom, or center) of " +
        "the window"
    )
    parser.add_argument(
        "--xposition", type=str,
        default="center",
        help="The x position (left, right, or center) of " +
        "the window"
    )
    parser.add_argument(
        "--xoffset", type=int,
        default=0,
        help="The offset to apply to the x position"
    )
    parser.add_argument(
        "--yoffset", type=int,
        default=0,
        help="The offset to apply to the y position"
    )
    parser.add_argument(
        "--background", type=str,
        default=None
    )
    parser.add_argument(
        "--foreground", type=str,
        default=None
    )
    parser.add_argument(
        "--activeBackground", type=str,
        default=None
    )
    parser.add_argument(
        "--activeForeground", type=str,
        default=None
    )
    parser.add_argument(
        "--disabledForeground", type=str,
        default=None
    )
    parser.add_argument(
        "--highlightBackground", type=str,
        default=None
    )
    parser.add_argument(
        "--highlightColor", type=str,
        default=None
    )
    parser.add_argument(
        "--insertBackground", type=str,
        default=None
    )
    parser.add_argument(
        "--selectColor", type=str,
        default=None
    )
    parser.add_argument(
        "--selectBackground", type=str,
        default=None
    )
    parser.add_argument(
        "--selectForeground", type=str,
        default=None
    )
    parser.add_argument(
        "--troughColor", type=str,
        default=None
    )

    args = parser.parse_args()

    colors = {
        'background': args.background,
        'foreground': args.foreground,
        'activeBackground': args.activeBackground,
        'activeForeground': args.activeForeground,
        'disabledForeground': args.disabledForeground,
        'highlightBackground': args.highlightBackground,
        'highlightColor': args.highlightColor,
        'insertBackground': args.insertBackground,
        'selectColor': args.selectColor,
        'selectBackground': args.selectBackground,
        'selectForeground': args.selectForeground,
        'troughColor': args.troughColor
    }

    colors = {k: colors[k] for k in colors if colors[k] is not None}

    # Tk throws a fit if you don't supply a background color
    # if you supply anything else
    if not colors.get('background') and len(colors) > 0:
        colors['background'] = "#000000"

    d = {}
    # Reversed, sorted, because we're clobbering values
    for x in reversed(sorted([f for f in scandir(args.index_dir) if
                              f.name.endswith(".json")], key=lambda x: x.name)):
        with open(x.path) as f:
            d.update(load(f))

    App(d,
        width=args.width, height=args.height,
        xposition=args.xposition, yposition=args.yposition,
        xoffset=args.xoffset, yoffset=args.yoffset,
        colors=colors)


if __name__ == "__main__":
    main()
