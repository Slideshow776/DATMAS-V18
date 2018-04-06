#!/usr/bin/env python3
'''
Example of using GooMPy with Tkinter

Copyright (C) 2015 Alec Singer and Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.
This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.

----------------------------------------------------------------------------
Edited by Sandra Moen:
Added: Better zoom function, marker input as list, and rewrote this as a tkinter.Canvas
Simply call module.name.Map(root, root_widget, markers) from main and a Goompy map will be drawn on a tkinter.Canvas.
Fixed a bug with keybindings.
'''

import sys
if sys.version_info[0] == 2: import Tkinter as tk
else: import tkinter as tk
from PIL import ImageTk
from goompy import GooMPy

WIDTH, HEIGHT = 640, 640 # resolution of one tile
LATITUDE, LONGITUDE =  58.97, 5.7331 # Stavanger
ZOOM = 12
MAPTYPE = 'roadmap'

class Map(tk.Canvas, tk.Tk):
    def __init__(self, root, widget, markers):
        self.root = root
        self.widget = widget

        tk.Canvas.__init__(self, widget, bg='#363636', width=WIDTH, height=HEIGHT)
        self.pack(fill='both', expand=True)

        self.label = tk.Label(self)

        self.label.bind('<B1-Motion>', self.callback_drag)
        self.label.bind('<Button-1>', self.callback_click)
        
        self.radiogroup = tk.Frame(self)
        self.radiovar = tk.IntVar()
        self.maptypes = ['roadmap', 'terrain', 'satellite', 'hybrid']
        self.add_radio_button('Road Map',  0)
        self.add_radio_button('Terrain',   1)
        self.add_radio_button('Satellite', 2)
        self.add_radio_button('Hybrid',    3)

        self.zoom_in_button  = self.add_zoom_button('+', +1)
        self.zoom_out_button = self.add_zoom_button('-', -1)

        self.zoomlevel = ZOOM

        maptype_index = 0
        self.radiovar.set(maptype_index)

        MARKERS_1 = markers # markers should be a list of lists: [[lat_a,_long_a],[lat_b,long_b],...[lat_z,long_z]]
        
        self.goompy = GooMPy(WIDTH, HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE, MARKERS_1)

        self.restart()

    def add_zoom_button(self, text, sign):
        button = tk.Button(self, text=text, width=1, command=lambda:self.zoom(sign))
        return button

    def reload(self):
        self.coords = None
        self.redraw()
        self['cursor']  = ''

    def restart(self): # A little trick to get a watch cursor along with loading        
        self['cursor']  = 'watch'
        self.after(1, self.reload)

    def add_radio_button(self, text, index):
        maptype = self.maptypes[index]
        tk.Radiobutton(self.radiogroup, text=maptype, variable=self.radiovar, value=index, 
                command=lambda:self.usemap(maptype)).grid(row=0, column=index)

    def callback_click(self, event):
        self.coords = event.x, event.y

    def callback_drag(self, event):
        self.goompy.move(self.coords[0]-event.x, self.coords[1]-event.y)
        self.image = self.goompy.getImage()
        self.redraw()
        self.coords = event.x, event.y

    def redraw(self):
        self.image = self.goompy.getImage()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label['image'] = self.image_tk

        self.label.place(x=0, y=0, width=WIDTH, height=HEIGHT) 

        self.radiogroup.place(x=0,y=0)

        x = int(self['width']) - 50
        y = int(self['height']) - 80

        self.zoom_in_button.place(x= x, y=y)
        self.zoom_out_button.place(x= x, y=y+30)

    def usemap(self, maptype):
        self.goompy.useMaptype(maptype)
        self.restart()

    def zoom(self, sign):
        newlevel = self.zoomlevel + sign # sign = 1 V -1
        if newlevel > 0 and newlevel < 22:
            self.zoomlevel = newlevel
            self.goompy.useZoom(newlevel)
            self.restart()
