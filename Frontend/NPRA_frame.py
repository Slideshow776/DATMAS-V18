import sys
from tkinter import *
sys.path.append('../Backend') # appends the backend directory so we can use the modules there
sys.path.append('../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets')
import map_canvas, NPRA_Traffic_Stations_load_data

WINDOW_WIDTH, WINDOW_HEIGHT = int(1366/1.2), int(768/1.2) # (1366, 768) is the resolution of an average laptop.

def main():
    root = Tk()
    WINDOW_WIDTH, WINDOW_HEIGHT = int(1366/1.2), int(768/1.2) # (1366, 768) is the resolution of an average laptop.
    root.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.wm_iconbitmap('sandra.ico')
    root.title("NIPH frame test")
    root.configure(background='#000000')
    
    # Graph
    frame = Frame(root, width=530, height=530, bg='#ff9900')
    frame.pack(fill='both', expand=True)

    # Map
    coordinates = NPRA_Traffic_Stations_load_data.get_all_coordinates(
        '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Stavanger/times nivå 1 STAVANGER.csv',
        '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Bergen/times nivå 1 BERGEN.csv',
        '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Oslo/times nivå 1 OSLO.csv',
        )
    map1 = map_canvas.Map(root, coordinates, WINDOW_WIDTH, WINDOW_HEIGHT) # creates a tkinter.Canvas
    map1.pack(fill='both', expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()