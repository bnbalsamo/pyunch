try:
    from os import scandir
except ImportError:
    try:
        from scandir import scandir
    except ImportError:
        raise ImportError("Could not import scandir. Update python to 3.5+ " +
                          "or install the standalone package. Eg:\n" +
                          "pip install scandir")
from os import access, X_OK, environ
from tkinter import *
from tkinter import ttk
from subprocess import Popen
from argparse import ArgumentParser


class App(object):
    def __init__(self, launcher, width=225, height=100,
                 yposition="center", xposition="center",
                 yoffset=0, xoffset=0, colors={}):
        self.launcher = launcher
        root = Tk(className="pyunch")
        root.tk_setPalette(**colors)
        root.title("pyunch")
        self.in_text = StringVar()
        self.in_entry = ttk.Entry(root, textvariable=self.in_text)
        self.lbox = Listbox(root,
                            listvariable=StringVar(
                                value=[x.name for x in self.launcher.execs if
                                       (self.in_text.get() in x.name)]),
                            height=height,
                            width=width,
                            selectmode="SINGLE")
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
            x = (ws/2) - (width/2)

        if yposition == "top":
            y = 0
        elif yposition == "bottom":
            y = hs-height
        else:
            y = (hs/2) - (height/2)

        x += xoffset
        y += yoffset

        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

        root.mainloop()

    def run(self, *args):
        try:
            sel = self.lbox.get(int(self.lbox.curselection()[0]))
            ex = [x for x in self.launcher.execs if sel in x.name][0]
            i = self.launcher.execs.index(ex)
            self.launcher.launch_index(i)

        except:
            cmd = self.in_text.get().split(" ")
            self.launcher.launch_str(cmd)
        self.exit()

    def sel_up(self, *args):
        if self.lbox.curselection():
            try:
                cur_index = int(self.lbox.curselection()[0])
                if cur_index == 0:
                    return
                new_index = cur_index-1
                self.lbox.select_clear(cur_index)
                self.lbox.select_set(new_index)
                self.lbox.see(new_index)
            except Exception as e:
                raise e
                self.lbox.select_set(0)
                self.lbox.see(0)
        self.in_entry.focus()

    def sel_down(self, *args):
        if self.lbox.curselection():
            try:
                cur_index = int(self.lbox.curselection()[0])
                if cur_index == self.lbox.size()-1:
                    return
                new_index = cur_index+1
                self.lbox.select_clear(cur_index)
                self.lbox.select_set(new_index)
                self.lbox.see(new_index)
            except Exception as e:
                raise e
                self.lbox.select_set(0)
                self.lbox.see(0)
        self.in_entry.focus()

    def box_update(self, *args):
        if self.in_text.get() == "":
            o_list = [x.name for x in self.launcher.execs]
        else:
            listvar = [x.name for x in self.launcher.execs
                       if self.in_text.get() in x.name]
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

            o_list = first+second+third

        self.lbox.config(listvariable=StringVar(value=o_list))
        self.lbox.selection_set(0)
        self.in_entry.focus()

    def exit(self, *args):
        exit()


class Launcher(object):

    _paths = []
    _execs = []

    def __init__(self, paths=None, recurse=False):

        self.paths = paths
        self.find_execs(recurse=recurse)
        self.execs.sort(key=lambda x: x.name.lower())

    def get_paths(self):
        return self._paths

    def set_paths(self, paths):
        del self.paths
        for x in paths:
            self.add_path(x)

    def del_paths(self):
        self._paths = []

    def add_path(self, x):
        self._paths.append(x)

    def find_execs(self, recurse=False):
        stack = [x for x in self.paths]
        while stack:
            path = stack.pop()
            for x in scandir(path):
                if x.is_file(follow_symlinks=True) and access(x.path, X_OK):
                    self.add_exec(x)
                if recurse is True:
                    if x.is_dir(follow_symlinks=True):
                        stack.append(x.path)

    def get_execs(self):
        return self._execs

    def set_execs(self, execs):
        del self.execs
        for x in execs:
            self.add_exec(x)

    def add_exec(self, x):
        self._execs.append(x)

    def del_execs(self):
        self._execs = []

    def launch_str(self, x):
        if isinstance(x, str):
            args = x.split(" ")
        elif isinstance(x, list):
            args = x
        Popen(args)

    def launch_index(self, i):
        self.launch_str(self.execs[i].path)

    paths = property(get_paths, set_paths, del_paths)
    execs = property(get_execs, set_execs, del_execs)


def main():
    parser = ArgumentParser()
    parser.add_argument("--no-environmental",
                        help="Don't grab the $PATH environmental variable " +
                        "automatically",
                        action="store_true")
    parser.add_argument("--recurse",
                        help="Recursively scan provided paths. WARNING: " +
                        "THIS CAN MAKE THINGS RUN SLOWLY IN DEEP DIRECTORY " +
                        "STRUCTURES.",
                        action="store_true")
    parser.add_argument("-p", "--path", help="Manually specify paths to " +
                        "parse looking for executables.",
                        action="append")
    parser.add_argument("-x", "--width",
                        type=int, default=225,
                        help="The width of the window")
    parser.add_argument("-y", "--height",
                        type=int, default=95,
                        help="The height of the window")
    parser.add_argument("--yposition", type=str,
                        default="center",
                        help="The y position (top, bottom, or center) of " +
                        "the window")
    parser.add_argument("--xposition", type=str,
                        default="center",
                        help="The x position (left, right, or center) of " +
                        "the window")
    parser.add_argument("--xoffset", type=int,
                        default=0,
                        help="The offset to apply to the x position")
    parser.add_argument("--yoffset", type=int,
                        default=0,
                        help="The offset to apply to the y position")
    parser.add_argument("--background", type=str,
                        default=None)
    parser.add_argument("--foreground", type=str,
                        default=None)
    parser.add_argument("--activeBackground", type=str,
                        default=None)
    parser.add_argument("--activeForeground", type=str,
                        default=None)
    parser.add_argument("--disabledForeground", type=str,
                        default=None)
    parser.add_argument("--highlightBackground", type=str,
                        default=None)
    parser.add_argument("--highlightColor", type=str,
                        default=None)
    parser.add_argument("--insertBackground", type=str,
                        default=None)
    parser.add_argument("--selectColor", type=str,
                        default=None)
    parser.add_argument("--selectBackground", type=str,
                        default=None)
    parser.add_argument("--selectForeground", type=str,
                        default=None)
    parser.add_argument("--troughColor", type=str,
                        default=None)

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

    to_pop = []
    for x in colors:
        if colors[x] is None:
            to_pop.append(x)
    for x in to_pop:
        del colors[x]
    if len(colors) > 0 and not colors.get('background'):
        colors['background'] = "#000000"

    paths = []
    if not args.no_environmental:
        paths = paths + environ['PATH'].split(":")
    if args.path:
        paths = paths + args.path
    l = Launcher(paths=paths, recurse=args.recurse)
    App(l,
        width=args.width, height=args.height,
        xposition=args.xposition, yposition=args.yposition,
        xoffset=args.xoffset, yoffset=args.yoffset,
        colors=colors)


if __name__ == "__main__":
    main()
