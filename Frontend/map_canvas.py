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

@edit: Sandra Moen, https://github.com/Slideshow776, winter/spring 2018
    Implemented: 
        - Better zoom: Can now double click and use mousewheel
        - Marker input as list
        - Is now a tkinter.Canvas
        - Fixed a bug with keybindings.
'''

import sys, time
if sys.version_info[0] == 2: import Tkinter as tk
else: import tkinter as tk
from PIL import ImageTk
from goompy import GooMPy

#WIDTH, HEIGHT = 1033, int(768/1.2)
LATITUDE, LONGITUDE =  58.97, 5.7331 # Stavanger
ZOOM, MAX_ZOOM_OUT_LEVEL, MAX_ZOOM_IN_LEVEL = 12, 4, 22
MAPTYPE = 'roadmap'

class Map(tk.Canvas, tk.Tk):
    def __init__(self, root, width, height, coordinates=None,):
        self.WIDTH = width
        self.HEIGHT = height

        tk.Canvas.__init__(self, root, bg='#fff7ff', width=self.WIDTH, height=self.HEIGHT)
        self.pack(fill='both', expand=True, side='right')

        self.label = tk.Label(self)

        self.label.bind('<B1-Motion>', self.drag)
        self.label.bind('<Button-1>', self.click)
        self.label.bind('<Double-Button-1>', self.move_and_zoom)
        self.bind_all("<MouseWheel>", self.move_and_zoom)
                
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

        #MARKERS_1 = markers # markers should be a list of lists: [[lat_a,_lon_a],[lat_b,lon_b],...[lat_z,lon_z]]

        self.goompy = GooMPy(self.WIDTH, self.HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE, coordinates)

        self.restart()

    def set_focus_here(self):
        self.bind_all("<MouseWheel>", self.move_and_zoom)

    def add_zoom_button(self, text, sign):
        button = tk.Button(self, text=text, width=1, command=lambda:self.zoom(sign))
        return button

    def reload(self):
        self.coords = 0, 0
        self.redraw()
        self['cursor']  = ''

    def restart(self): # A little trick to get a watch cursor along with loading        
        self['cursor']  = 'watch'
        self.after(1, self.reload)

    def add_radio_button(self, text, index):
        maptype = self.maptypes[index]
        tk.Radiobutton(self.radiogroup, text=maptype, variable=self.radiovar, value=index, 
                command=lambda:self.usemap(maptype)).grid(row=0, column=index)

    def click(self, event):
        self.coords = event.x, event.y

    def move_and_zoom(self, event):
        if 1 > int(-1*(event.delta/120)): sign = 1
        else: sign = -1
        newlevel = self.zoomlevel + sign # sign = 1 V -1
        if newlevel > MAX_ZOOM_OUT_LEVEL and newlevel < MAX_ZOOM_IN_LEVEL:
            self.zoomlevel = newlevel

        self.goompy.move_and_zoom(event.x, event.y, self.zoomlevel)
        self.image = self.goompy.getImage()
        self.redraw()
        self.coords = event.x, event.y
        self.restart()

    def drag(self, event):
        self.goompy.move(self.coords[0]-event.x, self.coords[1]-event.y)
        self.image = self.goompy.getImage()
        self.redraw()
        self.coords = event.x, event.y

    def redraw(self):
        self.image = self.goompy.getImage()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label['image'] = self.image_tk

        self.label.pack(side='right', expand=True, fill='both')
        #self.label.place(x=0, y=0, width=self.WIDTH, height=self.HEIGHT) 

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
        if newlevel > MAX_ZOOM_OUT_LEVEL and newlevel < MAX_ZOOM_IN_LEVEL: # acceptable levels are: [1, 2, ... , 21]
            self.zoomlevel = newlevel
            self.goompy.useZoom(newlevel)
            self.restart()
