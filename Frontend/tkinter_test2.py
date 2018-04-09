import tkinter as tk
import tkinter.ttk as ttk 
from PIL import Image, ImageTk
 
class DemoSplashScreen:
    def __init__(self, parent):
        self.parent = parent 
        self.setSplash()
        self.setWindow()
 
    def setSplash(self):
        # import image using Pillow
        self.image = Image.open('py.jpg')
        self.imgSplash = ImageTk.PhotoImage(self.image)
 
    def setWindow(self):
        # grab the size of the image file
        width, height = self.image.size
 
        halfWidth = (self.parent.winfo_screenwidth()-width)//2
        halfHeight = (self.parent.winfo_screenheight()-height)//2
        
        # set the window position in the middle of the screen
        self.parent.geometry("%ix%i+%i+%i" %(width, height, halfWidth, halfHeight))
 
        # set Image via Label Component
        self.label = tk.Label(self.parent, image=self.imgSplash)
        self.label.pack()
    
    def get_label(self): return self.label
         
if __name__ == '__main__':
    root = tk.Tk()

    # removes the title and window frame limit
    root.overrideredirect(True)
    progressbar = ttk.Progressbar(orient=tk.HORIZONTAL, length=100, mode='indeterminate', maximum=10)
    progressbar.pack(side="bottom")
    app = DemoSplashScreen(root)
    progressbar.start()
    
    # closes the window after 5 seconds
    root.after(5000, print("dasdadasdada"))
     
    root.mainloop()