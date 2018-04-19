#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
# @author: Eugene Bakin @ https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df
"""
@edit: Sandra Moen, https://github.com/Slideshow776, winter/spring 2018
    Implemented: 
        - Mouse wheel scrolling
        - Setting tkinter focus
        - Better ability ti resize the frame 
"""


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)
        
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
            if interior.winfo_reqheight() != self.canvas.winfo_height():
                # update the canvas's width to fit the inner frame
                self.canvas.config(height=interior.winfo_reqheight())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            size = (self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
            """if interior.winfo_reqheight() != canvas.winfo_height():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, height=canvas.winfo_height())"""
        self.canvas.bind('<Configure>', _configure_canvas)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def set_focus_here(self):
        self.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def resetView(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

if __name__ == "__main__":
    class SampleApp(Tk):
        def __init__(self):
            root = Tk.__init__(self)
            
            container = Frame(root, bg='magenta')
            container.pack(fill='both', expand=True)

            self.frame = VerticalScrolledFrame(container)
            self.frame.pack(fill='both', expand=True)
            
            frame1 = Frame(self.frame.interior, bg='orange', width = 200, height = 200)
            frame1.pack(fill='both', expand=True)
            frame2 = Canvas(self.frame.interior, bg='pink', width = 200, height = 200)
            frame2.pack(fill='both', expand=True)

    app = SampleApp()
    app.mainloop()
