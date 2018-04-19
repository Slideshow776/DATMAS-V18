#!/usr/bin/env python3

import sys
if sys.version_info[0] == 2: import Tkinter as tk
else: import tkinter as tk

class NIPH_frame(tk.Frame, tk.Tk):
    def __init__(self, root):
        self.root = root

        tk.Frame.__init__(self, root, bg='#fff7ff')

        frame1 = tk.Frame(self, bg = 'red')
        frame1.pack()

        frame2 = tk.Frame(self, bg = 'magenta')
        frame2.pack()


def main():
    NIPH_frame()

if __name__ == '__main__':
    main()