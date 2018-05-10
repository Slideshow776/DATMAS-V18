from tkinter import *

master = Tk()

def callback(year):
    print(year)

years = [2017, 2016, 2015, 2014, 2013]
var = IntVar(value=years[0])

for year in years:    
    c = Checkbutton(master, text=year, variable=year,
    command=lambda year=year: callback(year))
    c.grid(row=2018-year, column=1)
    if year == 2017: c.select()

mainloop()