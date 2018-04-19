from tkinter import *

COLOR1, COLOR2, COLOR3, COLOR4 = '#363636', '#F75C95', '#ffb1e6', '#fff7ff' # color theme : darker to lighter

class dropdown_button:
    def __init__(self, root, name, items):
        var = StringVar(value=name)
        menubutton = Menubutton(root, textvariable=var, indicatoron=True,
                                borderwidth=1, relief="raised", width=20,
                                bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        main_menu = Menu(menubutton, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        menubutton.configure(menu=main_menu)

        def buttonCallback(value):
            print("value is", value)

        
        for item in range(len(items)):
            menu = Menu(main_menu, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
            main_menu.add_cascade(label=items[item][0], menu=menu)
            for value in items[item][1:]:
                menu.add_radiobutton(value=value, label=value, variable=value,
                command= lambda item=item, value=value: self._button_callback([items[item][0], value]))
        menubutton.pack()
    
    def _button_callback(self, value):
        #button_command = value
        print("this was pressed: ", value)


def main():
    root = Tk()
    items = (
            ["Oslo", "15/16", "16/17"],
            ["Stavanger", "15/16", "16/17"],
            ["Bergen", "15/16", "16/17"],
            ["All of Norway", "15/16", "16/17"]
        )
    dropdown_button(root, 'NPRA', items)
    root.mainloop()


if __name__ == '__main__':
    main()